# Gabarito — Lista 1 (Módulo 01)

> **Documento do professor** — divulgar aos alunos somente após o prazo de entrega.
> Resolução detalhada, passo a passo, com referências ao local da teoria para consulta (`teoria_modulo1.md`). Valores de simulação conferidos numericamente.

---

## Questão 1 — Modelagem

**Consulte:** teoria §1.1.4 (modelos matemáticos) e §1.2.2 (obtenção de G(s)); exemplo semelhante: Exercício 1.4.7 dos exercícios resolvidos (sistema de 1ª ordem).

**a)** Com τ = 4 e K = 2: **4ẏ + y = 2u**. Laplace com CI nulas: 4s·Y(s) + Y(s) = 2U(s) →
**G(s) = 2/(4s + 1)** (ou 0,5/(s + 0,25) na forma de polos).

**b)** Polo: 4s + 1 = 0 → **s = −0,25** (estável, §1.3.1). Valor de regime pelo TVF (sistema estável, pode usar!): y(∞) = lim s→0 s·(1/s)·G(s) = G(0) = **2**.

**c)** y(t) = 2(1 − e^(−t/4)). No gráfico: curva exponencial subindo de 0 a 2; em t = τ = 4 s atinge 63,2% do valor final; ts(5%) ≈ 3τ = 12 s.

---

## Questão 2 — Laplace e frações parciais

**Consulte:** teoria §1.2.2 (FT), §1.2.4 (frações parciais e resíduos); Exercício 1.2.1 dos exercícios resolvidos (mesmo método).

**a)** G(s) = 6/(s² + 4s + 3) = 6/[(s+1)(s+3)]; U(s) = 1/s → **Y(s) = 6/[s(s+1)(s+3)]**.

**b)** Y(s) = A/s + B/(s+1) + C/(s+3). Resíduos ("cubra o fator, substitua o polo"):
A = 6/[(1)(3)] = **2**; B = 6/[(−1)(2)] = **−3**; C = 6/[(−3)(−2)] = **1**.

**c)** y(t) = **2 − 3e^(−t) + e^(−3t)**. Verificações: y(0) = 2 − 3 + 1 = 0 ✓ (CI nulas); y(∞) = 2 = G(0)·1 ✓. Polo dominante: **−1** (o mais próximo do eixo imaginário, decai mais devagar — §1.4.1); o polo −3 só aparece no início da subida.

---

## Questão 3 — Estabilidade e Routh

**Consulte:** teoria §1.3.1 (BIBO) e §1.3.2 (Routh, inclusive os atalhos literais de 2ª e 3ª ordem); Exercícios 1.3.1 e 1.3.2 dos exercícios resolvidos.

**a)** s² + 2s + 5: atalho de 2ª ordem — a = 2 > 0, b = 5 > 0 → **ESTÁVEL** (polos −1 ± j2).

**b)** s² − 2s + 5: a = −2 < 0 → **INSTÁVEL**; os dois polos são +1 ± j2 → **2 polos no SPD**.

**c)** s³ + 2s² + 3s + 4: atalho de 3ª ordem — a = 2 > 0, c = 4 > 0 e a·b = 6 > c = 4 → **ESTÁVEL**.

**d)** s³ + 2s² + 3s + 12: a·b = 6 < 12 = c → **INSTÁVEL**. Tabela para contar: s³: 1, 3 | s²: 2, 12 | s¹: (6−12)/2 = −3 | s⁰: 12. 1ª coluna: 1, 2, −3, 12 → **2 trocas → 2 polos no SPD** (conferido numericamente: +0,306 ± j2,12).

**e)** s⁴ + 3s³ + s² + 6s + 2: s⁴: 1, 1, 2 | s³: 3, 6, 0 | s²: b₁ = (3−6)/3 = −1, b₂ = (6−0)/3 = 2 | s¹: c₁ = (−6−6)/(−1) = 12 | s⁰: 2. 1ª coluna: 1, 3, −1, 12, 2 → **2 trocas → INSTÁVEL, 2 polos no SPD** (conferido: +0,273 ± j1,34).

---

## Questão 4 — Realimentação

**Consulte:** teoria §1.3.3 (FTMF e vantagens) e §1.3.6 (erro em MF); Exercício 1.3.6 dos exercícios resolvidos (planta instável estabilizada).

**a)** T(s) = kG/(1 + kG) = k/(s − 2 + k).

