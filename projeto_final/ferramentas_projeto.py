"""
ferramentas_projeto.py — Laboratório de Controle Automático (Ifes Guarapari)
Projeto final — servo de posição com motor CC

Utilitários para o projeto final. NÃO fazem o projeto por você: cuidam da
"encanação" (ler CSV, medir métricas sempre do mesmo jeito, simular o laço
digital EXATAMENTE como o firmware `firmware/pid_motor/pid_motor.ino` executa).

Uso típico (nos roteiros das aulas, na mesma pasta deste arquivo):

    from ferramentas_projeto import *
    CFG = dict(MODO=3, CPG=1.3167, KP=2.7, KI=1.3, KD=0.15, N=30, ZM=33, EM=0.8)
    d = coletar("mf_nominal_1", PORTA, **CFG)          # ensaio na BANCADA -> dados/mf_nominal_1.csv
    s = simular(GEMEO, **CFG)                          # o MESMO ensaio no gêmeo digital
    imprime_metricas(metricas_ensaio(d))
    plota_ensaio(s, d, rotulos=["gêmeo", "bancada"])

    salvar_parametros(CPG=1.3167, Km=5.78)             # guarda em dados/parametros_bancada.json
    P = carregar_parametros()                          # ... e recupera na aula seguinte

Unidades (as mesmas do firmware v3):
    ângulo em graus; PWM em [-255, 255]; tempo em segundos;
    Km   = ganho de velocidade em regime  [graus/s por unidade de PWM]
    kp   = [PWM/grau],  ki = [PWM/(grau·s)],  kd = [PWM·s/grau]

Dependências: numpy, matplotlib (control e scipy só no seu notebook).
"""

from collections import deque

import numpy as np

__all__ = [
    "carregar_csv", "reamostrar", "metricas_degrau", "metricas_ensaio",
    "imprime_metricas", "MotorSimulado", "simula_firmware", "simular", "coletar",
    "salvar_parametros", "carregar_parametros", "plota_ensaio", "linhas_firmware",
    "PERFIL_PADRAO", "ajusta_fopdt", "simula_fopdt", "inclinacao", "analisa_pid",
    "desenha_lgr", "robustez", "veredito", "portas",
]

# Perfil do firmware v2 (MODO 3): (instante [s], referência [graus])
PERFIL_PADRAO = [(0.0, 0.0), (2.0, 90.0), (7.0, -90.0), (12.0, 0.0)]
T_FIM_PADRAO = 17.0


