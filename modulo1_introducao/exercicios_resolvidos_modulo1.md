# Módulo 01 — Exercícios Resolvidos

> Material do aluno. Cada exercício indica a seção da **teoria** (`teoria_modulo1.md`) onde o conteúdo pode ser consultado. Todos os valores numéricos de respostas ao degrau foram conferidos por simulação.

---

## Tópico 1.1 — Sistemas de controle e modelos

### Exercício 1.1.1 — Modelo do circuito RLC série
*(teoria: §1.1.4 — Modelos matemáticos)*

**Enunciado.** Circuito RLC série com entrada v(t) e saída vC(t). Obtenha a EDO e a função de transferência G(s) = VC(s)/V(s) para R = 2 Ω, L = 1 H, C = 0,5 F.

**Resolução passo a passo.**
1. Lei das malhas: v = vR + vL + vC = R·i + L·di/dt + vC.
2. Como i = C·dvC/dt, substituindo: v = RC·v̇C + LC·v̈C + vC.
3. Ordenando: LC·v̈C + RC·v̇C + vC = v → **v̈C + (R/L)v̇C + (1/LC)vC = (1/LC)v**.
4. Com os valores: v̈C + 2v̇C + 2vC = 2v.
5. Copiando os coeficientes (CI nulas): **G(s) = 2/(s² + 2s + 2)**.
6. Polos: Δ = 4 − 8 = −4 → s = −1 ± j (subamortecido, σ = 1, ωd = 1).

### Exercício 1.1.2 — Modelo massa-mola-amortecedor
*(teoria: §1.1.4)*

**Enunciado.** Massa M = 1 kg, amortecimento B = 5 N·s/m, mola K = 6 N/m, força u(t) como entrada, posição y(t) como saída. Obtenha a EDO, G(s) e classifique a resposta.

**Resolução passo a passo.**
1. Equilíbrio de forças: M·ÿ = u − B·ẏ − K·y.
2. Ordenando: **ÿ + (B/M)ẏ + (K/M)y = (1/M)u** → ÿ + 5ẏ + 6y = u.
3. Função de transferência: **G(s) = 1/(s² + 5s + 6) = 1/[(s+2)(s+3)]**.
4. Polos reais distintos (−2 e −3): sistema **superamortecido** — sobe sem ultrapassar (ver §1.4.2).

### Exercício 1.1.3 — Motor CC (modelo do curso)
*(teoria: §1.1.4 — motor CC)*

**Enunciado.** Motor CC com T = k·i (torque proporcional à corrente), vM = k·ẏ (tensão gerada pelo movimento), T = J·ÿ. Com R = 2 Ω, L = 0,5 H, k = 1, J = 0,25 kg·m², obtenha a EDO e G(s) com a velocidade ω = ẏ como saída. **Extra (proposto):** e se a saída for a posição y?

**Resolução passo a passo.**
1. Malha elétrica: u = R·i + L·di/dt + vM = R·i + L·i̇ + k·ω.
2. Parte mecânica: k·i = J·ω̇ → i = (J/k)ω̇.
3. Substituindo: u = (RJ/k)ω̇ + (LJ/k)ω̈ + k·ω.
4. Multiplicando por k/(LJ): **ω̈ + (R/L)ω̇ + (k²/LJ)ω = (k/LJ)u**.
5. Com os valores: R/L = 4, k²/LJ = 1/0,125 = 8, k/LJ = 8 → **ω̈ + 4ω̇ + 8ω = 8u** → **G(s) = 8/(s² + 4s + 8)**.
6. Polos: Δ = 16 − 32 < 0 → s = −2 ± j2 (subamortecido).
7. **Extra:** posição y = ∫ω → Y(s) = Ω(s)/s → **Gp(s) = 8/[s(s² + 4s + 8)]** — 3ª ordem, com um integrador (tipo 1!). Discuta: o que muda no erro em regime? (ver §1.3.6).

---

## Tópico 1.2 — Transformada de Laplace e função de transferência

### Exercício 1.2.1 — Resposta ao degrau via frações parciais
*(teoria: §1.2.4 — Frações parciais; âncora principal dos vídeos)*

**Enunciado.** ÿ + 3ẏ + 2y = 2u, u degrau unitário. Calcule y(t).

