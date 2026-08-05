# Módulo 02 — Exercícios Resolvidos

> Material do aluno. Cada exercício indica a seção da **teoria** (`teoria_modulo2.md`) onde o conteúdo pode ser consultado. Todos os valores numéricos de respostas ao degrau foram conferidos por simulação.

---

## Tópico 2.1 — Regiões de desempenho no plano-s e aproximações

### Exercício 2.1.1 — A região combinada
*(teoria: §2.1.3–§2.1.6; âncora principal)*

**Enunciado.** Requisitos: $M_p \leq 20\,\%$, $t_p \leq 3{,}14$ s e $t_s(2\,\%) \leq 8$ s. (a) Desenhe a região do plano-s onde os polos dominantes devem estar. (b) Verifique se os candidatos $\square_1 = -0{,}5+1j$ e $\square_2 = -0{,}6+1{,}1j$ atendem. (c) Para o candidato válido, estime $M_p$, $t_p$, $t_s(2\,\%)$ e $t_r(10\text{–}90\,\%)$.

**Resolução passo a passo.**
1. **Overshoot → setor:** $M_p \leq 20\,\% \Rightarrow \zeta \geq 0{,}456 \Rightarrow \beta \leq \arccos(0{,}456) = 62{,}9°$.
2. **Instante de pico → faixa:** $t_p = \pi/\omega_d \leq 3{,}14 \Rightarrow \omega_d \geq \pi/3{,}14 = 1$ rad/s.
3. **Acomodação → semirreta:** $t_s(2\,\%) = 4/\sigma \leq 8 \Rightarrow \sigma \geq 0{,}5$.
4. **Candidato $\square_1 = -0{,}5+1j$:** $\sigma = 0{,}5$ ✓ (no limite), $\omega_d = 1$ ✓ (no limite), mas $\beta = \mathrm{arctg}(1/0{,}5) = 63{,}4° > 62{,}9°$ ✗ — **reprovado no overshoot** (cairia $M_p \approx 20{,}7\,\%$).
5. **Candidato $\square_2 = -0{,}6+1{,}1j$:** $\sigma = 0{,}6 \geq 0{,}5$ ✓; $\omega_d = 1{,}1 \geq 1$ ✓; $\omega_n = \sqrt{0{,}6^2+1{,}1^2} = 1{,}253$; $\zeta = 0{,}6/1{,}253 = 0{,}479 \geq 0{,}456$ ✓ ($\beta = 61{,}4°$). **Aprovado.**
6. **Estimativas para $\square_2$:**
   - $M_p = e^{-\zeta\pi/\sqrt{1-\zeta^2}} = e^{-0{,}479\pi/0{,}878} \approx 18{,}0\,\%$ ✓;
   - $t_p = \pi/1{,}1 = 2{,}86$ s ✓;
   - $t_s(2\,\%) = 4/0{,}6 = 6{,}67$ s ✓;
   - $t_r(10\text{–}90\,\%) \approx 1{,}6/\omega_n = 1{,}6/1{,}253 = 1{,}28$ s.

### Exercício 2.1.2 — Aproximação de 3ª ordem por 2ª e a regra dos 5×
*(teoria: §2.1.8; âncora principal)*

**Enunciado.** Seja $T(s) = \dfrac{4\,p_3}{(s^2+2s+4)(s+p_3)}$ (par dominante $-1 \pm 1{,}73j$). (a) Estime $M_p$ e $t_p$ pela aproximação de 2ª ordem. (b) Usando a regra dos 5×, para quais valores de $p_3$ a aproximação é confiável? (c) Compare com os valores simulados para $p_3 = 10$, $3$ e $1$.

**Resolução passo a passo.**
1. **Par dominante:** $\omega_n = \sqrt{4} = 2$; $2\zeta\omega_n = 2 \Rightarrow \zeta = 0{,}5$; $\omega_d = \sqrt{3} = 1{,}73$.
2. **Aproximação de 2ª ordem:** $M_p = e^{-0{,}5\pi/\sqrt{0{,}75}} = 16{,}3\,\%$; $t_p = \pi/1{,}73 = 1{,}81$ s.
3. **Regra dos 5×:** confiável se $p_3 \geq 5 \times |\mathrm{Re}| = 5 \times 1 = 5$.
4. **Simulação (ganho DC sempre mantido em 1):**
   - $p_3 = 10$ ($10\times$): $M_p = 15{,}9\,\%$ — praticamente o previsto ✓;
   - $p_3 = 3$ ($3\times$): $M_p = 12{,}2\,\%$ — a aproximação já erra visivelmente;
   - $p_3 = 1$ ($1\times$): $M_p = 0\,\%$ — **o overshoot morreu**: o polo real passa a dominar a resposta (vira quase 1ª ordem).
