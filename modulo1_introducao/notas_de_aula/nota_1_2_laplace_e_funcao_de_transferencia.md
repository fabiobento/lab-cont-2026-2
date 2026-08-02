# Nota de Aula 1.2 — Transformada de Laplace e Função de Transferência

> **Documento do professor** — guia de quadro, linha a linha, com falas sugeridas.
> Duração prevista: 2 h (semana 3). Lab associado: **Lab 02**.

**Mapa dos vídeos deste tópico (não mostrar aos alunos):**

| Vídeo | Título | Uso na aula |
|---|---|---|
| 01 | Transformada de Laplace | Linearidade, invariância, LIT; definição; propriedades; TVF (Q1–Q2) |
| 02 | Função de Transferência | G(s) copiando coeficientes; polos e zeros; Bhaskara; forma fatorada (Q3–Q4) |
| 03 | Calculando a Saída do Sistema | Tabela de TL; frações parciais; truque dos resíduos; polos repetidos (Q4–Q6) |

---

## Q1 — Linearidade e invariância no tempo (20 min)

**Quadro:**

```
COMBINAÇÃO LINEAR = soma ponderada (pesos reais)
 ex.: 1·u1 + 2u2 + 2u3 ;  21u1 − 7u2 + √3·u3 ;  0·u1 + 0,4u2 − √2·u3

SISTEMA LINEAR: u1 → y1 e u2 → y2  ⇒  α·u1 + β·u2 → α·y1 + β·y2
 (para TODA combinação linear de quaisquer entradas)

SISTEMA INVARIANTE NO TEMPO: entrada atrasada ⇒ saída atrasada do mesmo tanto
 (mesma entrada hoje, amanhã ou daqui a um mês ⇒ mesma saída)

Curso: sistemas LIT/LTI (Lineares e Invariantes no Tempo)
Como reconhecer: EDO ORDINÁRIA, LINEAR, com COEFICIENTES CONSTANTES
 ordinária: derivadas só em t | linear: combinação linear das derivadas
 coeficientes constantes: a2, a1, a0, b2, b1, b0 ∈ ℝ
Não é LIT? → aproximação ou técnicas avançadas (outros cursos)
```

**Fala:** "Aviso para os matemáticos de plantão que gostam de rigor: este é um curso de engenharia, e na engenharia fazemos aproximações. O segredo é saber o quê, quando e até onde aproximar. Lembrem do parcimonioso: modelo nem detalhado demais, nem grosseiro demais."

## Q2 — A Transformada de Laplace e suas propriedades (25 min)

**Quadro:**

```
DEFINIÇÃO (unilateral à direita):
 F(s) = ∫₀^∞ e^(−st) f(t) dt ,   s ∈ ℂ

 "Empacotamento" do sinal — interessam as PROPRIEDADES, não a integral!

P1) Linearidade: TL da combinação linear = combinação linear das TLs
P2) Derivada (CI nulas, f(0)=0):  L{ḟ} = s·F(s)
P3) Teorema do Valor Final (se f(t) converge):
    lim_{t→∞} f(t) = lim_{s→0} s·F(s)
```

**Quadro — dedução de L{f̈} (linha a linha):**

```
Seja g = ḟ. Então f̈ = ġ.
L{f̈} = L{ġ} = s·G(s)         (por P2, se g(0) = ḟ(0) = 0)
G(s) = L{ḟ} = s·F(s)         (por P2, se f(0) = 0)
∴ L{f̈} = s·(s·F(s)) = s²·F(s)
Mesmo raciocínio: L{f⁽ⁿ⁾} = sⁿ·F(s)
⇒ CI nulas: cada derivada vira um fator s multiplicando a transformada.
```

**Fala:** "Uma integral de zero a infinito, que meda! Número complexo! Não precisa ter medo: nós não vamos usá-la diretamente. Calcular essa integral para várias funções seria desperdício de tempo — e lembrem: somos preguiçosos."

