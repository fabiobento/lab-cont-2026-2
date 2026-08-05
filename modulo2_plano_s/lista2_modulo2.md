# Lista 2 — Módulo 02: Projeto no Plano-s (LGR, Avanço, Atraso, PID)

> **Laboratório de Controle Automático** — Engenharia Elétrica, Ifes Campus Guarapari.
> Material do aluno. Consulte a teoria em `teoria_modulo2.md` (as questões indicam a seção de apoio) e os exercícios resolvidos em `exercicios_resolvidos_modulo2.md`.
> Entrega: conforme cronograma (semana 10). Resolva à mão e confira numericamente quando indicado.

---

## Questão 1 — Regiões de desempenho (§2.1.3–§2.1.6)

Requisitos: $M_p \leq 10\,\%$, $t_p \leq 2$ s, $t_s(5\,\%) \leq 3$ s e $t_r(10\text{–}90\,\%) \leq 0{,}4$ s.

a) Traduza cada requisito para uma fronteira no plano-s ($\beta$, $\omega_d$, $\sigma$, $\omega_n$) e esboce a região combinada.
b) Verifique se um par de polos em $-1{,}5 \pm 2j$ atende **todos** os requisitos. Se algum falhar, diga qual.

## Questão 2 — Aproximação de 3ª por 2ª ordem (§2.1.8)

Seja $T(s) = \dfrac{4\,p_3}{(s^2+2s+4)(s+p_3)}$.

a) Para $p_3 = 12$: a regra dos 5× autoriza a aproximação? Estime $M_p$ e $t_p$.
b) Para $p_3 = 2$: o que você espera qualitativamente para o overshoot? Justifique pelo conceito de dominância.
c) Por que é essencial manter o ganho DC igual a 1 ao acrescentar o polo $-p_3$ na FT de teste?

## Questão 3 — Condição de ângulo e de módulo (§2.2.3–§2.2.4)

Seja $G(s) = \dfrac{2}{s(s+4)}$.

a) Verifique se $\square_a = -2+2j$ pertence ao LGR e, em caso afirmativo, calcule o ganho $k$ que o torna polo de malha fechada.
b) Repita para $\square_b = -1+3j$.
c) Esboce o LGR de $G$ (encontro, direção dos ramos) e marque os dois pontos.

## Questão 4 — Esboço completo de LGR (§2.2.6)

Seja $G(s) = \dfrac{1}{(s+2)(s+4)(s+6)}$ com controle proporcional $k$.

a) Determine: trechos do LGR no eixo real; número e ângulos das assíntotas; centroide.
b) Via Routh, encontre o ganho crítico e o ponto de cruzamento com o eixo imaginário.
c) Calcule o(s) ponto(s) de saída do eixo real (descarte candidatos fora dos trechos).
d) Para que faixa de $k$ o sistema de malha fechada é estável?

## Questão 5 — Projeto de avanço de fase (§2.3.3–§2.3.5)

Seja $G(s) = \dfrac{1}{s(s+2)}$. Requisitos: $M_p = 16{,}3\,\%$ e $t_p \approx 0{,}63$ s ($\omega_d = 5$ rad/s).

a) Determine $\zeta$, $\omega_n$ e o polo desejado $\square_d$.
b) Calcule a contribuição de fase necessária do controlador.
c) Projete o avanço **por cancelamento** do polo $-2$: posição do polo $-b$ e ganho $k$.
d) Estime $M_p$ e $t_p$ do sistema compensado. A ordem do sistema compensado ajuda ou atrapalha a previsão? Por quê?

## Questão 6 — Projeto de atraso de fase (§2.4.2–§2.4.3)

Seja $G(s) = \dfrac{1}{s(s+4)}$ com controle proporcional $k = 20$ (polos de MF: $-2 \pm 4j$; $M_p \approx 20{,}8\,\%$).

a) Calcule $k_v$ e o erro em regime para rampa unitária.
b) Projete um atraso de fase que **reduza o erro à metade**, com o zero seguindo a regra do 1/10. Escreva $C(s)$.
c) Calcule a contribuição de fase do par no ponto $-2+4j$ e preveja o efeito sobre o overshoot.
d) Onde estará o terceiro polo de malha fechada, aproximadamente? Qual é o efeito dele na resposta?

## Questão 7 — PI para planta tipo 0 (§2.4.4)

Seja $G(s) = \dfrac{4}{(s+2)(s+6)}$. Requisitos: $M_p \approx 16\,\%$ ($\zeta = 0{,}5$), $\omega_d = 3$ rad/s e $e_{ss}(\text{degrau}) = 0$.

a) Explique por que o atraso de fase comum **não** atende e o PI é obrigatório.
b) Com $\square_d = -1{,}73 + 3j$, calcule a posição do zero do PI (soma de fases = $-180°$) e o ganho $k$.
c) Escreva $C(s)$ e obtenha $k_p$ e $k_i$.
d) Preveja: o overshoot medido será maior ou menor que os 16,3 % da aproximação de 2ª ordem? Que efeito explica a diferença? (Dica: §2.1.9.)

## Questão 8 — Atraso de transporte (§2.5.4–§2.5.5)

Um forno é modelado por $G(s) = \dfrac{1}{s+2}$ com atraso de transporte $\tau = 0{,}25$ s, em malha fechada com ganho $k$.

a) Escreva o modelo completo $G_a(s)$ usando a aproximação de Padé de 1ª ordem e identifique o zero no semiplano direito.
b) Determine o ganho crítico $k_{crit} = a + 2/\tau$.
c) Sem calcular polos, diga o que acontece com o sistema para $k = 5$ e para $k = 15$.
d) Explique, em duas frases, por que o atraso reduz a margem de estabilidade — e o que isso implica para o projeto de controladores em sistemas com transporte longo (ex.: aquecedor a gás distante do ponto de uso).

## Questão 9 — Conceitos de projeto (§2.3.8, §2.5.1, §2.5.3)

Responda em poucas frases:

a) Na "receita de bolo" de 10 passos, o que se faz quando $\angle G(\square_d)$ é **maior** que $-180°$ com folga? E quando é **menor** que $-220°$?
b) Por que limitamos o avanço de fase a 40° por estágio? O que acontece fisicamente quando se exige mais?
c) Por que nenhum ambiente industrial implementa o PID "puro" $k_p + k_d s + k_i/s$? Escreva a forma realmente implementada e dê o nome dela.

---

> **Bônus (+0,5 na média do módulo):** desafio de Beakman — PI com zero em $-0{,}5$ para $G(s) = \dfrac{20}{(s-1)(s+2)(s+10)}$. Prove por Routh que nenhum $k$ estabiliza e explique geometricamente, pelo LGR, o motivo. (Ver Lab 08, Parte 4.)
