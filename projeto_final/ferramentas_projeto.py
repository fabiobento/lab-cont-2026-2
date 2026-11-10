"""
ferramentas_projeto.py — Laboratório de Controle Automático (Ifes Guarapari)
Projeto final — servo de posição com motor CC

Utilitários para o projeto final. NÃO fazem o projeto por você: cuidam da
"encanação" (ler CSV, medir métricas sempre do mesmo jeito, simular o laço
digital EXATAMENTE como o firmware `firmware/pid_motor/pid_motor.ino` executa).

Uso típico (no seu notebook, na mesma pasta deste arquivo):

    from ferramentas_projeto import *
    d = carregar_csv("dados/ensaio_nominal.csv")       # telemetria da bancada
    for m in metricas_ensaio(d): print(m)

    planta = dict(Km=5.0, tau=0.12, L=0.02, Fc=40, cpg=1.04)   # SEU modelo
    ctrl   = dict(kp=1.2, ki=0.6, kd=0.05, N=30, pwm_max=255, aw=1)
    s = simula_firmware(planta, ctrl)                  # mesmo formato do CSV
    plota_ensaio(s, d, titulo="simulação × bancada")

Unidades (as mesmas do firmware v2):
    ângulo em graus; PWM em [-255, 255]; tempo em segundos;
    Km   = ganho de velocidade em regime  [graus/s por unidade de PWM]
    kp   = [PWM/grau],  ki = [PWM/(grau·s)],  kd = [PWM·s/grau]

Dependências: numpy, matplotlib (control e scipy só no seu notebook).
"""

from collections import deque

import numpy as np

__all__ = [
    "carregar_csv", "reamostrar", "metricas_degrau", "metricas_ensaio",
    "imprime_metricas", "MotorSimulado", "simula_firmware", "plota_ensaio",
    "linhas_firmware", "PERFIL_PADRAO",
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
                    d_rele=120, h_rele=1.0, ref_rele=0.0, rele_fim=6.0):
    """Simula um ensaio completo, devolvendo um dicionário no MESMO formato do CSV
    da bancada: t, r, angle, pwm, u_pid.

    ctrl (só para modo='pid'): kp, ki, kd, N (padrão 30), Ts (padrão 0,02),
          pwm_max (255), aw (0 sem, 1 clamping, 2 back-calculation), Tt (0,2),
          zm_comp (0), e_morto (0)
    modo: 'pid' | 'malha_aberta' | 'rele'
    """
    c = dict(kp=1.0, ki=0.0, kd=0.0, N=30.0, Ts=0.02, pwm_max=255, aw=1,
             Tt=0.2, zm_comp=0, e_morto=0.0)
    if ctrl:
        c.update(ctrl)
    Ts = c["Ts"]
    perfil = perfil or PERFIL_PADRAO
    if T_fim is None:
        T_fim = {"pid": T_FIM_PADRAO, "malha_aberta": ma_fim + 1.0,
                 "rele": rele_fim}[modo]

    m = MotorSimulado(planta)
    I = xf = 0.0
    u_rele = 0
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
