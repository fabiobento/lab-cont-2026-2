# Módulo 03 — Controle Usando a Resposta em Frequência (Teoria)

> Texto teórico dos tópicos 3.1 a 3.5.
> Convenções do curso (Módulos 01 e 02): sistemas **SISO**; estabilidade = **BIBO**; malha padrão com realimentação unitária; $M_p = e^{-\zeta\pi/\sqrt{1-\zeta^2}}$; $t_p = \pi/\omega_d$; $t_r = (\pi - \arccos\zeta)/\omega_d$; $t_s(5\,\%) = 3/\sigma$.
> **Novidades deste módulo:** a **resposta em frequência** como dado experimental do sistema; o **diagrama de Bode** e seus esboços assintóticos; as margens de **fase (PM)** e de **ganho (GM)**; a **carta de Nichols-Black**; o **critério de Nyquist**; o **atraso de transporte** na frequência; e o projeto de **P**, **avanço**, **atraso**, **PD**, **PI** e **PID** diretamente no domínio da frequência — inclusive **sem conhecer a função de transferência**.
> **Convenção de esboço do curso:** quebras de módulo de ±20 dB/déc por polo/zero; fase interpolada por **reta de $\omega_q/5$ a $5\,\omega_q$** em torno de cada quebra (erro máximo ≈ **11°** = 0,19 rad); erro máximo de módulo de **3 dB** na quebra.
> **Ponte frequência ↔ tempo:** $\mathrm{PM} \approx 100\,\zeta$ (boa até $\zeta \approx 0{,}65$); $\omega_n \approx \omega_r \approx \omega_c$; e **sempre** uma folga de **5–10°** na PM para absorver as aproximações.

---

## 3.1 Resposta em Frequência e Diagrama de Bode

### 3.1.1 O desafio: projetar um controlador sem modelo?

Imagine a seguinte aposta. Um engenheiro experiente traz um carrinho motorizado (saída = posição, entrada = tensão no motor) e propõe: *"Projete um **controlador proporcional** que faça a malha fechada responder ao degrau com **30 % de overshoot**. Você **não** pode usar equações diferenciais nem função de transferência. Você tem **uma única chance** de fechar a malha — mas pode testar o sistema em **malha aberta** com quaisquer entradas, quantas vezes quiser."*

Parece impossível? Todos os nossos métodos até aqui (Módulos 01 e 02) partem da função de transferência. Mas há sistemas em que o modelo por princípios físicos **não existe na prática**: sistemas complexos demais, subsistemas inacessíveis, componentes cujos parâmetros desconhecemos. Foi exatamente esse o problema enfrentado pelos engenheiros dos **Laboratórios Bell nas décadas de 1920–1940** — **Black**, **Nyquist** e **Bode** — ao projetar os amplificadores dos primeiros cabos telefônicos transcontinentais. Sem computadores, eles desenvolveram técnicas **gráficas e experimentais** de uma simplicidade e poder impressionantes — e que até hoje estão entre as mais usadas na indústria.

A pergunta que guia o módulo: **o que podemos aprender sobre um sistema medindo apenas como ele responde a senoides de várias frequências?** A resposta: praticamente tudo — inclusive como projetar o controlador.

### 3.1.2 Resposta em frequência de sistemas LIT

Considere um sistema **linear e invariante no tempo (LIT)**, estável, com função de transferência

$$G(s) = \frac{K\,N(s)}{\prod_i (s - p_i)}, \qquad \mathrm{Re}(p_i) < 0,$$

excitado por uma **senoide** $u(t) = A\,\mathrm{sen}(\omega t)$. O que acontece com a saída?

**Dedução.** Escrevendo a senoide como $u(t) = \dfrac{A}{2j}\left(e^{j\omega t} - e^{-j\omega t}\right)$ e expandindo $Y(s) = G(s)U(s)$ em frações parciais, aparecem: (i) os termos associados aos polos $p_i$ de $G$ — que, sendo o sistema estável, **morrem com o tempo** ($e^{p_i t} \to 0$); e (ii) os termos associados aos polos da entrada, em $s = \pm j\omega$. O resíduo do termo em $s = j\omega$ é

$$a_0 = \lim_{s \to j\omega} (s - j\omega)\,G(s)\,\frac{A}{2j}\left(\frac{1}{s - j\omega} - \frac{1}{s + j\omega}\right) = \frac{A\,G(j\omega)}{2j}.$$

Sobrando apenas os termos que não morrem (o **regime permanente senoidal**):

$$y(t) = a_0 e^{j\omega t} + \bar{a}_0 e^{-j\omega t} = \frac{A\,|G(j\omega)|}{2j}\left(e^{j(\omega t + \angle G(j\omega))} - e^{-j(\omega t + \angle G(j\omega))}\right)$$

$$\boxed{\;y(t) = |G(j\omega)|\;A\;\mathrm{sen}\big(\omega t + \angle G(j\omega)\big)\;}$$

**Leitura do resultado (decora-se em 5 segundos e usa-se a vida inteira):** a saída em regime é uma senoide de **mesma frequência** da entrada, com **amplitude multiplicada por $|G(j\omega)|$** e **fase somada de $\angle G(j\omega)$**. O número complexo $G(j\omega)$ — a FT avaliada no eixo imaginário — **é** a resposta em frequência do sistema.

> ⚠️ **Por que "regime permanente"?** No início da resposta há também o transitório (os termos que morrem). Como o sistema é estável, basta esperar "alguns $t_s$" e sobra só a senoide de regime. É por isso que o ensaio experimental funciona: injeta-se a senoide, espera-se o transitório morrer, mede-se amplitude e defasagem.

**Exemplo-âncora (circuito RC).** $G(s) = \dfrac{1}{0{,}1034\,s + 1}$ ($R = 470\,\mathrm{k}\Omega$, $C = 220\,\mathrm{nF}$). Avaliando em três frequências:

| $\omega$ (rad/s) | $\|G(j\omega)\|$ | $\angle G(j\omega)$ | saída em regime (entrada de amplitude 1) |
|---|---|---|---|
| 1 | 0,995 | −5,9° | praticamente igual à entrada |
| 10 | 0,695 | −46,0° | amplitude cai para ~70 %, atraso crescente |
| 100 | 0,096 | −84,5° | quase nada passa; defasagem perto de −90° |

![Resposta em frequência do RC](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig01_resposta_frequencia.png)

O circuito é um **filtro passa-baixas**: frequências baixas passam, altas são atenuadas e defasadas. Todo sistema LIT estável "filtra" senoides dessa maneira — e a tabela (frequência → ganho, defasagem) **caracteriza completamente** o sistema.

> ✏️ **Pense:** por que a fase é negativa (atraso) e não positiva (adiantamento)? Um sistema causal não pode "prever" a entrada — lembre-se do "sistema adivinho" do Módulo 02.

### 3.1.3 Da medição ao diagrama de Bode

Num ensaio experimental, injetamos $u(t) = A\,\mathrm{sen}(\omega t)$ e medimos, em regime:

- **módulo:** $|G(j\omega)| = \dfrac{\text{amplitude da saída}}{\text{amplitude da entrada}}$;
- **fase:** medimos o atraso $\Delta t$ entre os picos da saída e da entrada e usamos a **regra de três** $\dfrac{\Delta t}{T} = \dfrac{|\angle G(j\omega)|}{360°}$ (um período $T$ corresponde a $360°$).

Repetindo para muitas frequências, obtemos uma tabela — e dela, um gráfico. Dois problemas práticos aparecem imediatamente:

1. **as frequências de interesse cobrem várias ordens de grandeza** (de 0,01 a 1000 rad/s, por exemplo) → eixo de frequências **logarítmico**;
2. **o módulo também varia por ordens de grandeza** → módulo em **decibéis**:
$$\boxed{|G(j\omega)|_{\mathrm{dB}} = 20\,\log_{10}|G(j\omega)|}$$

O **diagrama de Bode** é o par de gráficos: **módulo em dB × $\log_{10}\omega$** e **fase em graus × $\log_{10}\omega$**.

> 📌 **Para guardar:** $|G| = 1 \leftrightarrow 0$ dB; $10 \leftrightarrow 20$ dB; $100 \leftrightarrow 40$ dB; $0{,}1 \leftrightarrow -20$ dB; $2 \leftrightarrow +6$ dB; $1/2 \leftrightarrow -6$ dB; $\sqrt{2} \leftrightarrow +3$ dB. Multiplicar o ganho por $K$ **soma** $20\log_{10}K$ ao módulo — a escala log transforma multiplicações em somas (e é por isso que polos e zeros "somam contribuições", como veremos).

### 3.1.4 Da FT ao Bode (sem tabela)

Se conhecemos $G(s)$, não precisamos medir nada: basta **substituir $s$ por $j\omega$** e calcular módulo e fase. Para o RC:

$$G(j\omega) = \frac{1}{0{,}1034\,j\omega + 1} \;\Rightarrow\; |G(j\omega)| = \frac{1}{\sqrt{(0{,}1034\,\omega)^2 + 1}}, \qquad \angle G(j\omega) = -\mathrm{arctg}(0{,}1034\,\omega).$$

Em altas frequências ($\omega \gg 1/0{,}1034$): $|G|_{\mathrm{dB}} \approx -20\log_{10}(0{,}1034) - 20\log_{10}\omega$ — uma **reta** no eixo log, que cai 20 dB por década. E a fase tende a $-90°$. Esse comportamento "de retas" é geral — e é a base dos esboços assintóticos.

### 3.1.5 Esboço de Bode de 1ª ordem

Seja $G(s) = \dfrac{K}{s - p_1}$, $p_1 < 0$. Temos $|G(j\omega)| = \dfrac{|K|}{\sqrt{\omega^2 + p_1^2}}$ e $\angle G(j\omega) = -\mathrm{arctg}(\omega/|p_1|)$.

**Módulo — duas assíntotas** que se encontram na **frequência de quebra** $\omega_q = |p_1|$:

- $\omega \ll |p_1|$: $|G|_{\mathrm{dB}} \approx 20\log|K| - 20\log|p_1|$ (**reta horizontal**);
- $\omega \gg |p_1|$: $|G|_{\mathrm{dB}} \approx 20\log|K| - 20\log\omega$ (**reta de −20 dB/déc**).