# ---------------------------------------------------------------------------
# 1) Leitura de dados
# ---------------------------------------------------------------------------
def carregar_csv(caminho, nomes=None):
    """Lê um CSV de telemetria (com ou sem cabeçalho; ignora linhas '#').

    Retorna um dicionário {nome_da_coluna: np.ndarray}. Sem cabeçalho, os nomes
    são deduzidos do número de colunas (3: t,u,y | 4: t,r,angle,pwm |
    5: t,r,angle,pwm,u_pid), ou passados em `nomes`.
    """
    linhas, cab = [], None
    with open(caminho, encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
            campos = raw.split(",")
            try:
                linhas.append([float(c) for c in campos])
            except ValueError:
                if cab is None and not linhas:
                    cab = [c.strip() for c in campos]
    dados = np.array(linhas, dtype=float)
    if nomes is None:
        nomes = cab or {3: ["t", "u", "y"], 4: ["t", "r", "angle", "pwm"],
                        5: ["t", "r", "angle", "pwm", "u_pid"]}.get(
                            dados.shape[1], [f"c{i}" for i in range(dados.shape[1])])
    return {n: dados[:, i] for i, n in enumerate(nomes)}


def reamostrar(t, *sinais, Ts=0.02):
    """Reamostra sinais numa grade uniforme de período Ts (interpolação linear)."""
    tg = np.arange(t[0], t[-1] + 1e-12, Ts)
    return (tg,) + tuple(np.interp(tg, t, s) for s in sinais)


# ---------------------------------------------------------------------------
# 2) Métricas — SEMPRE medidas deste jeito (é o que vale na avaliação)
# ---------------------------------------------------------------------------
def metricas_degrau(t, r, y, t_ini, t_fim, faixa=0.05, janela_ess=1.0):
    """Métricas de UM degrau de referência ocorrido em t_ini (até t_fim).

    Definições (enunciado do projeto, Seção 4):
      Mp  [%]  = 100·(pico além da referência final)/|amplitude do degrau| (0 se não passar)
      ts  [s]  = último instante, contado a partir de t_ini, em que |y − r1| > faixa·|r1 − r0|
                 (nan se ainda estiver fora da faixa no fim do trecho)
      tr  [s]  = tempo de subida 10–90 % da amplitude
      ess [°]  = média de (r1 − y) no último `janela_ess` segundo do trecho
    """
    antes = t < t_ini
    seg = (t >= t_ini) & (t < t_fim)
    r0 = r[antes][-1] if antes.any() else 0.0
    r1 = r[seg][0]
    A = r1 - r0
    ts_, ys = t[seg] - t_ini, y[seg]
    z = (ys - r0) / A                                   # resposta normalizada 0 -> 1
    Mp = max(0.0, (z.max() - 1.0) * 100.0)
    fora = np.where(np.abs(z - 1.0) > faixa)[0]
    if len(fora) == 0:
        ts = 0.0
    elif fora[-1] == len(z) - 1:
        ts = float("nan")                               # não acomodou no trecho
    else:
        ts = ts_[fora[-1] + 1]
    i10 = np.argmax(z >= 0.1) if (z >= 0.1).any() else None
    i90 = np.argmax(z >= 0.9) if (z >= 0.9).any() else None
    tr = ts_[i90] - ts_[i10] if (i10 is not None and i90 is not None) else float("nan")
    fim = ts_ >= (ts_[-1] - janela_ess)
    ess = float(np.mean(r1 - ys[fim]))
    return dict(t_degrau=t_ini, r0=r0, r1=r1, Mp=Mp, ts=ts, tr=tr, ess=ess)


def metricas_ensaio(d, pwm_max=255, faixa=0.05, janela_ess=1.0):
    """Aplica `metricas_degrau` a cada degrau do perfil de referência do ensaio.

    Também informa, em cada trecho, por quanto tempo o PWM ficou saturado
    (t_sat: |pwm| >= pwm_max) — útil para a especificação 4. Passe o MESMO
    pwm_max usado no firmware (ex.: 100 no ensaio de saturação).
    """
    t, r, y = d["t"], d["r"], d["angle"]
    trocas = np.where(np.abs(np.diff(r)) > 1e-6)[0] + 1
    inicios = list(t[trocas])
    fins = inicios[1:] + [t[-1] + 1e-9]
    pwm = np.abs(d["pwm"]) if "pwm" in d else None
    lim = pwm_max
    saida = []
    for a, b in zip(inicios, fins):
        m = metricas_degrau(t, r, y, a, b, faixa, janela_ess)
        if pwm is not None:
            seg = (t >= a) & (t < b)
            m["t_sat"] = float(np.sum(pwm[seg] >= lim - 0.5) * np.median(np.diff(t)))
            m["pwm_max_obs"] = float(pwm[seg].max())
        saida.append(m)
    return saida


def imprime_metricas(lista, titulo=""):
    """Tabela legível das métricas (vírgula decimal)."""
    def f(x, nd=1):
        return "  —  " if x is None or (isinstance(x, float) and np.isnan(x)) else \
            f"{x:.{nd}f}".replace(".", ",")
    if titulo:
        print(titulo)
    print(f"{'degrau':>14} | {'Mp (%)':>7} | {'ts 5% (s)':>9} | {'tr (s)':>7} | "
          f"{'ess (°)':>7} | {'t_sat (s)':>9}")
    print("-" * 70)
    for m in lista:
        deg = f"{m['r0']:+.0f}°→{m['r1']:+.0f}°"
        print(f"{deg:>14} | {f(m['Mp']):>7} | {f(m['ts'], 2):>9} | {f(m['tr'], 2):>7} | "
              f"{f(m['ess'], 2):>7} | {f(m.get('t_sat'), 2):>9}")


# ---------------------------------------------------------------------------
# 3) Planta simulada: motor CC + ponte H + encoder
# ---------------------------------------------------------------------------
class MotorSimulado:
    """Modelo não linear da bancada, integrado com passo fino `dt`.

        tau·dω/dt = −ω + Km·(u_atrasado − atrito)     ω em graus/s
        dθ/dt     = ω                                 θ em graus

    Parâmetros (dicionário `planta`):
      Km   ganho de velocidade [graus/s por PWM]      (obrigatório)
      tau  constante de tempo mecânica [s]            (obrigatório)
      L    atraso puro do atuador [s]                 (padrão 0)
      Fc   zona morta "em movimento" [PWM] (atrito de Coulomb)  (padrão 0)
      Fs   PWM mínimo para TIRAR do repouso [PWM] (atrito estático; padrão = Fc)
      Fc_neg, Fs_neg  idem para o sentido negativo (padrão = positivo)
      cpg  contas por grau do encoder (None = sem quantização)
      dt   passo de integração [s] (padrão 0,5 ms)
    """

    def __init__(self, planta):
        p = dict(L=0.0, Fc=0.0, cpg=None, dt=5e-4)
        p.update(planta)
        p.setdefault("Fs", p["Fc"])
        p.setdefault("Fc_neg", p["Fc"])
        p.setdefault("Fs_neg", p["Fs"])
        self.p = p
        self.w = 0.0
        self.th = 0.0
        nL = int(round(p["L"] / p["dt"]))
        self.buf = deque([0.0] * nL)

    def _passo(self, u):
        p, dt = self.p, self.p["dt"]
        if self.buf:
            self.buf.append(u)
            u = self.buf.popleft()
        if self.w == 0.0:                                   # parado: vence o atrito estático?
            if u > p["Fs"]:
                self.w = dt * p["Km"] * (u - p["Fc"]) / p["tau"]
            elif u < -p["Fs_neg"]:
                self.w = dt * p["Km"] * (u + p["Fc_neg"]) / p["tau"]
        else:                                               # em movimento: Coulomb + viscoso
            atrito = p["Fc"] if self.w > 0 else -p["Fc_neg"]
            w_novo = self.w + dt * (p["Km"] * (u - atrito) - self.w) / p["tau"]
            limiar = p["Fs"] if self.w > 0 else p["Fs_neg"]
            if np.sign(w_novo) != np.sign(self.w) and abs(u) <= limiar:
                w_novo = 0.0                                # cruzou zero e "grudou"
            self.w = w_novo
        self.th += self.w * dt

    def avanca(self, u, T):
        """Aplica o PWM `u` (segurado, ZOH) durante T segundos."""
        for _ in range(int(round(T / self.p["dt"]))):
            self._passo(u)

    def contas(self):
        cpg = self.p["cpg"]
        return None if cpg is None else int(np.floor(self.th * cpg))

    def angulo_medido(self):
        """Ângulo como o firmware o vê (quantizado pelo encoder, se cpg dado)."""
        c = self.contas()
        return self.th if c is None else c / self.p["cpg"]


# ---------------------------------------------------------------------------
# 4) Réplica do firmware pid_motor.ino v2 (MODO 3 = PID, MODO 1 = malha aberta,
#    MODO 2 = relé) — mesmas equações, mesma ordem, mesmo truncamento do PWM
# ---------------------------------------------------------------------------
def simula_firmware(planta, ctrl=None, modo="pid", perfil=None, T_fim=None,
                    pwm_ma=150, ma_ini=0.5, ma_fim=2.5,
                    d_rele=120, h_rele=1.0, ref_rele=0.0, rele_fim=6.0,
                    rampa=10.0, sinal=1, base=140, amp=80, tb=0.2):
    """Simula um ensaio completo, devolvendo um dicionário no MESMO formato do CSV
    da bancada: t, r, angle, pwm, u_pid.

    ctrl (só para modo='pid'): kp, ki, kd, N (padrão 30), Ts (padrão 0,02),
          pwm_max (255), aw (0 sem, 1 clamping, 2 back-calculation), Tt (0,2),
          zm_comp (0), e_morto (0)
    modo: 'pid' | 'malha_aberta' | 'rele' | 'partida' | 'prbs'
    """
    c = dict(kp=1.0, ki=0.0, kd=0.0, N=30.0, Ts=0.02, pwm_max=255, aw=1,
             Tt=0.2, zm_comp=0, e_morto=0.0)
    if ctrl:
        c.update(ctrl)
    Ts = c["Ts"]
    perfil = perfil or PERFIL_PADRAO
    if T_fim is None:
        T_fim = {"pid": T_FIM_PADRAO, "malha_aberta": ma_fim + 1.0,
                 "rele": rele_fim, "partida": 15.0, "prbs": 30.0}[modo]

    m = MotorSimulado(planta)
    I = xf = 0.0
    u_rele = 0
    lfsr = 0xA5
    u_prbs = base + amp
    t_bit = tb
    c_prev = 0
    moveu, t_moveu = False, 0.0
    if modo == "prbs":
        m.avanca(u_prbs, Ts)                 # o firmware aplica o 1º nível antes da 1ª amostra
    reg = {k: [] for k in ("t", "r", "angle", "pwm", "u_pid")}
    n_am = int(np.floor(T_fim / Ts + 1e-9))
    for k in range(1, n_am + 1):
        t = k * Ts
        y = m.angulo_medido()
        r = u_pid = 0.0
        if modo == "malha_aberta":
            u = pwm_ma if (ma_ini - 1e-9 <= t < ma_fim - 1e-9) else 0
            u_pid = u
        elif modo == "rele":
            r = ref_rele
            e = r - y
            if e > h_rele:
                u_rele = d_rele
            if e < -h_rele:
                u_rele = -d_rele
            if u_rele == 0:
                u_rele = d_rele
            u = u_pid = u_rele
        elif modo == "partida":
            c_ = m.contas()
            if not moveu and abs(c_) >= 3:
                moveu, t_moveu = True, t
            if moveu:
                u = 0
                if t > t_moveu + 0.3 + 1e-9:
                    break
            else:
                u = sinal * int(min(rampa * t, 150.0))
            u_pid = u
        elif modo == "prbs":
            c_ = m.contas()
            u_pid = float(c_ - c_prev)
            c_prev = c_
            if t >= t_bit - 1e-9:
                b = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 4)) & 1
                lfsr = ((lfsr >> 1) | (b << 7)) & 0xFF
                u_prbs = base + amp if b else base - amp
                t_bit += tb
            u = u_prbs
        else:
            r = perfil[0][1]
            for ti, ri in perfil:
                if t >= ti - 1e-9:
                    r = ri
            e = r - y
            dxf = c["N"] * (-y - xf)
            uD = c["kd"] * dxf
            xf += dxf * Ts
            u_pid = c["kp"] * e + I + uD
            u_c = u_pid
            if c["zm_comp"] > 0 and abs(e) > c["e_morto"]:
                u_c += c["zm_comp"] * np.sign(u_pid)
            u_sat = float(np.clip(u_c, -c["pwm_max"], c["pwm_max"]))
            if c["aw"] == 1:
                empurra = (u_c >= c["pwm_max"] and e > 0) or (u_c <= -c["pwm_max"] and e < 0)
                if not empurra:
                    I += c["ki"] * e * Ts
            elif c["aw"] == 2:
                I += (c["ki"] * e + (u_sat - u_c) / c["Tt"]) * Ts
            else:
                I += c["ki"] * e * Ts
            u = int(u_sat)                     # (int) do C: trunca em direção ao zero
        for kk, v in zip(reg, (t, r, y, u, u_pid)):
            reg[kk].append(v)
        m.avanca(u, Ts)
    return {k: np.array(v, dtype=float) for k, v in reg.items()}