5. **Conclusão:** a regra dos 5× separa "fórmulas de 2ª ordem valem" de "refaça as contas com os polos de verdade".

### Exercício 2.1.3 — O efeito do zero (SPE e SPD)
*(teoria: §2.1.9; âncora principal)*

**Enunciado.** Seja $T_0(s) = \dfrac{4}{s^2+2s+4}$. Acrescente um zero mantendo o ganho DC: $T_1(s) = \dfrac{s+a}{a}\,T_0(s)$. (a) Explique por que $y_1(t) = y(t) + \dot y(t)/a$. (b) Preveja qualitativamente o efeito para $a = 10$, $5$ e $2$ e compare com a simulação. (c) E se o zero estiver em $+5$?

**Resolução passo a passo.**
1. **No tempo:** $Y_1 = \dfrac{s+a}{a}Y = Y + \dfrac{1}{a}sY \Rightarrow y_1(t) = y(t) + \dfrac{1}{a}\dot y(t)$ — o zero **soma a derivada** à resposta (com CI nulas).
2. **Previsão:** $a$ grande → derivada diluída → resposta ≈ original; $a$ pequeno → derivada pesa → mais overshoot e mais velocidade.
3. **Simulação ($T_0$: $M_p = 16{,}3\,\%$, $t_p = 1{,}81$ s, $t_r = 1{,}21$ s):**

| Zero | $M_p$ | $t_p$ | $t_r$ |
|---|---|---|---|
| $-10$ | 16,7 % | 1,70 s | 1,10 s |
| $-5$ | 18,0 % | 1,58 s | 0,97 s |
| $-2$ | 29,8 % | 1,21 s | 0,61 s |

   Confirma a previsão: quanto mais perto o zero, mais overshoot e mais rápido.
4. **Zero no SPD ($a = -5$, zero em $+5$):** $y_1 = y - |\dot y|/5$ → a resposta começa **indo para o lado errado**: mínimo de $-6{,}2\,\%$ (**undershoot**, fase não mínima) antes de subir e ultrapassar ($M_p = 17{,}3\,\%$). É o avião que afunda o bico antes de subir.

---

## Tópico 2.2 — O Lugar Geométrico das Raízes