## Q3 — Função de Transferência (25 min)

**Quadro — obtenção de G(s) (linha a linha):**

```
EDO genérica (vale p/ toda entrada):  ÿ + a1·ẏ + a0·y = b0·u
Laplace dos dois lados (CI nulas: y(0)=ẏ(0)=0):
 s²Y(s) + a1·s·Y(s) + a0·Y(s) = b0·U(s)
Y(s)·(s² + a1·s + a0) = b0·U(s)

FUNÇÃO DE TRANSFERÊNCIA:  G(s) = Y(s)/U(s) = b0/(s² + a1·s + a0)
 (razão entre as TLs da saída e da entrada, para CI nulas; vale p/ qualquer u)
 ⇒ Y(s) = G(s)·U(s)
```

**Quadro — exemplos (escreva os 3 e o caminho inverso):**

```
ÿ + 2ẏ + 3y = u            ⇒ G(s) = 1/(s² + 2s + 3)
y⃛ + 8ÿ + 4ẏ = 2u          ⇒ G(s) = 2/(s³ + 8s² + 4s)
ÿ + 3ẏ + 5y = 2ů + u       ⇒ G(s) = (2s + 1)/(s² + 3s + 5)

ATALHO: copiar coeficientes! numerador ← derivadas da ENTRADA;
 denominador ← derivadas da SAÍDA; nº de derivadas = expoente de s.
Inverso: G(s) = (s+1)/(s²+5s+10) ⇒ ÿ + 5ẏ + 10y = ů + u
```

## Q4 — Polos, zeros e raízes de polinômios (20 min)

**Quadro:**

```
POLOS de G(s) = raízes do DENOMINADOR  |  ZEROS = raízes do NUMERADOR

Raízes de polinômio com coeficientes reais: reais ou pares complexos conjugados.
Bhaskara: Δ = b² − 4ac ;  s = (−b ± √Δ)/2a

s² + 3s + 2 :  a=1, b=3, c=2 ⇒ Δ = 9 − 8 = 1 ⇒ s = −1, −2
 ⇒ forma fatorada: (s+1)(s+2)

s² + 2s + 2 :  Δ = 4 − 8 = −4 ⇒ raiz de número negativo NÃO existe em ℝ
 ⇒ números complexos: i² = −1 ⇒ s = −1 ± i  (complexos conjugados)
```

**Quadro — FT fatorada e forma geral:**

```
G(s) = (s+3)/(s²+3s+2) = (s+3)/[(s+1)(s+2)]
Geral (m zeros, n polos):
 G(s) = bm·(s−z1)(s−z2)···(s−zm) / [(s−p1)(s−p2)···(s−pn)]
Procedimento padrão: diagrama → EDO → FT → polos → denominador fatorado
 (normalmente só o denominador precisa estar fatorado)
```

## Q5 — Tabela de TL e cálculo da saída (20 min)

**Quadro (tabela — escrever as 8 linhas principais):**

```
degrau 1 ↔ 1/s | rampa t ↔ 1/s² | parábola t²/2 ↔ 1/s³ | e^{at} ↔ 1/(s−a)
sen(ωt) ↔ ω/(s²+ω²) | cos(ωt) ↔ s/(s²+ω²)
e^{at}sen(ωt) ↔ ω/((s−a)²+ω²) | e^{at}cos(ωt) ↔ (s−a)/((s−a)²+ω²)

(fig m1_fig10_sinais_tabela.png)
degrau = valor constante a atingir | rampa = velocidade constante | parábola = aceleração
e^{at}: a>0 diverge (quanto maior a, mais rápido); a<0 → 0 (quanto maior |a|, mais rápido)
ω controla a oscilação; sinal de a controla o envelope
```

**Quadro — Exemplo 1 (MMC, linha a linha):**

