# Lista 3 — Módulo 03: Projeto no Domínio da Frequência (Bode, Nichols-Black, Nyquist, Compensadores)

> **Laboratório de Controle Automático** — Engenharia Elétrica, Ifes Campus Guarapari.
> Material do aluno. Consulte a teoria em `teoria_modulo3.md` (as questões indicam a seção de apoio) e os exercícios resolvidos em `exercicios_resolvidos_modulo3.md`.
> Entrega: conforme cronograma (semana 15). Resolva à mão e confira numericamente quando indicado. Convenções do curso: módulo em dB ($20\log_{10}|G|$), fase assintótica por retas de $\omega_q/5$ a $5\omega_q$, $\mathrm{PM} \approx 100\zeta$, folga de 5–10° na PM alvo.

---

## Questão 1 — Resposta em frequência (§3.1.3)

Seja $G(s) = \dfrac{12}{s+3}$ com entrada $u(t) = 4\mathrm{sen}(2t)$.

a) Determine a saída em regime permanente $y_{rp}(t)$.
b) A partir de que instante, aproximadamente, a expressão de (a) passa a valer? Justifique.
c) Repita (a) para $u(t) = 4\mathrm{sen}(30t)$ e comente o que mudou — e o que **não** mudou — na saída.

## Questão 2 — Esboço do diagrama de Bode (§3.1.6–§3.1.7)

Seja $G(s) = \dfrac{20}{(s+1)(s+20)}$.

a) Coloque $G$ na forma de Bode e identifique: ganho de Bode (dB), frequências de quebra e declives de cada trecho do módulo assintótico.
b) Calcule o erro da assíntota de módulo em cada quebra — e mostre que vale a regra dos 3 dB.
c) Esboce a fase assintótica (retas de $\omega_q/5$ a $5\omega_q$), indicando os valores em $\omega = 0{,}2$; $4$; $100$ rad/s e a fase final.
d) Calcule a fase **exata** em $\omega = 20$ rad/s e mostre que o erro da assíntota é $\approx 11°$ — o erro máximo da convenção. Onde ele ocorre?

## Questão 3 — Margens de estabilidade e ajuste de ganho (§3.1.8, §3.1.10)

Seja $G(s) = \dfrac{2}{s(s+1)(s+5)}$.

a) Determine $\omega_c$ e a margem de fase.
b) Determine $\omega_f$, a margem de ganho (dB) e o ganho crítico $K_{crit}$; confira por Routh-Hurwitz.
c) Projete o ganho $K$ para que a malha fechada tenha PM $= 45°$. Estime o overshoot resultante pela ponte PM $\approx 100\zeta$.

## Questão 4 — Carta de Nichols-Black e pico de ressonância (§3.2.1–§3.2.4)

a) Para $T(s) = \dfrac{16}{s^2+2{,}4s+16}$, calcule $\omega_r$ e $M_r$ (vezes e dB) e estime $M_p$ e $t_r$ da resposta ao degrau pela ponte frequência–tempo.
b) Num certo $\omega_1$, uma malha aberta vale $G(j\omega_1) = 1\angle{-90°}$. Determine $|T(j\omega_1)|$ (vezes e dB) e $\angle T(j\omega_1)$ pela relação $T = G/(1+G)$ — e localize o ponto correspondente na carta.
c) Explique, em duas frases, por que o ajuste de ganho aparece na carta como **translação vertical** — e que informação da malha fechada essa translação revela sem nenhuma conta nova.

## Questão 5 — Critério de Nyquist (§3.3.4–§3.3.5)

Seja $G(s) = \dfrac{K}{(s+1)(s+3)(s+6)}$.

a) Determine o ponto de cruzamento do gráfico de Nyquist com o eixo real e a faixa de $K$ para a qual a malha fechada é estável. Confira por Routh.
b) Para $K = 63$, calcule a margem de ganho em dB.
c) Acrescenta-se um atraso de transporte de $0{,}1$ s. Calcule a nova margem de fase (com $K = 63$). O atraso alterou a margem de **ganho**? Justifique em uma frase.

## Questão 6 — Atraso de transporte (§3.3.7–§3.3.8)

Seja $G(s) = \dfrac{2}{s+1}e^{-0{,}5s}$.

a) Escreva as expressões de $|G(j\omega)|$ e $\angle G(j\omega)$. Por que a curva de módulo do Bode **não** muda com o atraso?
b) Determine $\omega_c$ e a margem de fase sem considerar o atraso.
c) Determine a margem de fase com o atraso.
d) Para que valor de atraso $\delta_{máx}$ essa malha fechada chega ao limite de estabilidade (PM $= 0°$)?
e) Explique, em duas frases, por que o gráfico de Nyquist de um sistema com atraso é uma espiral que cruza o eixo real infinitas vezes.

## Questão 7 — Projeto de avanço de fase (§3.4.3–§3.4.5)

Seja $G(s) = \dfrac{2}{s(s+1)}$. Requisitos: $M_p \leq 20\%$ e $t_r \leq 1{,}2$ s.

a) Traduza os requisitos para PM alvo e $\omega_c$ alvo (com a folga de praxe).
b) Calcule $\alpha$, $T$ e $K$ e escreva $C(s)$.
c) Estime o overshoot pela ponte PM $\approx 100\zeta$ e diga por que a simulação costuma dar um valor um pouco **maior** que essa estimativa.

## Questão 8 — Projeto de atraso de fase (§3.4.6)

Seja $G(s) = \dfrac{6}{(s+1)(s+3)}$ em malha fechada unitária.

a) Calcule $e_{ss}$ ao degrau e a margem de fase atuais.
b) Projete um compensador de atraso para $e_{ss} \leq 10\%$ (com folga), preservando a dinâmica. Escreva $C(s)$.
c) Verifique a contribuição de fase do par na frequência de cruzamento. Ela ameaça a PM?
d) Estime a constante de tempo da "cauda lenta" introduzida pelo compensador.

## Questão 9 — Projeto de PID na frequência (§3.5.1–§3.5.4)

Seja $G(s) = \dfrac{0{,}5}{(s+0{,}5)(s+2)}$. Requisitos: $M_p \leq 15\%$, $t_r \leq 0{,}7$ s e $e_{ss} = 0$ ao degrau.

a) Escolha $\omega_c$ e a PM alvo justificando a folga adotada.
b) Projete o estágio PD ($k_p$, $k_d$ e polo de filtragem).
c) Projete o estágio PI e escreva $C(s)$ completo.
d) Estime a PM efetiva compensada (descontando PI e polo de filtragem) e o overshoot esperado.

---

> **Bônus (+0,5 na média do módulo):** o maior atraso tolerável — seja $G(s) = \dfrac{2}{s(s+1)(s+2)}e^{-\delta s}$ em malha fechada unitária. Determine o maior atraso $\delta_{máx}$ que a malha suporta antes de atingir o limite de estabilidade. (Dica: encontre $\omega_c$ e a PM sem atraso; o atraso consome PM a uma taxa de $\delta\omega_c$ radianos. Confira a conta de $\omega_c$ observando que $\omega^2(\omega^2+1)(\omega^2+4) = 4$ admite solução em $0{,}5 < \omega^2 < 1$.)
