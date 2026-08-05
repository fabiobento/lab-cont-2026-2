# Módulo 04 — Exercícios Resolvidos (Não Linearidades em Malhas de Controle)

> No mínimo 3 exercícios por tópico, com resolução completa passo a passo e verificação computacional quando aplicável.
> Números âncora do módulo: **windup** — $G = 1/(10s+1)$, PI $k_p = 2$, $k_i = 0{,}5$, saturação $\pm 1{,}3$: ideal $M_p = 11{,}5\,\%$ / $t_s = 19{,}7$ s → windup $23{,}2\,\%$ / $39{,}3$ s → anti-windup $3{,}2\,\%$ / $13{,}4$ s. **Ciclo-limite** — $G = 1/[s(s+1)(s+2)]$ com relé $d = 1$: previsto $A = 4/(6\pi) = 0{,}212$, $\omega = \sqrt{2} = 1{,}41$ rad/s; simulado $A = 0{,}220$, $\omega = 1{,}38$ rad/s; $K_u = 6$ (Routh ✓).

---

## Tópico 4.1 — Não linearidades estáticas e seus efeitos na malha

### Exercício 4.1.1 — O "ganho efetivo" da saturação

**Enunciado.** Um amplificador de potência tem ganho nominal $k = 2$ e satura em $\pm 2$ V (nível $s = 1$ na entrada). (a) Esboce a característica estática. (b) Calcule a saída para $e = 0{,}5$; $e = 1$; $e = 3$. (c) Usando a função descritiva, calcule o **ganho efetivo** que uma senoide de amplitude $A = 2$ "enxerga" ao atravessar o amplificador, e compare com o ganho nominal.

**Resolução passo a passo.**

1. **Característica estática:** reta de inclinação 2 passando pela origem até $(\pm 1, \pm 2)$; constante em $\pm 2$ fora dessa faixa — o formato da figura `m4_fig01`, com $k = 2$ e $s = 1$.
2. **Saídas pontuais:** $e = 0{,}5$ está na região linear → $u = 2 \times 0{,}5 = 1$ V; $e = 1$ está exatamente no joelho → $u = 2$ V; $e = 3 > s$ → saturado → $u = +2$ V (o triplo da entrada *não* gera o triplo da saída!).
3. **Ganho efetivo para $A = 2 > s = 1$:** aplicando a função descritiva da saturação:
$$N(2) = \frac{2k}{\pi}\left[\mathrm{arcsen}\!\left(\frac{s}{A}\right) + \frac{s}{A}\sqrt{1 - \left(\frac{s}{A}\right)^2}\right] = \frac{4}{\pi}\left[\mathrm{arcsen}(0{,}5) + 0{,}5\sqrt{0{,}75}\right]$$
4. **Conta:** $\mathrm{arcsen}(0{,}5) = 0{,}5236$ rad; $0{,}5\sqrt{0{,}75} = 0{,}4330$; soma $= 0{,}9566$; $N(2) = \dfrac{4}{\pi}\times 0{,}9566 = 1{,}218$.
5. **Interpretação:** a senoide de amplitude 2 atravessa o amplificador como se o ganho fosse **1,218** — uma queda de **39 %** em relação ao nominal 2. É a primeira manifestação do tema do módulo: *a mesma peça tem ganhos diferentes dependendo da amplitude do sinal*. Uma malha projetada (margens calculadas!) com $k = 2$ opera, sob sinais grandes, com margens correspondentes a $k \approx 1{,}2$ — mais folgadas, neste caso (a saturação *reduz* o ganho), mas com resposta mais lenta.

*(teoria: §4.1.3 e §4.3.3 — característica da saturação e sua função descritiva; figura `m4_fig01`)*

---

### Exercício 4.1.2 — Zona morta: o erro que nenhum ganho elimina

**Enunciado.** Um motor CC tem atrito estático equivalente a uma zona morta de largura $d = 0{,}5$ V no acionamento: tensões de comando com $|u_{cmd}| \leq 0{,}5$ V **não movem o eixo**. O motor é controlado em malha fechada (realimentação unitária de posição) por um controlador proporcional $k_p$, com a zona morta **entre o controlador e a planta**. (a) Para referência de posição $r = 2$ (rad), mostre que existe uma **faixa** de valores estacionários possíveis para $y$ e determine-a. (b) O que acontece com essa faixa quando $k_p$ aumenta? (c) Por que a ação integral "resolve" o problema — e qual é o risco?

