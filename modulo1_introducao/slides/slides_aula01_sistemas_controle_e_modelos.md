# Slides — Aula 01: Sistemas de Controle e Modelos Matemáticos

> **Documento do professor.** Formato de cada slide: **Tela** (o que aparece), **Figura** (arquivo em `imagens/` — todas as URLs no formato GitHub já estão na teoria), **Roteiro falado** (o que dizer). Vídeos de apoio à preparação: tópico 1.1, vídeos 01–07.

---

### Slide 1 — Abertura

**Tela:** Laboratório de Controle Automático — Módulo 01 · Aula 01: O que é um sistema (de controle)?

**Roteiro:** "Bem-vindos. Este é um curso de controle com sabor de laboratório: toda a teoria que virmos no quadro será reproduzida por vocês na simulação, no mesmo ciclo. Hoje respondemos três perguntas: o que é um sistema, o que é controlar e como descrevemos um sistema matematicamente."

---

### Slide 2 — O que é um sistema

**Tela:** Sistema = qualquer coisa que transforma entradas em saídas. Exemplos: forno elétrico (tensão → temperatura), carro (acelerador → velocidade), caixa d'água com descarga (válvula → nível).

**Figura:** m1_fig01_caixa_descarga.png

**Roteiro:** "A caixa d'água de Ktesibius, 250 a.C., é o avô de todos os controles automáticos. Reparem: o princípio — medir a saída e agir na entrada — não mudou em dois mil anos."

---

### Slide 3 — Entradas, saídas e perturbações

**Tela:** Diagrama SISO: u (entrada manipulada) → [SISTEMA] → y (saída). Perturbação d: entrada que NÃO controlamos (vento, porta do forno, ladeira).

**Figura:** (diagrama Mermaid da teoria §1.1.2)

**Roteiro:** "SISO: uma entrada, uma saída — o curso inteiro será assim. E já nasce aqui o drama do controle: o mundo insiste em mandar entradas que não pedimos. O nome disso é perturbação."

---

### Slide 4 — Objetivo do controle

**Tela:** Fazer a saída y seguir uma referência r, APESAR das perturbações, com requisitos: rapidez (tr, ts), precisão (erro), suavidade (Mp). Metáfora do elevador.

**Roteiro:** "Pensem no elevador: queremos que ele chegue rápido (rapidez), pare no nível certo (precisão) e sem solavanco nem ultrapassagem (suavidade). Controle é o equilíbrio desses três desejos — e eles brigam entre si."

---

### Slide 5 — O gráfico da saída

**Tela:** y × t é o documento central do curso. Forno: r = 180 °C. Carro: r = 100 km/h.

**Figura:** m1_fig03_graficos_saida.png

**Roteiro:** "Decorem este gráfico: tudo que faremos no curso — estabilidade, erro, transitório — é lido AQUI. Quando eu disser 'tempo de acomodação', vocês já sabem onde olhar."

---

### Slide 6 — Requisitos no gráfico

**Tela:** As quatro grandezas: tr, ts, Mp, erro em regime — prévia informal (formalização na aula 4).

**Figura:** m1_fig04_requisitos_grafico.png

**Roteiro:** "Não decorem fórmulas hoje. Guardem os NOMES e onde cada um mora no gráfico: subida, acomodação, sobressinal e o erro que sobra no fim."

---

### Slide 7 — Análise × Projeto

**Tela:** ANÁLISE: dado o sistema, prever o comportamento. PROJETO: dado o comportamento desejado, escolher o controlador. Este curso: os dois, terminando em projeto.

**Roteiro:** "Análise é ler a radiografia; projeto é receitar o remédio. O semestre inteiro caminha para o projeto — na aula 4 vocês já farão o primeiro de verdade."

---

### Slide 8 — Malha aberta × malha fechada

**Tela:** MA: u não depende de y. MF: mede y, compara com r, e = r − y, u = k·e. Demo do servo com massas.

**Figura:** m1_fig05_servo_malha.png

**Roteiro:** "Controle remoto da TV é malha aberta: você aperta e torce. Dirigir é malha fechada: o olho mede, o cérebro compara, a mão corrige. No servo com 2 rad/s de referência: em malha aberta a massa pesada derrubou a velocidade; em malha fechada, quase nem sentiu."

---

### Slide 9 — O controle proporcional

**Tela:** u = k·e. Túnel de vento: erro grande → sopro forte; erro pequeno → sopro fraco.

**Roteiro:** "O controlador mais parcimonioso do mundo: sopra proporcionalmente ao erro. É o primeiro que projetaremos — e vocês verão suas virtudes E suas limitações."

---

### Slide 10 — Modelos matemáticos: por quê

**Tela:** Modelo = EDO que aproxima o sistema. Parcimonioso: nem detalhado demais, nem grosseiro demais. Procedimento: leis físicas → EDO → (aula 2) função de transferência.

**Roteiro:** "Modelo bom é modelo preguiçoso: captura o essencial com o mínimo de equações. Lembrem do forno: se a dinâmica que interessa é de minutos, não modelamos o jitter de milissegundos da rede elétrica."

---

### Slide 11 — Massa-mola-amortecedor

**Tela:** M·ÿ = u − B·ẏ − K·y → ÿ + (B/M)ẏ + (K/M)y = (1/M)u

**Figura:** m1_fig07_massa_mola.png

**Roteiro:** "Newton: a resultante acelera a massa. A mola puxa de volta, o amortecedor freia. Pronto — está aí a EDO, uma linha de física e duas de arrumação."

---

### Slide 12 — RLC e Motor CC

**Tela:** RLC: v̈C + (R/L)v̇C + (1/LC)vC = (1/LC)v. Motor CC (velocidade): ÿ + (R/L)ẏ + (k²/LJ)y = (k/LJ)u — derivado de T = k·i, vM = k·ẏ, T = J·ÿ.

**Figuras:** m1_fig08_rlc.png · m1_fig09_motor_cc.png

**Roteiro:** "Reparem o milagre: três sistemas completamente diferentes — mecânico, elétrico, eletromecânico — e todos caem na MESMA forma: ÿ + a1·ẏ + a0·y = b0·u. É por isso que a teoria de controle existe: ela é sobre essa forma, não sobre o objeto."

---

### Slide 13 — A forma geral e o que vem a seguir

**Tela:** ÿ + a1ẏ + a0y = b0u — mas resolver EDO na unha para cada caso? Não. Próxima aula: Transformada de Laplace — derivada vira multiplicação por s.

**Roteiro:** "Na próxima aula vem a ferramenta que faz a engenharia de controle ser viável: a Transformada de Laplace. Lembrem do lema do curso: somos preguiçosos — no bom sentido. Tragam a tabela de transformadas."
