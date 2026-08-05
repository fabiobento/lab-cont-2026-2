# Módulo 03 — Exercícios Resolvidos

> Material do aluno. Cada exercício indica a seção da **teoria** (`teoria_modulo3.md`) onde o conteúdo pode ser consultado. Todos os valores numéricos de margens e de respostas ao degrau foram conferidos por simulação (python-control 0.10.2). Convenções do curso: ângulos em graus, módulo em dB ($20\log_{10}|G|$), fase assintótica por retas de $\omega_q/5$ a $5\omega_q$, $\mathrm{PM} \approx 100\,\zeta$.

---

## Tópico 3.1 — Resposta em frequência e diagrama de Bode

### Exercício 3.1.1 — A saída em regime é uma senoide
*(teoria: §3.1.3; âncora principal)*

**Enunciado.** Seja $G(s) = \dfrac{8}{s+4}$ com entrada $u(t) = 2\,\mathrm{sen}(3t)$. Determine a saída em regime permanente $y_{rp}(t)$ e estime depois de quanto tempo ela é atingida.

**Resolução passo a passo.**
1. **Teorema da resposta em frequência:** em regime, $y_{rp}(t) = A\,|G(j\omega)|\,\mathrm{sen}\big(\omega t + \angle G(j\omega)\big)$, com $A = 2$ e $\omega = 3$ rad/s.
2. **Módulo:** $|G(j3)| = \dfrac{8}{\sqrt{3^2 + 4^2}} = \dfrac{8}{5} = 1{,}6$.
3. **Fase:** $\angle G(j3) = -\mathrm{arctg}(3/4) = -36{,}9°$.
4. **Saída em regime:**
$$y_{rp}(t) = 2 \times 1{,}6\,\mathrm{sen}(3t - 36{,}9°) = 3{,}2\,\mathrm{sen}(3t - 36{,}9°)$$
5. **Quando vale?** A constante de tempo é $\tau = 1/4 = 0{,}25$ s → o transitório morre em $\approx 4\tau = 1$ s. A expressão acima só descreve a saída **depois disso**.
6. Compare com a figura `m3_fig01_resposta_frequencia.png` na teoria — mesma ideia, com o circuito RC.

### Exercício 3.1.2 — Esboço assintótico de Bode (dois polos reais)
*(teoria: §3.1.6–§3.1.7; âncora principal)*

**Enunciado.** Esboce o diagrama de Bode assintótico (módulo e fase) de $G(s) = \dfrac{40}{(s+2)(s+40)}$ e calcule o erro da aproximação nas frequências de quebra.

**Resolução passo a passo.**
1. **Forma de Bode:** $G(s) = \dfrac{40/80}{(s/2+1)(s/40+1)} = \dfrac{0{,}5}{(s/2+1)(s/40+1)}$ → ganho de Bode $K_B = 0{,}5$ → **patamar de $-6{,}02$ dB**. Quebras: $\omega_{q1} = 2$ e $\omega_{q2} = 40$ rad/s.
2. **Módulo assintótico:** $-6{,}02$ dB até $\omega = 2$; declive $-20$ dB/déc de $2$ a $40$; declive $-40$ dB/déc depois de $40$.
3. **Fase assintótica (retas de $\omega_q/5$ a $5\omega_q$):** polo em $2$ → reta de $0{,}4$ a $10$; polo em $40$ → reta de $8$ a $200$.

| Trecho | Contribuições ativas | Declive |
|---|---|---|
| $\omega < 0{,}4$ | nenhuma | $0°$ |
| $0{,}4 < \omega < 8$ | polo 2 ($-45°$/déc) | $-45°$/déc |
| $8 < \omega < 10$ | **os dois polos** | $-90°$/déc |
| $10 < \omega < 200$ | polo 40 ($-45°$/déc) | $-45°$/déc |
| $\omega > 200$ | nenhuma | $-180°$ (final) |

4. **Erro na quebra (módulo):** em $\omega = 2$: exato $|G| = \dfrac{40}{\sqrt{8}\,\sqrt{1604}} = 0{,}353 \to -9{,}04$ dB; assintótico $-6{,}02$ dB → **erro de $-3$ dB** ✓ (como manda a regra). Em $\omega = 40$: exato $-35{,}06$ dB; assintótico $-6{,}02 - 20\log_{10}(20) = -32{,}04$ dB → **erro de $-3$ dB** ✓.
5. **Erro na fase:** em $\omega = 40$ o exato é $-\mathrm{arctg}(20) - \mathrm{arctg}(1) = -87{,}1° - 45° = -132{,}1°$; o assintótico dá $-90° - 45°\log_{10}(40/8) = -90° - 31{,}5° = -121{,}5°$ → erro de $\approx 11°$, justamente o **erro máximo da convenção** (nas extremidades das retas, $\omega_q/5$ e $5\omega_q$). Para projeto, isso é irrelevante — e é por isso que o curso adota essa convenção.
6. Compare com as figuras `m3_fig02_bode_1a_ordem.png` (erro de 3 dB e convenção de fase) e `m3_fig03_bode_2a_polos_reais.png` (soma de contribuições).