**Resolução passo a passo.**

1. **Condição de equilíbrio:** em regime, $y$ é constante → o comando também. O comando é $u_{cmd} = k_p\,(r - y)$. Se $|k_p(r - y)| \leq d$, o motor não recebe torque efetivo e o eixo **permanece onde está** — qualquer $y$ nessa condição é um equilíbrio possível.
2. **A faixa estacionária:** $|k_p(2 - y)| \leq 0{,}5 \iff |2 - y| \leq \dfrac{0{,}5}{k_p}$, ou seja $y \in \left[2 - \dfrac{0{,}5}{k_p},\; 2 + \dfrac{0{,}5}{k_p}\right]$.
3. **Exemplo numérico:** $k_p = 4$ → $y_{ss} \in [1{,}875;\; 2{,}125]$ — erro residual de até **0,125 rad**; $k_p = 40$ → faixa $\pm 0{,}0125$ rad. A faixa **estreita com $k_p$, mas nunca zera**: sempre existe um erro limite $|e_{ss}| \leq d/k_p$.
4. **Item (c):** o integrador soma o erro enquanto ele existir — mesmo pequeno — até que $u_{cmd}$ vença a zona morta e o eixo se mova: **elimina o erro de regime**. O risco: dentro da zona morta a planta "não responde", o integrador continua carregando, e quando o eixo finalmente se move, a carga acumulada pode produzir **ultrapassagem → erro de sinal oposto → nova carga** — nasce um **ciclo-limite de baixa frequência** (oscilação lenta em torno do alvo, comum em robôs com folga de engrenagem). É o mesmo mecanismo do windup (§4.2), agora causado pela zona morta.

*(teoria: §4.1.4 — zona morta; figura `m4_fig02`, painel esquerdo)*

---

### Exercício 4.1.3 — O termostato: ciclo-limite exato, sem aproximação

**Enunciado.** Um forno é modelado por $G(s) = \dfrac{1}{10s + 1}$ (temperatura normalizada) e controlado liga-desliga por um **relé com histerese**: potência $+1$ (ligado) ou $-1$ (desligado), comutando para ligado quando $y$ cai abaixo de $-0{,}5$ e para desligado quando $y$ sobe acima de $+0{,}5$ ($h = 0{,}5$), referência nula. (a) Mostre que, em regime, a temperatura oscila entre $-0{,}5$ e $+0{,}5$. (b) Calcule **exatamente** o período da oscilação. (c) Explique por que o método da função descritiva tem dificuldade com este sistema.

**Resolução passo a passo.**

1. **Dinâmica por trechos:** com o relé ligado ($u = +1$), a equação é $10\dot{y} + y = 1$, solução $y(t) = 1 + (y_0 - 1)\,e^{-t/10}$; com o relé desligado ($u = -1$), $y(t) = -1 + (y_0 + 1)\,e^{-t/10}$.
2. **O ciclo em regime:** suponha o relé **desligando** em $y = +0{,}5$. A partir daí $u = -1$ e a temperatura cai: $y(t) = -1 + 1{,}5\,e^{-t/10}$. Ela cai até atingir $-0{,}5$, quando o relé **liga**. Simetricamente, sobe de $-0{,}5$ a $+0{,}5$ com $u = +1$ — e o ciclo se repete. Amplitude da oscilação: $\boxed{A = h = 0{,}5}$ (exatamente a banda da histerese!).
3. **Meio período (descida):** impondo $y(t_{1/2}) = -0{,}5$:
$$-0{,}5 = -1 + 1{,}5\,e^{-t_{1/2}/10} \;\Rightarrow\; e^{-t_{1/2}/10} = \frac{0{,}5}{1{,}5} = \frac{1}{3} \;\Rightarrow\; t_{1/2} = 10\,\ln 3 = 10{,}99\ \mathrm{s}$$
4. **Período:** por simetria (subida idêntica), $\boxed{T = 20\,\ln 3 = 21{,}97\ \mathrm{s}}$. Simulação direta da malha: $T \approx 21{,}5$ s ✓ (diferença de ~2 % por resolução do chaveamento na malha de tempo).
5. **Item (c) — a dificuldade da função descritiva:** o balanço harmônico exige $\angle N(A) + \angle G(j\omega) = -180°$. Aqui $\angle N = -\mathrm{arcsen}(h/A) \in (-90°, 0)$ e $\angle G = -\mathrm{arctg}(10\omega) \in (-90°, 0)$: a soma **só atinge $-180°$ assintoticamente** ($\omega \to \infty$, $A \to h^+$) — o método não encontra interseção finita e "perde" o ciclo-limite que a análise exata de chaveamento (itens 1–4) revela. Moral: planta de **1ª ordem filtra pouco** os harmônicos da onda do relé, e a hipótese de filtragem falha. **A função descritiva é poderosa, mas não é universal** — quando ela e a simulação discordam, acredite na simulação.