# ---------------------------------------------------------------------------
# 4b) Mesmas chaves do firmware: simular() no gêmeo  ×  coletar() na bancada
# ---------------------------------------------------------------------------
_MODOS = {1: "malha_aberta", 2: "rele", 3: "pid", 4: "partida", 5: "prbs"}


def simular(planta, **cfg):
    """Simula no gêmeo digital um ensaio descrito com as MESMAS chaves de coletar()
    (MODO, KP, KI, KD, N, PWM_MAX, AW, TT, ZM, EM, PWM_MA, MA_INI, MA_FIM, D, H, REF,
    RAMPA, SINAL, BASE, AMP, TB, T, R, TR). CPG é ignorado: a quantização vem de
    planta["cpg"]. Tempos em ms, como no firmware."""
    modo = int(cfg.get("MODO", 3))
    if modo not in _MODOS:
        raise ValueError("MODO 0 (calibração) não se simula: é a sua mão girando a roda.")
    ctrl = dict(kp=cfg.get("KP", 1.0), ki=cfg.get("KI", 0.0), kd=cfg.get("KD", 0.0),
                N=cfg.get("N", 30.0), pwm_max=cfg.get("PWM_MAX", 255), aw=cfg.get("AW", 1),
                Tt=cfg.get("TT", 0.2), zm_comp=cfg.get("ZM", 0), e_morto=cfg.get("EM", 0.0))
    perfil = None
    if "R" in cfg:
        tr = cfg.get("TR", [0, 2000, 7000, 12000][:len(cfg["R"])])
        perfil = [(t_ / 1000.0, r_) for t_, r_ in zip(tr, cfg["R"])]
    T = cfg.get("T", 0)
    return simula_firmware(
        planta, ctrl, modo=_MODOS[modo], perfil=perfil, T_fim=(T / 1000.0 if T else None),
        pwm_ma=cfg.get("PWM_MA", 100), ma_ini=cfg.get("MA_INI", 500) / 1000.0,
        ma_fim=cfg.get("MA_FIM", 2500) / 1000.0, d_rele=cfg.get("D", 120),
        h_rele=cfg.get("H", 1.0), ref_rele=cfg.get("REF", 0.0),
        rele_fim=(T / 1000.0 if T else 6.0), rampa=cfg.get("RAMPA", 10.0),
        sinal=1 if cfg.get("SINAL", 1) >= 0 else -1, base=cfg.get("BASE", 140),
        amp=cfg.get("AMP", 80), tb=cfg.get("TB", 200) / 1000.0)