**Erro máximo:** na quebra, o valor exato é $|G(j|p_1|)| = \dfrac{|K|}{\sqrt{2}\,|p_1|}$, ou seja, **−3 dB abaixo da assíntota** — o maior erro do esboço de módulo. ($1/\sqrt{2} = 0{,}707 \leftrightarrow -3{,}01$ dB.)

**Fase — convenção do curso:** a fase exata é $-\mathrm{arctg}(\omega/|p_1|)$, que vai de $0°$ a $-90°$ passando por **−45° na quebra**. Esboçamos por três segmentos:

- $0°$ para $\omega < |p_1|/5$;
- **reta de $|p_1|/5$ a $5\,|p_1|$** (no eixo log), passando por −45° na quebra — **tangente à curva exata**;
- $-90°$ para $\omega > 5\,|p_1|$.

A reta tem inclinação de $90°/\log_{10}(25) = 64{,}4°$/década. **Erro máximo da fase: ≈ 11° (0,19 rad)**, nos pontos $|p_1|/5$ e $5\,|p_1|$.

![Bode assintótico × exato de 1ª ordem](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig02_bode_1a_ordem.png)

> 📌 **Convenção, não erro:** em alguns textos a reta da fase vai de $\omega_q/10$ a $10\,\omega_q$ ("uma década antes e depois", erro máx. 5,7°). **Neste curso usamos $\omega_q/5$ a $5\,\omega_q$** — é a construção que usaremos em todos os esboços e projetos, e é ela que dá o erro máximo de ≈ 11°.

**Zero de 1ª ordem:** $G(s) = K(s - z_1)$, $z_1 < 0$ — o efeito é o **oposto**: módulo sobe +20 dB/déc após a quebra em $|z_1|$; fase sobe de $0°$ a $+90°$ pela mesma reta de $|z_1|/5$ a $5|z_1|$.

### 3.1.6 Esboço de 2ª ordem com polos reais

Seja $G(s) = \dfrac{K}{(s-p_1)(s-p_2)}$, $p_1, p_2 < 0$. Em dB, **o módulo é a soma das contribuições**:

$$|G|_{\mathrm{dB}} = 20\log|K| - 20\log|s-p_1|\Big|_{s=j\omega} - 20\log|s-p_2|\Big|_{s=j\omega}$$

e a fase também: $\angle G = \angle K - \mathrm{arctg}(\omega/|p_1|) - \mathrm{arctg}(\omega/|p_2|)$. Logo:

- **módulo:** plano → **−20 dB/déc** após a 1ª quebra → **−40 dB/déc** após a 2ª;
- **fase:** $0°$ → **−90°** → **−180°**, com uma reta de $\omega_q/5$ a $5\,\omega_q$ por polo (se as retas se sobrepuserem, somam-se as contribuições em cada frequência).

![Bode de 2ª ordem com polos reais](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig03_bode_2a_polos_reais.png)

Na figura, com quebras separadas por 2 décadas ($p_2 = 100\,p_1$), o erro máximo da fase é ≈ **11,4°** — duas vezes o erro de um polo só nas vizinhanças das quebras. Como sempre confrontamos o esboço com a simulação, esse erro é mais do que aceitável para projeto.

> ✏️ **Pense:** e se fosse um zero e um polo, $|z_1| < |p_1|$? O módulo subiria +20 dB/déc e depois voltaria a cair, ficando plano; a fase subiria e retornaria a 0°. Guarde essa imagem — ela **é** o compensador de avanço de fase do §3.4.

### 3.1.7 Esboço de sistemas tipo 1 (polo na origem)

Seja $G(s) = \dfrac{K}{s(s-p_1)}$, $p_1 < 0$. O polo na origem tem quebra em $\omega = 0$ — que "some no $-\infty$" do eixo logarítmico. Consequências:

- **módulo:** a assíntota **já começa em −20 dB/déc** (contribuição do integrador $20\log K - 20\log\omega$), passando a **−40 dB/déc** após a quebra em $|p_1|$;
- **posicionar a assíntota:** vale $|G(j\omega)| \approx K/\omega$ antes da quebra — em particular, em $\omega = 1$: $|G| \approx K$ (ou seja, a assíntota inicial passa por $20\log K$ dB em $\omega = 1$);
- **fase:** **começa em −90°** (o integrador) e vai a −180° após a quebra.

![Bode de sistema tipo 1](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig04_bode_tipo1.png)

**Conexão preciosa com o Módulo 01 (erro em regime):** sistema **tipo 1** ⇔ $k_p = G(0) = \infty$ ⇔ erro nulo ao degrau. No Bode, $G(0) = \infty$ aparece como **ganho que cresce quando $\omega \to 0$** — ou seja, **assíntota de baixas frequências com inclinação de pelo menos −20 dB/déc ⇔ $e_{ss} = 0$ ao degrau**. A informação do erro em regime está nas **baixas frequências**; a do transitório, como veremos, nas vizinhanças do **cruzamento de 0 dB**.

### 3.1.8 Margem de fase e margem de ganho

Considere a malha fechada padrão com realimentação unitária e $G(s)$ em malha aberta. Os polos de malha fechada são as raízes de $1 + G(s) = 0$, ou seja, os pontos onde

$$G(s) = -1 \qquad (\text{módulo } 1, \text{ fase } -180°).$$

O **ponto crítico** $-1$ é o limiar da estabilidade: se a resposta em frequência $G(j\omega)$ "passa por $-1$" (módulo 1 **e** fase −180° na mesma frequência), a malha fechada tem polos sobre o eixo imaginário. As **margens** medem **o quanto estamos longe** desse ponto, com duas frequências-chave:

- $\boldsymbol{\omega_c}$ — **frequência de cruzamento**: $|G(j\omega_c)| = 1$ (0 dB);
- $\boldsymbol{\omega_f}$ — **frequência de fase**: $\angle G(j\omega_f) = -180°$.

$$\boxed{\mathrm{PM} = \angle G(j\omega_c) + 180°} \qquad\qquad \boxed{\mathrm{GM} = -|G(j\omega_f)|_{\mathrm{dB}}}$$

**Leitura:** a PM é "quantos graus faltam para a fase chegar a −180° na frequência em que o módulo vale 1" — a **distância angular** do ponto crítico. A GM é "quantos dB ainda posso aumentar o ganho antes de o módulo valer 1 na frequência em que a fase é −180°" — a **distância de ganho** do ponto crítico. PM > 0 e GM > 0 (com as hipóteses usuais) ⇔ malha fechada estável — e quanto maiores, mais "longe" da instabilidade.

**Efeito do ajuste de ganho.** Multiplicar a malha aberta por $K > 0$: o módulo **translada** de $20\log K$ dB (sobe se $K > 1$, desce se $K < 1$) e a **fase não muda**. Consequências diretas:

- $K > 1$: $\omega_c$ aumenta (cruzamento acontece mais à direita) → em geral **PM diminui** (resposta mais rápida e mais oscilatória);
- $K < 1$: $\omega_c$ diminui → **PM aumenta** (mais lento e mais amortecido).

![Margens no Bode e efeito do ganho](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig05_margens_bode.png)

Na figura: $G(s) = \dfrac{0{,}95}{s(s+1)(s+5)}$ tem $\omega_c = 0{,}187$ rad/s, **PM = 77,3°**, $\omega_f = 2{,}23$ rad/s, **GM = 30,0 dB**. Multiplicando por $K = 5$ (+14 dB), o cruzamento sobe para 0,751 rad/s e a PM cai para **44,5°** — sem tocar na fase.

### 3.1.9 A ponte com o tempo: PM × sobressinal

As margens vivem na frequência; nossos requisitos vivem no tempo. A ponte, para o sistema de **2ª ordem tipo 1** $G(s) = \dfrac{\omega_n^2}{s(s + 2\zeta\omega_n)}$, é **exata** e vale a dedução rápida: o cruzamento acontece em $\omega_c = \omega_n\sqrt{\sqrt{1+4\zeta^4} - 2\zeta^2}$, e substituindo na definição de PM:

$$\mathrm{PM} = \mathrm{arctg}\left(\frac{2\zeta}{\sqrt{\sqrt{1+4\zeta^4} - 2\zeta^2}}\right)$$

Traçando PM × $\zeta$, a curva é **praticamente uma reta até $\zeta \approx 0{,}65$** (erro de ~5°):

$$\boxed{\mathrm{PM} \approx 100\,\zeta}$$

E, com $\omega_n \approx \omega_c$ (confronte: $\omega_c/\omega_n = \sqrt{\sqrt{1+4\zeta^4}-2\zeta^2}$ varia só entre 1 e 0,79 para $\zeta \in [0{,}3;\,1]$), temos o **kit de tradução frequência ↔ tempo**:

$$\mathrm{PM} \approx 100\,\zeta, \qquad \omega_n \approx \omega_c, \qquad \text{e daí } M_p,\ t_p,\ t_r,\ t_s \text{ pelas fórmulas do Módulo 01.}$$

![PM × ξ](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig06_pm_x_zeta.png)

**Exemplo numérico.** $G(s) = \dfrac{1}{s(s+1)}$ ($\omega_n = 1$, $\zeta = 0{,}5$): $\omega_c = 0{,}786$ rad/s, PM = 51,8° → $\zeta \approx 0{,}5$ → $M_p \approx 16\,\%$ ✔ (simulação: 16,3 %). Triplicando o ganho ($3G$): $\omega_c = 1{,}594$ rad/s, PM = 32,1° → $\zeta \approx 0{,}32$ → $M_p \approx 35\,\%$ (simulação: 38,8 % — a aproximação já cobra seu preço; veremos a folga que resolve isso).

### 3.1.10 Projeto do ganho P pela margem de fase (1º projeto do módulo)

**Receita.** Requisito de overshoot $M_p$ → $\zeta$ (pela inversa da fórmula do overshoot) → **PM alvo = $100\,\zeta$** → no diagrama de Bode (medido ou calculado) da malha aberta:

