# Nota de Aula 1.1 — Sistemas, Controle e Modelos Matemáticos

> **Documento do professor** — guia de quadro, pronto para transcrição linha a linha, com falas sugeridas.
> Duração prevista: 2 h (semana 2). Lab associado: **Lab 01**.

**Mapa dos vídeos deste tópico (não mostrar aos alunos):**

| Vídeo | Título | Uso na aula |
|---|---|---|
| 01 | O que é Sistema? | Abertura: Ktesibius e a caixa de descarga (Q1) |
| 02 | Exemplos de Sistemas | Sistema/entrada/saída/perturbação/SISO; atividade de exemplos (Q1–Q2) |
| 03 | O Objetivo de Controle de Sistemas | Objetivo + requisitos; elevador (Q2) |
| 04 | O Gráfico da Saída | Gráfico y×t; referência; erro; requisitos no gráfico (Q2–Q3) |
| 05 | Análise e Projeto | Análise × projeto; MA × MF; servo didático; realimentação humana (Q3–Q4) |
| 06 | Exemplo de Malha Fechada | u = k·e; ajuste do ganho (túnel de vento); importância dos modelos (Q4) |
| 07 | Modelos Matemáticos | Modelo parcimonioso; as 3 modelagens completas (Q5–Q6) |

---

## Q1 — O que é sistema (15 min)

**Quadro:**

```
SISTEMA = uma parte do universo que escolhemos para estudar.
(etimologia: grego synistanai, "fazer funcionar junto")
```

**Fala sugerida:** "Sistema vem da palavra grega antiga *synistanai*, que significa 'fazer funcionar junto'. E é na Grécia Antiga que nossa jornada começa: anoitecer quente de verão, cerca de 270 a.C., o jovem Ktesibius está ajudando o pai na barbearia quando tem uma ideia... Jazinga! Ok, não vamos falar da Grécia Antiga, mas dos inventos de Ktesibius — um dos primeiros sistemas de controle automático de que se tem registro."

**Quadro (desenho da caixa de descarga — projetar fig `m1_fig01_caixa_descarga.png`):**

```
Problema de Ktesibius: manter NÍVEL CONSTANTE no reservatório com furo
(relogio de água: nível constante ⇒ vazão constante ⇒ boa medida do tempo)

Solução: BOIA + GANGORRA + VÁLVULA
 nível baixo  → boia desce → válvula abre  → entra água
 nível sobe   → boia sobe  → válvula fecha progressivamente
 nível desejado → válvula completamente fechada
 caiu o nível (evaporação/descarga) → ciclo recomeça
```

**Fala:** "Alguém podia ficar o tempo todo completando o nível. Ou deixar entrar água sem parar e jogar o excesso fora — desperdício. Ktesibius resolveu com uma boia ligada a uma válvula por uma gangorra. É a caixa de descarga da sua casa, 300 anos antes de Cristo."

**Quadro (exemplos e definições):**

```
Exemplos de sistema: recipiente com água, forno, corpo em queda livre,
antena, braço robótico, carro, aeronave, foguete, satélite, chuveiro, ferro de passar.

SAÍDA = grandeza de interesse  (seta SAINDO do bloco)
ENTRADA = grandeza que atua no sistema e afeta a saída  (seta ENTRANDO)

[u] → [ SISTEMA ] → [y]

PERTURBAÇÃO = entrada que NÃO podemos manipular
 (temperatura ambiente do forno; vento na aeronave)

SISO = Single Input Single Output (1 entrada, 1 saída) — TODO o curso
 (recipiente: nível OU temperatura; a outra grandeza/entrada vira perturbação)

O que caracteriza o sistema: a RELAÇÃO entrada–saída
 direta: ↑gás ⇒ ↑temperatura | oposta: ↑freio ⇒ ↓velocidade
 (carro popular anos 80 ≠ carro de corrida)
```

**Atividade (3 min):** "Pensem em 2 ou 3 sistemas do dia a dia. Definam: sistema, entrada, saída, relação direta ou oposta. SISO: uma entrada e uma saída só!"

---

## Q2 — Objetivo do controle, gráfico da saída, referência e erro (20 min)

**Quadro:**

```
OBJETIVO DO CONTROLE: modificar o comportamento do sistema DE FORMA EFICIENTE.
 modificar comportamento = alterar a relação entrada–saída p/ atender requisitos
 eficiente = menor complexidade, menor custo, menor intervenção humana possíveis

REQUISITOS DE DESEMPENHO = o que você quer que o sistema faça, e como.
 1) velocidade de resposta   2) oscilações (poucas/nenhuma)   3) y acompanha r
 Exemplo: o ELEVADOR (rápido, sem oscilar, parando no nível do piso)
```