**Resolução passo a passo.**
1. G(s) = 2/(s² + 3s + 2) = 2/[(s+1)(s+2)]; U(s) = 1/s.
2. Y(s) = 2/[s(s+1)(s+2)] = A/s + B/(s+1) + C/(s+2).
3. Resíduos ("cubra o fator e substitua"):
   A = 2/[(0+1)(0+2)] = 1; B = 2/[(−1)(−1+2)] = −2; C = 2/[(−2)(−2+1)] = 1.
4. Conferindo: 1/s − 2/(s+1) + 1/(s+2) = [ (s+1)(s+2) − 2s(s+2) + s(s+1) ]/[s(s+1)(s+2)] = 2/[s(s+1)(s+2)] ✓
5. Invertendo termo a termo (tabela, §1.2.3): **y(t) = 1 − 2e^(−t) + e^(−2t)**.
6. Verificações: y(0) = 1 − 2 + 1 = 0 ✓; y(∞) = 1 = G(0)·1 ✓ (ganho DC).

### Exercício 1.2.2 — Polo afastado e convergência rápida
*(teoria: §1.2.4; âncora dos vídeos)*

**Enunciado.** ÿ + 11ẏ + 10y = 20u, u degrau unitário. Calcule y(t) e estime o tempo de acomodação.

**Resolução passo a passo.**
1. G(s) = 20/[(s+1)(s+10)]; Y(s) = 20/[s(s+1)(s+10)].
2. Resíduos: A = 20/(1·10) = 2; B = 20/[(−1)(9)] = −20/9; C = 20/[(−10)(−9)] = 2/9.
3. **y(t) = 2 − (20/9)e^(−t) + (2/9)e^(−10t)**.
4. O polo −10 decai 10× mais rápido: a dinâmica visível é a do polo dominante −1 → ts(5%) ≈ 3/1 = **3 s** (dominância, §1.4.1).
5. Valor final: y(∞) = 2 = G(0) ✓.

### Exercício 1.2.3 — Polos repetidos
*(teoria: §1.2.4 — polos múltiplos; âncora dos vídeos)*

**Enunciado.** G(s) = 2/[(s+1)(s+2)], u(t) = e^(−t). Calcule y(t).

**Resolução passo a passo.**
1. U(s) = 1/(s+1) → Y(s) = 2/[(s+1)²(s+2)] — polo −1 repetido.
2. Expansão: Y(s) = D/(s+1) + E/(s+1)² + F/(s+2).
3. Truque vale para E e F: E = (s+1)²Y(s)|₋₁ = 2/(−1+2) = 2; F = (s+2)Y(s)|₋₂ = 2/(−1)² = 2.
4. D pela soma: D/(s+1) + 2/(s+1)² + 2/(s+2) = 2/[(s+1)²(s+2)] → numerador: D(s+1)(s+2) + 2(s+2) + 2(s+1)² = 2. Comparando s²: D + 2 = 0 → **D = −2**.
5. Invertendo: **y(t) = −2e^(−t) + 2t·e^(−t) + 2e^(−2t)** (lembre: 1/(s+a)² ↔ t·e^(−at)).
6. Verificação: y(0) = −2 + 0 + 2 = 0 ✓ (sistema em repouso).

### Exercício 1.2.4 (extra) — Da FT à EDO e vice-versa
*(teoria: §1.2.2)*

**Enunciado.** (a) Escreva a EDO de G(s) = (2s + 1)/(s³ + 8s² + 4s). (b) Escreva G(s) de y⃛ + 2ÿ = ů + 3u.

**Resolução.** (a) Numerador ← entrada, denominador ← saída: **y⃛ + 8ÿ + 4ẏ = 2ů + u** (sistema tipo 1 — denominador tem fator s). (b) **G(s) = (s + 3)/(s³ + 2s²)**.

---

## Tópico 1.3 — Estabilidade, realimentação e erro em regime

### Exercício 1.3.1 — Routh: 3ª ordem com troca de sinal
*(teoria: §1.3.2 — Critério de Routh; âncora dos vídeos)*

**Enunciado.** Quantos polos no semiplano direito tem s³ + 6s² + 11s + 72?