1. encontre a frequência $\omega$ em que a **fase** vale $\mathrm{PM}_{alvo} - 180°$ — ela será o novo $\omega_c$;
2. faça o módulo valer 1 nessa frequência: $\boxed{K = 1/|G(j\omega)|}$ (em dB: $K_{\mathrm{dB}} = -|G(j\omega)|_{\mathrm{dB}}$).

**Folga de segurança (regra prática do curso):** as aproximações ($\mathrm{PM} \approx 100\zeta$, $\omega_n \approx \omega_c$, sistema não é 2ª ordem exata) custam alguns graus e alguns pontos percentuais. Como requisitos de $M_p$ são **desigualdades** ("$M_p \leq X$"), projetamos com **5–10° a mais** de PM: $\mathrm{PM}_{proj} = 100\zeta + (5°\text{ a }10°)$. PM a mais nunca estraga um requisito de overshoot máximo.

**Exemplo-âncora.** $G(s) = \dfrac{10}{s(s+2)}$, requisito $M_p \leq 20\,\%$ (± alguns pontos).

- Com $K = 1$: simulação mostra $M_p = 35{,}1\,\%$ ✗;
- $M_p = 20\,\% \Rightarrow \zeta = 0{,}456 \Rightarrow$ PM alvo $= 45°$ → fase alvo $= -135°$;
- no Bode: fase $= -135{,}0°$ em $\omega = 2$ rad/s, onde $|G(j2)| = 1{,}77$ (4,95 dB);
- $K = 1/1{,}77 = 0{,}56$ → novo $\omega_c = 2$ rad/s, PM = 45°;
- **simulação: $M_p = 23{,}3\,\%$** — um pouco acima dos 20 %, exatamente o custo das aproximações (com folga de +5°, teríamos ficado abaixo).

![Projeto de P pela PM](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig07_projeto_P_pm.png)

> 🏆 **O desafio do início do módulo, resolvido:** projetamos o ganho proporcional para um requisito de overshoot **sem escrever uma equação diferencial, sem fechar a malha uma única vez** — apenas medindo (ou calculando) a resposta em frequência em malha aberta. Se a planta for desconhecida, a tabela de $|G|$ e $\angle G$ vem do **ensaio com senoides**; o procedimento é idêntico.

---

## 3.2 Carta de Nichols-Black e Especificação de Desempenho no Domínio da Frequência

### 3.2.1 Bode de 2ª ordem subamortecido: o pico de ressonância

Até aqui esboçamos sistemas com polos reais. E quando os polos são **complexos conjugados subamortecidos**? Seja

$$G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}, \qquad \zeta < 1.$$

O módulo é $|G(j\omega)| = \dfrac{\omega_n^2}{\sqrt{(\omega_n^2 - \omega^2)^2 + (2\zeta\omega_n\omega)^2}}$. As assíntotas continuam valendo (0 dB até $\omega_n$, −40 dB/déc depois), mas o que acontece **perto da quebra** depende fortemente de $\zeta$: para $\zeta$ pequeno, o denominador fica pequeno e aparece um **pico de ressonância**.

Derivando $|G(j\omega)|$ em relação a $\omega$ e igualando a zero, encontra-se a **frequência de ressonância** e o **pico de ressonância**:

$$\boxed{\omega_r = \omega_n\sqrt{1 - 2\zeta^2} \quad (\zeta \leq 0{,}707)} \qquad\qquad \boxed{M_r = \frac{1}{2\zeta\sqrt{1-\zeta^2}}}$$

(Para $\zeta > 0{,}707$ não há pico — a curva desce monotonicamente.)

**Exemplo.** $\zeta = 0{,}3$, $\omega_n = 1$: $\omega_r = \sqrt{1 - 0{,}18} = 0{,}906$ rad/s; $M_r = \dfrac{1}{2 \times 0{,}3 \times 0{,}954} = 1{,}75$ (4,85 dB).

![Bode subamortecido: família em ξ](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig08_bode_subamortecido.png)

Repare na ponte que se desenha: $M_p$ (tempo) ↔ $\zeta$ ↔ $M_r$ (frequência). **O pico de ressonância é o "overshoot do domínio da frequência"** — e em breve ele vai nos dar um segundo caminho para ler o amortecimento diretamente de um gráfico.

### 3.2.2 Malha aberta × malha fechada: o cálculo ponto a ponto

A pergunta central da seção: **conhecendo a resposta em frequência de malha aberta $G(j\omega)$, qual é a de malha fechada $T(j\omega) = \dfrac{G(j\omega)}{1 + G(j\omega)}$?**

Se temos $G(j\omega)$ tabelado (ensaio experimental!), podemos calcular ponto a ponto. Escrevendo $G(j\omega) = |G|(\cos\varphi + j\,\mathrm{sen}\,\varphi)$:

$$|T(j\omega)| = \frac{|G|}{\sqrt{(1 + |G|\cos\varphi)^2 + (|G|\,\mathrm{sen}\,\varphi)^2}}, \qquad \angle T(j\omega) = \varphi - \mathrm{arctg}\left(\frac{|G|\,\mathrm{sen}\,\varphi}{1 + |G|\cos\varphi}\right).$$

Funciona — mas é tedioso (nos anos 1940, muito tedioso). Dois casos limites ajudam a intuir:

- $|G| \gg 1$ (baixas frequências): $T \approx 1$ — a malha fechada "copia" a referência;
- $|G| \ll 1$ (altas frequências): $T \approx G$ — malha fechada ≈ malha aberta.

**Exemplo (RC, $K = 1$).** No ponto $(0°;\ 0$ dB$)$: $|T| = \dfrac{1}{\sqrt{(1+1)^2}} = \dfrac{1}{2} = -6{,}02$ dB, $\angle T = 0° - \mathrm{arctg}(0) = 0°$. Em $\omega = 100$ ($-84{,}5°$; $-20{,}3$ dB): $|T| \approx -20{,}3$ dB, $\angle T \approx -84{,}5°$ — é o caso $|G| \ll 1$, $T \approx G$.

Complicado fazer à mão para dezenas de pontos, não? Foi para resolver exatamente isso que nasceu a ferramenta a seguir.

### 3.2.3 A carta de Nichols-Black

A **carta de Nichols-Black** é um papel milimetrado especial:

- **eixos:** fase de malha aberta (graus) × módulo de malha aberta (dB) — ou seja, as duas informações do Bode fundidas numa única curva parametrizada por $\omega$;
- **impressos no papel:** os **lugares geométricos de $|T|$ constante** (em dB) e de $\angle T$ constante (em graus) — as curvas que respondem "se a malha aberta passa por este ponto, a malha fechada vale tanto".

**Como usar:** desenha-se a curva de malha aberta (fase × módulo, marcando algumas frequências ao longo dela) e **lê-se diretamente** o módulo e a fase de malha fechada onde a curva cruza os lugares impressos. A "perda" da referência explícita de frequência é o preço — por isso marcamos frequências na curva.

![A carta de Nichols-Black](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig09_carta_nb.png)

Na figura, a curva do RC ($K = 1$): passa por $(0°;\ 0\ \mathrm{dB})$ — e o lugar geométrico que passa por ali é o de $|T| = -6$ dB, $\angle T = 0°$ (confira com o cálculo ponto a ponto acima!); em $\omega = 100$, está praticamente sobre o lugar de $-20$ dB — $T \approx G$.

> 📌 **Geometria da carta:** os lugares de $|T|$ são "ilhas" em torno do ponto crítico $(-180°;\ 0\ \mathrm{dB})$ — quanto mais perto dele a curva passa, maior o $|T|$ de malha fechada (ressonância!). Os lugares de $\angle T$ são curvas quase verticais. Os valores ±(0,25–12) dB e de −15° em −15° são os mais usados.

### 3.2.4 Ajuste de ganho na carta: a translação vertical

Multiplicar a malha aberta por $K$: a fase não muda e o módulo soma $20\log K$ dB — na carta, isso é uma **translação vertical pura** da curva inteira. Antigamente, desenhava-se a curva num **papel transparente** e arrastava-se sobre a carta até a tangência desejada — projeto gráfico literal.

**Exemplo-âncora.** $G(s) = \dfrac{100}{s^2 + 4s + 29}$:

- $K = 1$: a curva cruza 0 dB com fase ≈ −154° → $\omega_c \approx 11$ rad/s, **PM ≈ 26°**;
- $K = 10$ (+20 dB): a curva inteira sobe 20 dB; o novo cruzamento acontece com fase ≈ −173° → $\omega_c \approx 32$ rad/s, **PM ≈ 7°** — quase instável!

![Ajuste de ganho na carta](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig10_nb_ajuste_ganho.png)

A leitura de PM na carta é imediata: **PM = 180° + (fase no ponto em que a curva cruza a linha de 0 dB)**. E o pico de ressonância de malha fechada é o **maior lugar de $|T|$ que a curva tangencia**.

### 3.2.5 A dupla PM ↔ Mr e ωc ≈ ωr (exemplo-âncora)

Vamos juntar tudo num exemplo que será referência para os projetos: $G(s) = \dfrac{2{,}4}{s(s+1{,}2)}$, malha fechada $T(s) = \dfrac{2{,}4}{s^2 + 1{,}2s + 2{,}4}$.

**Leitura na carta:** a curva de malha aberta **tangencia o lugar de 3 dB** → $M_r = 3$ dB $= 1{,}41$. Da fórmula do pico de ressonância (§3.2.1), agora usada **ao contrário**:

$$1{,}41 = \frac{1}{2\zeta\sqrt{1-\zeta^2}} \;\Rightarrow\; 8\zeta^4 - 8\zeta^2 + 1 = 0 \;\Rightarrow\; \zeta^2 = \frac{8 \pm \sqrt{64-32}}{16} \;\Rightarrow\; \zeta = 0{,}38 \ \text{ou}\ 0{,}92.$$

Descartamos $\zeta = 0{,}92$ (a fórmula de $M_r$ exige $\zeta \leq 0{,}707$ — e sistemas com $\zeta$ alto não têm pico). Com $\zeta = 0{,}38$: $M_p = e^{-\pi \times 0{,}38/\sqrt{1-0{,}38^2}} \approx 0{,}27$.