def portas():
    """Lista as portas seriais (Arduinos) conectadas. No Ubuntu: /dev/ttyUSB0 (clone CH340)
    ou /dev/ttyACM0 (Uno original)."""
    try:
        from serial.tools import list_ports
    except ImportError:
        print("pyserial não instalado — veja projeto_final/INSTALACAO_UBUNTU.md")
        return []
    lista = [p for p in list_ports.comports() if "USB" in p.device or "ACM" in p.device or "COM" in p.device]
    if not lista:
        print("nenhum Arduino encontrado — confira o cabo USB (e o brltty: INSTALACAO_UBUNTU.md, §2.2)")
    for p in lista:
        print(f"  {p.device:15s} {p.description}")
    return [p.device for p in lista]


def _fmt(v):
    if isinstance(v, (list, tuple, np.ndarray)):
        return ",".join(_fmt(x) for x in v)
    if isinstance(v, (float, np.floating)):
        return f"{float(v):.6g}"
    return str(v)


def coletar(nome, porta, dir_dados="dados", timeout=None, **cfg):
    """Executa um ensaio NA BANCADA (firmware pid_motor v3) e salva dados/<nome>.csv.

    Abrir a porta serial reinicia o Arduino; a função espera o "# pronto", envia a
    configuração (mesmas chaves de simular()) e grava a telemetria até "# fim do ensaio".
    Feche o Monitor Serial da Arduino IDE antes (a porta só pode ter um dono).
    """
    import os
    import time
    os.makedirs(dir_dados, exist_ok=True)
    caminho = os.path.join(dir_dados, nome if nome.endswith(".csv") else nome + ".csv")
    if str(porta).lower() == "virtual":
        return _coletar_virtual(caminho, **cfg)
    try:
        import serial
    except ImportError as exc:
        raise ImportError("pyserial não instalado — veja projeto_final/INSTALACAO_UBUNTU.md") from exc
    linhas = []
    try:
        ser_ = serial.Serial(porta, 115200, timeout=0.5)
    except serial.SerialException as exc:
        msg = str(exc)
        if "Permission denied" in msg:
            raise RuntimeError(f"Sem permissão para {porta}: o usuário precisa estar no grupo dialout "
                               "(INSTALACAO_UBUNTU.md, §2.3) e sair/entrar da sessão.") from exc
        raise RuntimeError(f"Não consegui abrir {porta}. Portas encontradas: {portas()} "
                           "(feche a Arduino IDE / Monitor Serial se estiverem abertos).") from exc
    with ser_ as ser:
        t0 = time.time()
        while True:
            txt = ser.readline().decode("utf-8", errors="ignore").strip()
            if txt.startswith("# pronto"):
                break
            if time.time() - t0 > 8:
                raise RuntimeError(
                    "O Arduino não respondeu. Confira: (1) o firmware gravado é o pid_motor v3; "
                    "(2) a porta está certa; (3) o Monitor Serial da IDE está fechado.")
        for k, v in cfg.items():
            ser.write(f"{k}={_fmt(v)}\n".encode())
            time.sleep(0.01)
        ser.write(b"GO\n")
        limite = time.time() + (timeout or 120)
        while time.time() < limite:
            txt = ser.readline().decode("utf-8", errors="ignore").strip()
            if not txt:
                continue
            if txt.startswith("#"):
                if "chave desconhecida" in txt or txt.startswith("# MODO"):
                    print(txt)
                if "fim do ensaio" in txt:
                    break
                continue
            campos = txt.split(",")
            if len(campos) == 5:
                try:
                    linhas.append([float(x) for x in campos])
                except ValueError:
                    pass
        else:
            print("atenção: tempo esgotado antes do fim do ensaio (aumente timeout=)")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("t,r,angle,pwm,u_pid\n")
        for l_ in linhas:
            f.write(",".join(f"{x:g}" for x in l_) + "\n")
    print(f"{len(linhas)} amostras salvas em {caminho}")
    return carregar_csv(caminho)


