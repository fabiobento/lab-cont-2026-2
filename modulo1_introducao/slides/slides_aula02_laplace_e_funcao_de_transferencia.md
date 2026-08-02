# Slides — Aula 02: Transformada de Laplace e Função de Transferência

> **Documento do professor.** Formato: **Tela** / **Figura** / **Roteiro falado**. Vídeos de apoio à preparação: tópico 1.2, vídeos 01–03.

---

### Slide 1 — Abertura

**Tela:** Aula 02: Da EDO à Função de Transferência — a ferramenta central do curso.

**Roteiro:** "Hoje ganhamos a superpotência do curso. Até aqui, modelo era EDO — e resolver EDO para cada entrada é trabalho braçal. Depois de hoje: álgebra."

---

### Slide 2 — Para quem vale a TL

**Tela:** Sistemas LIT: Lineares (combinação linear na entrada → combinação linear na saída) + Invariantes no tempo (mesma entrada, mesma saída, sempre). Como reconhecer: EDO ordinária, linear, coeficientes constantes.

**Roteiro:** "Aviso aos matemáticos: este é um curso de engenharia, e engenharia é saber o quê, quando e até onde aproximar. Sistema não é LIT? Ou aproximamos, ou ele vai para outro curso."

---

### Slide 3 — A definição (e o alívio)

**Tela:** F(s) = ∫₀^∞ e^(−st) f(t) dt, s ∈ ℂ. "Empacotamento" do sinal. Não vamos calcular essa integral: vamos usar as PROPRIEDADES.

**Roteiro:** "Integral impronunciável, número complexo — e boa notícia: ninguém aqui vai integrar nada. Somos preguiçosos: outros já integraram; nós usamos a tabela e as propriedades."

---

### Slide 4 — As três propriedades que importam

**Tela:** P1) Linearidade. P2) Derivada com CI nulas: L{ḟ} = s·F(s) ⇒ L{f̈} = s²F(s) ⇒ L{f⁽ⁿ⁾} = sⁿF(s). P3) TVF: lim_{t→∞} f(t) = lim_{s→0} sF(s) (se converge!).

**Roteiro:** "A P2 é a mágica: cada derivada vira um s multiplicando. Dedução no quadro: se g = ḟ, então L{f̈} = L{ġ} = s·G(s) = s·(sF(s)) = s²F(s). E a P3 nos dará o erro em regime sem resolver nada — daqui a duas aulas."

---

### Slide 5 — Função de Transferência

**Tela:** ÿ + a1ẏ + a0y = b0u → (Laplace, CI nulas) → G(s) = Y(s)/U(s) = b0/(s² + a1s + a0). Vale para QUALQUER entrada. Y(s) = G(s)·U(s).

**Roteiro:** "FT é a razão entre as transformadas da saída e da entrada, com condições iniciais nulas. Saída no tempo = FT × entrada... no mundo de Laplace. Multiplicação em vez de EDO."

---

### Slide 6 — O atalho: copiar coeficientes

**Tela:** Numerador ← derivadas da ENTRADA; denominador ← derivadas da SAÍDA; nº de derivadas = expoente. Exemplos: ÿ+2ẏ+3y=u → 1/(s²+2s+3); y⃛+8ÿ+4ẏ=2u → 2/(s³+8s²+4s); ÿ+3ẏ+5y=2ů+u → (2s+1)/(s²+3s+5). Inverso também vale.

**Roteiro:** "Vejam o alívio: escrever a FT é copiar. E o caminho inverso — da FT à EDO — é igualmente mecânico. Façam o exercício relâmpago: G = (s+1)/(s²+5s+10), qual a EDO?"

---

### Slide 7 — Polos e zeros

**Tela:** POLOS = raízes do denominador (o futuro do sistema mora aqui). ZEROS = raízes do numerador. Raízes de polinômio real: reais ou pares conjugados. Bhaskara: s²+3s+2 → −1,−2 → (s+1)(s+2); s²+2s+2 → Δ<0 → −1±i.

**Roteiro:** "Decorem esta frase: a personalidade do sistema está nos polos do denominador. Complexos conjugados? Vai oscilar. Reais negativos? Vai deslizar. Positivos? Vai explodir — próxima aula."

---

### Slide 8 — A tabela de transformadas

**Tela:** degrau ↔ 1/s | rampa ↔ 1/s² | e^(at) ↔ 1/(s−a) | sen(ωt) ↔ ω/(s²+ω²) | e^(at)sen(ωt) ↔ ω/((s−a)²+ω²) + demais linhas.

**Figura:** m1_fig10_sinais_tabela.png

**Roteiro:** "Leiam os sinais: a > 0 diverge, a < 0 apaga; ω gira; o sinal de a no envelope decide se a oscilação cresce ou morre. Esta tabela estará disponível nas provas — mas quem usa todo dia acaba decorando."

---

### Slide 9 — O problema: Y(s) não está na tabela

**Tela:** ÿ+3ẏ+2y=2u, degrau: Y(s) = 2/[s(s+1)(s+2)]. Não consta na tabela. Solução: FRAÇÕES PARCIAIS — quebrar em pedaços que constam.

**Roteiro:** "Quase nunca Y(s) está na tabela inteiro. A saída é decompor: escrever como soma de frações simples, inverter cada uma, somar — e a linearidade (P1) garante que isso é legítimo."

---

### Slide 10 — Frações parciais: MMC

**Tela:** 2/[s(s+1)(s+2)] = A/s + B/(s+1) + C/(s+2) → 2 = A(s+1)(s+2) + Bs(s+2) + Cs(s+1) → A=1, B=−2, C=1 → y(t) = 1 − 2e^(−t) + e^(−2t).

**Roteiro:** "MMC resolve sempre: agrupe por potências de s, monte o sisteminha, resolva. E CONFIRA somando as frações de volta — conferir é de graça."

---

### Slide 11 — O truque dos resíduos

**Tela:** Ri = (s−pi)·Y(s)|_{s=pi} — "cubra o fator, substitua o polo". Ex.: 20/[s(s+1)(s+10)]: A=2, B=−20/9, C=2/9 → y(t) = 2 − (20/9)e^(−t) + (2/9)e^(−10t).

**Figura:** m1_fig11_saida_fracoes.png

**Roteiro:** "O MMC monta um sistema; o truque dá cada resíduo numa linha. Multiplique pelos dois lados o denominador da fração e faça s igual ao polo — o fator some dos outros termos."

---

### Slide 12 — Polos repetidos

**Tela:** Y(s) = 2/[(s+1)²(s+2)] = D/(s+1) + E/(s+1)² + F/(s+2). Truque dá E=2 e F=2; D pela soma: D=−2. y(t) = −2e^(−t) + 2t·e^(−t) + 2e^(−2t). Lembre: 1/(s+a)² ↔ t·e^(−at).

**Roteiro:** "Polo repetido: o truque só pega o resíduo da potência mais alta e os dos polos simples; o resto, feche pela soma — que ainda confere os outros. Não fechou? Algum resíduo está errado."

---

### Slide 13 — Recapitulando e ponte

**Tela:** Hoje: LIT → TL → G(s) → polos → frações parciais → y(t). Próxima aula: o que os polos dizem sobre ESTABILIDADE — e por que realimentar muda tudo.

**Roteiro:** "Saímos da EDO e chegamos a y(t) só com álgebra. Na próxima aula fazemos a pergunta mais importante do curso: o sistema explode ou não? E a resposta cabe numa tabelinha — o critério de Routh."