**E as frequências?** No zoom da carta, o ponto de tangência com o lugar de 3 dB ($\omega_r$) e o cruzamento de 0 dB ($\omega_c$) acontecem praticamente na mesma frequência: $\omega_r \approx \omega_c \approx 1{,}3$ rad/s. E como $\omega_n \approx \omega_c$, prevemos o transitório inteiro:

$$t_r = \frac{\pi - \arccos(0{,}38)}{1{,}3\sqrt{1-0{,}38^2}} \approx 1{,}5\ \mathrm{s}.$$

**Conferindo na simulação:** $M_p = 26{,}7\,\%$ (previsto 27 %!) e $t_r = 1{,}38$ s (previsto ~1,5 s — erro < 10 %).

![Mr e ωr ≈ ωc na carta](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig11_nb_mr_wc.png)

**O kit de tradução completo (agora com dois caminhos para $\zeta$):**

$$\mathrm{PM} \approx 100\,\zeta \quad\text{ou}\quad M_r = \frac{1}{2\zeta\sqrt{1-\zeta^2}}; \qquad \omega_n \approx \omega_r \approx \omega_c; \qquad \text{fórmulas de } M_p, t_r, t_p, t_s.$$

### 3.2.6 Até onde vão as traduções? (2ª ordem tipo 0 e 3ª ordem)

As relações acima foram deduzidas para 2ª ordem **tipo 1** sem zeros. Será que valem para outros sistemas? Vamos testar a cara e a coragem — aplicando-as onde "não deveriam" valer.

**Teste 1 — 2ª ordem tipo 0:** $G(s) = \dfrac{3}{(s+0{,}02)(s+1)}$. Do Bode: $\omega_c = 1{,}6$ rad/s, fase = −147° → **PM = 33°**. Fingindo que valem as relações: $\zeta \approx 0{,}33$, $\omega_n \approx 1{,}6$ → $M_p \approx 33\,\%$, $t_r \approx 1{,}2$ s. **Simulação: $M_p = 38{,}1\,\%$, $t_r = 1{,}13$ s** — boa aproximação! (Na carta, a curva fica entre os lugares de 3 e 6 dB → $M_r \approx 5$ dB → $\zeta \approx 0{,}3$ → $M_p \approx 37\,\%$ — coerente pelo segundo caminho.)

**Teste 2 — 3ª ordem:** $G(s) = \dfrac{60}{(s+0{,}02)(s+1)(s+15)}$. Do Bode: $\omega_c = 1{,}9$ rad/s, **PM = 22°** → $\zeta \approx 0{,}22$, $\omega_n \approx 1{,}9$ → $M_p \approx 49\,\%$, $t_r \approx 1$ s. **Simulação: $M_p = 54{,}5\,\%$, $t_r = 0{,}97$ s** — ainda muito razoável!

![Extensão das relações](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig12_extensao_relacoes.png)

> 📌 **Regra de tradução (com carimbo de honestidade):** as relações $\mathrm{PM} \approx 100\,\zeta$, $M_r \leftrightarrow \zeta$ e $\omega_n \approx \omega_c$ **valem, com algum cuidado, para qualquer sistema** — 2ª ordem tipo 0, 3ª ordem, ordens maiores. A precisão cai conforme o sistema se afasta do "par dominante de 2ª ordem", e é por isso que projetamos com **folga de 5–10° na PM** e sempre **conferimos por simulação**. É o preço honesto de projetar sem modelo.

### 3.2.7 Projeto com requisito de sobressinal (3ª ordem)

**Problema:** $G(s) = \dfrac{60}{(s+0{,}02)(s+1)(s+15)}$ (o sistema do Teste 2, com $M_p = 54\,\%$). **Requisito: $M_p < 30\,\%$.**

1. $M_p = 30\,\% \Rightarrow \zeta = 0{,}36$; folga: escolhemos $\zeta = 0{,}40$ ($M_p = 25\,\%$) → **PM alvo = 40° + 5° de folga = 45°** → fase alvo = −135°;
2. no Bode: fase = −135° em $\omega = 0{,}9$ rad/s, onde $|G| = 9{,}9$ dB;
3. $K = -9{,}9$ dB $\approx 0{,}32$;
4. previsão: $M_p \approx 25\,\%$; $t_r \approx \dfrac{\pi - \arccos(0{,}45)}{0{,}9\sqrt{1-0{,}45^2}} \approx 2{,}5$ s.

**Simulação com $K = 0{,}32$: $M_p = 24{,}4\,\%$ ✔ (previsto 25 %!); $t_r = 2{,}0$ s** (previsto 2,5 s — a estimativa de $\omega_n$ foi a mais frouxa desta vez; mesmo assim, útil e conservadora).

![Projeto com requisito de Mp](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig13_projeto_3a_mp.png)

### 3.2.8 Projeto com requisito de instante de pico — e o limite do ganho puro

**Problema:** $G(s) = \dfrac{0{,}005}{(s+0{,}03)(s+0{,}1)(s+0{,}5)}$. Com $K = 1$: $M_p = 17{,}8\,\%$, $t_p = 34{,}2$ s. **Requisito: $t_p \leq 25$ s.**

Agora o requisito é de **velocidade**, não de overshoot — a tradução é por $\omega_n$:

1. $t_p = \pi/\omega_d \leq 25 \Rightarrow \omega_d \geq 0{,}126$ → escolhemos $\omega_n = 0{,}13$ rad/s ($\omega_d \approx \omega_n$ para $\zeta$ moderado);
2. o novo cruzamento deve acontecer em $\omega_c = 0{,}13$ → lemos no Bode: $|G(j0{,}13)| = -7{,}3$ dB → **$K = +7{,}3$ dB $\approx 2{,}3$**;
3. nessa frequência a fase é −144° → **PM = 36°** → $\zeta \approx 0{,}35$ → conferindo: $\omega_d = 0{,}13\sqrt{1-0{,}35^2} = 0{,}12$ (levemente abaixo do pedido — aceitável com a folga) e **$M_p$ previsto ≈ 31 %**.

**Simulação com $K = 2{,}3$: $t_p = 23{,}1$ s ✔ (< 25 s); $M_p = 40{,}8\,\%$** — bem acima dos 31 % previstos.

![Projeto com requisito de tp](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig14_projeto_wn.png)

> ⚠️ **Moral (importante!):** com um ganho puro, mexemos num **único botão** — o cruzamento. Quando os requisitos de $M_p$ e de velocidade apontam para direções compatíveis (aqui: acelerar aumentou o overshoot, mas não havia requisito de $M_p$), tudo bem. Quando **$M_p$ e $t_p$/$t_r$ são simultâneos e apertados**, ganho puro **não basta**: precisamos remodelar a curva — e é para isso que servem os **compensadores de avanço e atraso** do §3.4 e os **PD/PI/PID** do §3.5. As estimativas também pioram em 3ª ordem: sempre simular antes de entregar.

---

## 3.3 Diagrama de Nyquist e Atraso de Transporte

### 3.3.1 O diagrama polar: a resposta em frequência em coordenadas polares

Existe uma terceira representação da resposta em frequência (depois do Bode e da carta de Nichols-Black): o **diagrama polar**, em que desenhamos $G(j\omega)$ **no plano complexo** — eixo $x$ = parte real, eixo $y$ = parte imaginária — com $\omega$ varrendo de $0$ a $\infty$. Cada ponto da curva é um vetor: **raio = $|G(j\omega)|$, ângulo = $\angle G(j\omega)$**.

> ⚠️ **Atenção:** no polar, o módulo é lido **em escala linear** (sem dB!) — é o comprimento do vetor.

**Exemplo-âncora.** $G(s) = \dfrac{10}{(s+1)(s+10)}$:

| $\omega$ | $\|G\|$ | $\angle G$ | ponto |
|---|---|---|---|
| 0 | 1 | 0° | (1; 0) |
| 1 | 0,70 | −50,7° |  |
| 3 | 0,30 | −88,3° | quase sobre o eixo imaginário |
| 10 | 0,07 | −129,3° |  |
| 100 | 0,001 | −173,7° |  |
| → ∞ | 0 | −180° | origem, "chegando pela esquerda" |

![Diagrama polar](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig15_polar.png)

Do Bode ao polar é direto (mesmas duas informações, outra embalagem). Mas por que queremos mais uma representação? Porque ela sustenta o **critério de estabilidade mais geral que veremos no curso** — e que responde perguntas que o Bode não responde, como "para que **faixas** de ganho a malha fechada é estável?" quando a planta já nasce instável.

### 3.3.2 O princípio do argumento

A base matemática do critério é uma propriedade elegante das funções de variável complexa. Seja $G(s) = \dfrac{K(s-z_1)}{(s-p_1)(s-p_2)}$ e $\gamma$ um contorno fechado no plano-s, percorrido em um sentido, **sem passar por polos nem zeros** de $G$.

A fase de $G$ num ponto $s$ do contorno é a soma de ângulos de vetores: $\angle G(s) = \angle K + \alpha_1 - \beta_1 - \beta_2$ (ângulos dos vetores de cada zero e cada polo até o ponto $s$). Quando $s$ dá **uma volta completa** pelo contorno:

- **raiz fora do contorno:** o ângulo do vetor oscila mas **volta ao valor inicial** — contribuição líquida zero;
- **zero dentro do contorno:** o ângulo dá **uma volta completa no mesmo sentido** do contorno: contribui **+360°**;
- **polo dentro do contorno:** o ângulo dá uma volta **no sentido contrário**: contribui **−360°**.

Fazendo o balanço, o mapa de $\gamma$ por $G(s)$ é uma curva fechada que dá **$N$ voltas em torno da origem** (no sentido do contorno), com

$$\boxed{N = Z - P}$$

onde $Z$ = número de zeros e $P$ = número de polos de $G$ **dentro do contorno**. É o **princípio do argumento**: contando voltas do mapa, contamos raízes dentro do contorno — sem resolver equação nenhuma.

![Princípio do argumento](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig16_principio_argumento.png)

### 3.3.3 O contorno de Nyquist e o critério