*(teoria: §4.1.5 — histerese e relé; §4.3.9 — limitações do método; figura `m4_fig02`, painel direito)*

---

## Tópico 4.2 — Windup do integrador e anti-windup

### Exercício 4.2.1 — A aritmética do windup (quanto o integrador "enche"?)

**Enunciado.** Na malha-âncora do módulo — $G(s) = \dfrac{1}{10s+1}$, PI $u = k_p e + k_i\int e$ com $k_p = 2$, $k_i = 0{,}5$, saturação em $\pm 1{,}3$, degrau unitário — **estime** a carga do integrador no instante em que a saída cruza a referência, supondo o atuador saturado durante toda a subida. Compare com a carga de regime e explique o sobressinal observado (23,2 % contra 11,5 % do caso ideal).

**Resolução passo a passo.**

1. **Subida com atuador saturado:** enquanto saturado, $u = 1{,}3$ constante → a planta responde como a um degrau de 1,3: $y(t) = 1{,}3\,(1 - e^{-t/10})$.
2. **Instante do cruzamento** ($y = 1$): $1 = 1{,}3(1 - e^{-t^*/10}) \Rightarrow e^{-t^*/10} = \dfrac{0{,}3}{1{,}3} \Rightarrow t^* = 10\,\ln\!\dfrac{1{,}3}{0{,}3} = 14{,}66$ s.
3. **Carga acumulada:** com $e(t) = 1 - y(t) = -0{,}3 + 1{,}3\,e^{-t/10}$:
$$x_i(t^*) = \int_0^{t^*} e\,dt = \Big[-0{,}3\,t + 13\,\big(1 - e^{-t/10}\big)\Big]_0^{14{,}66} = -4{,}40 + 13\times 0{,}769 = 5{,}6$$
4. **Carga de regime:** em $y = r = 1$ permanente, $e = 0$ e o integrador sustenta sozinho o $u_{ss} = 1$ necessário (ganho DC unitário): $x_{i,ss} = \dfrac{u_{ss}}{k_i} = \dfrac{1}{0{,}5} = 2{,}0$.
5. **O diagnóstico:** no cruzamento, o integrador carrega **5,6** — um excesso de **3,6 (180 %!)** sobre o necessário. Enquanto esse excesso não escoar ($e < 0$ por muitos segundos), o $u$ pedido permanece alto, a planta continua acelerada e a saída ultrapassa: nasce o sobressinal de 23,2 % e a acomodação de ~39 s (contra 19,7 s do ideal). **Windup é isso: carga acumulada durante a saturação que precisa "descarregar" via erro de sinal oposto.**

*(teoria: §4.2.1–4.2.2; figuras `m4_fig03` e `m4_fig04`; valores confirmados pela simulação do Lab 15)*

---

### Exercício 4.2.2 — Projetando o anti-windup

**Enunciado.** (a) Escreva a regra do **clamping** para o PI do exercício anterior (saturação $\pm 1{,}3$), em pseudocódigo. (b) Para a estratégia de **back-calculation**, calcule a constante de rastreamento $T_t$ recomendada para: (i) o PI da malha-âncora ($T_i = 4$ s); (ii) o PID sintonizado por Ziegler-Nichols no experimento do relé do tópico 4.3 ($T_i = 2{,}22$ s, $T_d = 0{,}555$ s). (c) Por que o anti-windup exige que a saturação esteja **dentro** do controlador (software), mesmo quando o atuador já satura sozinho?

