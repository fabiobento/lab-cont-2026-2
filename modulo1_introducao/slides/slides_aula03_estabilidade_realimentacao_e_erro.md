# Slides — Aula 03: Estabilidade, Realimentação e Erro em Regime

> **Documento do professor.** Formato: **Tela** / **Figura** / **Roteiro falado**. Vídeos de apoio à preparação: tópico 1.3, vídeos 01–06.

---

### Slide 1 — Abertura

**Tela:** Aula 03: O sistema explode? E se sim, a realimentação conserta?

**Roteiro:** "Hoje respondemos a pergunta número um da engenharia de controle: é estável? E descobrimos por que fechar a malha é a ideia mais poderosa do curso."

---

### Slide 2 — Estabilidade BIBO

**Tela:** BIBO: TODA entrada limitada → saída limitada. Condição: TODOS os polos com parte real negativa. Exemplos divergentes: 1/s + degrau → rampa; 1/(s²+1) + cos t → (t/2)sen t.

**Figura:** m1_fig12_bibo.png

**Roteiro:** "A definição é exigente: TODA entrada limitada. Um único contra-exemplo derruba. Polo na origem? Degrau vira rampa. Polos ±j? Entrada na frequência certa vira ressonância."

---

### Slide 3 — O problema de fatorar

**Tela:** Polos de ordem alta exigem fatorar polinômios — inviável na mão. Alternativa: CRITÉRIO DE ROUTH — conta polos no semiplano direito SEM fatorar.

**Roteiro:** "Bhaskara para 5ª ordem não existe. Routh dá a informação que importa — quantos polos perigosos — com uma tabelinha de multiplicar e dividir."

---

### Slide 4 — Montando a tabela de Routh

**Tela:** s³+6s²+11s+6: linhas s³: 1, 11 | s²: 6, 6 | s¹: (66−6)/6 = 10 | s⁰: 6. 1ª coluna sem troca de sinal → estável (confira: (s+1)(s+2)(s+3)).

**Roteiro:** "Alternem os coeficientes nas duas primeiras linhas; daí para baixo, cada elemento é um determinante normalizado. Regra: trocas de sinal na primeira coluna = polos no semiplano direito."

---

### Slide 5 — Routh: casos com troca de sinal

**Tela:** s³+6s²+11s+72 → 1ª coluna 1, 6, −1, 72 → 2 trocas → 2 polos no SPD. 4ª ordem: s⁴+2s³−s²+20s+5 → 1, 2, −11, 20,9, 5 → 2 trocas.

**Roteiro:** "Façam comigo no caderno. E atenção: Routh diz QUANTOS, não ONDE — para localizar, só fatorando ou simulando."

---

### Slide 6 — Atalhos literais

**Tela:** 2ª ordem s²+as+b: estável ⇔ a>0 E b>0. 3ª ordem s³+as²+bs+c: estável ⇔ a>0, c>0 E a·b>c.

**Roteiro:** "2ª ordem: olhe os sinais e mate a questão. 3ª ordem: o produto do meio tem que ganhar do de fora. Decorem — cai em toda prova e em todo projeto."

---

### Slide 7 — FTMF: fechando a malha

**Tela:** G = N/D, controle k, MF unitária: T(s) = kG/(1+kG) = kN/(D+kN). Ex.: G = 1/(s−1) → polo em 1−k → ESTÁVEL ⇔ k>1. A realimentação MOVE os polos!

**Roteiro:** "Olhem a álgebra trabalhando para nós: o denominador de malha fechada é D + kN — o ganho k entra na conta dos polos. Controlar é isso: mover polos."

---

### Slide 8 — Três vantagens da realimentação

**Tela:** 1) Estabiliza (move polos). 2) Reduz sensibilidade: G=A com variação de 20% → MA 16,7% × MF 1,5% (kA=10). 3) Atenua perturbação por 1/(1+kA). Regra: ganho de malha alto ajuda — até certo ponto.

**Figura:** m1_fig05_servo_malha.png

**Roteiro:** "Lembrem do servo com massas: em malha fechada, a perturbação quase sumiu. Por quê? Porque o efeito dela foi dividido por (1+kA). E a variação da própria planta — envelhecimento, temperatura — também é engolida pela malha."

---

### Slide 9 — Faixa de estabilidade

**Tela:** T(s) com denominador s³+6s²+11s+(6+k): Routh → −6 < k < 60. Limites: k=60 → −6, ±j√11 (oscila); k=−6 → polo na origem. G com denominador s³+11s²+8s−20 → 2 < k < 10,8.

**Roteiro:** "Ganho maior é sempre melhor? NÃO. O segundo exemplo: a realimentação estabiliza uma planta instável — mas só numa faixa. Ganho alto demais desestabiliza, porque todo sistema real tem atraso. Instinto de projetista: sempre pergunte QUAL a faixa."

---

### Slide 10 — Erro em regime: malha aberta e a armadilha

**Tela:** MA: y(∞) = G(0)·r. Exemplos: G=1/[(s+1)(s+2)] → ess=0,5; G=2/[(s+1)(s+2)] → ess=0, rampa: erro cresce. ARMADILHA: TVF exige convergência — G=(s²+29s+208)/(s³+6s²+10s+208) é instável: o TVF mente!

**Figura:** m1_fig13_erro_regime.png

**Roteiro:** "Decorem a ordem das operações: PRIMEIRO estabilidade, DEPOIS valor final. Inverter essa ordem é o erro mais comum da prova — e da profissão."

---

### Slide 11 — Erro em malha fechada: kp, kv, ka

**Tela:** E(s) = R/(1+L), L = kG. Degrau: ess=1/(1+kp), kp=lim L(s). Rampa: ess=1/kv, kv=lim sL(s). Parábola: ess=1/ka, ka=lim s²L(s). TIPO = nº de polos na origem de L.

**Roteiro:** "O tipo do sistema é o RG dele: tipo 0 acompanha degrau com erro finito; tipo 1 zera o degrau e acompanha rampa com erro finito; tipo 2 zera os dois. Cada integrador na malha sobe um degrau na escada de precisão."

---

### Slide 12 — Tabela de erros e resumo

**Tela:** Tabela tipo × entrada (0: finito/∞/∞; 1: 0/finito/∞; 2: 0/0/finito). Resumo do tópico: BIBO ⇔ polos no SPE; Routh conta sem fatorar; MF estabiliza, insensibiliza, atenua; erro via kp/kv/ka — sempre após checar estabilidade.

**Roteiro:** "⚠️ Errata: em algum material por aí vocês lerão 'tipo 0 tem erro infinito ao degrau' — errado: tipo 0 tem erro FINITO ao degrau; infinito é à rampa. Próxima aula: QUÃO BEM o sistema responde — e o primeiro projeto de verdade."