Queremos saber se a **malha fechada** tem polos no **semiplano direito** (SPD). Ideia: usar um contorno que **abraque o SPD inteiro**:

- o **eixo imaginário** de $-j\infty$ a $+j\infty$;
- fechado por uma **semicircunferência de raio $R \to \infty$** pela direita;
- percorrido no **sentido horário** (convenção do curso).

Aplicamos o princípio do argumento à função $1 + KG(s)$: seus **zeros** são exatamente os **polos de malha fechada** (raízes de $\mathrm{den}_G + K\,\mathrm{num}_G = 0$) e seus **polos** são os **polos de malha aberta**. E "voltas de $1 + KG$ em torno da origem" = "voltas de $KG$ em torno do ponto $-1$" = **voltas de $G$ em torno de $-1/K$** (dividindo por $K$). Resultado — o **critério de Nyquist**:

$$\boxed{Z = N + P}$$

- $Z$ = número de polos de **malha fechada** no SPD (queremos $Z = 0$);
- $P$ = número de polos de **malha aberta** no SPD (conhecido — olhamos a FT);
- $N$ = número de **voltas horárias** que o diagrama de Nyquist de $G(j\omega)$ dá em torno do ponto $-1/K$ (horária conta +1, anti-horária conta −1).

**Leitura operacional:** com $P$ polos instáveis de malha aberta, a estabilidade de malha fechada exige exatamente **$P$ voltas anti-horárias** em torno de $-1/K$. E quando a planta é estável ($P = 0$), basta que a curva **não circunde** o ponto $-1/K$.

> ⚠️ **E se houver polo na origem (tipo 1 ou mais)?** O polo está **sobre** o contorno — e o princípio exige que o contorno não passe por raízes. Solução: a **indentação** — um desvio semicircular de raio $r \to 0$ pela direita, deixando o polo da origem "de fora". Veremos o efeito dela no mapa em §3.3.5.

![Contorno de Nyquist](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig17_contorno_nyquist.png)

### 3.3.4 Do Bode ao Nyquist completo

O contorno cobre **todo** o eixo imaginário ($\omega$ de $-\infty$ a $+\infty$), mas só precisamos traçar metade:

**Simetria (FTs com coeficientes reais):** $G(-j\omega) = \overline{G(j\omega)}$ — a metade $\omega < 0$ é a **reflexão da metade $\omega > 0$ no eixo real**. Basta traçar o polar ($\omega: 0 \to +\infty$) e espelhar.

**E a semicircunferência de raio infinito?** Parametrizando $s = R\,e^{j\theta}$, $\theta: +90° \to -90°$:

- FT **estritamente própria** (grau do numerador < grau do denominador): $|G| \sim R^{g_{num} - g_{den}} \to 0$ — toda a semicircunferência mapeia **na origem**, e a curva chega lá com ângulo $(g_{num} - g_{den}) \times 90°$;
- FT **própria** (graus iguais): mapeia num ponto finito do eixo real.

**Exemplo-âncora (continuação).** $G(s) = \dfrac{10}{(s+1)(s+10)}$: polar de §3.3.1 + reflexão = diagrama completo. A curva fechada **não circunda $-1/K$** para nenhum $K > 0$ → $N = 0$; com $P = 0$: $Z = 0$ — **estável para todo $K > 0** ✔ (confirma o que o LGR do Módulo 02 diria).

![Nyquist completo](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig18_nyquist_completo.png)

### 3.3.5 Esboço do Nyquist a partir da FT: três exemplos de análise de estabilidade

**Exemplo 1 — $G(s) = \dfrac{1}{s+1}$:** $G(0) = 1$, fase $0° \to -90°$, módulo $1 \to 0$: um semicírculo no semiplano direito do plano-G (diâmetro de 0 a 1). Nunca circunda $-1/K$ (que está no eixo real **negativo**). $N = 0$, $P = 0$ → **estável $\forall K > 0$**.

**Exemplo 2 — planta instável $G(s) = \dfrac{1}{s-1}$ ($P = 1$):** $G(0) = -1$ (fase $-180°$), fase $-180° \to -90°$: semicírculo no semiplano **esquerdo**. Dois casos:

- **$K > 1$:** o ponto $-1/K$ está **entre $-1$ e a origem** → a curva dá **1 volta anti-horária** em torno dele: $N = -1$ → $Z = -1 + 1 = 0$ → **estável** ✔
- **$K < 1$:** $-1/K$ está à esquerda de $-1$, fora da curva: $N = 0$ → $Z = 1$ → **instável** ✗

> 📌 **Moral:** com planta instável de 1ª ordem, existe **ganho MÍNIMO** ($K > |p_1|$) — ao contrário da intuição de que "ganho menor é sempre mais seguro". O LGR do Módulo 02 mostrava o mesmo (o ramo sai do polo instável e só cruza para o SPE quando $K$ é grande o suficiente); o Nyquist mostra **por voltas** — e funciona também quando nem LGR nem Routh se aplicam com facilidade.

**Exemplo 3 — tipo 1: $G(s) = \dfrac{1}{s(s+1)(s+2)}$:** aqui entra a **indentação**. O desvio $s = r\,e^{j\theta}$, $\theta: -90° \to +90°$, mapeia em $G \approx \dfrac{1}{2r\,e^{j\theta}}$ — uma **semicircunferência de raio infinito**, percorrida de $+90°$ a $-90°$ (sentido horário), que "fecha" o diagrama pelo lado direito do plano-G. O polar em si: fase de $-90°$ ($\omega \to 0^+$, módulo $\to \infty$) a $-270°$ ($\omega \to \infty$, origem), **cruzando o eixo real negativo** onde a fase é $-180°$:

$$\angle G(j\omega) = -90° - \mathrm{arctg}\,\omega - \mathrm{arctg}(\omega/2) = -180° \;\Rightarrow\; \omega = \sqrt{2}, \quad |G(j\sqrt{2})| = \frac{1}{\sqrt{2}\,\sqrt{3}\,\sqrt{6}} = \frac{1}{6}.$$

A curva cruza o eixo real em $-1/6$. Contando voltas:

- $0 < K < 6$: $-1/K$ está à **esquerda** de $-1/6$ → sem voltas → $N = 0$, $Z = 0$ → **estável** ✔
- $K > 6$: $-1/K$ cai **dentro** do laço → 2 voltas horárias → $Z = 2$ → **instável** ✗

Resultado: estável para $0 < K < 6$ — **exatamente** o que Routh dá ($s^3 + 3s^2 + 2s + K$: $K < 6$). Duas ferramentas, mesma resposta — cada uma com sua geometria.

![Análise de estabilidade por Nyquist](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig19_nyquist_estabilidade.png)

> ⚠️ **Nota prática (por que saber esboçar importa):** os programas de computador traçam Nyquist com problemas de escala — módulos que vão a zero ou a infinito esmagam a figura. Quem sabe o **formato esperado** do esboço interpreta o gráfico do computador (e detecta quando ele mente); quem não sabe, fica olhando para um borrão.

### 3.3.6 Margem de ganho no Nyquist: existe limite INFERIOR de ganho

No Bode (§3.1.8) definimos GM como "quantos dB posso subir até encostar no ponto crítico". No Nyquist, a geometria fica ainda mais rica quando a curva cruza o eixo real negativo **mais de uma vez**.

**Exemplo (planta instável com zero):** $G(s) = \dfrac{s+2}{(s+1)(s-5)}$ — $P = 1$, $G(0) = \dfrac{2}{1 \times (-5)} = -0{,}4$. A fase começa em $-180°$, **cai abaixo** de $-180°$ (influência do polo $-1$), **volta** a $-180°$ (influência do zero $-2$) e termina em $-90°$ — a curva cruza o eixo real negativo **duas vezes**: em $-0{,}4$ ($\omega = 0$) e em

$$-R = G(j\sqrt{3}) = -0{,}25 \qquad (\omega = \sqrt{3}\ \text{rad/s — confira pela fase!})$$

Para $P = 1$, a estabilidade exige $N = -1$ (uma volta **anti-horária**). Inspecionando a figura: isso acontece quando $-1/K$ está **entre** $-R$ e $-0{,}4$... na verdade, exatamente quando $0 < 1/K < R$, ou seja,

$$K > \frac{1}{R} = 4 \;\Rightarrow\; \textbf{estável para } K > 4.$$

Conferindo por Routh: $(s+1)(s-5) + K(s+2) = s^2 + (K-4)s + (2K-5)$ → estável ⇔ $K > 4$ ✔ (e $K > 2{,}5$, menos restritivo).

![Margem de ganho inferior](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig20_nyquist_margem_inferior.png)

**Margens de ganho, versão completa:** para um ganho $K$ dentro da faixa estável, existem **duas** margens: a **superior** (quanto posso aumentar — aqui, $\infty$) e a **inferior** (quanto posso diminuir — aqui, até $K = 4$: GM inferior $= \dfrac{1}{RK}$). O Bode "clássico" só enxerga a superior; o Nyquist enxerga as duas.

### 3.3.7 Atraso de transporte: modelagem e efeito no Bode

O **atraso de transporte** (tempo morto) é o intervalo entre a ação e o início da reação: $y(t) = u(t - \delta)$. Pela propriedade do deslocamento temporal de Laplace (Módulo 01):

$$Y(s) = e^{-\delta s}\,U(s) \;\Rightarrow\; \boxed{G(s) = G_n(s)\,e^{-\delta s}}$$

onde $G_n(s)$ é a parte racional. No Módulo 02, tratamos o atraso **no plano-s** com a **aproximação de Padé** (uma FT racional que "imita" $e^{-\delta s}$). Na frequência, não precisamos de aproximação — o atraso tem resposta em frequência **exata e simplicíssima**:

$$e^{-j\delta\omega} = \cos(\delta\omega) - j\,\mathrm{sen}(\delta\omega) \;\Rightarrow\; \left|e^{-j\delta\omega}\right| = 1, \qquad \angle e^{-j\delta\omega} = -\delta\omega.$$

**Leitura:** o atraso **não altera o módulo** (nem por 1 dB) e **subtrai fase linearmente com $\omega$** — no eixo logarítmico do Bode, uma queda cada vez mais vertiginosa, **que nunca converge**.