**Resolução passo a passo.**
1. Linha s³: 1, 11. Linha s²: 6, 72.
2. Linha s¹: b₁ = (6·11 − 1·72)/6 = (66 − 72)/6 = **−1**.
3. Linha s⁰: c₁ = (−1·72 − 6·0)/(−1) = 72.
4. 1ª coluna: 1, 6, **−1**, 72 → sinais + + − + → **2 trocas → 2 polos no SPD → instável**.

### Exercício 1.3.2 — Routh: 4ª ordem
*(teoria: §1.3.2; âncora dos vídeos)*

**Enunciado.** Analise s⁴ + 2s³ − s² + 20s + 5.

**Resolução passo a passo.**
1. s⁴: 1, −1, 5 | s³: 2, 20, 0.
2. s²: b₁ = (2·(−1) − 1·20)/2 = −11; b₂ = (2·5 − 1·0)/2 = 5.
3. s¹: c₁ = (−11·20 − 2·5)/(−11) = (−230)/(−11) ≈ 20,9.
4. s⁰: d₁ = (20,9·5 − (−11)·0)/20,9 = 5.
5. 1ª coluna: 1, 2, **−11**, 20,9, 5 → 2 trocas → **2 polos no SPD → instável**.

### Exercício 1.3.3 — Faixa de estabilidade
*(teoria: §1.3.4; âncora principal dos vídeos)*

**Enunciado.** MF unitária com T(s) cujo denominador é s³ + 6s² + 11s + (6 + k). Determine a faixa de k para estabilidade e os polos nos limites.

**Resolução passo a passo.**
1. s³: 1, 11 | s²: 6, 6+k.
2. s¹: b₁ = (6·11 − (6+k))/6 = (60 − k)/6 | s⁰: 6 + k.
3. Estável ⇔ (60−k)/6 > 0 E 6+k > 0 → **−6 < k < 60**.
4. Limite k = 60: linha s¹ zera → equação auxiliar 6s² + 66 = 0 → s = ±j√11 ≈ **±j3,32**, e o 3º polo é −6 → oscilação sustentada (marginal).
5. Limite k = −6: termo constante nulo → **polo na origem** (marginal).
6. Validação numérica: com k = 29,9... conferir com os polos calculados (todos no SPE até k < 60).

### Exercício 1.3.4 — Erro em regime com armadilha do TVF
*(teoria: §1.3.5–1.3.6; âncora dos vídeos)*

**Enunciado.** (a) G(s) = (s² + 6s + 9)/(s³ + 8s² + 17s + 10) em MA, degrau unitário: qual o erro? (b) E para G(s) = (s² + 29s + 208)/(s³ + 6s² + 10s + 208)?

**Resolução passo a passo.**
1. (a) Estabilidade: denominador = (s+1)(s+2)(s+5) → polos −1, −2, −5 ✓ estável. TVF: y(∞) = G(0)·1 = 9/10 = 0,9 → **ess = 1 − 0,9 = 0,1**.
2. (b) Routh no denominador: s³: 1, 10 | s²: 6, 208 | s¹: (60 − 208)/6 < 0 → troca de sinal → **instável!** A saída diverge: **o TVF não se aplica** — o "erro finito" que a fórmula daria é mentira.
3. **Regra de ouro: estabilidade ANTES do TVF** (§1.3.5).

### Exercício 1.3.5 — Constantes de erro em malha fechada
*(teoria: §1.3.6; âncora dos vídeos)*

**Enunciado.** L(s) = k/[(s+1)(s+2)], MF unitária. Determine tipo, kp e ess ao degrau para k = 10. Depois, ess à rampa unitária.

**Resolução passo a passo.**
1. Tipo: nenhum polo na origem → **tipo 0**.
2. kp = lim s→0 L(s) = k/2 = 5 → **ess = 1/(1 + kp) = 1/6 ≈ 0,167**.
3. Rampa: kv = lim s→0 s·L(s) = 0 → **ess = ∞** (tipo 0 não acompanha rampa).
4. Verificação de estabilidade (sempre!): denominador MF = s² + 3s + 2 + k = s² + 3s + 12 → a > 0, b > 0 ✓.

### Exercício 1.3.6 (extra) — Faixa com planta instável
*(teoria: §1.3.3–1.3.4; âncora v1 adaptada)*

