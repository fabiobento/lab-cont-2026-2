# Nota de Aula 1.3 — Estabilidade, Realimentação e Erro em Regime

> **Documento do professor** — guia de quadro, linha a linha, com falas sugeridas.
> Duração prevista: 2 h (semana 4). Lab associado: **Lab 03**.

**Mapa dos vídeos deste tópico (não mostrar aos alunos):**

| Vídeo | Título | Uso na aula |
|---|---|---|
| 01 | Estabilidade BIBO | Definição; condição sobre os polos; exemplos divergentes (Q1) |
| 02 | Critério de Routh | Tabela de Routh; exemplos 2ª/3ª/4ª ordem; casos literais (Q2–Q3) |
| 03 | Vantagens da Realimentação | FTMF; estabilização; sensibilidade; perturbação (Q4–Q5) |
| 04 | Faixa de Estabilidade | k variável; faixas de estabilidade com Routh (Q6) |
| 05 | Erro em Malha Aberta | ess via TVF em MA (Q7) |
| 06 | Erro em Malha Fechada | kp, kv, ka; tipo do sistema; tabela de erros (Q8–Q9) |

---

## Q1 — Estabilidade BIBO (15 min)

**Quadro:**

```
DEFINIÇÃO: sistema BIBO-estável ⇔ TODA entrada LIMITADA gera saída LIMITADA
 (Bounded Input, Bounded Output)

Resposta = soma de parcelas e^{pᵢt} (polos pᵢ). Para a saída não explodir:
 CONDIÇÃO: TODOS os polos com parte real NEGATIVA (semiplano esquerdo)

Exemplos (fazer no quadro):
 G(s) = 1/s, u = degrau: Y = 1/s² ⇒ y = t (rampa!) → DIVERGE
   (polo na origem; entrada limitada, saída ilimitada ⇒ não é BIBO)
 G(s) = 1/(s²+1), u = cos t: Y = s/(s²+1)² ⇒ y = (t/2)·sen t → DIVERGE
   (polos ±j; ressonância: entrada na frequência natural)
Contra-exemplo clássico: G = 1/(s−1) é estável para u = e^{t}? NÃO interessa:
 a definição exige TODA entrada limitada.
```

**Fala:** "Um único contra-exemplo derruba a estabilidade. Não basta achar uma entrada limitada que gera saída limitada — têm que ser todas."

## Q2 — Critério de Routh: montagem da tabela (25 min)

**Quadro — montagem (linha a linha):**

```
Polinômio: a₃s³ + a₂s² + a₁s + a₀  (ex.: s³ + 6s² + 11s + 6)
Linha s³: coeficientes das potências ÍMPARES... convenção: s³ e s¹ →  1   11
Linha s²: coeficientes das potências restantes (s², s⁰)          →  6    6
Linha s¹: b₁ = (6·11 − 1·6)/6 = 10 ;  b₂ = (6·0 − 1·0)/6 = 0     → 10    0
Linha s⁰: c₁ = (10·6 − 6·0)/10 = 6                               →  6

REGRA (Routh): nº de raízes no semiplano DIREITO =
               nº de TROCAS DE SINAL na 1ª coluna
Aqui: 1, 6, 10, 6 — todos positivos ⇒ 0 trocas ⇒ ESTÁVEL
 (confira: s³+6s²+11s+6 = (s+1)(s+2)(s+3) — polos −1, −2, −3 ✓)
```

**Quadro — exemplos rápidos (escrever todos):**

```
s² + 3s + 2:  1ª coluna 1, 3, 2 → estável ✓ (polos −1, −2)
s² + s − 2:   1ª coluna 1, 1, −2 → 1 troca ⇒ 1 polo no SPD (de fato: (s+2)(s−1))

s³ + 6s² + 11s + 72:  b₁ = (66−72)/6 = −1
  1ª coluna: 1, 6, −1, 72 → DUAS trocas ⇒ 2 polos no SPD (instável)

4ª ordem: s⁴ + 2s³ − s² + 20s + 5
 s⁴: 1, −1, 5 | s³: 2, 20, 0
 s²: b₁ = (2·(−1)−1·20)/2 = −11 ; b₂ = (2·5−0)/2 = 5
 s¹: c₁ = (−11·20 − 2·5)/(−11) = (−230)/(−11) ≈ 20,9
 s⁰: 5
 1ª coluna: 1, 2, −11, 20,9, 5 → 2 trocas ⇒ 2 polos no SPD
```