def _coletar_virtual(caminho, **cfg):
    """PORTA = "virtual": o ensaio roda na planta virtual do gabarito (material do
    professor, pasta gabarito/), com o atrito sorteado em ±5 % a cada ensaio."""
    import importlib.util
    import os
    arq_pv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gabarito", "planta_virtual.py")
    if not os.path.exists(arq_pv):
        raise RuntimeError("PORTA='virtual' só existe no material do professor. Use a porta do Arduino.")
    spec = importlib.util.spec_from_file_location("planta_virtual", arq_pv)
    pv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pv)
    cpg_v = pv.CPG_VERDADEIRO
    cpg_fw = float(cfg.get("CPG", 1.0))           # o que o "firmware" usa para converter
    modo = int(cfg.get("MODO", 3))
    if modo == 0:                                 # a "mão" gira a roda 5 voltas em ~14 s
        T = cfg.get("T", 30000) / 1000.0
        t = np.arange(0.02, T + 1e-9, 0.02)
        th = 1800.0 * (1 - np.cos(np.pi * np.clip((t - 2) / 14, 0, 1))) / 2
        c = np.floor(th * cpg_v)
        d = dict(t=t, r=0 * t, angle=c / cpg_fw, pwm=0 * t, u_pid=c)
    else:
        d = simular(pv.planta_com_variacao(0.05), **cfg)
        d["angle"] = np.round(d["angle"] * cpg_v) / cpg_fw     # contas / CPG do firmware
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("t,r,angle,pwm,u_pid\n")
        for linha in zip(d["t"], d["r"], d["angle"], d["pwm"], d["u_pid"]):
            f.write(",".join(f"{x:g}" for x in linha) + "\n")
    print(f"[bancada virtual] {len(d['t'])} amostras salvas em {caminho}")
    return carregar_csv(caminho)