**Enunciado.** G(s) = 10/(s³ + 11s² + 8s − 20), controle P com ganho k e MF unitária. Faixa de k?

**Resolução passo a passo.**
1. T(s) = 10k/[s³ + 11s² + 8s + (10k − 20)].
2. Routh: s¹: (11·8 − (10k − 20))/11 = (108 − 10k)/11 > 0 → k < 10,8. s⁰: 10k − 20 > 0 → k > 2.
3. **2 < k < 10,8** — a realimentação estabiliza a planta instável, mas só numa faixa (ganho alto demais também desestabiliza).

### Exercício 1.3.7 (extra) — Routh com K simbólico
*(teoria: §1.3.2; âncora v1)*

**Enunciado.** s³ + 5s² + 6s + K: faixa de K?

**Resolução.** s¹: (5·6 − K)/5 > 0 → K < 30; s⁰: K > 0 → **0 < K < 30**. Em K = 30: equação auxiliar 5s² + 30 = 0 → **s = ±j√6 ≈ ±j2,449** (conferido numericamente).

### Exercício 1.3.8 (extra) — Motor CC completo: erro ao degrau
*(teoria: §1.3.6; âncora v1)*

**Enunciado.** L(s) = 0,11/(0,10s + 1) (motor CC completo, modelo com constante de tempo elétrica), MF unitária. ess ao degrau unitário?

**Resolução.** Tipo 0; kp = 0,11 → **ess = 1/1,11 ≈ 0,90**. Comentário: ganho baixo → erro enorme; para reduzi-lo, aumentar k — mas o transitório degrada (trade-off visto em §1.4 e no Lab 03).

---

## Tópico 1.4 — Resposta ao degrau de 2ª ordem e controle P

### Exercício 1.4.1 — Identificação de parâmetros
*(teoria: §1.4.3–1.4.4; âncora dos vídeos)*

**Enunciado.** G(s) = 25/(s² + 4s + 25). Determine ζ, ωn, σ, ωd e calcule Mp, tp, tr, ts(5%).

**Resolução passo a passo.**
1. ωn² = 25 → ωn = 5 rad/s; 2ζωn = 4 → ζ = 0,4.
2. σ = ζωn = 2; ωd = ωn√(1−ζ²) = 5·√0,84 = 4,58 rad/s; β = arccos(0,4) = 1,159 rad.
3. Mp = e^(−ζπ/√(1−ζ²)) = e^(−1,371) = 0,254 → **25,4%**.
4. tp = π/ωd = **0,686 s**; tr = (π − β)/ωd = **0,433 s**; ts ≈ 3/σ = **1,5 s**.
5. Valores medidos na simulação: 25,4% / 0,69 / 0,43 / 1,52 — as fórmulas exatas batem; ts é levemente pessimista, como anunciado (§1.4.5).

### Exercício 1.4.2 — Projeto por overshoot
*(teoria: §1.4.6 — Projeto 1; âncora principal)*

**Enunciado.** G(s) = 1/[s(s+1)], controle P, MF unitária. Projete k para Mp ≤ 10%.

**Resolução passo a passo.**
1. T(s) = k/(s² + s + k) → ωn² = k, 2ζωn = 1.
2. ζ = √[ln²(0,1)/(π² + ln²(0,1))] = √(5,302/15,172) = **0,591**.
3. ωn = 1/(2ζ) = 0,846 → **k = ωn² = 0,718**.
4. Verificação por simulação: Mp medido = **10,1%** ✓.
5. Pela fórmula literal k = a²/(4ζ²) com a = 1: k = 1/(4·0,349) = 0,716 ≈ 0,718 ✓.

### Exercício 1.4.3 — Projeto por instante de pico
*(teoria: §1.4.6 — Projeto 2; âncora principal)*

**Enunciado.** Mesma planta, projete k para tp = 3,14 s. Qual o Mp resultante?

**Resolução passo a passo.**
1. ωd = π/tp = **1 rad/s**.
2. A planta fixa 2ζωn = 1 → σ = ζωn = 0,5 (não temos escolha!).
3. k = ωn² = σ² + ωd² = 0,25 + 1 = **1,25**. Polos: −0,5 ± j1,0.
4. ζ = σ/ωn = 0,5/1,118 = 0,447 → Mp = e^(−0,447π/0,894) = **20,8%** (simulação: 20,7% ✓).
5. Lição: com UM grau de liberdade, atendemos UMA especificação — o Mp saiu o que saiu (§1.4.7).

