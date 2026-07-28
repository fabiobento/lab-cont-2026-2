# Projeto Final — Controle PID de um sistema físico real

## Guia completo e autossuficiente

**Unidade IV** · Semanas 13–15 (6 h presenciais + trabalho extraclasse) · **Peso: 30 % (relatório) + 10 % (seminário)**

Este projeto materializa o objetivo geral da disciplina: *"desenvolver e testar, em um
sistema real de controle, controladores analógicos e digitais para sistemas físicos
dinâmicos."*

Esta é a **versão expandida** do guia do projeto: além das instruções originais, cada
planta traz agora a **fundamentação teórica completa** (modelo, identificação, sintonia de
partida e armadilhas) e cada etapa traz **procedimentos e checklists** com as fórmulas das
apostilas das Unidades I–IV — de modo que o grupo não precise consultar nenhum material
externo para executar o projeto do início ao fim.

---

## 1. Plantas disponíveis (grupos de 3–4 estudantes)

O laboratório dispõe de **3 kits idênticos** (motoredutor CC com encoder de quadratura,
ponte H L298N e Arduino com shield/display). Com o mesmo kit, dois problemas de controle
**estruturalmente diferentes** podem ser atacados; a planta térmica é uma terceira opção,
montável com componentes de baixo custo (ver lista de materiais no `firmware/README.md`).

| Opção | Planta | Variável controlada | Modelo esperado | Desafio central |
|---|---|---|---|---|
| A | Kit motor CC — **velocidade** | ω [rad/s] | $\dfrac{K_m}{\tau_m s + 1}$ (tipo 0, estável) | zona morta do conjunto ponte H + atrito; erro de regime exige ação I |
| B | Kit motor CC — **posição** | θ [rad] | $\dfrac{K_m}{s(\tau_m s + 1)}$ (tipo 1, polo na origem) | P puro oscila: quem amortece é o D; windup em degraus grandes; Nyquist com polo na origem |
| C | Sistema térmico (resistor de potência + LM35) | temperatura [°C] | FOPDT $\dfrac{K e^{-\theta s}}{\tau s + 1}$ | tempo morto; atuador unidirecional; ensaios longos |

Cada grupo assume **uma** opção; como as opções A e B usam o mesmo kit, os 3 kits atendem
até 6 grupos em regime de revezamento (A e B alternam bancada; a identificação da opção B
aproveita o modelo de velocidade da opção A: basta acrescentar o integrador).

Aquisição: Arduino (ou equivalente) executando o laço de controle com período fixo $h$ e
enviando telemetria $(t, r, y, u)$ pela serial; análise e projeto no Python com
`python-control`.

> **Firmware de referência:** a pasta `firmware/` do repositório contém sketches prontos
> para as três plantas (PID digital completo com anti-windup, modo relé para identificação,
> transferência manual/automático bumpless e telemetria CSV) e o registrador
> `telemetry.py`. Os grupos devem **calibrar as constantes de bancada, justificar o
> período de amostragem e compreender cada bloco do código** — o firmware é ponto de
> partida documentado, não caixa-preta, e o relatório deve explicar as escolhas feitas
> sobre ele.

### 1.A Fundamentação — Opção A: velocidade do motor CC

**Modelo (Unidade I, §5.5).** Desprezando a indutância de armadura, a FT tensão →
velocidade é de 1ª ordem:
$$G_{vel}(s) = \frac{\Omega(s)}{V(s)} = \frac{K_m}{\tau_m s + 1},\qquad
K_m = \frac{K_t}{R_ab_m + K_tK_e},\quad \tau_m = \frac{R_aJ}{R_ab_m + K_tK_e}.$$
O kit didático tem $K_m$ da ordem de alguns rad/s por volt e $\tau_m$ da ordem de 0,1–2 s —
mas os valores do **seu** kit saem do ensaio, não da teoria.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-2-35-nise.png)

