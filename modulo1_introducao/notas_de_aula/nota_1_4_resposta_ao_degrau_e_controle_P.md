# Nota de Aula 1.4 — Resposta ao Degrau de 2ª Ordem e Controle Proporcional

> **Documento do professor** — guia de quadro, linha a linha, com falas sugeridas.
> Duração prevista: 2 h (semana 5). Lab associado: **Lab 04**. Encerra o **Projeto P** (primeira nota de projeto).

**Mapa dos vídeos deste tópico (não mostrar aos alunos):**

| Vídeo | Título | Uso na aula |
|---|---|---|
| 01 | Por que 2ª Ordem | Dominância; quando aproximação vale/falha (Q1) |
| 02 | Diferentes Respostas | Super/sub/criticamente amortecido, não amortecido (Q2) |
| 03 | Características da Resposta Subamortecida | Mp, tp, tr, ts (Q3) |
| 04 | Parametrização de 2ª Ordem | σ, ωd, ζ, ωn; geometria dos polos (Q4) |
| 05 | Fórmulas de 2ª Ordem | Derivação de Mp, tp, tr, ts (Q5–Q6) |
| 06 | Projeto: Overshoot | ζ de Mp; k = 0,718; fórmula literal (Q7) |
| 07 | Projeto: Instante de Pico | ωd de tp; k = 1,25; fórmula literal (Q8) |

---

## Q1 — Por que estudar 2ª ordem? (10 min)

**Quadro:**

```
Sistemas de ordem superior ≈ soma de parcelas de 1ª e 2ª ordem.
POLO DOMINANTE: o mais próximo do eixo imaginário (menor |σ|) → decai mais
 devagar → DITA a resposta. Polos 5×+ mais rápidos: desprezíveis.

Boa aproximação:  5/[(s²+s+1)(s+5)]  ≈ 5/[5(s²+s+1)]  (polo −5 = 5× σ dos demais)
                  64/[(s²+s+1)(s²+12s+64)] ≈ (par −6±j5,3 é 6× mais rápido)
Aproximação RUIM: 1/[(s²+s+1)(s+1)]: polo −1 tão lento quanto o par!
 Mp real 16,3% × Mp da aproximação 8,1% → erro grosseiro.
(fig m1_fig14_aproximacoes.png)
```

**Fala:** "Dominância é a licença poética do engenheiro: se um polo está 5 vezes mais longe do eixo, ele morre 5 vezes mais rápido e a gente finge que ele não existe."

## Q2 — Os quatro tipos de resposta (15 min)

**Quadro:**

```
G(s) = ωn²/(s² + 2ζωn·s + ωn²), polos dependem de ζ:
 ζ > 1: SUPERAMORTECIDO — 2 polos reais; sobe devagar, sem ultrapassar
 ζ = 1: CRITICAMENTE AMORTECIDO — polo duplo real; o mais rápido SEM Mp
 0 < ζ < 1: SUBAMORTECIDO — par complexo conjugado; oscila e ultrapassa
 ζ = 0: NÃO AMORTECIDO — polos ±jωn; oscila para sempre
(fig m1_fig15_tipos_resposta.png — comparar os 4 no mesmo gráfico)
```

## Q3 — As quatro grandezas da resposta subamortecida (15 min)

**Quadro:**

```
Mp — máximo sobressinal: o quanto ultrapassa o valor final (%)
tp — instante de pico: quando ocorre o máximo
tr — tempo de subida (0→100%): 1º cruzamento do valor final
ts — tempo de acomodação (±5%): entrada DEFINITIVA na faixa
(fig m1_fig16_caracteristicas.png — anotar as 4 grandezas na curva)

Exemplo canônico: G(s) = 25/(s² + 4s + 25)
 Mp = 25,4% | tp = 0,69 s | tr = 0,43 s | ts = 1,5 s
 (medir no gráfico com a turma — depois conferir pelas fórmulas)
```

## Q4 — Parametrização: σ, ωd, ζ, ωn (20 min)

**Quadro (linha a linha):**

```
Polos: s² + 2ζωn·s + ωn² = 0 ⇒ s = −ζωn ± j·ωn√(1−ζ²) = −σ ± jωd

 σ = ζωn   (parte real: velocidade de decaimento do envelope e^{−σt})
 ωd = ωn√(1−ζ²)  (frequência amortecida: a oscilação que se vê)
 ωn: frequência natural (distância do polo à origem!)
 ζ: razão de amortecimento; β = arccos ζ (ângulo do polo com o eixo real)

GEOMETRIA: |polo| = √(σ² + ωd²) = ωn ;  cos β = σ/ωn = ζ
(fig m1_fig17_polos_sigma_wd.png — desenhar o triângulo no plano s)

TRÊS SISTEMAS (fig m1_fig18_tres_sistemas.png): mover σ move o polo na
 horizontal (muda ts); mover ωd move na vertical (muda tp, oscilação);
 mover ζ move sobre o círculo de raio ωn (muda Mp).
```

## Q5 — Derivação das fórmulas (25 min)

**Quadro — resposta ao degrau (linha a linha):**