**b)** Polo em s = 2 − k < 0 → **k > 2**.

**c)** k = 6: T(s) = 6/(s + 4), polo −4 ✓ estável. y(∞) = T(0)·1 = 6/4 = 1,5 → ess = r − y(∞) = 1 − 1,5 = **−0,5**. (Erro negativo: a saída ultrapassa a referência em regime — normal quando o ganho DC de malha fechada passa de 1.)

**d)** (i) Estabilização: a malha moveu o polo de +2 para 2 − k (SPE se k > 2); (ii) sensibilidade: variações da planta são atenuadas por 1/(1+kA); (iii) perturbações somadas na saída são divididas por (1 + ganho de malha). Em malha aberta, nenhuma das três existiria — a saída divergiria.

---

## Questão 5 — Faixa de estabilidade

**Consulte:** teoria §1.3.4; Exercício 1.3.3 dos exercícios resolvidos (método idêntico, incluindo a equação auxiliar).

**a)** Routh para s³ + 4s² + 5s + (2+k): s³: 1, 5 | s²: 4, 2+k | s¹: (20 − 2 − k)/4 = (18−k)/4 | s⁰: 2+k.
Condições: (18−k)/4 > 0 → k < 18; 2+k > 0 → k > −2. **Faixa: −2 < k < 18**.

**b)** k = 18: linha s¹ zera → equação auxiliar 4s² + 20 = 0 → s = ±j√5 ≈ **±j2,236**; o terceiro polo é **−4** (marginal: oscilação sustentada de frequência √5 rad/s). Conferido numericamente.

**c)** Ex.: k = −3 (instável: 2+k < 0, polo positivo), k = 0 (estável: polos de s³+4s²+5s+2, todos no SPE), k = 20 (instável: 2 polos no SPD). Verificação numérica recomendada conforme Lab 03, Parte 3.

---

## Questão 6 — Erro em regime em malha fechada

**Consulte:** teoria §1.3.6 (kp, kv, ka, tipo do sistema) e §1.3.5 (verificar estabilidade antes do TVF); Exercício 1.3.5 dos exercícios resolvidos.

**a)** L(s) = 20/[(s+1)(s+4)]: nenhum polo na origem → **tipo 0**.
kp = lim s→0 L = 20/4 = **5**; kv = lim s→0 s·L = **0**; ka = lim s→0 s²·L = **0**.
Estabilidade MF (obrigatória!): denominador s² + 5s + 4 + 20 = s² + 5s + 24 → a, b > 0 ✓.

**b)** Degrau: ess = 1/(1+kp) = **1/6 ≈ 0,167**. Rampa: ess = 1/kv = **∞**. Parábola: ess = 1/ka = **∞**.

**c)** L₂(s) = L(s)/s ganha um polo na origem → **tipo 1**: degrau → ess = 0 (kp = ∞); rampa → kv = lim s·L₂ = 5 → ess = **0,2** (finito); parábola → ainda ∞. Um integrador sobe o sistema um degrau na "escada de precisão".

---

## Questão 7 — A armadilha do valor final

**Consulte:** teoria §1.3.5 (a ordem obrigatória: estabilidade ANTES do TVF); Exercício 1.3.4 dos exercícios resolvidos (mesma armadilha).

O aluno **inverteu a ordem das operações**. Routh no denominador s³ + 4s² + 3s + 50: s³: 1, 3 | s²: 4, 50 | s¹: (12−50)/4 = −9,5 | s⁰: 50 → 1ª coluna: 1, 4, −9,5, 50 → **2 trocas → sistema INSTÁVEL (2 polos no SPD)**.

Logo a saída ao degrau **diverge** — não existe valor de regime e o TVF não se aplica. O "erro nulo" é um número sem significado físico. **Regra de ouro: primeiro estabilidade, depois valor final.**

---

## Questão 8 — Transitório de 2ª ordem

**Consulte:** teoria §1.4.3 (grandezas), §1.4.4 (parametrização) e §1.4.5 (fórmulas); Exercício 1.4.1 dos exercícios resolvidos (mesmo roteiro).

**a)** ωn² = 36 → **ωn = 6 rad/s**; 2ζωn = 6 → **ζ = 0,5**. σ = ζωn = **3**; ωd = 6√(1−0,25) = **5,196 rad/s**. Polos: −3 ± j5,196. Triângulo: catetos 3 (horizontal) e 5,196 (vertical), hipotenusa 6, ângulo β = arccos 0,5 = 60° = 1,047 rad.