**Figura P.1 — Servomotor CC controlado pela armadura: esquema eletromecânico usado na
dedução do modelo.** (Fonte: NISE, Figura 2.35, Cap. 2)

**Identificação (Unidade I, §6).** Como a resposta ao degrau não tem tempo morto apreciável,
basta: (i) característica estática — varra o PWM em degraus, registre $\omega_{regime}$ ×
PWM: a inclinação dá $K_m$ (em rad/s por unidade de PWM) e o **intercepto morto** dá a zona
morta $\delta$; (ii) dinâmica — num degrau, meça $t_{63}$ ⟹ $\tau_m = t_{63}$ (a resposta
cruza 63,2 % do regime em uma constante de tempo).

**Não-linearidades dominantes (Unidade III, §1).** Zona morta $\delta$ (banda de erro
residual $|e| \le \delta/K_p$ com P puro — por isso a ação I é obrigatória) e saturação do
PWM em 100 % (maior velocidade alcançável $\omega_{max} = K_m \cdot PWM_{max}$: **confira
se sua referência é alcançável antes de culpar a sintonia**).

**Sintonia de partida (Unidade IV).** Planta tipo 0 sem tempo morto: PI por lambda com
$T_i = \tau_m$ e $K_p = \dfrac{1}{K_m}\cdot\dfrac{\tau_m}{\lambda}$,
$\lambda = \tau_m/3$ como ponto de partida; PD raramente necessário. Auditar:
PM ≥ 45°, GM ≥ 6 dB. Ação I com **anti-windup** (degraus grandes saturam o PWM —
Unidade III, §2).

**Armadilhas de bancada:** velocidade por diferenças do encoder é ruidosa em baixa rotação
(filtre a medição, não o erro); a zona morta varia com a carga no eixo — meça-a no início
de cada sessão.

### 1.B Fundamentação — Opção B: posição do motor CC

**Modelo.** Acrescenta-se o integrador cinemático $\omega = \dot\theta$:
$$G_{pos}(s) = \frac{K_m}{s(\tau_m s + 1)}$$
— tipo 1, com **polo na origem**. Consequências diretas (Unidade II): erro de regime ao
degrau já é nulo com P puro (o integrador está na planta); o erro à rampa é $1/K_v$,
$K_v = K_pK_m$.

**O desafio central.** A malha fechada com P puro tem característica
$\tau_m s^2 + s + K_pK_m = 0$: o coeficiente de $s$ é fixo em $1/\tau_m$, logo
$\zeta = \dfrac{1}{2\sqrt{K_pK_m\tau_m}}$ **cai com o ganho** — o P puro oscila porque não
há quem forneça amortecimento. Quem amortece é a **ação D** (Unidade IV, §1.2): com PD,
$\tau_m s^2 + (1 + K_pK_mT_d)s + K_pK_m = 0$ e o termo $(1 + K_pK_mT_d)$ é ajustável. É o
caso em que a derivada (na medição, com filtro!) não é opcional.

**Estabilidade com polo na origem (Unidade II, §6.3).** O Bode de fase começa em $-90°$
pelo integrador; a leitura correta de estabilidade é pelo **Nyquist com o contorno
deformado** (indentação à direita do polo na origem ⟹ arco infinito). Nas simulações de
margem, interprete PM/GM com esse cuidado.

**Windup (Unidade III, §2).** Degraus grandes de posição saturam o PWM por períodos longos
(a planta é lenta para acompanhar): o integrador do controlador carrega e o sobressinal
explode. **Anti-windup por back-calculation é obrigatório**, e o 2DOF (ponderação $b < 1$
na referência — Unidade IV, §6) reduz o chute de referência.

**Identificação.** Não identifique posição diretamente (a resposta ao degrau cresce sem
limite — tipo 1!). Identifique **velocidade** como na opção A e monte $G_{pos} = G_{vel}/s$.
Valide com degrau pequeno em malha fechada proporcional conhecida.