**Exemplo-âncora.** $G(s) = \dfrac{4}{(s+0{,}1)(s+1)}\,e^{-0{,}2s}$:

- sem atraso: $\omega_c = 1{,}9$ rad/s, **PM = 31°** → $\zeta \approx 0{,}31$ → $M_p \approx 36\,\%$ (simulação: 41,2 %, $t_r = 0{,}95$ s);
- com atraso: $\omega_c$ **inalterado** (o módulo não mudou!), mas a fase em $\omega_c$ cai de $\delta\omega_c = 0{,}2 \times 1{,}9 = 0{,}38$ rad $\approx 22°$ → **PM ≈ 9,6°** → $\zeta \approx 0{,}10$ → $M_p$ previsto $\approx 73\,\%$;
- **simulação com atraso (Padé ordem 8): $M_p = 78{,}8\,\%$, $t_r = 1{,}05$ s** — o atraso de 0,2 s quase **dobrou** o overshoot.

![Atraso no Bode](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig21_atraso_bode.png)

![Atraso no degrau](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig23_atraso_degrau.png)

O remédio imediato (quando não se pode projetar compensador): **reduzir o ganho** — $\omega_c$ cai, $\delta\omega_c$ cai junto, a PM se recupera (ao custo de velocidade e de erro em regime).

### 3.3.8 O atraso no Nyquist: a espiral

Fechando o tópico com a imagem mais importante sobre atrasos. O sistema $G_n(s) = \dfrac{4}{(s+0{,}1)(s+1)}$ tem fase que vai de $0°$ a $-180°$: seu Nyquist **nunca cruza o eixo real negativo** → **estável para todo $K > 0$** (margem de ganho infinita!).

Com o atraso $e^{-0{,}2s}$: a fase passa a ser $\angle G_n - 0{,}2\,\omega$ — **decresce sem limite** — enquanto o módulo continua indo a zero. A curva passa de "arco que morre na origem" para uma **espiral com infinitas voltas** em torno da origem: cruza o eixo real negativo **infinitas vezes**, cada vez mais perto da origem.

![Espiral de Nyquist](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig22_atraso_nyquist.png)

**Consequência:** onde não havia cruzamento nenhum, agora há infinitos. Aumentando $K$ a partir de zero, em algum momento o ponto $-1/K$ é "engolido" por uma volta da espiral — e a malha fechada ganha 2 polos no SPD (depois 4, 6...). **O sistema que era estável para qualquer ganho é desestabilizado por ganho suficientemente grande.**

> 📌 **Para nunca esquecer:** o atraso de transporte não aparece no denominador de $T(s)$ como um polo a mais — ele é um **termo transcendental** com infinitas "raízes escondidas". Por isso ele é uma das preocupações centrais do engenheiro de controle: redes de comunicação, processos industriais com transporte de material, sistemas digitais com tempo de cálculo — todos carregam atraso. Na frequência, ele se resume a uma frase: **come fase, não come módulo — e fase é a moeda da estabilidade.**

---

## 3.4 Projeto de Controladores no Domínio da Frequência

No §3.2.8 vimos o limite do ganho puro: um botão só (o cruzamento) não atende requisitos simultâneos de transitório e de regime. A saída é dar **dinâmica** ao controlador — remodelar a curva de malha aberta onde ela precisa ser remodelada. A matéria-prima são dois tijolos: **um zero** e **um polo**.

### 3.4.1 Efeito de acrescentar um zero no Bode

Seja $G(s) = G_n(s)(s - z_1)$, $z_1 < 0$. Somando as contribuições (§3.1.5):

- **módulo:** +$20\log|z_1|$ em baixas frequências e **+20 dB/déc** acima da quebra em $|z_1|$;
- **fase:** sobe de $0°$ a **+90°**, pela reta de $|z_1|/5$ a $5|z_1|$ (+45° em $|z_1|$; equação da reta: $\varphi = 90°\,\dfrac{\log(5\omega/|z_1|)}{\log 25}$).

**Adicionar um zero aumenta a fase — logo, aumenta a PM** onde a quebra estiver. Ótimo! Só há um problema: um elemento com **zero puro** é uma FT **imprópria** (grau do numerador > grau do denominador) — o "sistema adivinho" do Módulo 02 — **não realizável** na prática. Precisamos casá-lo com um polo.

![Efeito do zero no Bode](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig24_efeito_zero_bode.png)

### 3.4.2 Efeito de acrescentar um polo no Bode

Seja $G(s) = G_n(s)/(s - p_1)$, $p_1 < 0$: efeito **exatamente oposto** ao do zero — módulo cai −20 dB/déc após a quebra, fase cai de $0°$ a $-90°$ (mesma reta de $|p_1|/5$ a $5|p_1|$).

Se zero e polo estiverem **na mesma frequência**, seus efeitos se cancelam — não há vantagem. A jogada inteligente é colocá-los em **frequências diferentes**. E note: o polo sozinho, ou o **par zero-polo**, é **próprio** → realizável.

![Efeito do polo no Bode](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig25_efeito_polo_bode.png)

### 3.4.3 Zero e depois polo ($|z_1| < |p_1|$): o avanço de fase

Considere o par $G_n(s)\,\dfrac{s - z_1}{s - p_1}$ com $|z_1| < |p_1|$ (zero **antes** do polo — por exemplo, 2 décadas de separação, $|z_1| = 1$, $|p_1| = 100$):

- **módulo:** em baixas frequências o par custa $20\log(|z_1|/|p_1|) = -40$ dB; entre as quebras, sobe +20 dB/déc; depois do polo, **estaciona em 0 dB** (zero e polo se cancelam);
- **fase:** sobe com o zero, desce com o polo — um **"morro"** com **máximo na média geométrica** das quebras:

$$\boxed{\omega_{máx} = \sqrt{|z_1|\,|p_1|}} \qquad \text{(média aritmética no eixo log!)}$$

Se zero e polo estiverem longe um do outro, o pico se aproxima de +90°; próximos, o pico é menor. Esse elemento — que **adianta a fase** numa faixa de frequências escolhida — é o **compensador de avanço de fase** (em inglês, *lead*).

![Efeito do par zero-polo](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig26_efeito_par_bode.png)

### 3.4.4 As fórmulas do avanço de fase (dedução completa)

Parametrizamos o compensador (com ganho unitário em altas frequências) como

$$C_a(s) = \frac{Ts + 1}{\alpha Ts + 1}, \qquad \alpha < 1 \;\; (\Leftrightarrow |z_1| = 1/T < 1/(\alpha T) = |p_1|).$$

**Fase máxima e onde ela ocorre.** A fase exata é $\varphi(\omega) = \mathrm{arctg}(T\omega) - \mathrm{arctg}(\alpha T\omega)$. O máximo ocorre em $\omega_{máx} = \dfrac{1}{T\sqrt{\alpha}}$ (a média geométrica — confira derivando!). Substituindo e usando $\mathrm{tg}(a-b) = \dfrac{\mathrm{tg}\,a - \mathrm{tg}\,b}{1 + \mathrm{tg}\,a\,\mathrm{tg}\,b}$:

$$\mathrm{tg}\,\varphi_{máx} = \frac{\sqrt{1/\alpha} - \sqrt{\alpha}}{2} \;\Rightarrow\; \cos\varphi_{máx} = \sqrt{1 - \mathrm{sen}^2\varphi_{máx}} \;\Rightarrow\; \boxed{\mathrm{sen}\,\varphi_{máx} = \frac{1-\alpha}{1+\alpha}} \;\Leftrightarrow\; \boxed{\alpha = \frac{1 - \mathrm{sen}\,\varphi_{máx}}{1 + \mathrm{sen}\,\varphi_{máx}}}$$

**Ganho do compensador em $\omega_{máx}$:** $|C_a(j\omega_{máx})| = \sqrt{\dfrac{1 + T^2\omega_{máx}^2}{1 + \alpha^2T^2\omega_{máx}^2}} = \dfrac{1}{\sqrt{\alpha}}$ (em dB: $-10\log\alpha > 0$). O compensador "de brinde" **levanta o módulo** onde adianta a fase — precisamos contabilizar isso no ganho $K$.

![Fórmulas do avanço](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig27_avanco_formulas.png)

### 3.4.5 A receita de projeto do avanço (6 passos)

**Dados:** requisitos de transitório ($M_p$, $t_r$/$t_p$) traduzidos em **PM desejada** e **$\omega_c$ desejado** (PM $\approx 100\zeta + 5°$–$10°$ de folga; $\omega_n \approx \omega_c$ pelas fórmulas de $t_r$/$t_p$).

1. **Traduzir** os requisitos: PM e $\omega_c$ alvos (com a folga).
2. **Medir** no Bode da planta (experimental ou calculado) a fase e o módulo em $\omega_c$: PM atual $= \angle G(j\omega_c) + 180°$.
3. **Decidir:** se a PM atual já for suficiente — **só ganho resolve** ("se dá com controlador mais simples, por que complicar?"; excesso de PM é bom, pois requisitos de $M_p$ são desigualdades).
4. Senão, a fase que falta: $\varphi_{máx} = \mathrm{PM}_{desejada} - \angle G(j\omega_c) - 180°$ e $\alpha = \dfrac{1 - \mathrm{sen}\,\varphi_{máx}}{1 + \mathrm{sen}\,\varphi_{máx}}$.
5. **Posicionar** o pico em $\omega_c$: $T = \dfrac{1}{\omega_c\sqrt{\alpha}}$.
6. **Corrigir o ganho:** em $\omega_c$, o par introduz $1/\sqrt{\alpha}$; para fazer $|C\,G(j\omega_c)| = 1$: $\boxed{K = \frac{\sqrt{\alpha}}{|G(j\omega_c)|}}$ — ou, em dB, $\boxed{K_{\mathrm{dB}} = 10\log\alpha - |G(j\omega_c)|_{\mathrm{dB}}}$.

**Controlador final:** $C(s) = K\,\dfrac{Ts+1}{\alpha Ts + 1}$. Depois: **simular e conferir** (e iterar, se preciso).