### Exercício 3.1.3 — Margens de ganho e de fase na mão
*(teoria: §3.1.8; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{4}{s(s+2)(s+4)}$: (a) determine $\omega_c$, PM, $\omega_f$ e GM; (b) diga até que ganho extra $K$ a malha fechada permanece estável; (c) recalcule a PM para $K = 4$ e comente.

**Resolução passo a passo.**
1. **Cruzamento de ganho:** $|G(j\omega_c)| = \dfrac{4}{\omega_c\sqrt{\omega_c^2+4}\,\sqrt{\omega_c^2+16}} = 1$. Testando $\omega = 0{,}5$: $|G| = 4/(0{,}5 \times 2{,}062 \times 4{,}031) = 0{,}962 < 1$ → $\omega_c$ um pouco menor: **$\omega_c \approx 0{,}483$ rad/s** (confirmação numérica).
2. **PM:** $\angle G(j\omega_c) = -90° - \mathrm{arctg}(0{,}483/2) - \mathrm{arctg}(0{,}483/4) = -90° - 13{,}6° - 6{,}9° = -110{,}4°$ → $\boxed{\mathrm{PM} = 69{,}6°}$.
3. **Cruzamento de fase:** $-90° - \mathrm{arctg}(\omega_f/2) - \mathrm{arctg}(\omega_f/4) = -180°$ → os dois arctg somam $90°$ → $\omega_f = \sqrt{2 \times 4} = \sqrt{8} = 2{,}83$ rad/s.
4. **GM:** $|G(j\omega_f)| = \dfrac{4}{2{,}83 \times \sqrt{12} \times \sqrt{24}} = \dfrac{4}{48} = 0{,}0833$ → $\boxed{\mathrm{GM} = 21{,}6\ \mathrm{dB}}$, ou seja, fator $12$: **estável para $0 < K < 12$**.
5. **Conferência por Routh:** característico $s^3 + 6s^2 + 8s + 4K$ → linha $s^1$: $(48 - 4K)/6 > 0 \Rightarrow K < 12$ ✓ — as duas ferramentas concordam, como sempre devem.
6. **Com $K = 4$:** novo $\omega_c$: $|4G| = 1$ → $\omega_c = 1{,}5$ rad/s ($|G(j1{,}5)| = 4/(1{,}5 \times 2{,}5 \times 4{,}27) = 0{,}25$ ✓). $\angle G = -90° - 36{,}9° - 20{,}6° = -147{,}4°$ → **PM $= 32{,}6°$**. A GM cai para $21{,}6 - 12 = 9{,}6$ dB.
7. **Comentário:** PM $69{,}6° \Rightarrow \zeta \approx 0{,}7$ → resposta mansa (simulação: $M_p = 0{,}7\,\%$ — a fórmula superestima por causa do 3º polo). Com $K = 4$, PM $32{,}6° \Rightarrow \zeta \approx 0{,}33$: bem mais oscilatório. Ganho "de graça" não existe.
8. Compare com a figura `m3_fig05_margens_bode.png` na teoria (mesma leitura, outra planta).

### Exercício 3.1.4 — Projeto de controlador P pela PM
*(teoria: §3.1.10; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{5}{s(s+5)}$, projete $C(s) = K$ para $M_p \leq 25\,\%$ na malha fechada. Verifique por simulação.

**Resolução passo a passo.**
1. **Requisito → PM:** $M_p \leq 25\,\% \Rightarrow \zeta \geq 0{,}4 \Rightarrow \mathrm{PM} \approx 100\,\zeta \geq 40°$. Projeta-se com folga: **PM alvo $= 45°$**.
2. **Onde a fase vale $-135°$?** $\angle G = -90° - \mathrm{arctg}(\omega/5) = -135° \Rightarrow \omega = 5$ rad/s — será a nova $\omega_c$.
3. **Quanto de ganho falta?** $|G(j5)| = \dfrac{5}{5\sqrt{50}} = 0{,}1414$ → $K = 1/0{,}1414 = \sqrt{50} = 7{,}07$ (isto é, $+17$ dB).
4. **Verificação:** malha fechada $T(s) = \dfrac{35{,}4}{s^2 + 5s + 35{,}4}$: $\omega_n = 5{,}95$, $\zeta = 5/(2 \times 5{,}95) = 0{,}42$ → $M_p$ previsto $\approx 23\,\%$ ✓.
5. **Simulação:** $M_p = 23{,}3\,\%$ ✓ (previsto 20–23 % pela trilha PM → $\zeta$ → $M_p$).
6. **Observação importante:** o ganho **move a curva de módulo inteira** para cima/para baixo sem tocar na fase — por isso o projeto de P pela PM é sempre "achar onde a fase dá a PM desejada e empurrar o módulo até lá". Compare com `m3_fig07_projeto_P_pm.png`.

---

## Tópico 3.2 — Carta de Nichols-Black e especificação na frequência

### Exercício 3.2.1 — Pico de ressonância analítico
*(teoria: §3.2.1–§3.2.2; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{25}{s^2 + 2s + 25}$, calcule $\omega_r$ e $M_r$ (em vezes e em dB) e confira o valor exato de $|G(j\omega_r)|$.

**Resolução passo a passo.**
1. **Parâmetros:** $\omega_n = \sqrt{25} = 5$ rad/s; $2\zeta\omega_n = 2 \Rightarrow \zeta = 0{,}2$.
2. **Existe ressonância?** $\zeta = 0{,}2 < 1/\sqrt{2} = 0{,}707$ ✓ → sim.
3. **Frequência de ressonância:** $\omega_r = \omega_n\sqrt{1 - 2\zeta^2} = 5\sqrt{1 - 0{,}08} = 5 \times 0{,}959 = 4{,}80$ rad/s.
4. **Pico:** $M_r = \dfrac{1}{2\zeta\sqrt{1-\zeta^2}} = \dfrac{1}{2 \times 0{,}2 \times \sqrt{0{,}96}} = \dfrac{1}{0{,}392} = 2{,}55$ → $20\log_{10}(2{,}55) = 8{,}1$ dB.
5. **Conferência direta:** $|G(j4{,}8)| = \dfrac{25}{\sqrt{(25 - 4{,}8^2)^2 + (2 \times 4{,}8)^2}} = \dfrac{25}{\sqrt{3{,}84 + 92{,}16}} = \dfrac{25}{9{,}8} = 2{,}55$ ✓.
6. **Significado:** uma senoide de $\approx 4{,}8$ rad/s é **amplificada 2,55 vezes** — o sistema "grita" perto de $\omega_n$. Compare com `m3_fig08_bode_subamortecido.png`.

### Exercício 3.2.2 — Lendo a malha fechada ponto a ponto
*(teoria: §3.2.3–§3.2.4; âncora principal)*

**Enunciado.** Num certo $\omega_1$, a malha aberta vale $G(j\omega_1) = 2\angle{-120°}$. Determine $|T(j\omega_1)|$ (vezes e dB) e $\angle T(j\omega_1)$ da malha fechada unitária, sem usar a carta.

**Resolução passo a passo.**
1. **Relação fundamental:** $T = \dfrac{G}{1+G}$ → basta calcular $1 + G$ em notação fasorial.
2. $G = 2\big(\cos(-120°) + j\,\mathrm{sen}(-120°)\big) = 2(-0{,}5 - 0{,}866j) = -1 - 1{,}732j$.
3. $1 + G = -1{,}732j$ → $|1+G| = 1{,}732$ e $\angle(1+G) = -90°$.
4. $|T| = \dfrac{|G|}{|1+G|} = \dfrac{2}{1{,}732} = 1{,}155$ → $20\log_{10}(1{,}155) = 1{,}25$ dB.
5. $\angle T = \angle G - \angle(1+G) = -120° - (-90°) = -30°$.
6. **O que a carta faria por você:** o ponto $(-120°,\ 6{,}02\ \mathrm{dB})$ cai aproximadamente sobre a curva de módulo constante $1{,}25$ dB e a curva de fase constante $-30°$ da carta de Nichols-Black — a carta nada mais é do que essa conta resolvida para **todos** os pontos de uma vez.
7. **Observação:** $|T| > 1$ em malha aberta com $|G| = 2$: a malha fechada **amplifica** mais do que a malha aberta nessa frequência — sintoma de proximidade do ponto crítico.

### Exercício 3.2.3 — De $M_r$ para $M_p$: a ponte frequência–tempo
*(teoria: §3.2.2 e §3.2.6; âncora principal)*

**Enunciado.** A resposta em frequência de malha fechada de um sistema apresenta pico de ressonância $M_r = 6$ dB. Estime o overshoot da resposta ao degrau.

**Resolução passo a passo.**
1. $M_r = 6$ dB → em vezes: $M_r = 10^{6/20} = 2{,}0$.
2. **Invertendo a fórmula do pico:** $2\zeta\sqrt{1-\zeta^2} = 1/M_r = 0{,}5$ → $4\zeta^2(1-\zeta^2) = 0{,}25$. Com $x = \zeta^2$: $x^2 - x + 0{,}0625 = 0$ → $x = \dfrac{1 - \sqrt{0{,}75}}{2} = 0{,}067$ (a raiz $0{,}933$ daria $\zeta > 0{,}707$, sem ressonância — descartada).
3. $\zeta = \sqrt{0{,}067} = 0{,}259$.
4. **Overshoot:** $M_p = e^{-\zeta\pi/\sqrt{1-\zeta^2}} = e^{-0{,}259\pi/0{,}966} = e^{-0{,}842} \approx 43\,\%$.
5. **Moral:** mediu-se o pico no analisador de espectro (6 dB) → sabe-se que o degrau vai ultrapassar $\approx 43\,\%$. A trilha $M_r \to \zeta \to M_p$ (e sua irmã $\mathrm{PM} \approx 100\zeta$) é o que torna o projeto na frequência útil para especificações no tempo.
6. Compare com `m3_fig11_nb_mr_wc.png` (leitura de $M_r$ na carta + resposta ao degrau).

### Exercício 3.2.4 — Projeto de ganho na carta de Nichols-Black
*(teoria: §3.2.5; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{8}{s(s+2)(s+4)}$, use a carta de Nichols-Black para ajustar $K$ de modo que a malha fechada tenha $M_p \leq 25\,\%$. Verifique por simulação.

**Resolução passo a passo.**
1. **Requisito → PM:** $M_p \leq 25\,\% \Rightarrow \zeta \geq 0{,}4$; com folga: **PM alvo $= 45°$**.
2. **Onde a fase vale $-180° + 45° = -135°$?** $-90° - \mathrm{arctg}(\omega/2) - \mathrm{arctg}(\omega/4) = -135°$ → $\mathrm{arctg}(\omega/2) + \mathrm{arctg}(\omega/4) = 45°$. Tentando $\omega = 1{,}12$: $29{,}3° + 15{,}7° = 45{,}0°$ ✓ → nova $\omega_c = 1{,}12$ rad/s.
3. **Translação vertical necessária:** $|G(j1{,}12)| = \dfrac{8}{1{,}12 \times \sqrt{5{,}26} \times \sqrt{17{,}26}} = \dfrac{8}{10{,}7} = 0{,}748$ → $-2{,}5$ dB. Na carta, o ponto $(-135°,\ -2{,}5\ \mathrm{dB})$ precisa subir até 0 dB: **ganho de $+2{,}5$ dB** → $K = 10^{2{,}5/20} = 1{,}34$.
4. **Interpretação gráfica:** ajuste de ganho = **translação vertical da curva inteira** na carta; o projeto é "deslizar a curva até ela cruzar 0 dB exatamente na coluna $-135°$".
5. **Verificação:** $T(s) = \dfrac{10{,}7}{s^3 + 6s^2 + 8s + 10{,}7}$; simulação: $M_p = 23{,}8\,\%$ ✓, $t_r = 1{,}68$ s.
6. **Por que não cravar $M_p = 25\,\%$?** A trilha PM $\approx 100\zeta$ → $M_p$ é aproximada (vale para 2ª ordem pura); o 3º polo e o zero implícito da malha deslocam um pouco o resultado. Projete sempre com folga e **confirme por simulação**.

---

## Tópico 3.3 — Critério de Nyquist e atraso de transporte

### Exercício 3.3.1 — Esboço do gráfico polar
*(teoria: §3.3.1; âncora principal)*

**Enunciado.** Esboce o gráfico polar de $G(s) = \dfrac{5}{(s+1)(s+5)}$ calculando pontos em $\omega = 0$, $1$, $5$ e $\omega \to \infty$.

**Resolução passo a passo.**
1. **$\omega = 0$:** $G(0) = 5/5 = 1\angle 0°$ → ponto $(1,\ 0)$ — a curva **começa no eixo real positivo** (sistema tipo 0).
2. **$\omega = 1$:** $|G| = \dfrac{5}{\sqrt{2}\,\sqrt{26}} = 0{,}693$; $\angle G = -\mathrm{arctg}(1) - \mathrm{arctg}(0{,}2) = -45° - 11{,}3° = -56{,}3°$.
3. **$\omega = 5$:** $|G| = \dfrac{5}{\sqrt{26}\,\sqrt{50}} = 0{,}186$; $\angle G = -\mathrm{arctg}(5) - \mathrm{arctg}(1) = -78{,}7° - 45° = -123{,}7°$.
4. **$\omega \to \infty$:** $|G| \to 0$; $\angle G \to -180°$ (dois polos: $-90°$ cada) → a curva **chega à origem tangenciando o eixo real negativo**.
5. **Esboço:** sai de $(1,0)$, mergulha no 4º quadrante, cruza para o 3º e morre na origem "deitada" sobre o eixo real negativo. O ramo de $\omega < 0$ é o **espelho** em relação ao eixo real.
6. **Ligação com Bode:** é a mesma informação, outra embalagem — cada ponto do polar é um ponto (módulo, fase) do Bode. Compare com `m3_fig15_polar.png`.

### Exercício 3.3.2 — Nyquist: faixa de estabilidade em K
*(teoria: §3.3.4–§3.3.5; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{K}{s(s+1)(s+4)}$ em malha fechada unitária, use o critério de Nyquist para determinar a faixa de $K$ estável. Confira por Routh.

**Resolução passo a passo.**
1. **Polos de malha aberta:** $0$, $-1$, $-4$ → **$P = 0$** no SPD (o polo na origem é contornado pela indentação — §3.3.4). Estabilidade exige $Z = N + P = 0$ → **$N = 0$**: o contorno não pode circular o ponto $-1$.
2. **Cruzamento com o eixo real:** $\angle G = -180°$ quando $-90° - \mathrm{arctg}(\omega) - \mathrm{arctg}(\omega/4) = -180°$ → $\mathrm{arctg}(\omega) + \mathrm{arctg}(\omega/4) = 90°$ → $\omega = \sqrt{1 \times 4} = 2$ rad/s.
3. **Onde cruza:** $|G(j2)| = \dfrac{K}{2\sqrt{5}\,\sqrt{20}} = \dfrac{K}{20}$ → cruzamento em $-K/20$.
4. **Condição:** $-K/20 > -1$ (cruzamento à **direita** de $-1$) → $\boxed{0 < K < 20}$. Com $K = 20$, a curva passa exatamente por $-1$ (polos sobre o eixo $j\omega$ — marginalmente estável); com $K > 20$, duas voltas horárias → 2 polos instáveis.
5. **Routh confere:** característico $s^3 + 5s^2 + 4s + K$ → linha $s^1$: $(20 - K)/5 > 0$ → $K < 20$ ✓. Auxiliar: $5s^2 + 20 = 0$ → $s = \pm 2j$ — exatamente a frequência do cruzamento ✓.
6. **GM:** $20\log_{10}(20/K)$ — para $K = 1$: GM $= 26$ dB. Compare com `m3_fig19_nyquist_estabilidade.png`.

### Exercício 3.3.3 — O atraso rouba margem de fase
*(teoria: §3.3.7–§3.3.8; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{2}{s(s+2)}\,e^{-0{,}4s}$: (a) calcule a PM sem considerar o atraso; (b) calcule a PM com o atraso; (c) estime o efeito no overshoot e verifique por simulação.

**Resolução passo a passo.**
1. **$\omega_c$ (o atraso não muda o módulo!):** $|G| = \dfrac{2}{\omega\sqrt{\omega^2+4}} = 1$ → $\omega^2(\omega^2 + 4) = 4$ → com $x = \omega^2$: $x^2 + 4x - 4 = 0$ → $x = -2 + \sqrt{8} = 0{,}828$ → $\omega_c = 0{,}910$ rad/s.
2. **PM sem atraso:** $\angle G = -90° - \mathrm{arctg}(0{,}910/2) = -90° - 24{,}5° = -114{,}5°$ → PM $= 65{,}5°$.
3. **Perda de fase do atraso:** $\Delta\phi = -\delta\omega_c = -0{,}4 \times 0{,}910 = -0{,}364$ rad $= -20{,}9°$ → **PM $= 65{,}5° - 20{,}9° = 44{,}6°$**.
4. **Estimativa no tempo:** sem atraso: $\zeta \approx 0{,}66$ → $M_p \approx 6\,\%$; com atraso: $\zeta \approx 0{,}45$ → $M_p \approx 21\,\%$.
5. **Simulação (atraso via Padé de ordem 8):** sem atraso: $M_p = 4{,}3\,\%$, $t_r = 2{,}36$ s; com atraso: $M_p = 25{,}1\,\%$, $t_r = 2{,}05$ s — a previsão da PM capturou a **degradação** (a simulação é um pouco pior que a estimativa porque o Padé adiciona dinâmica própria).
6. **Na carta e no Nyquist:** o atraso **afunda a fase** sem tocar o módulo → na carta a curva desliza para a esquerda; no Nyquist ela **espirala** em torno da origem (cruza o eixo real infinitas vezes). Compare com `m3_fig21_atraso_bode.png` e `m3_fig22_atraso_nyquist.png`.
7. **Regra prática:** quanto maior $\omega_c$, mais o mesmo atraso $\delta$ custa ($\delta\omega_c$). Sistemas rápidos sofrem mais com atraso — é por isso que controladores digitais (que inserem $\approx T_s/2$ de atraso médio) limitam a banda de malha.

---

## Tópico 3.4 — Projeto de compensadores de avanço e de atraso na frequência

### Exercício 3.4.1 — As três fórmulas do avanço
*(teoria: §3.4.3–§3.4.4; âncora principal)*

**Enunciado.** Projete a **forma** de um compensador de avanço $C(s) = K\dfrac{Ts+1}{\alpha Ts+1}$ que forneça $\phi_{máx} = 30°$ exatamente em $\omega_c = 10$ rad/s. Calcule $\alpha$, $T$, a posição de zero e polo e o ganho do compensador em $\omega_{máx}$.

**Resolução passo a passo.**
1. **Fase máxima → $\alpha$:** $\mathrm{sen}\,\phi_{máx} = \dfrac{1-\alpha}{1+\alpha}$ → $\alpha = \dfrac{1 - \mathrm{sen}\,30°}{1 + \mathrm{sen}\,30°} = \dfrac{0{,}5}{1{,}5} = \dfrac{1}{3}$.
2. **Posicionar o pico em $\omega_c$:** $\omega_{máx} = \dfrac{1}{T\sqrt{\alpha}} = 10$ → $T = \dfrac{1}{10\sqrt{1/3}} = \dfrac{1}{5{,}774} = 0{,}173$ s.
3. **Zero e polo:** zero em $-1/T = -5{,}77$; polo em $-1/(\alpha T) = -17{,}3$ — o polo fica $1/\alpha = 3$ vezes mais longe que o zero (a "receita geométrica": $\omega_{máx} = \sqrt{5{,}77 \times 17{,}3} = 10$ ✓, média geométrica).
4. **Ganho do compensador em $\omega_{máx}$:** $10\log_{10}(1/\alpha) = 10\log_{10}3 = 4{,}77$ dB **de alta** — é o preço a pagar: o avanço levanta o módulo onde levanta a fase.
5. **E o $K$?** Depende da planta: $K\big|_{\mathrm{dB}} = 10\log_{10}\alpha - |G(j\omega_c)|_{\mathrm{dB}}$ — o compensador (forma + ganho) deve fazer $|CG(j\omega_c)| = 0$ dB. Sem a planta não há $K$: este exercício cobriu a **forma**; o próximo cobre o conjunto.
6. Compare com `m3_fig26_efeito_par_bode.png` e `m3_fig27_avanco_formulas.png`.

### Exercício 3.4.2 — Projeto completo de avanço de fase
*(teoria: §3.4.5; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{4}{s(s+2)}$, projete um compensador de avanço para $M_p \leq 25\,\%$ e $t_r \leq 0{,}5$ s. Verifique por simulação.

**Resolução passo a passo.**
1. **Requisitos → frequência:** $M_p \leq 25\,\% \Rightarrow \mathrm{PM} \geq 40°$; com folga de $5$–$10°$: **PM alvo $= 50°$**. Velocidade: $t_r \approx 1{,}8/\omega_c \leq 0{,}5$ → $\omega_c \geq 3{,}6$ → **$\omega_c$ alvo $= 4$ rad/s**.
2. **Situação atual em $\omega_c = 4$:** $|G(j4)| = \dfrac{4}{4\sqrt{20}} = 0{,}2236$ ($-13{,}0$ dB); $\angle G = -90° - \mathrm{arctg}(2) = -153{,}4°$ → **PM atual $= 26{,}6°$** (com ganho ajustado para cruzar em 4).
3. **Fase a avançar:** $\phi = 50° - 26{,}6° = 23{,}4°$ (a folga já está embutida na PM alvo — não some folga duas vezes).
4. **Forma:** $\alpha = \dfrac{1 - \mathrm{sen}\,23{,}4°}{1 + \mathrm{sen}\,23{,}4°} = \dfrac{0{,}603}{1{,}397} = 0{,}431$; $T = \dfrac{1}{4\sqrt{0{,}431}} = \dfrac{1}{4 \times 0{,}657} = 0{,}381$ s; $\alpha T = 0{,}164$ s. Zero em $-2{,}62$, polo em $-6{,}09$.
5. **Ganho:** $K = \dfrac{\sqrt{\alpha}}{|G(j4)|} = \dfrac{0{,}657}{0{,}2236} = 2{,}94$.
$$\boxed{C(s) = 2{,}94\,\dfrac{0{,}381s+1}{0{,}164s+1}}$$
6. **Conferência de projeto:** PM compensada em $\omega_c = 4$: exatamente $50{,}0°$ ✓ (a construção garante isso por simetria).
7. **Simulação:** $M_p = 19{,}1\,\%$ ✓ ($\leq 25\,\%$), $t_r = 0{,}46$ s ✓ ($\leq 0{,}5$ s) — com margem nos dois requisitos, porque a PM alvo tinha folga.
8. **Previsão vs. simulação:** PM $= 50° \Rightarrow \zeta \approx 0{,}5 \Rightarrow M_p \approx 16\,\%$; simulado $19{,}1\,\%$ — a diferença é o efeito do zero do compensador na malha fechada (§2.1.9: zeros aumentam overshoot). Normal e esperado.
9. Compare com `m3_fig28_projeto_avanco.png`.

### Exercício 3.4.3 — Projeto de atraso de fase: matando o erro estacionário
*(teoria: §3.4.6; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{8}{(s+1)(s+4)}$ em malha fechada unitária, o erro ao degrau é $e_{ss} = 33\,\%$ — inaceitável. Projete um compensador de atraso para $e_{ss} \leq 10\,\%$ **sem estragar a dinâmica**. Verifique por simulação.

**Resolução passo a passo.**
1. **Erro atual:** $G(0) = 8/4 = 2$ → $k_p = 2$ → $e_{ss} = 1/(1+2) = 33{,}3\,\%$.
2. **Quanto falta:** $e_{ss} \leq 0{,}1$ → $k_{pc} \geq 9$. Com folga (projeta-se para $e_{ss} = 1/12 = 8{,}3\,\%$): $k_{pc} = 11$ → o compensador precisa multiplicar o ganho DC por $\dfrac{z}{p} = \dfrac{11}{2} = 5{,}5$.
3. **Dinâmica atual:** $\omega_c$: $|G(j\omega)| = \dfrac{8}{\sqrt{\omega^2+1}\,\sqrt{\omega^2+16}} = 1$ → $\omega_c = 1{,}57$ rad/s ($\sqrt{3{,}47}\times\sqrt{18{,}47} = 1{,}862 \times 4{,}298 = 8{,}0$ ✓). PM atual $= 180° - \mathrm{arctg}(1{,}57) - \mathrm{arctg}(0{,}39) = 180° - 57{,}5° - 21{,}4° = 101°$ — **sobrando**: o atraso vai "gastar" uns $5°$ disso.
4. **Posicionamento:** polo em $p = -\omega_c/10 = -0{,}157$; zero em $z = -5{,}5 \times 0{,}157 = -0{,}864$.
$$\boxed{C(s) = \dfrac{s+0{,}864}{s+0{,}157}}$$
   Em $\omega_c = 1{,}57$ (uma década acima do zero), o par contribui $\approx +5{,}7° - 5{,}7° \approx 0°$ de fase e $\approx 0$ dB de módulo: **a dinâmica não sente o compensador** — mas o ganho DC foi multiplicado por $5{,}5$.
5. **Simulação:** sem $C$: $e_{ss} = 33{,}3\,\%$, $M_p = 3{,}8\,\%$, $t_r = 0{,}99$ s; com $C$: $e_{ss} = 8{,}3\,\%$ ✓, $M_p = 1{,}4\,\%$, $t_r = 1{,}29$ s — erro no alvo e dinâmica praticamente preservada.
6. **O mecanismo:** o atraso é um "PI com o pole quase em cima do zero": em alta frequência o par se cancela; em DC vale $z/p$. Compare com `m3_fig29_projeto_atraso.png` e a figura `m3_fig25_efeito_polo_bode.png`.

---

## Tópico 3.5 — PD, PI e PID na frequência

### Exercício 3.5.1 — PD pelas fórmulas diretas
*(teoria: §3.5.1; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{1}{s(s+4)}$, projete um PD (com polo de filtragem) para PM $= 60°$ em $\omega_c = 4$ rad/s. Verifique por simulação.

**Resolução passo a passo.**
1. **Planta em $\omega_c = 4$:** $|G(j4)| = \dfrac{1}{4\sqrt{32}} = 0{,}0442$; $\angle G = -90° - \mathrm{arctg}(1) = -135°$ → PM atual (com ganho) $= 45°$.
2. **Fase a avançar:** $\phi = 60° - 45° = 15°$.
3. **Fórmulas diretas do PD** (o PD ideal $k_p + k_d s$ tem fase $+\phi$ e módulo $1/|G|$ em $\omega_c$):
$$k_p = \dfrac{\cos\phi}{|G(j\omega_c)|} = \dfrac{0{,}966}{0{,}0442} = 21{,}9; \qquad k_d = \dfrac{\mathrm{sen}\,\phi}{\omega_c\,|G(j\omega_c)|} = \dfrac{0{,}259}{4 \times 0{,}0442} = 1{,}46$$
4. **Polo de filtragem** (o PD puro é impróprio — $k_d s$ explode em alta frequência): coloca-se um polo em $-100\,\omega_c = -400$, que custa só $-0{,}6°$ de fase em $\omega_c$:
$$\boxed{C(s) = \dfrac{21{,}9 + 1{,}46\,s}{s/400 + 1}}$$
5. **Conferência:** PM compensada real: $59{,}4°$ (os $-0{,}6°$ do polo de filtragem) ✓.
6. **Simulação:** $M_p = 11{,}4\,\%$, $t_r = 0{,}50$ s — PM $= 60° \Rightarrow \zeta \approx 0{,}6 \Rightarrow M_p \approx 9{,}5\,\%$; o zero do PD empurra um pouco para cima, como sempre.
7. **Conexão com o plano-s:** é o mesmo PD do Módulo 02, mas obtido **sem LGR**: duas fórmulas e pronto. Compare com `m3_fig32_pd_bode.png`.

### Exercício 3.5.2 — PI: erro zero, cauda lenta
*(teoria: §3.5.2; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{12}{(s+1)(s+6)}$ em malha fechada unitária: (a) calcule $e_{ss}$ e a PM atuais; (b) projete um PI que zere $e_{ss}$ preservando a dinâmica; (c) verifique por simulação e comente a "cauda lenta".

**Resolução passo a passo.**
1. **Erro atual:** $G(0) = 12/6 = 2$ → $e_{ss} = 1/(1+2) = 33{,}3\,\%$.
2. **Dinâmica atual:** $\omega_c = 1{,}65$ rad/s ($|G(j1{,}65)| = \dfrac{12}{\sqrt{3{,}72}\,\sqrt{38{,}2}} = \dfrac{12}{11{,}9} \approx 1{,}01$); PM $= 180° - \mathrm{arctg}(1{,}65) - \mathrm{arctg}(0{,}275) = 180° - 58{,}8° - 15{,}4° = 105{,}8°$ — folgadíssima.
3. **Projeto do PI** (§3.5.2: PI = atraso com o polo **em** $0$; zero uma década abaixo de $\omega_c$):
$$\boxed{C(s) = \dfrac{s + 0{,}165}{s}}$$
   Em $\omega_c = 1{,}65$: fase do PI $= \mathrm{arctg}(1{,}65/0{,}165) - 90° = 84{,}3° - 90° = -5{,}7°$ → PM cai para $\approx 100°$ (aceitável) e a malha vira **tipo 1** → $e_{ss} = 0$.
4. **Simulação:** sem PI: $e_{ss} = 33{,}3\,\%$, $M_p = 1{,}0\,\%$; com PI: $M_p = 0\,\%$, $y(30\ \mathrm{s}) = 0{,}99$ — erro a caminho de zero ✓, **mas** a resposta demora $10$ s para atingir $0{,}9$: a **cauda lenta do integrador**.
5. **Comentário didático:** o PI troca "erro de 33 % para sempre" por "erro que morre devagar". O par polo-no-zero/zero-perto-dele cria um modo lento ($\approx e^{-0{,}16t}$) que arrasta a convergência final — mesmo com PM de $100°$. Quem define a velocidade inicial continua sendo $\omega_c$; quem define a "rampa final" é o zero do PI.
6. Compare com `m3_fig34_pi_bode.png`.

### Exercício 3.5.3 — PID completo: PD para a dinâmica, PI para o erro
*(teoria: §3.5.3–§3.5.4; âncora principal)*

**Enunciado.** Para $G(s) = \dfrac{0{,}02}{(s+0{,}1)(s+0{,}2)}$, projete um PID (PD com polo de filtragem × PI) para $M_p \leq 20\,\%$, $t_r \leq 5$ s e $e_{ss} = 0$ ao degrau. Verifique por simulação.

**Resolução passo a passo.**
1. **Requisitos → frequência:** $M_p \leq 20\,\% \Rightarrow \zeta \geq 0{,}46 \Rightarrow \mathrm{PM} \geq 46°$; folga de $\approx 10°$ para a fase da PI e o polo de filtragem: **PM alvo $= 60°$**. Velocidade: $t_r \approx 1{,}8/\omega_c \leq 5$ → $\omega_c \geq 0{,}36$; com folga: **$\omega_c = 0{,}46$ rad/s**.
2. **Planta em $\omega_c = 0{,}46$:** $|G| = \dfrac{0{,}02}{\sqrt{0{,}46^2+0{,}1^2}\,\sqrt{0{,}46^2+0{,}2^2}} = \dfrac{0{,}02}{0{,}471 \times 0{,}502} = 0{,}0847$ ($-21{,}4$ dB); $\angle G = -\mathrm{arctg}(4{,}6) - \mathrm{arctg}(2{,}3) = -77{,}7° - 66{,}5° = -144{,}2°$ → PM atual $= 35{,}8°$.
3. **PD:** $\phi = 60° - 35{,}8° = 24{,}2°$:
$$k_p = \dfrac{\cos 24{,}2°}{0{,}0847} = 10{,}8; \qquad k_d = \dfrac{\mathrm{sen}\,24{,}2°}{0{,}46 \times 0{,}0847} = 10{,}5$$
   Polo de filtragem em $-100\,\omega_c = -46$.
4. **PI:** zero uma década abaixo: $z_1 = -0{,}046$ → $C_{PI}(s) = \dfrac{s+0{,}046}{s}$.
$$\boxed{C(s) = \dfrac{10{,}8 + 10{,}5\,s}{s/46 + 1}\cdot\dfrac{s+0{,}046}{s}}$$
5. **Simulação:** $M_p = 15{,}7\,\%$ ✓ ($\leq 20\,\%$), $t_r = 4{,}12$ s ✓ ($\leq 5$ s), $y(120\ \mathrm{s}) = 0{,}9998$ → $e_{ss} \to 0$ ✓ (tipo 1). Os três requisitos atendidos simultaneamente.
6. **Receita geral (§3.5.4):** PD cuida de PM e $\omega_c$ (dinâmica); PI cuida de $e_{ss}$ (regime); a PI "rouba" $\approx 5°$ de PM — por isso a folga no passo 1. O PID é literalmente o **produto** dos dois.
7. Compare com `m3_fig35_projeto_pid.png` e a síntese na carta `m3_fig36_pd_pi_pid_nb.png`.

---

> **Encerramento do módulo:** com a frequência você projetou P, avanço, atraso, PD, PI e PID **sem desenhar um único LGR** — e de quebra ganhou as ferramentas para lidar com atraso de transporte e para especificar desempenho por $M_r$, PM e GM. No **Módulo 04**, abandonamos a hipótese de linearidade: saturação, zona morta, histerese e a técnica da função descritiva.