def salvar_parametros(dir_dados="dados", **kw):
    """Acrescenta/atualiza parâmetros da bancada em dados/parametros_bancada.json."""
    import json
    import os
    os.makedirs(dir_dados, exist_ok=True)
    arq_ = os.path.join(dir_dados, "parametros_bancada.json")
    p = {}
    if os.path.exists(arq_):
        with open(arq_, encoding="utf-8") as f:
            p = json.load(f)
    p.update({k: (float(v) if isinstance(v, (np.floating, np.integer)) else v) for k, v in kw.items()})
    with open(arq_, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2, ensure_ascii=False)
    print("parâmetros salvos:", ", ".join(kw))
    return p


def carregar_parametros(dir_dados="dados"):
    """Lê dados/parametros_bancada.json (os resultados das aulas anteriores)."""
    import json
    import os
    arq_ = os.path.join(dir_dados, "parametros_bancada.json")
    if not os.path.exists(arq_):
        print("ainda não há parâmetros salvos — rode as aulas anteriores primeiro")
        return {}
    with open(arq_, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 5) Gráfico padrão de ensaio
# ---------------------------------------------------------------------------
def plota_ensaio(*ensaios, rotulos=None, titulo="", xlim=None, mostra_u_pid=True):
    """Gráfico padrão: (cima) referência e ângulo; (baixo) PWM aplicado e pedido.
    Aceita vários ensaios (dicionários) para sobrepor (ex.: simulação × bancada)."""
    import matplotlib.pyplot as plt
    rotulos = rotulos or [f"ensaio {i+1}" for i in range(len(ensaios))]
    fig, ax = plt.subplots(2, 1, figsize=(10, 6.2), sharex=True,
                           gridspec_kw=dict(height_ratios=[1.6, 1]))
    ax[0].step(ensaios[0]["t"], ensaios[0]["r"], "k--", lw=1.1, where="post",
               label="referência")
    for d, rot in zip(ensaios, rotulos):
        ln, = ax[0].plot(d["t"], d["angle"], lw=1.7, label=rot)
        ax[1].plot(d["t"], d["pwm"], lw=1.4, color=ln.get_color(), label=f"PWM aplicado — {rot}")
        if mostra_u_pid and "u_pid" in d:
            ax[1].plot(d["t"], d["u_pid"], lw=1.0, ls=":", color=ln.get_color(),
                       label=f"u pedido — {rot}")
    ax[0].set_ylabel("ângulo (graus)")
    ax[0].grid(alpha=0.3)
    ax[0].legend(fontsize=8, loc="best")
    ax[1].set_ylabel("PWM")
    ax[1].set_xlabel("tempo (s)")
    ax[1].grid(alpha=0.3)
    ax[1].legend(fontsize=7, loc="best", ncol=2)
    if xlim:
        ax[1].set_xlim(*xlim)
    if titulo:
        ax[0].set_title(titulo)
    fig.tight_layout()
    return fig, ax