## Q3 — Routh com coeficientes literais (15 min)

**Quadro:**

```
2ª ordem: s² + a·s + b → 1ª coluna: 1, a, b
 ⇒ ESTÁVEL ⇔ a > 0 E b > 0   (decore: é o teste instantâneo de 2ª ordem!)

3ª ordem: s³ + a·s² + b·s + c
 s³: 1, b | s²: a, c | s¹: (ab−c)/a | s⁰: c
 ⇒ ESTÁVEL ⇔ a > 0, c > 0 E a·b > c
```

**Fala:** "Para 2ª ordem nem precisa de tabela: olhou os sinais, matou a questão. Para 3ª ordem, o produto do meio tem que ganhar do de fora — a·b > c."

## Q4 — FTMF e estabilização por realimentação (15 min)

**Quadro (linha a linha):**

```
G(s) = N(s)/D(s), controle P com ganho k, realimentação unitária
T(s) = kG/(1 + kG) = kN/(D + kN)

Exemplo: G(s) = 1/(s − 1)  ← INSTÁVEL (polo +1)
 T(s) = k/(s − 1 + k) → polo em s = 1 − k
 ESTÁVEL ⇔ k > 1.   Realimentação moveu o polo para o SPE!
```

## Q5 — Vantagens: sensibilidade e perturbação (20 min)

**Quadro — sensibilidade ao ganho (exemplo numérico):**

```
Planta: G = A (ganho puro). A varia: B = 0,2·A (20%).
MALHA ABERTA: y = A·r → variação na saída = 20%·(Ar)/(Ar)... erro relativo:
 y nominal = A ; y real = 1,2A ⇒ variação de 16,7%... 
 (fazer a conta exata: MA acompanha 100% da variação relativa da planta)
MALHA FECHADA: T = kA/(1+kA)
 kA = 10:  T = 10/11 = 0,909 → com 1,2·(kA)=12: T = 12/13 = 0,923 ⇒ varia só 1,5%!
 kA = 2:   T = 2/3 → 2,4/3,4 ⇒ varia 5,6%
REGRA DE BOLSO: quanto MAIOR o ganho de malha kA, MENOR a sensibilidade.
```

**Quadro — perturbação:**

```
Perturbação d somada na saída da planta (vento no servo, porta do forno abrindo):
 MA: y = G·u + d → perturbação passa INTEGRALMENTE
 MF: y = (kG·r + d)/(1 + kG) → efeito de d dividido por (1 + kA)
 ⇒ a realimentação ATENUA perturbações pelo fator 1/(1 + ganho de malha)
(fig m1_fig05_servo_malha.png — recordar a demo do servo com as massas)
```

## Q6 — Faixa de estabilidade (20 min)

**Quadro — Exemplo 1 (linha a linha):**

```
T(s) com denominador s³ + 6s² + 11s + (6 + k). Estável para quais k?
Routh: s³: 1, 11 | s²: 6, 6+k | s¹: (66 − 6 − k)/6 = (60−k)/6 | s⁰: 6+k
Condições: (60−k)/6 > 0 ⇒ k < 60 ;  6 + k > 0 ⇒ k > −6
FAIXA: −6 < k < 60
Nos limites: k = 60 ⇒ polos −6, ±j√11 (±j3,32) — oscilação pura (marginal)
             k = −6 ⇒ polo na origem (marginal)
```

**Quadro — Exemplos 2 e 3:**

```
T(s) = 10/(s³ + 8s² + 12s + 10k)...  ⇒ Routh ⇒ 0 < k < 8,6
G com denominador s³ + 11s² + 8s − 20 (instável em MA!), controle k:
 s³ + 11s² + 8s + (10k − 20) ⇒ Routh ⇒ 2 < k < 10,8
 (a realimentação ESTABILIZOU — mas só numa faixa! Ganho alto demais
  também desestabiliza. Intuição: atraso + ganho alto = oscilação.)
G(s) = 1/(s² + 2s − 3): denominador MF s² + 2s + (k−3) ⇒ k > 3
```

