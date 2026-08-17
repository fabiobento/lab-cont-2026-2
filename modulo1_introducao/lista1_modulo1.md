# Lista 1 — Módulo 01: Introdução aos Sistemas de Controle

> **Laboratório de Controle Automático** — Engenharia Elétrica, Ifes Campus Guarapari.
> Material do aluno. Consulte a teoria em `teoria_modulo1.md` (as questões indicam a seção de apoio) e os exercícios resolvidos em `exercicios_resolvidos_modulo1.md`.
> Entrega: conforme cronograma (semana 6). Resolva à mão e confira numericamente quando indicado.

---

## Questão 1 — Modelagem (§1.1.4)

Um tanque aquecido é modelado, em primeira aproximação, por τ·ẏ + y = K·u, com τ = 4 (constante de tempo) e K = 2 (ganho estático), sendo y a temperatura acima do ambiente e u a potência aplicada.

a) Escreva a EDO com os valores numéricos e obtenha a função de transferência G(s) = Y(s)/U(s).

b) Determine o polo e o valor de regime y(∞) para u degrau unitário.

c) Esboce y(t) e indique no gráfico a constante de tempo τ.

## Questão 2 — Laplace e frações parciais (§1.2.3)

Seja ÿ + 4ẏ + 3y = 6u, com u degrau unitário e condições iniciais nulas.

a) Obtenha G(s) e Y(s).

b) Expanda Y(s) em frações parciais pelo truque dos resíduos.

c) Escreva y(t), confira y(0) e y(∞), e identifique o polo dominante.

## Questão 3 — Estabilidade e Routh (§1.3.1–§1.3.2)

Para cada polinômio característico abaixo, diga se o sistema é estável e, se instável, quantos polos há no semiplano direito:

a) s² + 2s + 5

b) s² − 2s + 5

c) s³ + 2s² + 3s + 4
d) s³ + 2s² + 3s + 12

e) s⁴ + 3s³ + s² + 6s + 2

## Questão 4 — Realimentação (§1.3.3–§1.3.4)

Seja G(s) = 1/(s − 2) (instável) com controle proporcional u = k·e e realimentação unitária.

a) Obtenha a FTMF T(s).

b) Determine a faixa de k para estabilidade.

c) Para k = 6, calcule o erro em regime ao degrau unitário.

d) Explique, usando as três vantagens da realimentação, por que fechar a malha ajudou aqui.

## Questão 5 — Faixa de estabilidade (§1.3.4)

A FTMF de um sistema tem denominador s³ + 4s² + 5s + (2 + k).

a) Determine, via Routh, a faixa de k que mantém o sistema estável.

b) No limite superior da faixa, encontre os polos (dica: equação auxiliar).

c) Confira numericamente com 3 valores de k (abaixo, dentro e acima da faixa).

## Questão 6 — Erro em regime em malha fechada (§1.3.5–§1.3.6)

Seja L(s) = 20/[(s+1)(s+4)] em malha fechada unitária.

a) Classifique o tipo do sistema e calcule kp, kv e ka.

b) Calcule o erro em regime para: degrau unitário, rampa unitária e parábola unitária.

c) Sem refazer contas: o que acontece com os três erros se inserirmos um integrador, L₂(s) = L(s)/s? Justifique com base no tipo.

## Questão 7 — A armadilha do valor final (§1.3.5)

Um aluno aplicou o TVF a G(s) = (s² + 10s + 50)/(s³ + 4s² + 3s + 50) e concluiu "erro nulo em regime para degrau unitário em malha aberta". Critique o procedimento e diga qual é, de fato, o comportamento da saída.

## Questão 8 — Transitório de 2ª ordem (§1.4.3–§1.4.5)

Seja T(s) = 36/(s² + 6s + 36).

a) Determine ζ, ωn, σ e ωd, e localize os polos no plano s (esboce o triângulo σ–ωd–ωn).

b) Calcule Mp (%), tp, tr e ts(5%) pelas fórmulas.

c) Estime ts pelo valor medido numa simulação (ou pelo gráfico) e comente a diferença em relação à fórmula.

## Questão 9 — Projeto de controle P (§1.4.6)

Para a planta G(s) = 1/[s(s+2)] com controle proporcional e realimentação unitária:

a) Projete k para Mp ≤ 10% e verifique por simulação (ou pela fórmula de Mp).

b) Projete k para tp = 1,57 s e determine o Mp resultante.

c) É possível atender (a) e (b) simultaneamente com um único k? Justifique geometricamente (posição dos polos).

## Questão 10 — Dominância (§1.4.1)

Considere T₁(s) = 20/[(s² + 2s + 2)(s + 10)] e T₂(s) = 2/[(s² + 2s + 2)(s + 1)].

a) Em qual dos dois a aproximação por 2ª ordem dominante é justificável? Por quê?

b) Para esse sistema, escreva a aproximação com ganho DC preservado e preveja Mp, tp e ts(5%).

c) Simule ambos (exato × aproximação) e compare o Mp medido.

---

**Bônus (vale 0,5 na nota da lista).** No modelo do motor CC do curso (Questão derivada de §1.1.4), a saída de interesse passa a ser a **posição** y em vez da velocidade. Mostre que a FT de malha ganha um integrador (tipo 1) e conclua o que isso implica para o erro ao degrau em malha fechada. Compare com o erro da Questão 6.