### Exercício 2.2.1 — Condição de ângulo e de módulo
*(teoria: §2.2.3–§2.2.4; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{1}{s(s+6)}$, verifique se cada ponto pertence ao LGR e, pertencendo, calcule o ganho: $\square_a = -3+3j$; $\square_b = -3+4j$; $\square_c = -6+6j$.

**Resolução passo a passo.**
1. **Ângulos sempre dos vetores que saem dos polos** (não há zeros) até o ponto, medidos do eixo real positivo (use `atan2`!).
2. **$\square_a = -3+3j$:** vetor do polo $0$: $180° - 45° = 135°$; do polo $-6$: $45°$. $\angle G = -(135°+45°) = -180°$ ✓ **pertence**. Módulo: distâncias $\sqrt{18}$ e $\sqrt{18}$ → $k = \sqrt{18}\cdot\sqrt{18} = 18$.
3. **$\square_b = -3+4j$:** ângulos $180° - \mathrm{arctg}(4/3) = 126{,}9°$ e $\mathrm{arctg}(4/3) = 53{,}1°$ → soma $180°$ ✓ **pertence**. Distâncias $5$ e $5$ → $k = 25$.
4. **$\square_c = -6+6j$:** ângulos $135°$ (do polo $0$) e $90°$ (do polo $-6$) → soma $225° \neq 180°$ ✗ **não pertence ao LGR para nenhum $k$** — nem perca tempo calculando ganho.
5. **Conferindo:** o LGR de $1/(s(s+6))$ é o trecho $(-6,0)$ mais a vertical em $-3$: os pontos $\square_a$ e $\square_b$ estão sobre a vertical; $\square_c$, não.

### Exercício 2.2.2 — Projeto de controle P no plano-s
*(teoria: §2.2.5; âncora principal)*

**Enunciado.** $G(s) = \dfrac{10}{s(s+10)}$. Projete $C(s) = k$ para $M_p \leq 5\,\%$ com o **menor $t_p$ possível**. Verifique por simulação.

**Resolução passo a passo.**
1. $M_p \leq 5\,\% \Rightarrow \zeta \geq 0{,}69 \Rightarrow \beta \leq \arccos(0{,}69) = 46{,}37°$.
2. **LGR:** encontro em $-5$ ($k = 25$), depois vertical em $-5$. Para o **menor** $t_p$, subir no LGR **até o limite do setor**: polos escolhidos $-5 \pm j\,5\,\mathrm{tg}(46{,}37°) = -5 \pm 5{,}25j$.
3. **Condição de módulo** ($A = 10$ — não esqueça do $A$!): $k = \dfrac{|\square_d|\cdot|\square_d+10|}{10} = \dfrac{7{,}25 \times 7{,}25}{10} \approx 5{,}26$.
4. **Verificação:** $T(s) = \dfrac{52{,}6}{s^2+10s+52{,}6}$; $\omega_d = 5{,}25 \Rightarrow t_p = \pi/5{,}25 = 0{,}60$ s; simulação: $M_p = 5{,}0\,\%$ ✓, $t_p = 0{,}598$ s ✓.
5. **Discussão:** subir mais no LGR diminuiria $t_p$ mas furaria o overshoot. O projeto de P é a escolha de **um ponto sobre o LGR** — nada além disso é possível com ganho puro.

### Exercício 2.2.3 — Esboço completo de LGR (3ª ordem)
*(teoria: §2.2.6–§2.2.7; âncora principal)*

**Enunciado.** Esboce o LGR de $G(s) = \dfrac{200}{s(s+10)(s+20)}$: trechos no eixo real, assíntotas, centroide, cruzamento com o eixo imaginário e ponto de saída.

**Resolução passo a passo.**
1. **Ramos:** $n = 3$, $m = 0$ → 3 ramos, todos ao infinito.
2. **Eixo real:** à direita de um ponto em $(-10, 0)$ há 1 polo (ímpar) ✓; em $(-\infty, -20)$ há 3 (ímpar) ✓. Trechos: $(-10, 0)$ e $(-\infty, -20)$.
3. **Assíntotas:** $n-m = 3$ → ângulos $\dfrac{180°+l\cdot360°}{3}$: $60°$, $180°$, $300°$.
4. **Centroide:** $\sigma_a = \dfrac{(0-10-20) - 0}{3} = -10$.
5. **Cruzamento do eixo $j\omega$ (Routh):** característico $s^3 + 30s^2 + 200s + 200k$. Linha $s^1$: $\dfrac{30 \times 200 - 200k}{30} = 0 \Rightarrow k = 30$. Auxiliar: $30s^2 + 200 \times 30 = 0 \Rightarrow s = \pm j\sqrt{200} = \pm 14{,}1j$. (Instável para $k > 30$!)
6. **Ponto de saída:** $-\dfrac{1}{G} = -\dfrac{s^3+30s^2+200s}{200}$ → derivada $-(3s^2+60s+200) = 0$ → $s = -4{,}23$ ✓ (no trecho $(-10,0)$) e $s = -15{,}77$ ✗ (fora de qualquer trecho — descartada).
7. Compare com a figura `m2_fig15_lgr_200.png` na teoria.

### Exercício 2.2.4 — Regras 7 e 8 na prática (extra)
*(teoria: §2.2.6)*

**Enunciado.** Para $G(s) = \dfrac{1}{(s+1)(s+2)(s+3)}$, determine o ganho e o ponto de cruzamento com o eixo imaginário e os pontos de saída do eixo real.

**Resolução passo a passo.**
1. **Característico:** $(s+1)(s+2)(s+3) + k = s^3 + 6s^2 + 11s + (6+k)$.
2. **Routh:** linha $s^1$: $\dfrac{6 \times 11 - (6+k)}{6} = 0 \Rightarrow k = 60$.
3. **Auxiliar:** $6s^2 + 66 = 0 \Rightarrow s = \pm j\sqrt{11} = \pm 3{,}32j$ — cruzamento com $k = 60$.
4. **Saída:** $\dfrac{\mathrm{d}}{\mathrm{d}s}\left(-\dfrac{1}{G}\right) = -(3s^2+12s+11) = 0 \Rightarrow s = -1{,}42$ e $s = -2{,}58$.
5. **Teste dos trechos:** o LGR cobre $(-2, -1)$ e $(-\infty, -3)$. $-1{,}42 \in (-2,-1)$ ✓; $-2{,}58$ não está em trecho algum ✗ → **descartada**.
6. **Moral da regra 8:** a derivada de $-1/G$ sempre dá candidatos demais — só valem os que caem **sobre trechos do LGR**.

---

## Tópico 2.3 — Controlador de avanço de fase

### Exercício 2.3.1 — Da impossibilidade do P ao avanço: contribuição, duas soluções
*(teoria: §2.3.1–§2.3.5; âncora principal)*

**Enunciado.** $G(s) = \dfrac{4}{s(s+4)}$, requisitos $M_p \leq 5\,\%$ e $t_p \leq 1$ s (impossíveis com P — ver §2.3.1). (a) Calcule a contribuição de fase necessária. (b) Projete o avanço **por cancelamento** e verifique por simulação. (c) Projete com o **zero embaixo de $\square_d$** e compare.

**Resolução passo a passo.**
1. **Polo desejado:** $M_p = 5\,\% \Rightarrow \zeta = 0{,}69$; $t_p = 1 \Rightarrow \omega_d = \pi = 3{,}14$... adotamos $\square_d = -3{,}14 + 3{,}2j$ ($\zeta = 0{,}7$, $\omega_d = 3{,}2$ — folga mínima nos dois requisitos).
2. **Contribuição:** $\angle G(\square_d) = -(134{,}5° + 74{,}9°) = -209{,}5° \Rightarrow \angle C(\square_d) = 209{,}5° - 180° = +29{,}5°$.
3. **Cancelamento (zero sobre o polo $-4$):** ângulo do zero: $\mathrm{arctg}(3{,}2/0{,}86) = 74{,}9°$ → o polo deve contribuir $74{,}9° - 29{,}5° = 45{,}4°$ → $\mathrm{tg}(45{,}4°) = \dfrac{3{,}2}{b-3{,}14} \Rightarrow b = 6{,}3$. Ganho (com o cancelamento, $CG = \dfrac{4k}{s(s+6{,}3)}$): $k = \dfrac{|\square_d|\cdot|\square_d+6{,}3|}{4} = \dfrac{4{,}48 \times 4{,}50}{4} = 5{,}04$.
   $$C(s) = 5{,}04\,\frac{s+4}{s+6{,}3}$$
   **Simulação:** polos de MF $-3{,}15 \pm 3{,}2j$ ✓ e $-4$ (quase cancelado pelo zero); $M_p = 4{,}5\,\%$ ✓, $t_p = 0{,}98$ s ✓.
4. **Zero embaixo ($a = 3{,}14$):** ângulo do zero $= 90°$ → polo: $90° - 29{,}5° = 60{,}5°$ → $b = 3{,}14 + \dfrac{3{,}2}{\mathrm{tg}(60{,}5°)} = 4{,}95$; $k = \dfrac{4{,}48 \times 3{,}31 \times 3{,}68}{4 \times 3{,}2} = 4{,}27$ → $C(s) = 4{,}27\dfrac{s+3{,}14}{s+4{,}95}$.
   **Simulação:** polos de MF $-3{,}14 \pm 3{,}2j$ ✓ **e $-2{,}66$** — o 3º polo caiu **perto** do par desejado (sem dominância!) e matou o overshoot: $M_p = 1{,}6\,\%$, $t_p = 1{,}11$ s.
5. **Moral:** as duas soluções colocam o par desejado no lugar exato — mas o **terceiro polo** decide se o desempenho projetado se realiza. Sempre confira **todos** os polos de MF (§2.1.8).

### Exercício 2.3.2 — Projeto em dois estágios: P, depois avanço
*(teoria: §2.3.7; âncora principal)*

**Enunciado.** $G(s) = \dfrac{10}{s(s+10)}$. Estágio 1: projete P para $M_p \leq 20\,\%$. Estágio 2: acrescente um avanço que **dobre a velocidade** (dobrar $\sigma$ e $\omega_d$), mantendo $M_p = 20\,\%$.

**Resolução passo a passo.**
1. **Estágio 1:** $\zeta = 0{,}456 \Rightarrow \beta = 62{,}9°$ → polos $-5 \pm j\,5\,\mathrm{tg}(62{,}9°) = -5 \pm 9{,}8j$ → $k = \dfrac{11^2}{10} = 12{,}1$. Resposta: $M_p = 20\,\%$, $t_p \approx 0{,}32$ s.
2. **Estágio 2 — novo alvo:** $\square_d = -10 + 19{,}6j$.
3. **Fase da planta:** $\angle G(\square_d) = -207°$ → contribuição necessária $+27°$ (abaixo dos 40° ✓).
4. **Zero cancela o polo $-10$** → o polo do controlador contribui $90° - 27° = 63°$ → $\mathrm{tg}(63°) = \dfrac{19{,}6}{b - 10} \Rightarrow b = 20$.
5. **Ganho:** $k = \dfrac{|\square_d|\cdot|\square_d+20|}{10 \times 1} = \dfrac{22 \times 22}{10} = 48{,}4$.
   $$C(s) = 48{,}4\,\frac{s+10}{s+20} \;\Rightarrow\; T(s) = \frac{484}{s^2+20s+484}$$
6. **Verificação:** $\omega_n = 22$, $\zeta = 10/22 = 0{,}455$ → $M_p = 20{,}1\,\%$ ✓ e $t_p = \pi/19{,}6 = 0{,}16$ s — **mesmo overshoot, metade do tempo de pico**. O cancelamento zerou a ordem extra: 2ª ordem exata.

### Exercício 2.3.3 — Avanço para 3ª ordem e a regra dos 40°
*(teoria: §2.3.8; âncora principal)*

**Enunciado.** $G(s) = \dfrac{20(s+15)}{s(s+10)(s+20)}$, requisitos $M_p = 25\,\%$ e $t_p = 150$ ms. Projete o avanço pela bissetriz e verifique por simulação. O que a regra dos 40° diria se a contribuição necessária fosse $65°$?

**Resolução passo a passo.**
1. $\zeta = 0{,}404$; $\omega_d = \pi/0{,}15 = 21$ rad/s → $\square_d = -9{,}3 + 21j$.
2. $\angle G(\square_d) = -190{,}2°$ → contribuição $+10{,}2°$ (pequena — o LGR quase já passava por lá).
3. **Bissetriz:** $a = 9{,}3 - 21\,\mathrm{tg}(5{,}1°) = 7{,}4$ e $b = 9{,}3 + 21\,\mathrm{tg}(5{,}1°) = 11{,}2$; ganho $k = 26{,}1$:
   $$C(s) = 26{,}1\,\frac{s+7{,}4}{s+11{,}2}$$
4. **Simulação:** $M_p = 23{,}2\,\%$ (projeto: 25 %) e $t_p = 148$ ms ✓ — a diferença vem das aproximações: as fórmulas são de 2ª ordem, a planta tem 3 polos e 1 zero.
5. **Regra dos 40°:** $65°$ com um único par é **Fusca querendo andar como Ferrari** — o polo fica longe demais, o ganho explode e os outros polos de MF pagam a conta. Solução: **dois avanços em cascata** (cada um com até 40°) ou requisitos mais realistas.

---

## Tópico 2.4 — Controlador de atraso de fase e PI

### Exercício 2.4.1 — O mecanismo: dobrar $k_v$ sem mover os polos
*(teoria: §2.4.1–§2.4.2; âncora principal)*

**Enunciado.** $G(s) = \dfrac{1}{s(s+3{,}2)}$ com controle P, $k = 7{,}4$. (a) Calcule os polos de MF, $\zeta$, $\omega_n$, $k_v$ e $e_{ss}$ para rampa unitária. (b) Acrescente o atraso $(s+0{,}02)/(s+0{,}01)$ e repita. (c) Onde foram parar os polos de MF?

**Resolução passo a passo.**
1. **Sem atraso:** $T(s) = \dfrac{7{,}4}{s^2+3{,}2s+7{,}4}$ → polos $-1{,}6 \pm 2{,}2j$; $\omega_n = \sqrt{7{,}4} = 2{,}72$; $\zeta = 3{,}2/(2 \times 2{,}72) = 0{,}59$ → $M_p \approx 10\,\%$.
2. **Erro:** tipo 1, $k_v = \lim_{s\to0} s\cdot\dfrac{7{,}4}{s(s+3{,}2)} = \dfrac{7{,}4}{3{,}2} = 2{,}31$ → $e_{ss} = 1/2{,}31 = 0{,}43$.
3. **Com o atraso:** $C(s) = 7{,}4\dfrac{s+0{,}02}{s+0{,}01}$. Em $s \to 0$: $(0{,}02)/(0{,}01) = 2$ → $k_v = 4{,}62$ → $e_{ss} = 0{,}215$ (**metade** ✓).
4. **Polos de MF com o atraso:** $-1{,}595 \pm 2{,}196j$ (praticamente os mesmos $-1{,}6 \pm 2{,}2j$!) **e $-0{,}0201$** — um polo extra lento colado no zero do atraso (quase-cancelamento), responsável pela convergência lenta do erro.
5. **Por que funciona:** no ponto $-1{,}6+2{,}2j$, o par $0{,}02/0{,}01$ contribui $\approx 1$: $\dfrac{-1{,}6+2{,}2j+0{,}02}{-1{,}6+2{,}2j+0{,}01} \approx 1\angle{-0{,}5°}$. O transitório não sente; o regime, sim.

### Exercício 2.4.2 — O trade-off do fator (simulação guiada)
*(teoria: §2.4.3; âncora principal)*

**Enunciado.** Sobre o sistema do exercício anterior (polos $-1{,}6 \pm 2{,}2j$), projete atrasos com zero em $-0{,}16$ (regra do 1/10) para fator 2 e fator 10. Calcule a contribuição de fase de cada um e compare os overshoots simulados. Repita com o par afastado: $(s+0{,}8)/(s+0{,}08)$ (também fator 10).

**Resolução passo a passo.**
1. **Fator 2:** $C_1 = \dfrac{s+0{,}16}{s+0{,}08}$ (polo = zero/fator). Fase no ponto desejado: $\angle(\square_d+0{,}16) - \angle(\square_d+0{,}08) = 123{,}2° - 124{,}6° = -1{,}43°$.
2. **Fator 10:** $C_2 = \dfrac{s+0{,}16}{s+0{,}016}$ → fase $= -2{,}55°$.
3. **Par afastado, fator 10:** $C_3 = \dfrac{s+0{,}8}{s+0{,}08}$.
4. **Simulação (base: $M_p = 10\,\%$):**

| Controlador | Fase do par | $M_p$ |
|---|---|---|
| sem atraso | — | 10 % |
| $C_1$ (fator 2) | −1,43° | 14 % |
| $C_2$ (fator 10) | −2,55° | 17 % |
| $C_3$ (fator 10, longe) | ≈ −14° | 40 % |

5. **Trade-off:** quanto maior o fator e mais afastado o par, **mais fase roubada** e mais overshoot; por outro lado, o erro converge **mais rápido**. Perto da origem: transitório preservado, erro lento. A melhor maneira de decidir é **simular** — e se o overshoot ficar demais, reprojetar o avanço com folga (§2.5.2).

### Exercício 2.4.3 — PI para 3ª ordem do tipo 0
*(teoria: §2.4.4–§2.4.6; âncora principal)*

**Enunciado.** $G(s) = \dfrac{20}{(s+1)(s+2)(s+10)}$ (tipo 0!), requisitos $M_p = 16{,}3\,\%$ e $e_{ss}(\text{degrau}) = 0$. Projete o PI e verifique as duas posições de zero: $-0{,}123$ e $-0{,}73$.

**Resolução passo a passo.**
1. **Erro nulo com planta tipo 0 ⇒ só o PI resolve** (sobe o tipo; o atraso comum só reduz o erro). "Só use PI se estritamente necessário" — aqui é o caso.
2. **Par desejado:** $M_p = 16{,}3\,\% \Rightarrow \zeta = 0{,}5$; escolhemos $\omega_n = 2{,}46$ (verificando que o LGR com o PI passa pela região) → $\square_d = -1{,}23 + 2{,}13j$; o 3º polo ficará em $-10{,}54$ (longe: dominância ✓).
3. **Ganho pelo módulo** (com o polo do PI na origem): $k = 2{,}19$.
4. **Zero do PI:** chute inicial $= |\mathrm{Re}(\square_d)|/10 = 0{,}123$ → $C(s) = 2{,}19\dfrac{s+0{,}123}{s}$.
5. **Simulação:**
   - **zero $-0{,}123$:** erro → 0 ✓, mas convergência **lenta** (polo de MF em $-0{,}088$; resposta praticamente sem overshoot, $t_s \approx 20$ s);
   - **zero $-0{,}73$:** $M_p = 16{,}4\,\%$ (projeto: 16,3 % ✓), $t_p = 1{,}77$ s, $t_s = 3{,}6$ s, erro → 0 ✓ — resposta muito melhor!
6. **Moral:** a regra do 1/10 é **chute inicial**, não dogma. O PI cobra seu preço no transitório — ajuste o zero simulando.

> ⚡ **Desafio (resolvido no Lab 08):** tente um PI **com zero em $-0{,}5$** para $G(s) = \dfrac{20}{(s-1)(s+2)(s+10)}$ — planta **instável**. Você não vai conseguir: prove por Routh que nenhum $k$ estabiliza ($-400k^2 + 1350k - 2160 < 0\ \forall k$). E com o zero em $-0{,}123$? Estabiliza ($1{,}22 < k < 4{,}44$), mas com overshoot de quase 200 % — nem toda planta tem solução com qualquer controlador, e estabilidade não é desempenho.

---

## Tópico 2.5 — Avanço + atraso, PID e atraso de transporte

### Exercício 2.5.1 — Projeto completo de avanço e atraso (duas iterações)
*(teoria: §2.5.1–§2.5.2; âncora principal)*

**Enunciado.** $G(s) = \dfrac{200}{s(s+10)(s+20)}$, requisitos $M_p = 16{,}3\,\%$, $t_r(0\text{–}100\,\%) = 300$ ms e $e_{ss}(\text{rampa}) = 0{,}02$. Projete o controlador de avanço e atraso.

**Resolução passo a passo (a receita de 10 passos).**
1. **Parâmetros:** $\zeta = 0{,}5$; $t_r = (\pi - \arccos 0{,}5)/\omega_d = 0{,}3 \Rightarrow \omega_d = 7$; $k_v = 1/0{,}02 = 50$.
2. **Polo desejado:** $\square_d = -4{,}04 + 7j$ ($\sigma = 0{,}5 \times 7/\sqrt{0{,}75} = 4{,}04$).
3. **Fase da planta:** $\angle G(\square_d) = -193{,}3°$ → precisa de avanço: $+13{,}3°$ (≤ 40° ✓).
4. **Avanço — zero cancela o polo $-10$** (nunca o da origem!): fase do zero $= 49{,}6°$ → fase do polo $= 36{,}3°$ → $b = 4{,}04 + \dfrac{7}{\mathrm{tg}(36{,}3°)} = 13{,}57$; ganho $k = 8{,}33$ → $C_{av} = 8{,}33\dfrac{s+10}{s+13{,}57}$.
5. **Atraso:** $k_v = 8{,}33 \times \dfrac{10}{13{,}57} = 6{,}14$ → fator $= 50/6{,}14 = 8{,}14$; zero $= 4{,}04/10 \approx 0{,}4$; polo $= 0{,}4/8{,}14 = 0{,}05$.
   $$C(s) = 8{,}33\,\frac{s+10}{s+13{,}57}\cdot\frac{s+0{,}4}{s+0{,}05} \;\Rightarrow\; \textbf{simulação: } M_p = 22\,\%\ ✗,\ t_r = 328\text{ ms}$$
   O atraso roubou fase e estragou o overshoot!
6. **2ª iteração — avanço com folga:** exigir $M_p \approx 12\,\%$ ($\zeta = 0{,}56$) e $t_r = 275$ ms → $\omega_d = 7{,}9$ → $\square_d = -5{,}34 + 7{,}87j$ → $\angle G = -211{,}8°$ → avanço $31{,}8°$ → mesmo cancelamento: $b = 20{,}4$, $k = 13{,}4$ → $k_v = 6{,}6$ (mantemos o mesmo atraso).
   $$C(s) = 13{,}4\,\frac{s+10}{s+20{,}4}\cdot\frac{s+0{,}4}{s+0{,}05} \;\Rightarrow\; \textbf{simulação final: } M_p = 16{,}9\,\%\ ✓,\ t_r = 300\text{ ms} ✓,\ k_v \approx 50 ✓$$
7. **Moral:** projeto envolve arte — o avanço da 2ª iteração absorve o efeito do atraso. Se fosse só conta, o computador faria tudo.

### Exercício 2.5.2 — Projeto de PID e o ajuste do zero do PI
*(teoria: §2.5.3; âncora principal)*

**Enunciado.** $G(s) = \dfrac{2}{(s+2)(s+5)}$, requisitos $M_p = 16{,}3\,\%$, $t_p = 400$ ms e $e_{ss}(\text{degrau}) = 0$. Projete o PID e obtenha $k_p$, $k_i$, $k_d$.

**Resolução passo a passo.**
1. $\zeta = 0{,}5$; $\omega_d = \pi/0{,}4 = 7{,}9$ → $\square_d = -4{,}6 + 7{,}9j$.
2. $\angle G(\square_d) = -195{,}3°$ → avanço (zero do PD): $+15{,}3°$.
3. **Zero do PD:** $\mathrm{tg}(15{,}3°) = \dfrac{7{,}9}{a - 4{,}6} \Rightarrow a = 33{,}4$.
4. **Ganho** (dois zeros, polo na origem; $A = 2$ — não esqueça do $A$!): $k = \dfrac{|\square_d|\cdot|\square_d+2|\cdot|\square_d+5|}{2 \times |\square_d+33{,}4| \times |\square_d+0{,}46|} = 1{,}1$.
5. **Zero do PI (erro nulo ⇒ polo na origem):** chute $0{,}46$:
   $$C(s) = 1{,}1\,\frac{(s+33{,}4)(s+0{,}46)}{s} = 1{,}1s + 37{,}25 + \frac{16{,}9}{s}$$
   $$\boxed{k_p = 37{,}25,\quad k_i = 16{,}9,\quad k_d = 1{,}1}$$
6. **Ajuste do zero do PI (simulação):**

| Zero do PI | $k_p$ | $k_i$ | Resultado |
|---|---|---|---|
| $-0{,}46$ | 37,25 | 16,9 | converge devagar |
| $-2$ | 38,9 | 73,5 | rápido, overshoot grande demais |
| $-1$ | 37,8 | 36,7 | **satisfatório** ✓ |

7. **PID real:** $C(s) = P + \dfrac{I}{s} + D\,\dfrac{N}{1+N/s}$ — o "D" tem polo de filtro: **PID implementado = PI-Lead**.

### Exercício 2.5.3 — Atraso de transporte: análise e projeto
*(teoria: §2.5.4–§2.5.5; âncora principal)*

**Enunciado.** $G(s) = \dfrac{2}{s(s+4)}$ com atraso de transporte $\tau = 0{,}1$ s. (a) Mostre que, com $k = 10$, o atraso eleva o overshoot de $\approx 21\,\%$ para $\approx 49\,\%$ (use Padé de 1ª ordem). (b) Projete um avanço para $t_r = 0{,}5$ s e $M_p = 15\,\%$ **compensando o atraso**.

**Resolução passo a passo.**
1. **Padé 1ª ordem:** $e^{-0{,}1s} \approx -\dfrac{s - 20}{s + 20}$ → $G_a(s) = \dfrac{2}{s(s+4)}\cdot\dfrac{-s+20}{s+20}$.
2. **Sem atraso, $k = 10$:** $T = \dfrac{20}{s^2+4s+20}$ → $\zeta = 0{,}447$ → $M_p = 20{,}8\,\%$.
3. **Com atraso, mesmo $k$:** $T_a = \dfrac{20(-s+20)}{s^3+24s^2+60s+400}$ → polos $-22{,}1$ e $-0{,}95 \pm 4{,}1j$ → $\zeta = 0{,}223$ → **$M_p = 48{,}7\,\%$** (simulação com atraso puro: 49,5 % — a diferença é da própria aproximação de Padé e do zero em $+20$).
4. **Projeto:** $\zeta = 0{,}517$; $t_r(0\text{–}100\,\%) = (\pi - \arccos\zeta)/\omega_d = 0{,}5 \Rightarrow \omega_d = 4{,}23$ → $\square_d = -2{,}6 + 4{,}2j$.
5. **Avanço sem atraso:** $\angle G(\square_d) = -193{,}4°$ → $13{,}4°$.
6. **Fase do atraso em $\square_d$** (duas contas, mesmo valor!):
   - exponencial: $\angle e^{-0{,}1\square_d} = -0{,}1 \times 4{,}2\ \text{rad} = -24{,}1°$;
   - Padé: $\angle(-\square_d+20) - \angle(\square_d+20) = -10{,}5° - 13{,}6° = -24{,}1°$ ✓.
7. **Avanço total:** $13{,}4° + 24{,}1° = 37{,}5°$ — **dentro dos 40°** ✓ (sem compensar o atraso, faltariam 24°!).
8. **Cancelamento do polo $-4$:** fase do zero $= 71{,}6°$ → fase do polo $= 34{,}1°$ → $b = 2{,}6 + \dfrac{4{,}2}{\mathrm{tg}(34{,}1°)} = 8{,}8$; ganho $k = 14{,}26$:
   $$C(s) = 14{,}26\,\frac{s+4}{s+8{,}8} \;\Rightarrow\; \textbf{simulação com atraso: } M_p = 14{,}3\,\%\ ✓,\ t_r = 0{,}5\text{ s} ✓$$
9. **Discussão:** esse $t_r$ vale com o atraso na **realimentação**. Se o atraso estiver **entre a entrada e a saída medida**, o tempo de subida medido será $0{,}5 + 0{,}1 = 0{,}6$ s — e projetaríamos para $t_r = 0{,}4$ s. O overshoot, porém, **não depende da posição do atraso na malha** (verifique no Lab 09!).

---

> **Conferência numérica:** todos os $M_p$, $t_p$, $t_r$, $t_s$ e polos citados foram obtidos por simulação com `python-control` 0.10.2 (mesmos scripts dos Labs 05–09). Pequenas diferenças na 2ª casa decimal em relação às contas de quadro são esperadas (arredondamentos de projeto).