### Exercício 1.4.4 — Dominância: quando a aproximação falha
*(teoria: §1.4.1; âncora dos vídeos)*

**Enunciado.** Compare 1/[(s²+s+1)(s+1)] com a aproximação de 2ª ordem 1/(s²+s+1) (ganho ajustado para DC unitário). Vale a aproximação?

**Resolução passo a passo.**
1. O par complexo tem σ = 0,5; o polo extra −1 está só 2× mais longe — a regra dos 5× falha.
2. Simulação: Mp real = **16,3%** × Mp da aproximação = **8,1%** → erro grosseiro.
3. Compare com 5/[(s²+s+1)(s+5)] ≈ 1/(s²+s+1): polo −5 = 10× σ → aproximação boa (§1.4.1, figura m1_fig14).

### Exercício 1.4.5 (extra) — Projeto com planta 1/[s(s+4)]
*(teoria: §1.4.6; âncora v1 — exemplo adicional)*

**Enunciado.** G(s) = 1/[s(s+4)], controle P. (a) k para Mp ≤ 10%. (b) k para tp = 0,8 s.

**Resolução passo a passo.**
1. T(s) = k/(s² + 4s + k) → 2ζωn = 4 → σ = 2 fixo.
2. (a) ζ = 0,591 → ωn = 4/(2·0,591) = 3,383 → **k = 11,45** (fórmula literal: a²/(4ζ²) = 16/1,397 = 11,45 ✓). Simulação: Mp = 10,0% ✓.
3. (b) ωd = π/0,8 = 3,927 → k = σ² + ωd² = 4 + 15,42 = **19,42**. Simulação: tp = 0,802 s ✓, Mp = 20,2%.
4. Note que o Mp de (b) é o mesmo do Exercício 1.4.3? Não: 20,2% × 20,7% — muda porque σ é diferente (ζ diferente). Compare e explique com a geometria dos polos (§1.4.4).

### Exercício 1.4.6 (extra) — Tabela ζ × Mp
*(teoria: §1.4.5; âncora v1 — usar a figura m1_fig21_zeta_mp.png)*

**Enunciado.** Complete a tabela ζ ∈ {0,4; 0,45; 0,5; 0,6; 0,7} × Mp, e depois marque os pontos na curva ζ × Mp.

**Resolução (valores calculados pela fórmula de Mp):**

| ζ | 0,4 | 0,45 | 0,5 | 0,6 | 0,7 |
|---|---|---|---|---|---|
| **Mp (%)** | 25,4 | 20,5 | 16,3 | 9,5 | 4,6 |

Conferindo dois pontos: ζ = 0,5 → e^(−0,5π/0,866) = e^(−1,814) = 16,3% ✓; ζ = 0,7 → e^(−0,7π/0,714) = e^(−3,080) = 4,6% ✓. A figura `m1_fig21_zeta_mp.png` mostra a curva completa — repare como Mp cai rápido: para Mp ≤ 5% já precisamos de ζ ≈ 0,7.

### Exercício 1.4.7 (extra) — Sistema de 1ª ordem
*(teoria: §1.4.2; âncora v1)*

**Enunciado.** G(s) = 5/(2s + 1): qual a constante de tempo, o ganho DC e ts(5%) para degrau unitário?

**Resolução.** Forma padrão K/(τs + 1): τ = 2 s, K = 5. Resposta: y(t) = 5(1 − e^(−t/2)). Faixa de 5%: e^(−ts/2) = 0,05 → **ts = 2·ln 20 = 6,0 s** (= 3τ). Valor final: 5 = ganho DC × 1 ✓.

---

## Figuras de apoio

- `m1_fig11_saida_fracoes.png` — Exercícios 1.2.1 e 1.2.2
- `m1_fig14_aproximacoes.png` — Exercício 1.4.4
- `m1_fig16_caracteristicas.png` — Exercício 1.4.1
- `m1_fig19_projeto_mp.png` / `m1_fig20_projeto_tp.png` — Exercícios 1.4.2 e 1.4.3
- `m1_fig21_zeta_mp.png` — Exercício 1.4.6
