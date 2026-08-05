# Trabalho 1 — Identificação de Sistemas de 1ª Ordem com Atraso usando PRBS

**Laboratório de Controle Automático — Engenharia Elétrica — Ifes Campus Guarapari**
**Lançamento:** semana 5 · **Entrega:** semana 7 · **Valor:** 15 pontos · **Grupos:** até 3 integrantes

---

## 1. Objetivos

1. Excitar a planta (motor CC + ponte H + encoder magnético) com um sinal **PRBS** (*Pseudo-Random Binary Sequence*);
2. Coletar os sinais de entrada (PWM) e saída (velocidade) da planta;
3. Estimar um modelo que descreva a dinâmica da planta:
   - modelo de **1ª ordem com atraso** (FOPDT): $G(s) = \dfrac{K\,e^{-Ls}}{\tau s + 1}$;
   - aproximação de **Padé** do atraso (1ª e 10ª ordens);
4. Comparar os modelos com a resposta da planta real;
5. Discutir a **origem física do atraso** observado.

## 2. Bancada e software

O sistema de aquisição é formado por **Arduino** (controlador), **motor CC** (planta), **ponte H** (atuador) e **encoder magnético** (sensor). O firmware de aquisição está no repositório, em `firmware/prbs_aquisicao/`, e o script de telemetria/coleta em `firmware/telemetry.py`:

- o Arduino recebe do computador o comando de PWM (setpoint) via serial, estima a velocidade com o encoder e devolve os pares `(t, pwm, velocidade)`;
- o script `telemetry.py` grava os dados em CSV (`t, u, y`), pronto para análise em Python.

**No lugar do MATLAB/IDENT/tfest**, usaremos:

| Tarefa (2024/2, MATLAB) | Equivalente (2026/2, Python) |
|---|---|
| Geração do PRBS | firmware `prbs_aquisicao.ino` (variáveis `Tb` — período do bit — e `T` — duração total) |
| Reamostragem | `numpy.interp` sobre uma grade uniforme de período `Ts` |
| `ident` / `tfest` (FOPDT) | ajuste de curva com `scipy.optimize.curve_fit` (resposta ao degrau equivalente) ou mínimos quadrados na resposta PRBS |
| Aproximação de Padé | `control.pade(L, n)` + `control.series` |
| Comparação modelo × planta | `control.step_response` / `control.forced_response` |

> **Consulte:** teoria `modulo1_introducao/teoria_modulo1.md` §1.2 (modelos de 1ª ordem) e `modulo2_plano_s/teoria_modulo2.md` §2.5.6 (atraso de transporte e aproximação de Padé); Lab 09 (Padé com `control.pade`).

## 3. Roteiro

**Passo 1 — PRBS.** Carregue o firmware `prbs_aquisicao/` no Arduino e escolha o período de cada bit do PRBS (`Tb`). Regra prática: `Tb` deve ser da ordem de $\tau/5$ a $\tau/2$ da constante de tempo esperada da planta — rápido o suficiente para excitar a dinâmica, lento o suficiente para a saída responder. Ajuste a duração total (`T`) para conter dezenas de bits.

**Passo 2 — Coleta.** Execute `telemetry.py` para gerar os dados (PRBS = entrada; velocidade = saída) e salvar o CSV. **Se a resposta não ficar adequada** (saída "colada" nos trilhos ou sem variação visível), corrija `Tb`, ajuste `T` e repita.

**Passo 3 — Reamostragem.** Os dados não têm período de amostragem fixo (o laço do Arduino não é exato). Reamostre entrada e saída numa grade uniforme:

```python
import numpy as np
t, u, y = np.loadtxt("dados_motor.csv", delimiter=",", skiprows=1, unpack=True)
Ts = 0.02                                  # 20 ms — escolha e justifique
tg = np.arange(t[0], t[-1], Ts)
ug = np.interp(tg, t, u)
yg = np.interp(tg, t, y)
```

**Passo 4 — Estimação FOPDT.** Estime $K$, $\tau$ e $L$ de $G(s) = \dfrac{K e^{-Ls}}{\tau s + 1}$. Duas rotas aceitas:

- **(a) Ajuste direto na resposta PRBS** (recomendada): simule o candidato com `control.forced_response` e minimize o erro quadrático com `scipy.optimize.minimize`;
- **(b) Método gráfico/algébrico** sobre trechos quase-degrau do PRBS (ganho $K = \Delta y/\Delta u$; atraso $L$ pelo tempo morto; $\tau$ pelo ponto de 63,2%).

```python
import control as ct
from scipy.optimize import minimize

def custo(p):
    K, tau, L = p
    if K <= 0 or tau <= 1e-3 or L < 0:
        return 1e9
    nd = int(round(L / Ts))
    G = ct.tf([K], [tau, 1])
    _, ys = ct.forced_response(G, tg, np.roll(ug, nd))
    return np.mean((yg - ys) ** 2)

K, tau, L = minimize(custo, x0=[1.0, 0.5, 0.05], method="Nelder-Mead").x
```

**Passo 5 — Padé.** Aproxime o atraso com Padé de 1ª e 10ª ordens e monte os modelos equivalentes:

```python
num1, den1 = ct.pade(L, 1)      # e^{-Ls} ≈ (1 - Ls/2)/(1 + Ls/2)
num10, den10 = ct.pade(L, 10)
G_fopdt  = ct.tf([K], [tau, 1])                    # + atraso puro (para referência)
G_pade1  = ct.series(ct.tf([K], [tau, 1]), ct.tf(num1, den1))
G_pade10 = ct.series(ct.tf([K], [tau, 1]), ct.tf(num10, den10))
```

**Passo 6 — Comparação.** Aplique o **mesmo PRBS medido** aos três modelos (`forced_response`) e sobreponha à saída real. Reporte o erro quadrático médio de cada modelo e discuta: onde o Padé de 1ª ordem falha? O de 10ª ordem vale o custo?

**Passo 7 — Discussão do atraso.** Discuta a origem física do atraso encontrado: comunicação serial, amostragem/cálculo da velocidade por janela do encoder, dinâmica elétrica desprezada ($L_a$ da armadura), zona morta da ponte H. Quantifique a contribuição que você considera dominante.

## 4. Entrega e avaliação

- **Apresentação presencial** (agendar com o professor), máximo **10 minutos**, com **todos os integrantes** participando;
- Entregar, no repositório do grupo: o(s) CSV(s) de dados, o notebook/script Python da estimação e os gráficos comparativos;
- Serão avaliados: qualidade do PRBS (excitação), justificativa de `Tb`/`Ts`, correção numérica do modelo, qualidade da comparação e a discussão da origem do atraso.

**Bom trabalho!**