**Sintonia de partida.** LGR (Unidade II, §4) sobre $G_{pos}$ escolhendo o zero do PD em
$-1/T_d$ para puxar os ramos para a esquerda; ou loop shaping: crossover alvo
$\omega_{gc} \approx 1/(2\tau_m)$, derivada para PM ≥ 50°, integral fraca ($T_i$ grande)
só para tirar o erro de atrito.

### 1.C Fundamentação — Opção C: sistema térmico

**Modelo (Unidade I, §1.5).** Balanço de energia no resistor/corpo aquecido:
$$C_t\frac{d\Delta T}{dt} + \frac{1}{R_t}\Delta T = \Delta q_{in}
\;\Rightarrow\;
G(s) = \frac{Ke^{-\theta s}}{\tau s + 1},\qquad K = R_t\ [\text{°C/W}],\ \ \tau = R_tC_t,$$
com tempo morto $\theta$ do atraso térmico sensor–resistor e transporte. Valores típicos
de bancada: $\tau$ de dezenas a centenas de segundos, $\theta$ de alguns segundos —
**ensaios longos**: planeje cada ensaio de degrau com $5\tau$ de duração.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-26-ogata.png)

**Figura P.2 — (a) Sistema térmico de tanque aquecido; (b) diagrama de blocos — a estrutura
de 1ª ordem $1/(RCs)$ dentro da malha.** (Fonte: OGATA, Figura 4.26, Cap. 4)

**Identificação (Unidade I, §6).** Curva de reação com o método dos dois pontos:
$\tau = 1{,}5(t_{63} - t_{28})$, $\theta = t_{63} - \tau$, $K = \Delta T_{regime}/\Delta u$.
Cuidados específicos: medir a **temperatura ambiente antes e depois** (ela deriva ao longo
do ensaio e contamina $K$); trabalhar em variáveis-desvio $\Delta T = T - T_{amb}$;
amplitude de degrau que aqueça o suficiente para vencer o ruído do LM35 sem superaquecer
(regra: ficar abaixo de 60 °C).

**Não-linearidades dominantes.** **Atuador unidirecional**: o resistor só aquece — o
resfriamento é passivo e lento; o controlador deve poder ficar com $u = 0$ por longos
períodos (anti-windup especialmente crítico na descida). Saturação em potência máxima;
convecção que varia com o ambiente (perturbação de carga = sopro/ar condicionado).

**Sintonia de partida (Unidade IV, §3).** É a planta dos métodos por modelo:
- ZN-1 (curva de reação): PI $K_p = 0{,}9\tau/(K\theta)$, $T_i = \theta/0{,}3$;
- CHR-0 % (servo): tipicamente a melhor "de tabela";
- **lambda (recomendado):** $K_p = \dfrac{1}{K}\cdot\dfrac{\tau}{\lambda + \theta}$,
  $T_i = \tau$, com $\lambda = \max(\theta, \tau/3)$; $T_d = \theta/2$ se o ruído do LM35
  permitir derivada.

**Período de amostragem (Unidade IV, §7).** $h \le \tau/20$ é trivialmente atendido:
$h = 0{,}1$–$0{,}5$ s. A limitação aqui não é taxa, é a **resolução do LM35** (0,1–0,5 °C):
use média de amostras por ciclo de controle.

---

## 2. Etapas obrigatórias e entregas

### Semana 13 — Identificação (usa Labs 02, 03 e 07)

1. Levantar a característica estática da planta (detectar zona morta e faixa útil do
   atuador) — procedimento detalhado por planta na §1 acima;
2. Aplicar ensaio de degrau em ponto de operação seguro e identificar o modelo
   (método dos dois pontos/tangente) **ou** executar o experimento do relé para obter
   $(K_u, T_u)$, com $K_u = 4d/(\pi a)$ (Unidade III, §4.3).
   *Opção B (posição):* identifique primeiro a dinâmica de velocidade (como na opção A) e
   acrescente o integrador: $G_{pos}(s) = G_{vel}(s)/s$;