```
Y(s) = ωn²/[s(s²+2ζωn·s+ωn²)] ⇒ (inversas da tabela, completar quadrados)
 y(t) = 1 − [e^{−σt}/√(1−ζ²)]·sen(ωd·t + φ),  φ = arccos ζ

INSTANTE DE PICO: dy/dt = 0 ⇒ sen(ωd·t) = 0 ⇒ ωd·tp = π
 ⇒ tp = π/ωd          (EXATA)

MÁXIMO SOBRESSINAL: y(tp) = 1 + e^{−σπ/ωd}
 ⇒ Mp = e^{−ζπ/√(1−ζ²)}   (EXATA; em fração 0–1; ×100 p/ %)
 Inversa (deduzir isolando ζ — cai em prova!):
 ⇒ ζ = √[ ln²Mp / (π² + ln²Mp) ]     (Mp em FRAÇÃO, não %!)

TEMPO DE SUBIDA: y(tr) = 1 ⇒ sen(ωd·tr + φ) = 0 ⇒ ωd·tr + φ = π
 ⇒ tr = (π − β)/ωd,  β = arccos ζ   (EXATA)

TEMPO DE ACOMODAÇÃO: envelope ±e^{−σt}/√(1−ζ²) dentro de 5%:
 aproximação PESSIMISTA: e^{−σ·ts} = 0,05 ⇒ ts ≈ 3/σ
 (despreza o 1/√(1−ζ²) ⇒ fórmula simples e conservadora)
```

## Q6 — Conferindo o exemplo canônico (10 min)

**Quadro:**

```
G(s) = 25/(s² + 4s + 25): ωn² = 25 ⇒ ωn = 5 ; 2ζωn = 4 ⇒ ζ = 0,4
 σ = ζωn = 2 ; ωd = 5·√(1−0,16) = 5·0,9165 = 4,58
 Mp = e^{−0,4π/0,9165} = e^{−1,371} = 0,254 ⇒ 25,4% ✓ (medido: 25,4%)
 tp = π/4,58 = 0,686 s ✓ (medido: 0,69)
 tr = (π − arccos 0,4)/4,58 = (3,1416 − 1,159)/4,58 = 0,433 s ✓ (medido: 0,43)
 ts ≈ 3/2 = 1,5 s ✓ (medido: 1,52 — pessimista, como prometido)
```

## Q7 — PROJETO 1: atender Mp máximo (20 min)

**Quadro (linha a linha):**

```
PLANTA: G(s) = 1/[s(s+1)], controle P: u = k·e, realimentação unitária
 T(s) = k/[s² + s + k]  ⇒  ωn² = k, 2ζωn = 1

ESPECIFICAÇÃO: Mp ≤ 10%
1) ζ = √[ln²(0,1)/(π²+ln²(0,1))] = √[5,301/(9,870+5,301)] = √0,3493 = 0,591
2) 2ζωn = 1 ⇒ ωn = 1/(2·0,591) = 0,846
3) k = ωn² = 0,716 ⇒ k = 0,718 (arredondando nos cálculos)
VERIFICAÇÃO (simulação): Mp medido = 10,1% ✓
(fig m1_fig19_projeto_mp.png — antes × depois)

FÓRMULA LITERAL (G = 1/[s(s+a)], especificação Mp):
 ζ pela fórmula inversa; 2ζωn = a ⇒ ωn = a/(2ζ)
 ⇒ k = a²/(4ζ²) = a²(π² + ln²Mp)/(4·ln²Mp)
```

## Q8 — PROJETO 2: atender tp (15 min)

**Quadro (linha a linha):**

```
MESMA PLANTA. ESPECIFICAÇÃO: tp = 3,14 s (= π s — escolhido a dedo!)
1) ωd = π/tp = 1 rad/s
2) Polos: −σ ± j1. Mas 2ζωn = 1 ⇒ σ = ζωn = 0,5 (fixo pela planta!)
3) ωn² = σ² + ωd² = 0,25 + 1 = 1,25 ⇒ k = 1,25
VERIFICAÇÃO: polos −0,5 ± j1,0 ; tp medido = 3,14 s ✓ ; Mp = 20,7%
 (Mp não foi especificado — saiu o que saiu. Uma especificação por vez
  com UM grau de liberdade!)
(fig m1_fig20_projeto_tp.png)

FÓRMULA LITERAL (G = 1/[s(s+a)], especificação tp):
 ωd = π/tp ; σ = a/2 (fixo) ⇒ k = ωn² = σ² + ωd² = a²/4 + π²/tp²
```

## Q9 — Fechamento do módulo (5 min)

**Quadro:**

```
O QUE APRENDEMOS NO MÓDULO 1:
 modelo (EDO→FT) → estabilidade (BIBO, Routh) → regime (erro, kp/kv/ka)
 → transitório (Mp, tp, tr, ts) → PROJETO: k para atender especificação.
LIMITAÇÃO DO CONTROLE P: 1 grau de liberdade = 1 especificação por vez.
 E se quisermos Mp E tp E erro nulo? → precisamos de controladores
 mais ricos (módulos seguintes: lugar das raízes, resposta em frequência).
Projeto P (nota): reproduzir os dois projetos + simulação no Lab 04.
```

---

## Perguntas para a turma

1. Se ζ cresce (mantido ωn), o que acontece com Mp? (diminui — e com ts? diminui até certo ponto)
2. Por que ts = 3/σ é "pessimista"? (despreza 1/√(1−ζ²) < 1... na verdade despreza um fator que AMPLIFICA o envelope — a fórmula garante margem)
3. No projeto, quem fixa σ = 0,5 na planta 1/[s(s+1)]? (o coeficiente de s: 2ζωn = 1)
4. Quantas especificações o controle P atende por vez? (uma)

**Preparação do professor:** vídeos 01–07 do tópico 1.4; refazer as duas derivações de projeto e CONFERIR os valores simulados (10,1% e tp = 3,14 s); figuras `m1_fig14`–`m1_fig20` no projetor.