**Resolução passo a passo.**

1. **Clamping (pseudocódigo):**
```
u_PI = kp*e + ki*xi
u    = min(max(u_PI, -1.3), 1.3)
se (u_PI >=  1.3 e e > 0) ou (u_PI <= -1.3 e e < 0):
    dxi = 0        # saturado E o erro pede mais: congela
senão:
    dxi = e        # caso contrário integra normalmente
```
2. **Leitura da regra:** o congelamento só ocorre quando as duas condições se somam (saturado **e** erro a favor da saturação). Erro contra a saturação integra livre — é ele quem "tira" o atuador do teto.
3. **Back-calculation — PI:** $T_t \approx T_i = \boxed{4\ \mathrm{s}}$.
4. **Back-calculation — PID:** $T_t \approx \sqrt{T_i\,T_d} = \sqrt{2{,}22 \times 0{,}555} = \sqrt{1{,}232} = \boxed{1{,}11\ \mathrm{s}}$.
5. **Item (c):** a back-calculation compara o $u$ **pedido** com o $u$ **entregue**: $e_s = u - u_{PI}$. Se a saturação acontece só no atuador (hardware), o controlador não "vê" o $u$ real e o termo de correção não existe — o integrador carrega cego. Modelando o limitador **em software**, o controlador conhece exatamente o quanto foi cortado — e o anti-windup funciona. Bônus: o limite de software pode ser ajustado *abaixo* do físico (proteção).

*(teoria: §4.2.3–4.2.5; figura `m4_fig04` — painel direito mostra o clamping em ação)*

---

### Exercício 4.2.3 — Interpretando a tabela de resultados

**Enunciado.** A tabela abaixo resume os três experimentos da malha-âncora (degrau unitário). Para cada linha, **explique fisicamente** o resultado e responda: por que a linha 3 é *melhor* que a linha 1, que nem saturação tem?

| Cenário | $M_p$ | $t_s$ (±5 %) |
|---|---|---|
| 1 — PI ideal, sem saturação | 11,5 % | 19,7 s |
| 2 — PI com saturação $\pm 1{,}3$ | 23,2 % | 39,3 s |
| 3 — PI com saturação + clamping | 3,2 % | 13,4 s |

**Resolução passo a passo.**

1. **Linha 1 (ideal):** o atuador "inventa" o que o PI pede — inclusive o pico $u(0^+) = k_p \times 1 = 2$. A resposta é exatamente a do projeto linear: rápida, com o sobressinal de 11,5 % do par de polos dominantes. **É irreal**: nenhum atuador de 1,3 entrega 2.
2. **Linha 2 (windup):** o teto físico limita a aceleração (subida mais lenta), o integrador enche 180 % a mais (Exercício 4.2.1), e o excesso cobra seu preço depois do cruzamento: sobressinal dobrado e acomodação dobrada. **O projeto linear não avisou nada disso** — daí a regra prática: *saturou na simulação linear? Refaça com a não linearidade.*
3. **Linha 3 (clamping):** durante a saturação o integrador congela — chega ao cruzamento com a carga "na medida", sem excesso para descarregar → quase sem sobressinal (3,2 %). E a subida usa o **teto físico o tempo todo** ($u = 1{,}3$), acelerando mais que a linha 1 depois do instante em que o $u$ ideal cairia abaixo de 1,3 → acomodação *mais rápida* (13,4 s).
4. **A resposta da pergunta:** a linha 1 "gasta" seus 11,5 % de sobressinal porque o projeto linear equilibra rapidez × amortecimento com atuador infinito. A linha 3 usa o atuador real no seu **máximo** durante toda a subida e entrega o integrador calibrado no ponto de cruzamento. **Saturação bem gerenciada não é degradação: é operação no limite físico — que é o melhor que a física permite.**
5. **Lição de projeto (para o firmware do projeto final):** todo PID implementado em software deve nascer com (i) limitador de saída e (ii) anti-windup — três linhas de código que transformam o comportamento da malha.