3. Validar o modelo com um ensaio de amplitude diferente (reportar RMSE) —
   **checklist de validação:** mesmo ponto de operação? amplitude diferente da usada na
   identificação? RMSE pequeno em relação à variação total (regra prática: ≤ 10 %)?
   resíduos sem tendência (erro aleatório, não sistemático)?
4. **Entrega parcial 1:** notebook com dados brutos, modelo identificado e validação.

### Semana 14 — Projeto e implementação (usa Labs 08, 09, 10 e 11)

1. Sintonizar PI ou PID por **dois métodos** (por exemplo, ZN e lambda — fórmulas no §1 da
   sua planta e na apostila da Unidade IV, §3) e comparar em simulação
   ($M_p$, $t_s$, IAE e **esforço de comando** $u(t)$ — o quarto gráfico que muitos
   esquecem);
2. Auditar a sintonia escolhida: **PM ≥ 45°, GM ≥ 6 dB, $M_s \le 2$**
   (`ct.margin` e a *gang of four*, Unidade IV, §5);
3. Simular com a não-linearidade dominante identificada (saturação do PWM, zona morta) —
   a comparação linear × saturado deve aparecer no relatório;
4. Embarcar o PID digital (estrutura do Lab 10: derivada filtrada da medição, anti-windup
   por back-calculation, $h \le \tau/10$; equações na Unidade IV, §7.3) e ensaiar na
   bancada;
5. **Entrega parcial 2:** notebook de projeto + código embarcado + primeiro ensaio real.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-26-ogata.png)

**Figura P.3 — A arquitetura PI-D que deve estar no seu firmware: P e I sobre o erro, D
(filtrada) sobre a medição.** (Fonte: OGATA, Figura 8.26, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-13-4-nise.png)

**Figura P.4 — Por que $h$ importa: o segurador de ordem zero reconstrói o comando em
degraus, introduzindo um atraso médio de $h/2$ que consome margem de fase.**
(Fonte: NISE, Figura 13.4, Cap. 13)

### Semana 15 — Validação, relatório e seminário

1. Ensaios finais: degrau de referência, perturbação de carga (por exemplo, sopro no
   sistema térmico, atrito adicional no motor) e, se aplicável, comparação 1DOF × 2DOF
   (ponderação $b$ — Unidade IV, §6);
2. Comparar quantitativamente **bancada × simulação** ($M_p$, $t_s$, IAE) e discutir as
   discrepâncias (dinâmicas não modeladas, não-linearidades, quantização) — **a discussão
   das discrepâncias vale mais que a concordância**: é onde a análise crítica da rubrica
   mora;
3. Seminário de 15 min por grupo com demonstração ao vivo.

---

## 3. Estrutura do relatório técnico (máx. 12 páginas)

1. **Introdução e descrição da planta** — esquema elétrico/mecânico, instrumentação,
   faixas de operação e limites do atuador (incluindo a não-linearidade dominante);
2. **Identificação** — ensaios (com gráficos dos dados brutos), modelo com valores e
   unidades, validação com RMSE;
3. **Projeto do controlador** — os dois métodos comparados, a sintonia escolhida com
   justificativa, auditoria de robustez (PM/GM/$M_s$ + figuras de Bode/Nyquist),
   simulações com e sem não-linearidade;
4. **Implementação digital** — período de amostragem justificado, proteções (anti-windup,
   limites, desligamento), equações a diferenças efetivamente implementadas;
5. **Resultados experimentais** — ensaios finais, tabela bancada × simulação
   ($M_p$, $t_s$, IAE), análise crítica das discrepâncias;
6. **Conclusões e limitações** — o que o modelo não capturou; o que faria diferente;
7. **Apêndice** — código completo (notebooks + firmware).

## 4. Rubrica de avaliação