**Fala:** "Vou contar um segredo: controle de sistemas é coisa de preguiçoso. Estamos o tempo todo procurando atalhos. Pensem no controle remoto: invenção de quem não queria levantar do sofá. Deu trabalho criar o primeiro — mas depois é só usar. Neste curso estaremos construindo o nosso controle remoto."

**Quadro (gráficos — projetar fig `m1_fig03_graficos_saida.png`):**

```
GRÁFICO DA SAÍDA: y × t
 ex.: drone (2 m → 4 m → pouso ~6 min) — nada diz sobre o movimento horizontal!
 ex.: levitador magnético (1 cm → 2 cm → 1 cm); carro (0–100 km/h em 10 s);
      avião (30° esq → 30° dir → norte)

REFERÊNCIA r = valor desejado.  A partir de r definimos a entrada u.
ERRO (de rastreamento):  e = r − y     [mais rigoroso: e(t) = r(t) − y(t)]

ex.: forno a gás: r = 180 °C; dia frio → y = 160 °C → e = 20 °C
ex.: carro: r = 100 km/h; pedal → combustível → rotação → velocidade real
```

**Quadro (requisitos no gráfico — fig `m1_fig04_requisitos_grafico.png`):**

```
Requisito: seguir degrau de 100 km/h, acelerar em 8 s, erro < 10 %
 → faixa de ±10 % no gráfico; reta vertical em t = 8 s
 saída 1: atende | saída 2: não atende (lenta + erro grande) | saída 3: parcial
```

---

## Q3 — Análise e projeto; malha aberta × malha fechada (20 min)

**Quadro:**

```
ANÁLISE: verificar se o sistema atende aos requisitos.
 (test-drive funciona, mas desgasta, consome e leva tempo... eficiente?)
PROJETO: se não atende → definir o CONTROLE (alterar a relação e–s).

MALHA ABERTA: u depende SÓ de r. Confiança cega no projeto.
 [r] → [ajuste] → [u] → [sistema] → [y]
 (cinema em cima da hora: se não pegar trânsito, ok; se pegar...)

MALHA FECHADA: realimentamos y; e = r − y ajusta u.
 [r] → (⊖) → [e] → [ajuste] → [sistema] → [y]
          ↑__________realimentação__________|
 (também: controle com realimentação; "retroação/retroalimentação" — eu uso realimentação)
```

**Demonstração do servo didático (fig `m1_fig05_servo_malha.png`):**

```
Servo: saída = velocidade de rotação; entrada = tensão no motor; r = 2 rad/s.
 MALHA ABERTA: ganho ajustado → y ≈ 2 rad/s.
  + massas (↑ inércia): o sistema NÃO percebe → mesmo u → velocidade cai ~metade!
 MALHA FECHADA: u ajustado pelo erro.
  + massas: tendência de queda ⇒ ↑erro ⇒ ↑u ⇒ corrige. Diferença MUITO pequena.
  (o erro residual é o que "empurra" o motor)
```

**Fala:** "Os seres humanos usam realimentação o tempo todo: o motorista olha o velocímetro e ajusta o pedal — malha fechada humana. O forno a gás é malha aberta. Se alguém medisse a temperatura sem parar e ajustasse o gás pela diferença — aí sim, malha fechada, com o ser humano fechando a malha."

---

## Q4 — Controle proporcional e a importância dos modelos (15 min)

**Quadro:**

```
CONTROLE PROPORCIONAL:  u(t) = k · e(t)     k = GANHO
 (base de tudo; nem sempre suficiente — mas entenda-o bem!)

Ajuste do ganho (túnel de vento / queda livre):
 k pequeno demais → entrada pequena → y sobe devagar (cada vez mais devagar)
 k grande demais  → entrada elevada → y PASSA do valor; pode DIVERGIR
 k adequado       → rápido, sem ultrapassar
 (fig m1_fig06_ajuste_ganho.png)
```

**Fala:** "Eu testei isso no túnel de vento: ganho pequeno, o corpo sobe devagar; ganho muito grande — eu saí girando, a câmera nem acompanhou. Ajuste experimental é ineficiente E potencialmente perigoso. A saída elegante: modelos matemáticos."

**Quadro:**

```
POR QUE MODELOS MATEMÁTICOS?
 análise e projeto TEÓRICOS: sem gastar recursos, sem riscos,
   sem nem precisar do sistema real (pode estar longe ou nem construído)
 fluxo: análise/projeto teórico → SIMULAÇÃO → validação experimental
 com o modelo: associar características da saída ↔ características do sistema
   (sem precisar calcular a saída!)
```