### 3.4.6 Exemplo-âncora de avanço (completo, passo a passo)

**Planta:** $G(s) = \dfrac{0{,}005}{s(s+0{,}05)}$. **Requisitos:** $t_r \leq 18$ s e $M_p \leq 30\,\%$.

1. **Tradução:** $M_p = 30\,\% \Rightarrow \zeta = 0{,}358$ → usamos $\zeta = 0{,}35$: PM $\geq 35°$; com folga de +5°: **PM alvo = 40°**. Velocidade: $t_r = \dfrac{\pi - \arccos(0{,}35)}{\omega_n\sqrt{1-0{,}35^2}} \leq 18 \Rightarrow \omega_n \geq 0{,}11$ → **$\omega_c$ alvo = 0,11 rad/s**.
2. **Medida:** em $\omega = 0{,}11$: $|G| \approx -9{,}2$ dB (0,35), fase $\approx -157°$ → **PM atual = 23°** ✗ (e não adianta só ganho: para cruzar em 0,11 precisaríamos de $K = 1/0{,}35$ e a PM ficaria nos mesmos 23°).
3. **Fase que falta:** $\varphi_{máx} = 40° + 157° - 180° = 17°$ → $\alpha = \dfrac{1 - \mathrm{sen}\,17°}{1 + \mathrm{sen}\,17°} = 0{,}54$.
4. **Posicionamento:** $T = \dfrac{1}{0{,}11\sqrt{0{,}54}} = 12$ → $\alpha T = 6{,}5$.
5. **Ganho:** $K_{\mathrm{dB}} = 10\log(0{,}54) - (-9{,}2) = -2{,}7 + 9{,}2 = 6{,}5$ dB → $K = 2{,}1$.

$$\boxed{C(s) = 2{,}1\,\frac{12s + 1}{6{,}5s + 1}}$$

**Conferência:** sistema compensado com $\omega_c = 0{,}115$ rad/s e **PM = 40,9°** ✔; simulação da malha fechada: **$M_p = 29{,}6\,\%$** (≤ 30 % ✔), **$t_r = 15{,}5$ s** (≤ 18 s ✔). Projeto aprovado de primeira — guardando este compensador: ele volta no §3.5.2, numa comparação reveladora com o PD.

![Projeto de avanço](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig28_projeto_avanco.png)

### 3.4.7 Atraso de fase: ajustando a constante de erro sem estragar o transitório

O problema agora é outro: suponha que o transitório já está bom ($\omega_c$ e PM nos valores certos), mas o **erro em regime** não. Erro em regime ↔ **ganho DC** — e subir o ganho DC com um $K$ simples levanta a curva inteira, destruindo $\omega_c$ e PM.

**A jogada:** inverter a ordem do par — $|p_1| < |z_1|$ (polo **antes** do zero). Aí:

- **módulo:** em baixas frequências, **ganha** $20\log(z_1/p_1)$ dB (o ganho DC fica multiplicado por $z/p$!); depois do zero, volta a 0 dB — as frequências do cruzamento ficam **intocadas**;
- **fase:** cai entre as quebras e **retorna a 0°** depois (uns $5\times$ acima da quebra do zero).

**Nome e regra de posicionamento:** como o efeito colateral é **atrasar a fase** (comendo alguns graus de PM), posicionamos o par **bem abaixo** do cruzamento: **polo em $\omega_c/10$** (ou $\omega_c/20$, $\omega_c/200$ quando se quer ainda menos perturbação). É o **compensador de atraso de fase** (em inglês, *lag*).

**Exemplo-âncora.** $G(s) = \dfrac{10}{(s+1)(s+2)}$ (tipo 0): $k_p = G(0) = 5$ → $e_{ss} = \dfrac{1}{1+5} = 16{,}7\,\%$. **Requisito: $e_{ss} \leq 10\,\%$.**

1. Folga: projetamos para a **metade** do erro: $e_{ss} = 1/12 = 8{,}3\,\%$ → $k_{p,c} = 11$ → precisamos multiplicar o ganho DC por $\dfrac{z}{p} = \dfrac{11}{5} = 2{,}2$.
2. Do Bode: $\omega_c = 2{,}76$ rad/s → polo em $\omega_c/10$: $p = -0{,}27$; zero: $z = 2{,}2 \times 0{,}27 = 0{,}61$.
$$\boxed{C(s) = \frac{s + 0{,}61}{s + 0{,}27}}$$
3. **Conferência:** simulação da malha fechada — $e_{ss}$: $0{,}167 \to 0{,}081$ (**metade** ✔); $M_p$: $22{,}1\,\% \to 22{,}7\,\%$; $t_r$: $0{,}65 \to 0{,}67$ s — o transitório **quase não sentiu**.

![Projeto de atraso](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig29_projeto_atraso.png)

> ✏️ **Pense (diferença de filosofia):** no avanço, escolhemos a frequência onde o compensador **age** (o pico vai para $\omega_c$). No atraso, escolhemos a frequência onde ele **não age** (as quebras vão para longe de $\omega_c$) — ele trabalha nas baixas frequências sem perturbar o cruzamento. Avanço = transitório; atraso = regime.

### 3.4.8 Projeto completo: avanço + atraso

**Planta:** $G(s) = \dfrac{1}{(s+5)(s+10)}$. **Requisitos:** $M_p < 10\,\%$, $t_r \leq 0{,}1$ s **e** $e_{ss} \leq 0{,}05$ — três requisitos simultâneos, o caso que o ganho puro não resolve.

**Etapa 1 — avanço (transitório):**
1. Tradução: $M_p = 10\,\% \Rightarrow \zeta = 0{,}59$ → PM $\geq 59°$; $t_r \leq 0{,}1 \Rightarrow \omega_n \geq 27$ → **$\omega_c$ alvo = 27 rad/s**.
2. Medida em 27 rad/s: fase = $-149{,}2°$ (PM atual = 31°), $|G| = -58{,}0$ dB.
3. Fase que falta: $59° - 31° = 28°$ — **+ 5° prevendo a perda de fase que o compensador de atraso vai causar** → $\varphi = 33°$ → $\alpha = 0{,}30$.
4. $T = \dfrac{1}{27\sqrt{0{,}3}} = 0{,}07$ ($\alpha T = 0{,}021$); $K_{\mathrm{dB}} = 10\log(0{,}3) + 58{,}0 = -5{,}3 + 58{,}0 = 52{,}5$ dB → $K = 420$.
$$C_1(s) = 420\,\frac{0{,}07s + 1}{0{,}021s + 1}$$

**Etapa 2 — atraso (regime):** com $C_1$: $k_p = \dfrac{420}{50} = 8{,}4$ → $e_{ss} = \dfrac{1}{9{,}4} = 10{,}6\,\%$ ✗ (requisito: 5 %).

1. $e_{ss} = 0{,}05 = 1/20$ → $k_p = 19$ → razão necessária: $\dfrac{19}{8{,}4} \approx 2$ → $z/p = 2$ (o **dobro**).
2. Polo bem longe: $p = -\omega_c/200 = -0{,}14$; zero: $z = 2p = -0{,}28$.
$$C_2(s) = \frac{s + 0{,}28}{s + 0{,}14}$$

**Controlador final:** $C(s) = C_1(s)\,C_2(s)$.

**Conferência por simulação:** $M_p = 7{,}4\,\%$ ✔ (< 10 %), $t_r = 0{,}075$ s ✔ (≤ 0,1 s), $e_{ss} = 0{,}060 \approx 5\,\%$ ✔. **Os três requisitos atendidos** — e note como a etapa de atraso quase não perturbou o transitório (os 5° de previsão fizeram seu trabalho).

![Projeto avanço + atraso](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig30_projeto_avanco_atraso.png)

### 3.4.9 Síntese visual: avanço e atraso na carta de Nichols-Black

As três curvas do exemplo anterior na carta contam a história inteira de uma vez:

- **$G$ (azul):** nem cruza 0 dB nas frequências úteis → malha fechada lenta e com erro grande;
- **$C_1G$ (verde):** o avanço **empurrou a curva para a direita e para cima** na região do cruzamento — PM ≈ 60°, $\omega_c \approx 27$ — comportamento de 2ª ordem subamortecido ($M_p \approx 10\,\%$), mas o ganho em baixas continuou baixo;
- **$C_1C_2G$ (vermelha):** o atraso **levantou só as baixas frequências**; perto do cruzamento, **vermelha e verde se unem** — PM e $\omega_c$ preservados, erro corrigido.

![Avanço e atraso na carta](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig31_avanco_atraso_nb.png)

> 📌 **Resumo do tópico em uma frase:** o **avanço** remodela o **meio** da curva (PM e $\omega_c$ — o transitório), o **atraso** remodela as **baixas** (ganho DC — o regime), e os dois juntos atendem especificações completas — tudo lendo (ou medindo) apenas a resposta em frequência da planta.

---

## 3.5 Controladores PD, PI e PID no Domínio da Frequência

No Módulo 02, projetamos PD, PI e PID **no plano-s** (pelo LGR). Agora os reencontramos **na frequência** — com fórmulas diretas de projeto e uma leitura geométrica que os liga aos compensadores de avanço e atraso: **PD = avanço com o polo no infinito; PI = atraso com o polo em zero**.

### 3.5.1 O controlador PD na frequência

Se um zero puro já aumenta a fase onde queremos (§3.4.1), o controlador mais simples possível com essa propriedade é

$$C(s) = k_p + k_d\,s = k_p\left(1 + \frac{k_d}{k_p}s\right) \qquad \text{(PD: proporcional + derivada do erro).}$$

**Projeto (dedução das fórmulas diretas).** Requisitos traduzidos em PM e $\omega_c$ alvos; seja $\varphi$ a fase que falta: $\varphi = \mathrm{PM}_{desejada} - \angle G(j\omega_c) - 180°$.

