# Slides — Aula 04: Resposta ao Degrau de 2ª Ordem e Projeto de Controle P

> **Documento do professor.** Formato: **Tela** / **Figura** / **Roteiro falado**. Vídeos de apoio à preparação: tópico 1.4, vídeos 01–07. Esta aula encerra o **Projeto P** (nota).

---

### Slide 1 — Abertura

**Tela:** Aula 04: O transitório — e o primeiro projeto da vida de vocês.

**Roteiro:** "Até aqui: o sistema é estável e sabemos o erro no fim. Falta o meio do caminho: COMO ele chega lá. Hoje saem as fórmulas do transitório e o primeiro projeto com especificação de verdade."

---

### Slide 2 — Por que 2ª ordem?

**Tela:** Sistemas reais = soma de parcelas de 1ª/2ª ordem. Polo DOMINANTE: o mais lento (mais perto do eixo jω) dita a resposta. Regra prática: 5× mais longe → desprezível. Boa: 5/[(s²+s+1)(s+5)]. Ruim: 1/[(s²+s+1)(s+1)] — Mp real 16,3% × 8,1% da aproximação.

**Figura:** m1_fig14_aproximacoes.png

**Roteiro:** "Dominância é licença poética do engenheiro: polo 5 vezes mais longe morre 5 vezes mais rápido — a gente finge que não existe. Mas cuidado com a regra: 2× não é 5×."

---

### Slide 3 — Os quatro tipos de resposta

**Tela:** ζ>1 superamortecido (lento, sem Mp) | ζ=1 crítico (o mais rápido SEM ultrapassar) | 0<ζ<1 subamortecido (oscila e ultrapassa) | ζ=0 não amortecido (oscila para sempre).

**Figura:** m1_fig15_tipos_resposta.png

**Roteiro:** "Decorem a cara de cada uma. O interessante para controle é o subamortecido: é onde mora o trade-off rapidez × suavidade."

---

### Slide 4 — As quatro grandezas

**Tela:** Mp (sobressinal), tp (instante de pico), tr (subida 0–100%), ts (acomodação ±5%). Exemplo canônico: 25/(s²+4s+25) → Mp=25,4%, tp=0,69, tr=0,43, ts=1,5.

**Figura:** m1_fig16_caracteristicas.png

**Roteiro:** "Meçam comigo no gráfico: o pico, o primeiro cruzamento, a entrada definitiva na faixa de ±5%. Agora vamos prever esses números sem simular nada."

---

### Slide 5 — Parametrização: o triângulo dos polos

**Tela:** Polos −σ±jωd; σ=ζωn (velocidade do envelope), ωd=ωn√(1−ζ²) (oscilação visível), ωn=√(σ²+ωd²) (distância à origem), ζ=cos β.

**Figura:** m1_fig17_polos_sigma_wd.png

**Roteiro:** "Um triângulo retângulo esconde tudo: hipotenusa ωn, cateto horizontal σ, vertical ωd, e ζ é o cosseno do ângulo. Geometria do ensino médio governando o transitório."

---

### Slide 6 — Movendo os polos, movendo a resposta

**Tela:** Mover σ (horizontal) → muda ts. Mover ωd (vertical) → muda tp e a oscilação. Mover ζ (sobre o círculo de raio ωn) → muda Mp.

**Figura:** m1_fig18_tres_sistemas.png

**Roteiro:** "Guardem o mapa: especificação de tempo olha para σ e ωd; especificação de sobressinal olha para o ângulo. Projeto = colocar o polo no lugar certo."

---

### Slide 7 — As fórmulas (e suas deduções)

**Tela:** tp=π/ωd (exata) · Mp=e^(−ζπ/√(1−ζ²)) (exata) · ζ=√[ln²Mp/(π²+ln²Mp)] (inversa, Mp em fração!) · tr=(π−β)/ωd, β=arccos ζ (exata) · ts≈3/σ (pessimista, ±5%).

**Roteiro:** "No quadro: derivando y(t) e igualando a zero sai tp; y(tp)−1 sai Mp; isolando ζ sai a inversa — decorem, cai em prova. E ts=3/σ é conservador de propósito: desprezamos um fator que só ajuda."

---

### Slide 8 — Conferindo o canônico

**Tela:** 25/(s²+4s+25): ωn=5, ζ=0,4 → σ=2, ωd=4,58 → fórmulas: 25,4% / 0,686 / 0,433 / 1,5 × medidos: 25,4% / 0,69 / 0,43 / 1,52. ✓

**Roteiro:** "Fórmula exata bate no centésimo; a aproximada de ts erra para o lado seguro, como prometido. Isso é engenharia: saber exatamente onde a aproximação mora."

---

### Slide 9 — PROJETO 1: Mp ≤ 10%

**Tela:** Planta 1/[s(s+1)], controle P → T(s)=k/(s²+s+k). Passos: ζ=√[ln²(0,1)/(π²+ln²(0,1))]=0,591 → ωn=1/(2ζ)=0,846 → **k=0,718**. Simulação: Mp=10,1% ✓. Literal: k=a²/(4ζ²).

**Figura:** m1_fig19_projeto_mp.png

**Roteiro:** "Três linhas de conta e um ganho projetado — sem tentativa e erro. Esse é o método: especificação → ζ → ωn → k. E a verificação na simulação é obrigatória: projetista que não verifica entrega bug."

---

### Slide 10 — PROJETO 2: tp = 3,14 s

**Tela:** Mesma planta: ωd=π/tp=1 → σ=0,5 (a planta fixa!) → k=σ²+ωd²=**1,25**. Polos −0,5±j1,0. Simulação: tp=3,14 s ✓, Mp=20,7% (não especificado — saiu o que saiu). Literal: k=a²/4+π²/tp².

**Figura:** m1_fig20_projeto_tp.png

**Roteiro:** "Notem quem manda: o coeficiente de s da planta fixou σ=0,5 — nossa única liberdade era subir ou descer o polo na vertical. UM ganho, UMA especificação."

---

### Slide 11 — A limitação do controle P

**Tela:** Um grau de liberdade = uma especificação por vez. Mp E tp E erro nulo juntos? Impossível com k puro → controladores mais ricos nos próximos módulos.

**Roteiro:** "Façam a conta: cada especificação pede o polo num lugar diferente. Com um parâmetro só, não dá. Guardem essa frustração — ela é a motivação dos próximos dois módulos."

---

### Slide 12 — Projeto P: entrega

**Tela:** Relatório do Lab 04: os dois projetos (dedução + k + gráfico + verificação), a demonstração da impossibilidade conjunta, e o bônus (planta 1/[s(s+4)] → k=11,45).

**Roteiro:** "O relatório é curto e objetivo: dedução, número, gráfico, comentário. Quem entregar só o gráfico sem a dedução está fazendo análise, não projeto. Dúvidas até o lab."

---

### Slide 13 — Fechamento do Módulo 01

**Tela:** Mapa do módulo: modelo (EDO→FT) → estabilidade (BIBO, Routh) → regime (kp/kv/ka) → transitório (Mp, tp, tr, ts) → projeto P. Próximo módulo: o plano s trabalhando a nosso favor — Lugar das Raízes.

**Roteiro:** "Em quatro semanas vocês foram de 'o que é um sistema' a 'projetar ganho com especificação'. O Módulo 02 vai generalizar esse desenho: veremos TODOS os lugares onde os polos podem morar quando o ganho varia — o Lugar das Raízes."