---

## Q5 — Modelagem: massa-mola-amortecedor e RLC (25 min)

**Quadro (conceito):**

```
MODELO = representação PARCIMONIOSA da realidade (econômica, com propósito).
Modelo matemático = equações diferenciais (de leis físicas).
derivada = taxa de variação instantânea (posição → velocidade → aceleração)
Notação de pontos: ẏ, ÿ, ... (u⁗ = 4ª derivada de u)
```

**Quadro — Exemplo 1 (fig `m1_fig07_massa_mola.png`), linha a linha:**

```
2ª Lei de Newton:  ΣF = m·a
 mola: −k·y  (proporcional ao deslocamento, sentido oposto)
 amortecedor: −b·ẏ  (proporcional à velocidade, sentido oposto)

 u − k·y − b·ẏ = m·ÿ

Forma preferida: saída à esquerda, entrada à direita, ÷ m:

 ÿ + (b/m)ẏ + (k/m)y = (1/m)u

Forma genérica:  ÿ + a1·ẏ + a0·y = b0·u
```

**Quadro — Exemplo 2 (fig `m1_fig08_rlc.png`), linha a linha:**

```
Convenção: passivos → corrente contrária à variação de tensão; terra = 0 V;
           fonte → corrente acompanha o aumento de tensão.
LKM: u = vR + vL + vC
Componentes: vR = R·i ;  vL = L·di/dt ;  i = C·dvC/dt   (malha única: 1 corrente)
Substituindo i:  vR = RC·v̇C ;  vL = LC·v̈C
Na LKM:  u = RC·v̇C + LC·v̈C + vC
÷ LC, com vC = y:

 ÿ + (R/L)ẏ + (1/LC)y = (1/LC)u      ⇒   ÿ + a1ẏ + a0y = b0u   ← Parece algo?
```

---

## Q6 — Modelagem: motor CC + carga; recapitulação (25 min)

**Quadro — Exemplo 3 (fig `m1_fig09_motor_cc.png`), linha a linha:**

```
Saída: velocidade de rotação y(t).  (modelo de radares, câmeras, braços robóticos)
Elétrica (LKM): u = vR + vL + vM ;  vR = R·i ;  vL = L·di/dt
Motor (uma única constante k):  T = k·i ;  vM = k·y   (fcem — acreditem!)
Mecânica (só o torque do motor):  T = J·ẏ
Das duas do torque:  i = (J/k)·ẏ
Nas tensões:  vR = (RJ/k)·ẏ ;  vL = (LJ/k)·ÿ
Na LKM:  u = (RJ/k)ẏ + (LJ/k)ÿ + k·y
÷ (LJ/k):

 ÿ + (R/L)ẏ + (k²/LJ)·y = (k/LJ)·u     ⇒   ÿ + a1ẏ + a0y = b0u   ← Familiar?
```

**Fala:** "Três sistemas completamente diferentes — mecânico, elétrico, eletromecânico — com a mesma estrutura de equação. É por isso que as ferramentas do curso valem para todos."

**Quadro (exercício proposto + kit de modelagem):**

```
EXERCÍCIO (para casa): saída = POSIÇÃO angular → T = J·ÿ
 ⇒ chegue a  y⃛ + a2·ÿ + a1·ẏ = b0·u   (3ª ordem!)

KIT DE MODELAGEM:
 ΣF = mÿ  /  ΣT = Jθ̈ ;  mola −ky ;  amortecedor −bẏ
 LKM ;  vR = Ri ;  vL = L·di/dt ;  i = C·dvC/dt ;  motor: T = ki, vM = ky
Daqui em diante, a EDO do sistema será fornecida. E o que fazemos com ela?
 → TRANSFORMADA DE LAPLACE (próxima aula)
```

---

## Perguntas para a turma (checagem rápida)

1. Qual a diferença entre entrada e perturbação? (resposta: manipulabilidade)
2. No servo em malha aberta, por que a velocidade cai com as massas? E por que em malha fechada quase não cai?
3. No exemplo do túnel de vento, qual o risco do ganho muito grande? (divergência/dano)
4. Por que as três modelagens dão a mesma forma de EDO — e por que isso é bom?

**Preparação do professor:** revisar vídeos 01–07 do pacote 01; figuras `m1_fig01, 03, 04, 05, 06, 07, 08, 09` no projetor; levar o exemplo do elevador e do forno de improviso.