1. **Fase do PD em $\omega_c$:** $\angle C(j\omega_c) = \mathrm{arctg}\left(\dfrac{k_d\,\omega_c}{k_p}\right) = \varphi$ → $\dfrac{k_d}{k_p} = \dfrac{\mathrm{tg}\,\varphi}{\omega_c}$ (o zero fica em $z_1 = -\dfrac{k_p}{k_d} = -\dfrac{\omega_c}{\mathrm{tg}\,\varphi}$).
2. **Módulo 1 em $\omega_c$:** $|C(j\omega_c)| = \sqrt{k_p^2 + k_d^2\omega_c^2} = \dfrac{1}{|G(j\omega_c)|}$. Dividindo as duas condições e usando $1 + \mathrm{tg}^2\varphi = 1/\cos^2\varphi$, saem as **fórmulas diretas**:

$$\boxed{k_p = \frac{\cos\varphi}{|G(j\omega_c)|} \qquad\qquad k_d = \frac{\mathrm{sen}\,\varphi}{\omega_c\,|G(j\omega_c)|}}$$

**O problema da realizabilidade (e a solução-padrão):** o PD ideal é **impróprio**. Comparando com o avanço $C_a = \dfrac{Ts+1}{\alpha Ts+1}$: quando $\alpha \to 0$, o polo $-1/(\alpha T) \to -\infty$ e o avanço **degenera num PD** — *o PD é um avanço com o polo no infinito*. A solução prática é trazer o polo de volta do infinito, mas **longe o bastante para não atrapalhar**: o **polo de filtragem** em

$$p_1 = -100\,\omega_c \qquad \Rightarrow \qquad C'(s) = \frac{k_p + k_d\,s}{s/p_1 + 1}.$$

Custo: em $\omega = p_1/100$, o módulo do filtro é $\approx 1$ e a fase é $-\mathrm{arctg}(0{,}01) \approx -0{,}6°$ — desprezível.

![PD na frequência](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig32_pd_bode.png)

### 3.5.2 O lado sombrio do PD: sinais com variação abrupta

Vamos projetar o PD para **exatamente o mesmo problema do exemplo-âncora de avanço** (§3.4.6): $G(s) = \dfrac{0{,}005}{s(s+0{,}05)}$, $M_p \leq 30\,\%$, $t_r \leq 18$ s → PM = 40°, $\omega_c = 0{,}11$ rad/s, $|G(j\omega_c)| = 0{,}35$, $\varphi = 17°$:

$$k_p = \frac{\cos 17°}{0{,}35} = 2{,}7, \qquad k_d = \frac{\mathrm{sen}\,17°}{0{,}11 \times 0{,}35} = 7{,}6, \qquad p_1 = -100\,\omega_c = -110$$

$$C'(s) = \frac{2{,}7 + 7{,}6\,s}{s/110 + 1}$$

**Simulação da malha fechada:** $M_p = 29{,}3\,\%$, $t_r = 15{,}1$ s — **praticamente idênticos** aos do avanço ($M_p = 29{,}6\,\%$, $t_r = 15{,}5$ s). No gráfico, as duas respostas se confundem. Então tanto faz usar um ou outro? **Não.** Olhemos o **sinal de controle** $u(t)$ (a tensão que o controlador injeta na planta):

- **avanço:** pico de **3,9** (unidades de tensão);
- **PD:** pico de **836** — **≈ 215 vezes maior!**

A razão está na cara do controlador: a derivada de um degrau é (idealmente) um **impulso**; a variação abrupta da referência passa pelo termo $k_d s$ e vira um pico violento. O polo de filtragem limita o pico (sem ele, seria infinito), mas $7{,}6 \times 110$ continua sendo um número grande demais para qualquer atuador real — que **satura**, invalidando o projeto linear, ou simplesmente **não consegue** aplicar o sinal.

![PD × avanço](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig33_pd_x_avanco.png)

> ⚠️ **Regra prática do curso:** use o PD (e o termo D do PID) **com parcimônia quando a referência muda abruptamente** — degraus de setpoint são a regra em muitos processos! Na prática industrial, o termo derivativo costuma atuar **sobre a saída medida** (que varia suavemente) e não sobre o erro; e muitas vezes **o avanço de fase vale o trabalho extra** de projetar $\alpha$ e $T$: mesmo desempenho na saída, esforço de controle civilizado. ("Crianças, não tentem isso em casa.")

### 3.5.3 O controlador PI na frequência

Se o PD é o avanço limite (polo no ∞), qual é o **atraso limite**? Levando o polo do par $|p_1| < |z_1|$ para **zero**:

$$C(s) = \frac{s - z_1}{s} = k_p\,\frac{s - z_1}{s} = k_p - \frac{k_p z_1}{s} = k_p + \frac{k_i}{s} \qquad (k_i = -k_p z_1)$$

— a forma canônica do **PI** (proporcional + integral do erro)! O **PI é um atraso de fase com o polo em zero**. E o que o polo em zero traz de novo? **Ganho DC infinito** → sistema **tipo 1** → **erro nulo em regime permanente** ao degrau (não só reduzido: **zero**).

**Bode do PI:** módulo caindo a −20 dB/déc até a quebra do zero, plano depois; fase de $-90°$ a $0°$. Como qualquer atraso, ele come fase perto do cruzamento — e a regra de posicionamento é a mesma:

$$|z_1| = \frac{k_i}{k_p} \leq \frac{\omega_c}{10}.$$

![PI na frequência](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig34_pi_bode.png)

### 3.5.4 O controlador PID: projeto completo na frequência

O PID conjuga os dois mundos — **PD cuidando do transitório** (em $\omega_c$) **e PI cuidando do regime** (ganho infinito em baixas):

$$C(s) = \underbrace{\frac{k_p + k_d\,s}{s/p_1 + 1}}_{\text{PD com filtro}} \times \underbrace{\frac{s - z_1}{s}}_{\text{PI}}$$

A resposta em frequência do PID é a **soma** (em dB e em graus) das respostas do PD e do PI: o PD dá a PM em $\omega_c$, $k_p$ acerta o cruzamento, e o zero do PI fica lá embaixo ($|z_1| \leq \omega_c/10$) custando só alguns graus — que já estavam previstos na folga.

**Exemplo-âncora (completo, passo a passo).** **Planta:** $G(s) = \dfrac{0{,}01}{(s+0{,}05)(s+0{,}07)}$. **Requisitos:** $M_p \leq 10\,\%$, $t_r \leq 15$ s, $e_{ss} = 0$.

1. **Tradução:** $M_p = 10\,\% \Rightarrow \zeta = 0{,}59$ → PM $= 59°$; com +5° de folga (que absorve também o efeito do PI): **PM alvo = 64°**. Velocidade: $t_r \leq 15 \Rightarrow \omega_n \geq 0{,}18$ → **$\omega_c$ alvo = 0,18 rad/s**.
2. **Medida:** em $\omega = 0{,}18$: $|G| = -11{,}2$ dB ($0{,}275$), fase $= -143{,}2°$ → PM atual $= 36{,}8°$.
3. **Fase que falta (PD):** $\varphi = 64° - 36{,}8° \approx 28°$ (arredondamos de 27,2°).
4. **Ganhos do PD:** $k_p = \dfrac{\cos 28°}{0{,}275} = 3{,}2$; $k_d = \dfrac{\mathrm{sen}\,28°}{0{,}18 \times 0{,}275} = 9{,}5$.
5. **Polo de filtragem:** $p_1 = -100\,\omega_c = -180$.
6. **Zero do PI:** $|z_1| = \omega_c/10 = 0{,}018$.

$$\boxed{C(s) = \frac{3{,}2 + 9{,}5\,s}{s/180 + 1}\cdot\frac{s + 0{,}018}{s}}$$

**Conferência:** malha aberta compensada com $\omega_c = 0{,}181$ rad/s e PM $= 59°$ (o PI custou ~5°, como previsto); **simulação da malha fechada: $M_p = 11{,}2\,\%$** (≈ 10 % ✔), **$t_r = 11{,}1$ s** ✔ (≤ 15 s), **$e_{ss} = 0$** ✔. Três requisitos, três ✔.

![Projeto PID](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig35_projeto_pid.png)

### 3.5.5 Síntese na carta — e o encerramento do módulo

Na carta de Nichols-Black, o mesmo exemplo mostra os três controladores em ação sobre $G(s) = \dfrac{0{,}01}{(s+0{,}05)(s+0{,}07)}$:

- **$G$ (azul):** $\omega_c \ll 1$ rad/s, PM ≈ 73° — **lento**; ganho em baixas de só 9 dB — **erro apreciável**;
- **com PD (magenta):** PM ≈ 65°, $\omega_c$ perto de 0,2 rad/s, pico de ressonância quase nulo — **rápido e bem amortecido**;
- **com PI (laranja):** a curva **dispara para cima** nas baixas frequências (ganho → ∞, $e_{ss} = 0$) — mas a **PM cai**;
- **com PID (verde):** **conjuga os efeitos** — PM quase a do PD e ganho infinito em baixas.

![PD, PI e PID na carta](https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/m3_fig36_pd_pi_pid_nb.png)

> 🏁 **O que este módulo entregou (e a promessa cumprida):** começamos com um desafio — projetar **sem modelo**, só com ensaios em malha aberta. O caminho inteiro foi: senoides → resposta em frequência → Bode → margens → tradução para o tempo (PM ≈ 100ξ, ωn ≈ ωc) → projeto de **P** (§3.1.10), de **P com requisitos de Mp/tp** (§3.2), de **avanço, atraso e avanço+atraso** (§3.4) e de **PD/PI/PID** (§3.5) — mais o **critério de Nyquist** para estabilidade com plantas difíceis e o tratamento exato do **atraso** na frequência (§3.3). Em **nenhum** passo a função de transferência foi necessária: uma tabela de $|G|$ e $\angle G$ medida no laboratório alimenta exatamente os mesmos procedimentos. Não é à toa que o PID projetado na frequência continua sendo, quase um século depois de Black, Nyquist e Bode, **a forma de controle mais usada na indústria**.
>
> **E o que falta?** Tudo até aqui supôs sistemas **lineares** (ou linearizáveis). No **Módulo 04**, enfrentaremos as **não linearidades** que todo sistema real tem — saturação, zona morta, histerese — e aprenderemos quando elas destroem nossos projetos lineares e quando podemos dominá-las (funções descritivas, ciclos limite e linearização). Até lá!

---