*(teoria: §4.2.2–4.2.5; figura `m4_fig03`; simulações do Lab 15)*

---

## Tópico 4.3 — Ciclos-limite, função descritiva e o experimento do relé

### Exercício 4.3.1 — Deduzindo a função descritiva do relé

**Enunciado.** Deduza $N(A) = \dfrac{4d}{\pi A}$ para o relé ideal de amplitude $d$, partindo da definição $N(A) = (a_1 + j b_1)/A$ com $a_1 = \dfrac{2}{T}\displaystyle\int_0^T u\,\mathrm{sen}(\omega t)\,dt$ e $b_1 = \dfrac{2}{T}\displaystyle\int_0^T u\,\cos(\omega t)\,dt$.

**Resolução passo a passo.**

1. **A saída do relé:** com $e(t) = A\,\mathrm{sen}(\omega t)$ ($A > 0$), o relé comuta exatamente nos zeros da entrada: $u(t) = +d$ no primeiro semiperíodo ($0 < t < T/2$) e $u(t) = -d$ no segundo — **onda quadrada em fase com a entrada**.
2. **Coeficiente $b_1$:** a onda quadrada é **ímpar** em relação ao eixo do tempo ($u(-t) = -u(t)$), e o cosseno é par → o produto é ímpar → a integral sobre o período é nula: $b_1 = 0$. (Conclusão geral: não linearidade estática ímpar e sem memória ⇒ $N$ real.)
3. **Coeficiente $a_1$:** explorando a simetria (os dois semiperíodos contribuem igual, e dentro do primeiro as duas metades também):
$$a_1 = \frac{2}{T}\int_0^T u\,\mathrm{sen}(\omega t)\,dt = \frac{4}{T}\int_0^{T/2} d\,\mathrm{sen}(\omega t)\,dt = \frac{4d}{T}\left[-\frac{\cos(\omega t)}{\omega}\right]_0^{T/2}$$
4. **Avaliando:** $\cos(\omega T/2) = \cos(\pi) = -1$ e $\cos(0) = 1$ → $a_1 = \dfrac{4d}{T}\cdot\dfrac{2}{\omega} = \dfrac{4d}{T}\cdot\dfrac{T}{\pi} = \dfrac{4d}{\pi}$.
5. **Resultado:** $N(A) = \dfrac{a_1}{A} = \boxed{\dfrac{4d}{\pi A}}$ — real, positivo, **inversamente proporcional à amplitude**. Note o papel do $\pi$: a onda quadrada tem primeiro harmônico de amplitude $4d/\pi \approx 1{,}27\,d$ — maior que a própria onda! (os harmônicos ímpares "completam" a forma achatada). Verificação numérica por Fourier (Lab 16): $A = 1$ → $N = 1{,}2732$ ✓.

*(teoria: §4.3.2–4.3.3; figura `m4_fig05`)*

---

### Exercício 4.3.2 — Previsão completa de um ciclo-limite

**Enunciado.** A planta $G(s) = \dfrac{2}{s(s+1)(s+4)}$ é realimentada (unitária) através de um relé ideal de amplitude $d = 1$, com referência nula. (a) Determine onde o Nyquist de $G$ cruza o eixo real. (b) Preveja amplitude e frequência do ciclo-limite. (c) O ciclo é estável? (d) Relacione o resultado com o ganho crítico de Routh da malha linear.

**Resolução passo a passo.**