```
ÿ + 3ẏ + 2y = 2u, u = degrau
G(s) = 2/(s²+3s+2), U(s) = 1/s ⇒ Y(s) = 2/[s(s+1)(s+2)]
Não está na tabela! Truque: EXPANSÃO EM FRAÇÕES PARCIAIS

 2/[s(s+1)(s+2)] = A/s + B/(s+1) + C/(s+2)
MMC: 2 = A(s+1)(s+2) + B·s(s+2) + C·s(s+1)
     = (A+B+C)s² + (3A+2B+C)s + 2A
2A = 2 ⇒ A = 1
A+B+C = 0 ⇒ B+C = −1 ;  3A+2B+C = 0 ⇒ 2B+C = −3
subtraindo: B = −2 ⇒ C = 1
CONFIRA somando: 1/s − 2/(s+1) + 1/(s+2) = 2/[s(s+1)(s+2)] ✓

Inversas (linearidade!):  y(t) = 1 − 2e^(−t) + e^(−2t)
```

## Q6 — Truque dos resíduos e polos repetidos (25 min)

**Quadro — Exemplo 2 (resíduos):**

```
ÿ + 11ẏ + 10y = 20u, u = degrau ⇒ Y(s) = 20/[s(s+1)(s+10)]

RESÍDUO: multiplique Y(s) pelo denominador da fração e faça s = polo:
 A = s·Y(s)|₀      = 20/(1·10)        = 2
 B = (s+1)·Y(s)|₋₁ = 20/[(−1)(9)]     = −20/9
 C = (s+10)·Y(s)|₋₁₀ = 20/[(−10)(−9)] = 2/9
Atalho: "cubra" o fator no denominador e substitua s pelo polo.
Fórmula geral (polo simples pi): Ri = (s − pi)·Y(s)|_{s=pi}

 y(t) = 2 − (20/9)e^(−t) + (2/9)e^(−10t)
(fig m1_fig11_saida_fracoes.png — Exemplos 1 e 2)
```

**Quadro — Exemplo 3 (polos repetidos):**

```
G(s) = 2/[(s+1)(s+2)], u(t) = e^(−t) ⇒ U(s) = 1/(s+1)
Y(s) = 2/[(s+1)²(s+2)]  ← polo múltiplo: o truque não resolve tudo

Expansão preferida (3 frações — fáceis na tabela):
 Y(s) = D/(s+1) + E/(s+1)² + F/(s+2)
 E = (s+1)²Y(s)|₋₁ = 2/(−1+2) = 2   (truque vale!)
 F = (s+2)Y(s)|₋₂ = 2/(−2+1)² = 2   (truque vale!)
 D: substitua E, F e compare numeradores (façam em casa!) ⇒ D = −2
 (existe fórmula direta com derivada — não vale a pena; fechar pela soma
  ainda CONFERE os outros resíduos: não fechou ⇒ algum está errado)

 y(t) = −2e^(−t) + 2t·e^(−t) + 2e^(−2t)

(Com 2 frações: (As+B)/(s+1)² + C/(s+2): truque só dá C = 2; (s+1)² e s=−1
 ⇒ B − A = 2, insuficiente; MMC ⇒ A = −2, B = 0.
 Identidade: −2/(s+1) + 2/(s+1)² = −2s/(s+1)²)

RECAPITULANDO: MMC sempre resolve; o truque só acelera.
```

---

## Perguntas para a turma

1. Quais as duas propriedades que o sistema precisa ter para usarmos a TL? (linear, invariante)
2. Por que "condições iniciais nulas" na definição de G(s)?
3. Escreva G(s) de ÿ + 4ẏ + 7y = 3ů − u sem fazer conta. ((3s−1)/(s²+4s+7))
4. Quando o truque dos resíduos não resolve sozinho? (polos repetidos)

**Preparação do professor:** vídeos 01–03 do tópico 1.2; refazer os 3 exemplos de frações parciais no papel; figuras `m1_fig10, m1_fig11` no projetor.