def linhas_firmware(kp, ki, kd, N=30.0):
    """Imprime as linhas para colar no bloco 4 do pid_motor.ino."""
    print(f"float kp = {kp:.4f};     // [PWM/grau]")
    print(f"float ki = {ki:.4f};     // [PWM/(grau.s)]")
    print(f"float kd = {kd:.4f};     // [PWM.s/grau]")
    print(f"const float N_FILT = {N:.1f};   // [rad/s]")


# ---------------------------------------------------------------------------
# 6) Funções de apoio dos roteiros (aulas 1 a 5)
# ---------------------------------------------------------------------------
def simula_fopdt(p, t, u, Ts=0.02):
    """Resposta do FOPDT  y = K e^{-Ls}/(tau s + 1) · (u − u0)  à entrada u (amostrada em Ts).
    p = [K, tau, L] ou [K, tau, L, u0]."""
    import control as ct
    K, tau, L = p[:3]
    u0 = p[3] if len(p) > 3 else 0.0
    nd = int(round(L / Ts))
    u_at = np.r_[np.full(nd, u[0]), u[:len(u) - nd]] - u0       # atraso = deslocar nd amostras
    _, y = ct.forced_response(ct.tf([K], [tau, 1]), t - t[0], u_at)
    return y


def ajusta_fopdt(t, u, y, chute, Ts=0.02):
    """Mínimos quadrados (Nelder-Mead) do FOPDT. chute = [K, tau, L] (sem desvio) ou
    [K, tau, L, u0] (com desvio). Devolve (parâmetros, EQM)."""
    from scipy.optimize import minimize

    def custo(p):
        if p[0] <= 0 or p[1] <= 1e-3 or p[2] < 0:
            return 1e9
        return float(np.mean((y - simula_fopdt(p, t, u, Ts)) ** 2))
    r = minimize(custo, chute, method="Nelder-Mead",
                 options=dict(maxiter=6000, xatol=1e-7, fatol=1e-9))
    return r.x, r.fun


def inclinacao(d, t1=1.5, t2=2.5):
    """Inclinação [graus/s] da reta ajustada ao ângulo entre t1 e t2."""
    m = (d["t"] >= t1) & (d["t"] < t2)
    return float(np.polyfit(d["t"][m], d["angle"][m], 1)[0])


def analisa_pid(G, L_ef, kp, ki, kd, N=30.0, gemeo=None, nome="", imprime=True, **extra):
    """Margens (com atraso por Padé de 3ª ordem e filtro da derivada), degrau LINEAR de 90°
    e, se `gemeo` for dado, o perfil completo no gêmeo digital (com as chaves extras
    do firmware, ex.: ZM=33, EM=0.8)."""
    import control as ct
    s = ct.tf("s")
    Pd = ct.tf(*ct.pade(L_ef, 3))
    Cy = kp + ki / s + kd * N * s / (s + N)
    gm, pm, _, wc = ct.margin(Cy * G * Pd)
    T = ct.feedback(G * Pd, Cy) * (kp + ki / s)
    tt = np.linspace(0, 6, 3001)
    _, y = ct.step_response(90 * T, tt)
    ml = metricas_degrau(np.r_[-1e-3, tt], np.r_[0, np.full_like(tt, 90)], np.r_[0, y], 0, 6)
    res = dict(kp=kp, ki=ki, kd=kd, GM_dB=20 * np.log10(gm), PM=pm, wc=wc,
               Mp_lin=ml["Mp"], ts_lin=ml["ts"], t_lin=tt, y_lin=y, T=T)
    if gemeo is not None:
        sim = simular(gemeo, MODO=3, KP=kp, KI=ki, KD=kd, N=N, **extra)
        res["sim"] = sim
        res["metricas_gemeo"] = metricas_ensaio(sim)
    if imprime:
        f = lambda x, n=2: f"{x:.{n}f}".replace(".", ",")
        print(f"{nome}  kp = {f(kp,3)}  ki = {f(ki,3)}  kd = {f(kd,3)}")
        print(f"   margens: GM = {f(res['GM_dB'],1)} dB · PM = {f(pm,1)}° · ωc = {f(wc,1)} rad/s")
        print(f"   modelo LINEAR, degrau de 90°: Mp = {f(ml['Mp'],1)} % · ts = {f(ml['ts'])} s")
        if gemeo is not None:
            imprime_metricas(res["metricas_gemeo"], "   GÊMEO DIGITAL (com atrito, quantização, saturação):")
    return res