1. **Cruzamento com o eixo real:** escreva o denominador de $G(j\omega)$:
$$j\omega(1 + j\omega)(4 + j\omega) = j\omega\big[(4 - \omega^2) + 5j\omega\big] = -5\omega^2 + j\omega(4 - \omega^2)$$
2. A parte imaginária zera em $\omega^2 = 4$ → $\boxed{\omega = 2\ \mathrm{rad/s}}$ (período $T = \pi \approx 3{,}14$ s). Nessa frequência: $G(j2) = \dfrac{2}{-5\times 4} = \boxed{-0{,}1}$.
3. **Balanço harmônico:** $N(A)\,G(j2) = -1 \Rightarrow \dfrac{4}{\pi A}\times 0{,}1 = 1 \Rightarrow \boxed{A = \dfrac{4}{10\pi} = 0{,}127}$.
4. **Estabilidade (Loeb):** para o relé, $-1/N(A) = -\pi A/4$ percorre o eixo real negativo de $0$ a $-\infty$ com $A$ crescente. Em $-0{,}1$: pontos à **esquerda** ($A$ maior) estão fora da envolvida (Nyquist de $G$ envolve pontos à esquerda de $-0{,}1$... conferindo: o Nyquist cruza em $-0{,}1$ e tende à origem — pontos entre $-0{,}1$ e $0$ são envolvidos? Não: a curva passa por $-0{,}1$ e fecha na origem; a região envolvida fica à **esquerda** do cruzamento). $A$ crescente sai da região envolvida para a não envolvida → **ciclo-limite estável**.
5. **Simulação (Lab 16):** $A = 0{,}133$, $\omega = 1{,}94$ rad/s — erros de 4,5 % e 3 %, típicos do método ✓.
6. **Item (d) — a ponte com Routh:** a malha linear com ganho $K$ tem característico $s^3 + 5s^2 + 4s + 2K$; Routh: $5\times 4 > 2K \Rightarrow K < 10$. E o balanço harmônico dá $N(A) = 10$ — **a função descritiva "mede" exatamente o ganho último**: $K_u = \dfrac{4d}{\pi A} = 10$. Routh (linear, exato) e função descritiva (não linear, aproximada) contam a mesma história por dois caminhos.

*(teoria: §4.3.4–4.3.6; figuras `m4_fig06`–`m4_fig08` para o caso análogo da planta $1/[s(s+1)(s+2)]$)*

---

### Exercício 4.3.3 — Do experimento do relé à sintonia PID

**Enunciado.** No experimento do relé (Åström) aplicado à planta do Exercício 4.3.2, com relé $d = 1$, mede-se na saída oscilação de amplitude $a = 0{,}127$ e período $P_u = 3{,}14$ s. (a) Calcule $K_u$ e $P_u$. (b) Monte as três sintonias de Ziegler-Nichols (P, PI, PID). (c) Cite dois cuidados práticos na medição.

**Resolução passo a passo.**

1. **Ganho último:** $\boxed{K_u = \dfrac{4d}{\pi a} = \dfrac{4}{\pi \times 0{,}127} = 10{,}0}$ (conferindo com Routh: $K < 10$ ✓ — a medição experimental e a análise teórica se confirmam mutuamente).
2. **Período último:** medido diretamente: $P_u = 3{,}14$ s ($\omega_u = 2$ rad/s).
3. **Tabela ZN:**
   - **P:** $k_p = 0{,}5 \times 10 = \boxed{5{,}0}$
   - **PI:** $k_p = 0{,}45 \times 10 = \boxed{4{,}5}$, $T_i = 3{,}14/1{,}2 = \boxed{2{,}62\ \mathrm{s}}$
   - **PID:** $k_p = 0{,}6 \times 10 = \boxed{6{,}0}$, $T_i = 3{,}14/2 = \boxed{1{,}57\ \mathrm{s}}$, $T_d = 3{,}14/8 = \boxed{0{,}39\ \mathrm{s}}$
4. **Cuidados práticos (item c):** (i) medir **depois** do transiente — descartar os 2–3 primeiros ciclos e tirar a média de vários períodos e semi-amplitudes (pico a pico ÷ 2); (ii) usar **relé com histerese** se houver ruído de medição — sem ela, o ruído comuta o relé fora de hora e corrói as medidas (com histerese $h$, a fórmula ganha correção: $K_u = \dfrac{4d}{\pi\sqrt{a^2 - h^2}}$ para $a > h$).
5. **E depois da sintonia?** ZN entrega resposta agressiva (amortecimento 1/4). O fluxo profissional: sintonizar pelo relé → medir a resposta → **refinar** com as ferramentas dos Módulos 02/03 (ex.: reduzir $k_p$ de 10–30 % se o sobressinal incomodar, reajustar $T_i$ pela cauda de acomodação).

*(teoria: §4.3.7–4.3.8; Lab 16 executa o experimento completo)*

---

### Exercício 4.3.4 — Saturação: quando o método prevê que NÃO oscila