| Critério | Peso |
|---|---:|
| Qualidade da identificação e validação do modelo | 20 % |
| Fundamentação do projeto (método, auditoria de margens, simulações) | 25 % |
| Implementação digital correta (anti-windup, filtro, amostragem) | 20 % |
| Resultados experimentais e análise crítica bancada × modelo | 20 % |
| Clareza do relatório e do seminário; organização do código | 15 % |

**Critérios transversais (PPC):** articulação entre o saber estudado e problemas reais;
análise crítica; iniciativa e criatividade; organização e clareza na expressão dos
conceitos.

## 5. Segurança de bancada

- Limitar por firmware o PWM máximo e a temperatura máxima (desligamento automático);
- Nunca deixar o sistema térmico energizado sem supervisão;
- Verificar polaridade e correntes máximas da ponte H antes de energizar;
- No kit do motor, fixar a base antes de energizar (a roda gera reação de torque) e manter
  dedos/cabelos/cabos longe da roda em movimento;
- Conferir que o encoder está alimentado em 5 V (nunca na tensão da ponte H).

---

## 6. Folha de consulta do projeto (as fórmulas que você vai usar)

| Etapa | Fórmula | Fonte |
|---|---|---|
| Identificação 1ª ordem | $K = \Delta y/\Delta u$; $\tau = t_{63}$ | Unidade I, §4.1 |
| Identificação FOPDT | $\tau = 1{,}5(t_{63}-t_{28})$; $\theta = t_{63}-\tau$ | Unidade I, §6.3 |
| Experimento do relé | $K_u = 4d/(\pi a)$; $T_u$ medido | Unidade III, §4.3 |
| Alcançabilidade | $y_{max} = G(0)\,u_{max}$ | Unidade III, §1.1 |
| Erro de regime | tipo 0: $1/(1+K_{pos})$; tipo 1: rampa $1/K_v$ | Unidade II, §2 |
| Amortecimento | $\zeta \approx PM/100$; $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ | Unidades I–II |
| ZN-2 | PI: $0{,}45K_u$, $T_u/1{,}2$; PID: $0{,}6K_u$, $T_u/2$, $T_u/8$ | Unidade IV, §3.1 |
| ZN-1 | PI: $0{,}9\tau/(K\theta)$, $\theta/0{,}3$; PID: $1{,}2\tau/(K\theta)$, $2\theta$, $0{,}5\theta$ | Unidade IV, §3.2 |
| Lambda | $K_p = \frac{1}{K}\frac{\tau}{\lambda+\theta}$; $T_i = \tau$; $\lambda = \max(\theta,\tau/3)$ | Unidade IV, §3.4 |
| Auditoria | PM ≥ 45°; GM ≥ 6 dB; $M_s \le 2$ | Unidades II e IV |
| Anti-windup | $\dot I = \frac{K_p}{T_i}e + \frac{1}{T_t}(u_{sat}-v)$; $T_t = \sqrt{T_iT_d}$ | Unidade III, §2.2 |
| 2DOF | $u = K_p(br - y) + \frac{K_p}{T_i}\int e - K_pT_d\dot y$ | Unidade IV, §6 |
| Amostragem | $h \le \tau/20$ (curso: $\tau/10$); atraso efetivo ≈ $h/2$ | Unidade IV, §7 |
| PID digital | $D[k] = \alpha(y[k]-y[k-1]) + (1-\alpha)D[k-1]$, $\alpha = \frac{NT_d}{NT_d+h}$ | Unidade IV, §7.3 |

## Referências rápidas

Toda a teoria citada está desenvolvida nas apostilas completas do repositório:
`apostila_unidade1_completa.md` (modelagem, Laplace, 1ª/2ª ordem, identificação, Bode),
`apostila_unidade2_completa.md` (malha fechada, Routh, LGR, margens, Nyquist),
`apostila_unidade3_completa.md` (não-linearidades, windup, relé) e
`apostila_unidade4_completa.md` (PID, sintonia, 2DOF, digital). Livros-âncora: Ogata,
Nise, Schaum (DiStefano et al.), FBS (Åström & Murray, gratuito) e Åström & Hägglund.