**Fala:** "A intuição do iniciante diz 'ganho maior é sempre melhor'. Errado: todo sistema real tem atraso, e ganho alto com atraso vira oscilação. Existe faixa ótima — e o Routh entrega ela de graça."

## Q7 — Erro em regime em malha aberta (15 min)

**Quadro:**

```
MA: E(s) = R(s) − Y(s) = R(s)[1 − G(s)]... na verdade, em MA o "erro" é
 r − y. Com TVF: ess = lim s→0 s·E(s)

Exemplos (u = degrau unitário, exceto indicado):
 G = 1/[(s+1)(s+2)]:  yss = G(0)·1 = 1/2 ⇒ ess = 0,5
 G = 2/[(s+1)(s+2)]:  yss = 1 ⇒ ess = 0  (ganho unitário em DC — sorte do projeto)
   com RAMPA: yss diverge; erro cresce: ess medido = 1,5... 
   (em MA o erro à rampa depende da inclinação: fazer a conta pelo TVF)
CUIDADO — ARMADILHA: TVF só vale se a saída CONVERGE!
 G = (s²+29s+208)/(s³+6s²+10s+208): numerador bonito, denominador instável
 (Routh: 1ª coluna troca de sinal) ⇒ y diverge ⇒ "ess" do TVF é MENTIRA.
 SEMPRE verificar estabilidade ANTES de aplicar o TVF.
(fig m1_fig13_erro_regime.png)
```

## Q8 — Erro em malha fechada: kp, kv, ka (20 min)

**Quadro (linha a linha):**

```
MF unitária, L(s) = kG(s) = FT de malha (aberta)
E(s) = R(s)/(1 + L(s))   ⇒   ess = lim s→0 s·R(s)/(1 + L(s))

DEGRAU:  ess = 1/(1 + kp),   kp = lim s→0 L(s)      — constante de posição
RAMPA:   ess = 1/kv,         kv = lim s→0 s·L(s)     — constante de velocidade
PARÁBOLA: ess = 1/ka,        ka = lim s→0 s²·L(s)    — constante de aceleração

TIPO do sistema = nº de polos de L(s) na ORIGEM (integradores puros)
 tipo 0: kp = k·b0/a0 (finito) ⇒ erro ao degrau FINITO; rampa/parábola: ∞
 tipo 1: kp = ∞ ⇒ erro ao degrau 0; kv finito ⇒ erro à rampa finito
 tipo 2: erros a degrau e rampa 0; erro à parábola finito

Exemplo: L(s) = k/[(s+1)(s+2)] (tipo 0): kp = k/2 ⇒ ess = 1/(1 + k/2) = 2/(2+k)
```

**⚠️ Errata da legenda (corrigir em aula):** num dos vídeos o professor diz "tipo 0 apresenta erro infinito para entrada degrau" — o correto é **erro FINITO ao degrau** (e infinito à rampa).

## Q9 — Fechamento e ponte com o projeto (5 min)

**Quadro:**

```
RESUMO DO TÓPICO:
 BIBO ⇔ polos no SPE | Routh conta polos no SPD sem fatorar
 Realimentação: estabiliza, reduz sensibilidade, atenua perturbação
 Erro em regime: TVF + kp/kv/ka; tipo do sistema manda
 TUDO isso assumindo: sistema estável em MF (verificar ANTES do TVF!)
Próximo tópico: QUÃO BEM o sistema responde (transitório) — e o primeiro
 projeto de verdade: escolher k para atender especificações.
```

---

## Perguntas para a turma

1. s² + 4s − 5: estável? (Não — b < 0; um polo no SPD)
2. Por que a realimentação atenua a perturbação? (divide por 1 + kA)
3. Tipo 1 tem erro nulo a quais entradas? (degrau; à rampa é finito)
4. Antes de usar o TVF, o que conferir? (estabilidade!)

**Preparação do professor:** vídeos 01–06 do tópico 1.3; refazer as tabelas de Routh (principalmente a 4ª ordem e a faixa −6 < k < 60); figuras `m1_fig05, m1_fig13` no projetor.