**Enunciado.** A malha linear $L(s) = \dfrac{K}{s(s+1)(s+2)}$ oscila na fronteira para $K = 6$ (Routh; Lab 12). Considere agora a mesma malha com o ganho $K$ seguido de uma **saturação** de ganho 1 e nível $s = 1$ na entrada da planta (relé "suave"). (a) Esboce a curva $-1/N(A)$ da saturação no plano complexo. (b) Para $K = 1$, o método prevê ciclo-limite? (c) E para $K = 10$? Interprete fisicamente.

**Resolução passo a passo.**

1. **A curva $-1/N(A)$ da saturação:** para $A \leq 1$, $N = 1$ (não satura) → $-1/N = -1$, um **ponto**; para $A > 1$, $N$ cai de 1 a 0 → $-1/N$ percorre o eixo real negativo de $-1$ até $-\infty$. **A curva é o semi-eixo real a partir de $-1$** (diferente do relé, que começa na origem!).
2. **Cruzamento do Nyquist:** como no exemplo-âncora, $K\,G(j\omega)$ cruza o eixo real em $-\dfrac{K}{6}$ (na frequência $\omega = \sqrt{2}$).
3. **$K = 1$:** cruzamento em $-1/6$, à **direita** de $-1$ → **não há interseção** com $-1/N(A)$ → o método prevê **ausência de ciclo-limite**: oscilações decaem para qualquer amplitude. Coerente: com $K = 1$ a malha linear é estável com folga ($K < 6$) e a saturação só *reduz* o ganho — se algo, fica mais estável.
4. **$K = 10$:** cruzamento em $-10/6 = -1{,}67 < -1$ → **interseção existe**. A amplitude prevista sai de $N(A) = \dfrac{1}{1{,}67} = 0{,}6$ — pela curva da saturação (figura `m4_fig05`), $N(A) = 0{,}6$ corresponde a $A \approx 2$ (conta: $N(2) = \dfrac{2}{\pi}[\mathrm{arcsen}(0{,}5) + 0{,}5\sqrt{0{,}75}] = 0{,}609$ → $A \approx 2{,}0$), na frequência $\omega = \sqrt{2}$.
5. **Interpretação física:** com $K = 10$ a malha linear seria **instável** — a oscilação cresceria sem limite. A saturação "segura" o crescimento: quando a amplitude passa de 1, o ganho efetivo $N(A)$ cai; em $A \approx 2$, o ganho efetivo total $10 \times 0{,}6 = 6$ é exatamente o crítico — a oscilação **estaciona**. É o mecanismo universal dos ciclos-limite por saturação: **a não linearidade transforma a instabilidade linear em oscilação permanente de amplitude finita**. (E é por isso que amplificadores "instáveis" não explodem: apitam numa amplitude fixa.)

*(teoria: §4.3.3–4.3.6; figuras `m4_fig05` e `m4_fig06`)*

---

## Tabela-resumo das contas âncora

| Conta | Resultado | Onde aparece |
|---|---|---|
| Saturação $k=2$, $s=1$: $N(2)$ | 1,218 (−39 % de ganho) | Ex. 4.1.1 |
| Zona morta $d=0{,}5$: faixa estacionária | $\|e_{ss}\| \leq d/k_p$ | Ex. 4.1.2 |
| Termostato $h=0{,}5$, $\tau=10$: período | $T = 20\ln 3 = 21{,}97$ s | Ex. 4.1.3 |
| Windup: carga no cruzamento × regime | $5{,}6$ × $2{,}0$ (excesso 180 %) | Ex. 4.2.1 |
| $T_t$ back-calculation | $T_i$ (PI) / $\sqrt{T_i T_d}$ (PID) | Ex. 4.2.2 |
| Relé $d=1$ + $1/[s(s+1)(s+2)]$ | $A = 0{,}212$, $\omega = \sqrt{2}$, $K_u = 6$ | §4.3.5 |
| Relé $d=1$ + $2/[s(s+1)(s+4)]$ | $A = 0{,}127$, $\omega = 2$, $K_u = 10$ | Ex. 4.3.2–4.3.3 |
| Saturação + $K/[s(s+1)(s+2)]$ | sem ciclo se $K < 6$; ciclo se $K > 6$ | Ex. 4.3.4 |