**b)** Mp = e^(−0,5π/0,866) = e^(−1,814) = **16,3%**; tp = π/5,196 = **0,605 s**; tr = (π − 1,047)/5,196 = **0,403 s**; ts ≈ 3/3 = **1,0 s**.

**c)** Simulação mede: Mp = 16,3%, tp = 0,604, tr = 0,403, ts(5%) ≈ 0,88 s. As três fórmulas exatas batem; ts da fórmula (1,0 s) é **pessimista** — despreza o fator 1/√(1−ζ²) que ajuda o envelope a entrar antes na faixa (§1.4.5).

---

## Questão 9 — Projeto de controle P

**Consulte:** teoria §1.4.6 (os dois projetos, com as fórmulas literais); Exercícios 1.4.2, 1.4.3 e 1.4.5 dos exercícios resolvidos.

T(s) = k/(s² + 2s + k) → ωn² = k, 2ζωn = 2 → **σ = 1 fixo pela planta**.

**a)** ζ = √[ln²(0,1)/(π²+ln²(0,1))] = 0,591 → ωn = 2/(2·0,591) = 1,692 → **k = 2,86** (literal: k = a²/(4ζ²) = 4/(4·0,349) = 2,86 ✓). Verificação: Mp medido = **10,0%** ✓.

**b)** ωd = π/1,57 ≈ 2,0 → k = σ² + ωd² = 1 + 4 = **5**. Polos: −1 ± j2. ζ = 1/√5 = 0,447 → Mp = e^(−0,447π/0,894) = **20,8%**. Verificação: tp medido = 1,571 s ✓, Mp = 20,8% ✓.

**c)** **Não.** A planta fixa σ = 1 (polos sobre a reta vertical Re(s) = −1). O item (a) exige ζ = 0,591 → polos −1 ± j1,37 (tp = 2,30 s ≠ 1,57 s); o item (b) exige polos −1 ± j2 (ζ = 0,447 → Mp = 20,8% > 10%). Com UM grau de liberdade (k), os polos caminham sobre uma única reta — cada especificação pede um ponto diferente dela (§1.4.7).

---

## Questão 10 — Dominância

**Consulte:** teoria §1.4.1 (polo dominante e a regra dos 5×); Exercício 1.4.4 dos exercícios resolvidos.

**a)** Em **T₁**: o par complexo tem σ = 1 e o polo extra está em −10 — **10× mais longe** → regra dos 5× satisfeita → aproximação justificável. Em T₂, o polo extra −1 está tão perto quanto o par (mesmo σ = 1) → aproximação **não** justificável.

**b)** Ganho DC de T₁: 20/(2·10) = 1 → aproximação com DC preservado: **T₁ ≈ 2/(s² + 2s + 2)**. Parâmetros: ωn = √2 = 1,414, ζ = 0,707 → σ = 1, ωd = 1. Previsões: Mp = e^(−π) = **4,3%**, tp = π/1 = **3,14 s**, ts ≈ 3/1 = **3,0 s**.

**c)** Simulação: exato → Mp = 4,3%, tp = 3,25 s; aproximação → Mp = 4,3%, tp = 3,14 s. Erros de poucos % — a dominância funciona quando a regra dos 5× é respeitada. (Em T₂, o erro seria grosseiro, como no exemplo 16,3% × 8,1% da teoria.)

---

## Bônus — Motor CC com saída em posição

**Consulte:** teoria §1.1.4 (motor CC) e §1.3.6 (tipo do sistema); Exercício 1.1.3 dos exercícios resolvidos.

Com velocidade: Ω(s)/U(s) = b0/(s² + a1s + a0). Posição é a integral da velocidade: Y(s) = Ω(s)/s →
**Gp(s) = b0/[s(s² + a1s + a0)]** — um **polo na origem**, ou seja, L(s) = k·Gp(s) passa a ser **tipo 1**.

Consequência (tabela de erros, §1.3.6): kp = ∞ → **erro nulo ao degrau** em malha fechada (o motor posiciona exatamente, desde que estável), enquanto o sistema da Questão 6 (tipo 0) deixava ess = 1/6. À rampa, o motor-posição tem erro finito 1/kv — acompanha velocidade de referência com atraso constante.