def desenha_lgr(Lmalha, sd=None, kmax=None, titulo="", xlim=(-40, 5), ylim=(-25, 25)):
    """Lugar das raízes de 1 + k·Lmalha(s) (Lmalha com o atraso já por Padé), com s_d marcado."""
    import matplotlib.pyplot as plt
    num = np.array(Lmalha.num[0][0], float)
    den = np.array(Lmalha.den[0][0], float)
    num = np.r_[np.zeros(len(den) - len(num)), num]
    ks = np.r_[0, np.logspace(-4, np.log10(kmax or 3.0), 3000)]
    raizes = np.array([np.sort_complex(np.roots(den + k * num)) for k in ks])
    fig, ax = plt.subplots(figsize=(6.4, 5))
    for j in range(raizes.shape[1]):
        ax.plot(raizes[:, j].real, raizes[:, j].imag, "b.", ms=1.2)
    ax.plot(np.roots(den).real, np.roots(den).imag, "kx", ms=9, label="polos de malha aberta")
    z = np.roots(num[np.argmax(num != 0):]) if np.count_nonzero(num) > 1 else []
    if len(z):
        ax.plot(np.real(z), np.imag(z), "go", mfc="none", ms=8, label="zeros de malha aberta")
    if sd is not None:
        ax.plot([sd.real, sd.real], [sd.imag, -sd.imag], "r*", ms=14, label="$s_d$ desejado")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_xlabel("Re(s)"); ax.set_ylabel("Im(s)"); ax.legend(fontsize=8, loc="lower left")
    ax.set_title(titulo or "Lugar das raízes")
    fig.tight_layout()
    return fig, ax


def robustez(gemeo, n=20, variacao=0.15, semente=0, **cfg):
    """Quantas de n plantas (atrito sorteado em ±variacao, Km ±8 %, tau ±10 %) atendem às
    especificações 1–3 nos três degraus do perfil, com a configuração cfg do firmware."""
    rng = np.random.default_rng(semente)
    ok = 0
    for _ in range(n):
        p = dict(gemeo)
        for k in ("Fc", "Fs", "Fc_neg", "Fs_neg"):
            if k in p:
                p[k] = gemeo[k] * (1 + variacao * rng.uniform(-1, 1))
        p["Km"] = gemeo["Km"] * (1 + 0.08 * rng.uniform(-1, 1))
        p["tau"] = gemeo["tau"] * (1 + 0.10 * rng.uniform(-1, 1))
        if "Fs" in p:
            p["Fs"] = max(p["Fs"], p.get("Fc", 0))
        if "Fs_neg" in p:
            p["Fs_neg"] = max(p["Fs_neg"], p.get("Fc_neg", 0))
        ms = metricas_ensaio(simular(p, MODO=3, **cfg))
        ok += all(m["Mp"] <= 15 and m["ts"] <= 2.5 and abs(m["ess"]) < 2 for m in ms)
    return ok


def veredito(m):
    """Imprime ✅/❌ das especificações 1–3 para as métricas de UM degrau."""
    f = lambda x, n=2: "—" if np.isnan(x) else f"{x:.{n}f}".replace(".", ",")
    print(("✅" if abs(m["ess"]) < 2 else "❌") + f" 1. |e_ss| = {f(abs(m['ess']))}° < 2°")
    print(("✅" if m["Mp"] <= 15 else "❌") + f" 2. Mp = {f(m['Mp'],1)} % ≤ 15 %")
    print(("✅" if m["ts"] <= 2.5 else "❌") + f" 3. ts = {f(m['ts'])} s ≤ 2,5 s")
