# Mapa de Conteúdo dos Vídeos — Pacote 01 (Introdução ao Controle de Sistemas)

> Documento de trabalho do professor — base para a regeneração do material do curso.
> Extraído das 23 transcrições limpas (`transcricoes_limpas/pacote01/`).
> Todos os exemplos numéricos dos vídeos foram **reverificados por simulação** (python-control 0.10.2) — status indicado em cada item.

**Convenções globais do professor nos vídeos (valem para todo o curso):**
- Curso todo **SISO** ("Single Input Single Output"); MIMO é "outros cursos".
- Estabilidade = **BIBO** ("a partir daqui, estável = BIBO estável").
- Malha padrão: **controle proporcional com realimentação unitária**, ganho `k`, `u(t) = k·e(t)`, `e = r − y`.
- Notação: `r` (referência), `u` (entrada), `y` (saída), `e` (erro); derivadas em **pontos** (`ÿ`, `u⁗` = 4ª derivada); EDO genérica `ÿ + a1·ẏ + a0·y = b0·u`.
- "Tipo numérico" do sistema = nº de polos na origem de G(s).
- `L(s)` = Função de Transferência de Malha (= k·G(s) no caso proporcional).
- Constantes de erro: `kp`, `kv`, `ka` (minúsculas).
- `tr` = tempo de subida **0–100 %** do valor final; `ts` = tempo de acomodação **±5 %** do valor final (fórmula `ts = 3/σ`); `Mp` chamado de **overshoot** (prefere o inglês).
- Tom: bem-humorado e informal — "controle é coisa de preguiçoso", "modelo parcimonioso", "Jazinga!", metáfora do controle remoto, π ≈ 3,14 ("parcimonioso"), "Pode isso, Arnaldo?".
- Recorrente: "isso é assunto de outros cursos" (MIMO, zeros de FT, tratamento do zero na 1ª coluna de Routh, controladores mais elaborados, demonstrações formais).

---

## Tópico 1.1 — Introdução (7 vídeos)

### t1.1_v01 — "O que é Sistema?"
- **Sequência falada:** etimologia grega *synistanai* ("fazer funcionar junto") → história de **Ktesibius** (~270 a.C., Alexandria) e o relógio de água → problema: manter nível constante num reservatório com furo → solução: boia + gangorra + válvula (= caixa de descarga moderna) → funcionamento qualitativo (nível baixo → boia desce → válvula abre; nível atingido → válvula fecha) → anúncio do curso (exemplos, termos, realimentação, projeto de controlador proporcional).
- **Números:** nenhum. **Deduzido:** nada (narrativo/qualitativo).
- **Obs.:** piada "Jazinga!"; um dos primeiros sistemas de controle automático com registro histórico.

### t1.1_v02 — "Exemplos de Sistemas"
- **Sequência:** sistema = "parte do universo que escolhemos para estudar" → exemplos (recipiente com água, forno, corpo em queda livre, antena, braço robótico, carro, aeronave, foguete, satélite, estação espacial, chuveiro, ferro de passar) → bloco → **saídas** = grandezas de interesse (nível/temperatura da água, temperatura do forno, velocidade/orientação da aeronave) → **entradas** (fluxo de água, ajuste do aquecedor, fluxo de gás, flaps/ailerons/profundor/leme, propulsão) → entradas não manipuláveis = **perturbações** (temperatura ambiente do forno; vento na aeronave) → **SISO**: escolher 1 entrada e 1 saída (nível OU temperatura; a outra vira perturbação) → representação padrão (bloco, seta entrando, seta saindo) → **relação entrada-saída caracteriza o sistema** (direta: gás↑→temperatura↑; oposta: freio↑→velocidade↓; carro popular anos 80 vs. carro de corrida) → **pausa-atividade**: aluno lista sistemas do dia a dia com entrada, saída e relação direta/oposta.
- **Números:** nenhum. **Deduzido:** nada (conceitual).

### t1.1_v03 — "O Objetivo de Controle de Sistemas"
- **Sequência:** objetivo = **modificar o comportamento (relação entrada-saída) de forma eficiente** (menor complexidade, menor custo, menor intervenção humana) → "controle é coisa de preguiçoso" + metáfora do controle remoto → **requisitos de desempenho** = características desejadas da resposta → associados a: **velocidade de resposta**, **oscilações** e **quão bem a saída acompanha a referência** → exemplo do **elevador** (rápido, sem oscilar em torno do andar, parando no nível exato).
- **Números:** nenhum. **Termos novos:** referência.

### t1.1_v04 — "O Gráfico da Saída"
- **Sequência:** gráfico `y × t` → 4 exemplos: **drone** (chão 1 min → 2 m por 2 min → 4 m por 2 min → pouso ~6 min; o gráfico não informa movimento horizontal) → **levitador magnético** (camada de ar 1 cm → 2 cm → 1 cm; didático ou trem maglev) → **carro** (0–100 km/h em 10 s, freada em 5 s) → **ângulo** (avião: 30° esq → 30° dir → norte) → **referência** e **erro de rastreamento** `e = r − y` → exemplo **forno a gás 180 °C** (dia frio → 160 °C → erro 20 °C; o botão define o fluxo de gás a partir da referência) → exemplo **carro 100 km/h** (pedal → combustível → rotação → velocidade) → notação `r, u, y, e(t), r(t), y(t)` → **requisitos no gráfico**: degrau de 100 km/h, faixa de ±10 %, aceleração em 8 s → três saídas: atende / não atende (lenta + erro grande) / atende parcialmente (erro ok, lenta).
- **Números:** 2 m/4 m/6 min; 1 cm/2 cm; 0–100 km/h em 10 s; 30°; 180 °C/160 °C/20 °C; 100 km/h; ±10 %; 8 s.
- **Deduzido:** nada (definições ilustradas). **Figuras:** 4 gráficos de exemplo + gráfico de requisitos com 3 curvas.

### t1.1_v05 — "Análise e Projeto"
- **Sequência:** **análise** (verificar se atende requisitos; test-drive gasta recursos — pergunta aberta: é a forma mais eficiente?) → **projeto** (definir o controle quando não atende) → **malha aberta** (entrada depende só da referência; "confiança cega"; metáfora do cinema em cima da hora) → **malha fechada** (realimenta a saída; erro ajusta a entrada; ele prefere "realimentação" a "retroação/retroalimentação") → **DEMONSTRAÇÃO DE LABORATÓRIO — servomecanismo didático**: saída = velocidade, entrada = tensão, **referência 2 rad/s**; em MA com massas adicionais (↑ inércia) a velocidade **cai quase pela metade**; em MF a variação é **muito pequena** (o erro residual mantém o motor girando) → gráficos comparativos MA × MF, sem/com massas, simultâneo → **realimentação intuitiva humana**: motorista + velocímetro (MF); forno a gás (MA); pessoa medindo a temperatura do forno fecha a malha → projetar = definir como funciona o bloco de ajuste.
- **Números:** 2 rad/s; "cai quase pela metade". **Figuras:** gráficos do servo (4 painéis).
- **Obs.:** demonstração física — no material do aluno vira **descrição + figuras recriadas**, sem menção a vídeo.

### t1.1_v06 — "Exemplo de Malha Fechada"
- **Sequência:** **controle proporcional** `u(t) = k·e(t)`, `k` = ganho → ajuste experimental × teórico do ganho → **DEMONSTRAÇÃO — túnel de vento / queda livre** (simulador e "de verdade"): ganho pequeno → resposta lenta; **ganho muito grande → sai girando** ("a câmera nem conseguiu acompanhar"); ganho adequado → aviso de segurança ("consulte instrutor qualificado") → ganho inadequado pode **danificar o sistema** → **importância dos modelos teóricos**: analisar/projetar sem o sistema real (pode estar longe ou nem construído) → fluxo: **análise/projeto teórico → simulação → validação experimental** → com o modelo, associar características da saída a características do sistema sem calcular a saída.
- **Notação:** `u(t) = k·e(t)`. **Obs.:** demonstração física → descrição + figuras conceituais.

### t1.1_v07 — "Modelos Matemáticos"
- **Sequência:** modelo = **representação parcimoniosa da realidade** com propósito (piada do dicionário) → modelos matemáticos = equações diferenciais de leis físicas → derivada = taxa de variação instantânea (posição→velocidade→aceleração) → **Ex1 massa-mola-amortecedor**: ΣF = ma; mola `−k·y`; amortecedor `−b·ẏ` → `u − k·y − b·ẏ = m·ÿ` → normalizada `ÿ + (b/m)ẏ + (k/m)y = u/m` → forma genérica `ÿ + a1ẏ + a0y = b0u` → notação de pontos → **Ex2 RLC série** (convenção: nos passivos a corrente é contrária à variação de tensão; terra = 0 V; na fonte a corrente acompanha o aumento de tensão) → LKM: `u = vR + vL + vC` → `vR = R·i`, `vL = L·di/dt`, `i = C·dvC/dt` → `u = RC·v̇C + LC·v̈C + vC` → `ÿ + (R/L)ẏ + (1/LC)y = (1/LC)u` → "**Parece algo que você já viu?**" → **Ex3 motor CC + carga (saída = velocidade)**: `u = vR + vL + vM`; **`T = k·i`, `vM = k·y` (constante única k; fcem — "acredite")**; parte mecânica **`T = J·ẏ` (sem atrito!)** → `i = (J/k)ẏ` → `vR = (RJ/k)ẏ`, `vL = (LJ/k)ÿ` → **`ÿ + (R/L)ẏ + (k²/LJ)y = (k/LJ)·u`** → "Familiar?" → **exercício proposto ao aluno**: saída = posição angular → `y⃛ + a2ÿ + a1ẏ = b0u` → "daqui diante a EDO será fornecida" → kit de leis disponíveis (2ª Newton translacional/rotacional, mola, amortecedor, LKM, R/L/C, motor como ponte eletromecânica) → gancho: Transformada de Laplace.
- **Deduzido passo a passo:** as 3 modelagens completas (é o vídeo mais "quadro" do tópico).
- **⚠ Divergência v1:** o motor do vídeo **não tem atrito viscoso B** e usa **constante única** para torque e fcem → EDO de **2ª ordem** para velocidade. Minha âncora v1 (modelo completo com La, Ra, J, B, Kt, Ke → 0,11/(0,10 s+1)) deve virar **exercício extra**, não exemplo principal.

---

## Tópico 1.2 — Transformada de Laplace e Função de Transferência (3 vídeos)

### t1.2_v01 — "Transformada de Laplace"
- **Sequência:** **linearidade** (combinação linear = soma ponderada; exemplos: `1·u1+2u2+2u3`, `21u1−7u2+√3·u3`, `0·u1+0,4u2−√2·u3`; definição formal) → **invariância no tempo** ("mesma entrada hoje, amanhã ou daqui a mês") → **LIT/LTI** → EDO ordinária linear com coeficientes constantes (ordinária = derivadas só em t; linear = combinação linear das derivadas; `a2,a1,a0,b2,b1,b0` constantes) → se não for LIT: aproximar ou "outros cursos" → **aviso aos matemáticos**: engenharia aproxima — parcimônia → **definição**: `F(s) = ∫₀^∞ e^{−st}f(t)dt`, s complexo ("não vamos calcular essa integral — somos preguiçosos") → metáfora do **empacotamento** → **propriedades**: linearidade; derivada com CI nulas `L{f'} = s·F(s)` → **dedução recursiva** `L{f''} = s²F(s)` (chamando `f' = g`) → generalização → **Teorema do Valor Final**: `lim f(t) = lim s·F(s)` → demonstrações em livros.
- **Deduzido:** `L{f''} = s²F(s)`.

### t1.2_v02 — "Função de Transferência"
- **Sequência:** EDO genérica → TL dos dois lados, CI nulas, Y(s) em evidência → **definição G(s) = Y(s)/U(s)** → **Ex1**: `ÿ+2ẏ+3y = u` → `G = 1/(s²+2s+3)` → **Ex2**: `y⃛+8ÿ+4ẏ = 2u` → `G = 2/(s³+8s²+4s)` → **Ex3**: `ÿ+3ẏ+5y = 2ů+u` → `G = (2s+1)/(s²+3s+5)` → **atalho**: copiar coeficientes (numerador ← derivadas da entrada; denominador ← derivadas da saída; nº de derivadas = expoente de s) → **caminho inverso**: `G = (s+1)/(s²+5s+10)` → `ÿ+5ẏ+10y = ů+u` → **polos** (raízes do denominador) e **zeros** (raízes do numerador) → parêntese: raízes de polinômios reais são reais ou **pares complexos conjugados** → **Bhaskara**: `s²+3s+2` → −1, −2 → forma fatorada → Δ < 0: `s²+2s+2` → **−1 ± i** (i² = −1) → FT fatorada: `(s+3)/[(s+1)(s+2)]` → forma geral `G = bm·Π(s−zi)/Π(s−pi)` → procedimento padrão: diagrama → EDO → FT → polos → denominador fatorado.
- **Deduzido:** obtenção das 4 FTs e as 2 Bhaskaras.

### t1.2_v03 — "Calculando a Saída"
- **Sequência:** `Y(s) = G(s)·U(s)` → **tabela de TL** (degrau 1/s; rampa 1/s²; parábola 1/s³; exponencial `e^{at} ↔ 1/(s−a)`; seno, cosseno, `e^{at}sen`, `e^{at}cos`) → familiarização gráfica (degrau = altura desejada; rampa = velocidade constante; parábola = aceleração constante; `e^t, e^{1,5t}, e^{2t}` divergem; `e^{−t}, e^{−2t}, e^{−4t}, e^{−10t}` decaem; ω controla a oscilação; sinal de a controla o envelope) → **Ex1 completo**: `ÿ+3ẏ+2y = 2u`, degrau → `Y = 2/[s(s+1)(s+2)]` → frações parciais pelo MMC: **A = 1, B = −2, C = 1** (sistema: A+B+C=0, 3A+2B+C=0) → conferência somando → **`y(t) = 1 − 2e^{−t} + e^{−2t}`** → **Ex2 com truque dos resíduos**: `ÿ+11ẏ+10y = 20u` → `Y = 20/[s(s+1)(s+10)]` → **A = 2** (s=0), **B = −20/9** (s=−1), **C = 2/9** (s=−10) → **`y(t) = 2 − (20/9)e^{−t} + (2/9)e^{−10t}`** → fórmula geral do resíduo + atalho de "**cobrir o fator**" → reaplicação no Ex1 → **polos repetidos**: `G = 2/[(s+1)(s+2)]`, `u = e^{−t}` → `Y = 2/[(s+1)²(s+2)]` → expansão preferida `D/(s+1) + E/(s+1)² + F/(s+2)`: **E = 2, F = 2** pelo truque, **D = −2** por substituição (contas deixadas ao aluno) → alternativa com 2 frações: C = 2, `B − A = 2` insuficiente → MMC → A = −2, B = 0 → identidade `−2/(s+1) + 2/(s+1)² = −2s/(s+1)²` → recapitulação (o truque só facilita; o MMC sempre resolve).
- **Deduzido:** as 3 expansões completas. ✔ Todos os resíduos conferem.

---

## Tópico 1.3 — Estabilidade, Realimentação e Erro (6 vídeos)

### t1.3_v01 — "BIBO Estabilidade"
- **Sequência:** noção intuitiva → **definição BIBO** (Bounded Input Bounded Output): estável **se e somente se** a saída é limitada para **toda** entrada limitada → estabilidade é **do sistema**, não de uma saída → classificação dos sinais da tabela (degrau limitado; rampa/parábola divergem; `e^{at}` depende de a; sen/cos limitados; `t·sen`, `t·cos` divergem; `t·e^{at}` depende) → busca de padrão nos **polos da transformada** → conclusões intermediárias: polo real < 0 → limitado; > 0 → diverge; **polo simples na origem → limitado; múltiplo → diverge**; par complexo com Re < 0 → limitado; **Re = 0 simples → limitado, repetido → diverge**; Re > 0 → diverge → separação `Y(s) = G(s)U(s)` em frações parciais `yG` (polos de G) + `yU` (polos de U); `yU` é limitada se u é limitada → análise recai sobre `yG` → **polo na origem em G**: `G = 1/s` + degrau → `1/s²` → **rampa diverge** → **par ±i em G**: `G = 1/(s²+1)` + `cos t` → **`y(t) = (t/2)·sen t` diverge** → **CONDIÇÃO NECESSÁRIA E SUFICIENTE: todos os polos de G com parte real negativa**.
- **Deduzido:** todo o raciocínio da condição BIBO. ✔ Exemplos conferem.

### t1.3_v02 — "O Critério de Routh-Hurwitz"
- **Sequência:** alternativa a calcular polos → 1ª ordem trivial (`s+1` → polo −1; `s−1` → polo +1) → 2ª ordem fatorada → **Tabela de Routh**: n+1 linhas; duas primeiras = coeficientes alternados (começa na 1ª linha) → multiplicação cruzada ÷ **pivô** (elementos inexistentes = 0) → **critério**: mesma sinal na 1ª coluna ⇒ polinômio Hurwitz ⇒ BIBO estável → **Ex 2ª ordem**: `s²+3s+2` (coluna 1, 3, 2 ✓); `s²+s−2` (troca ✗) → **literal 2ª**: `a>0, b>0` → **3ª ordem**: `s³+6s²+11s+6` (coluna **1, 6, 10, 6** ✓; menciona Cardano-Tartaglia) → `s³+6s²+11s+72` (coluna **1, 6, −1, 72** ✗) → **literal 3ª**: `a>0, c>0, a·b>c` → **4ª ordem**: exemplo com coluna **1, 2, −1, 20, 5** → **duas trocas = duas raízes com parte real positiva** ("calcule as raízes e confirme") → **generalização literal** (renomeia linhas aᵢ, bᵢ, cᵢ, dᵢ; `c1 = (b1a2 − a1b2)/b1` etc.; sempre 1ª coluna × coluna seguinte das duas linhas anteriores ÷ pivô; tabela perde uma coluna de linha par para ímpar; último elemento de linha par repete na próxima linha par; zeros à direita opcionais) → **nº de trocas de sinal = nº de raízes RHP** → pode parar na 1ª troca → **zero na 1ª coluna**: raiz no eixo imaginário ou raízes simétricas (±1, ±5, ±10) ⇒ não é BIBO estável; existe tratamento, "mas não neste curso" → exercício: criar polinômios e praticar.
- **Deduzido:** construção completa de todas as tabelas. ✔ Conferido (o polinômio do 2º exemplo de 3ª ordem é `s³+6s²+11s+72`).

### t1.3_v03 — "Vantagens da Realimentação"
- **Sequência:** convenção "estável = BIBO estável" → **FTMF**: diagrama com ganho k → `U = kE`, `Y = G·U`, `E = R − Y` → **`T(s) = kG/(1+kG) = kN/(D + kN)`** → **Vantagem 1 — estabilizar (alguns) instáveis**: `G = 1/(s−1)` → `T = k/(s−1+k)`, **k > 1** estável (ex. k = 2) → contra-exemplo: `G = 1/(s²−2s−2)` instável ∀k ("verifique com Routh"; controladores elaborados = outros cursos) → **Vantagem 2 — menor sensibilidade**: `G = A` (ganho puro), valor real `A+B` → erro relativo MA = `B/(A+B)`; MF = `B/[(1+kA)(A+B)]` → **numérico: B = 0,2·A e kA = 10 → 17 % (MA) vs. 1,5 % (MF); kA = 2 → 17 % vs. 5,6 %** → quanto maior k, menor a sensibilidade (também a erros de implementação do ganho, k+q) → **Vantagem 3 — rejeição de perturbação** N somada à entrada: MA `ΔY = A·N`; MF `ΔY = [1/(1+kA)]·A·N` → **desvantagem**: sensor custa caro/complexa; se MA tolerável, use MA → ganho inadequado pode **desestabilizar** a MF (gancho do próximo vídeo).
- **Deduzido:** FTMF e as 3 comparações algébricas. ✔ Números conferem.

### t1.3_v04 — "Faixa de Estabilidade"
- **Sequência:** Routh com parâmetro literal → **Ex1**: denominador `s³+6s²+11s+(6+k)` → coluna `1, 6, (60−k)/6, 6+k` → **−6 < k < 60** → casos-limite: **k = 60 → polos −6, ±j√11** (instável); **k = −6 → polo na origem**; k > 60 → 2 trocas; k < −6 → 1 troca → **três exemplos de (des)estabilização**: (a) `G = 1/(s²+2s−3)` [polos +1, −3] → MF estável **k > 3** (k = 3 → polo na origem) — instável MA estabilizado por P; (b) **`G = 10/(s³+8s²+12s+10)`** [MA estável — verificado por Routh] → MF estável **k < 8,6** — **ganho inadequado desestabiliza**; (c) **`G = 10/(s³+11s²+8s−20)`** [MA instável] → MF estável **2 < k < 10,8** — faixa limitada → **múltiplos parâmetros**: (i) denominador `s²−s−2+kt·s+k` → **kt > 1 e k > 2** (independentes); (ii) `T = (as+b)/(s³+3s²+2s−1+as+b)` → **b > 1 e a > (b−7)/3** (acoplados); (iii) `T = (ks+a)/(s³+3s²+2s+ks+a)` → **ka > 0 e 3k − ka > −6** → a = 2 ⇒ k > 0; a = 4 ⇒ 0 < k < 6 → **nem sempre há solução**: "tente achar k para `T = k/(s²−s−6+ks−1)`" (impossível — fica como desafio).
- **Deduzido:** todas as tabelas. ✔ Conferido por `numpy.roots`: k=60 → −6, ±j3,3166 (=√11); k=8,6 → −8, ±j3,464; k=2 → polo na origem; k=10,8 → −11, ±j2,828.
- **⚠ Divergência v1:** minha âncora de Lista1 (`s³+5s²+6s+K`, 0<K<30, ωu=√6) não aparece nos vídeos → o exemplo do vídeo (`s³+6s²+11s+(6+k)`) vira o principal; a minha vira exercício.

### t1.3_v05 — "Erro em Malha Aberta"
- **Sequência:** motivação das 3 entradas (**degrau** = valor constante: altitude, temperatura, apontamento de radar; **rampa** = velocidade constante: pouso de aeronave, radar-satélite, perfil térmico, câmera-bola; **parábola** = aceleração: lançamento de foguete) → **Ex1**: `G = 1/[(s+1)(s+2)]`, degrau → E(s) → frações parciais → **e∞ = 0,5** → observação: **só o resíduo da fração 1/s importa** (demais polos estáveis) = aplicação do TVF → **Ex2**: `G = 2/[(s+1)(s+2)]` → cancelamento de s → **erro → 0** → alternativa: valor final da saída menos a entrada → **Ex3**: `G = (s²+6s+9)/(s³+8s²+17s+10)` → **y∞ = 0,9 → e∞ = 0,1** ("apague os termos com s") → degrau de amplitude 5 → erro 5× (linearidade) → **PEGADINHA**: `G = (s²+29s+208)/(s³+6s²+10s+208)` → e∞ = 0? **NÃO — sistema instável** ("confira com Routh"; "Pode isso, Arnaldo?") → não existe valor final → **rampa**: Ex1 → fração 1/s² com resíduo **b = 0,5** → **erro diverge (0,5·t)** → Ex2 → cancelamento → **a = 1,5 → erro → 1,5** → **análise literal** (numerador …+bs+c; denominador …+es+f): parábola exige **c = f e b = e**, erro `(d−a)/f`; rampa exige **c = f**, erro `(e−b)/f`; degrau: `(f−c)/f` → **RESUMO em cascata**: coeficientes de s⁰ iguais ⇒ erro nulo ao degrau; s¹ iguais ⇒ erro nulo à rampa; s² iguais ⇒ erro nulo à parábola → G não pode ter polo na origem e precisa ser estável → TVF só vale se o sinal converge.
- **Deduzido:** Ex1 e Ex2 completos (degrau e rampa); literais comentados. ✔ Conferido (ess = 0,5; 0; rampa → 1,5).

### t1.3_v06 — "Erro em Malha Fechada"
- **Sequência:** MA/MF são conceitos relativos → `T = kG/(1+kG)` → **novo elemento: Função de Transferência de Malha `L(s) = k·G(s)`** ("parte do controle remoto") → **`E(s) = R(s)/(1+L(s))`** → TVF → degrau: **`kp = lim L(s)`, e∞ = 1/(1+kp)** → rampa: **`kv = lim sL(s)`, e∞ = 1/kv** → parábola: **`ka = lim s²L(s)`, e∞ = 1/ka** → relação com polos na origem: 0 polos → `kp = k·G(0)`, kv = ka = 0; 1 polo → kp = ∞, ka = 0; 2 polos → kp = kv = ∞ → **TIPO NUMÉRICO** = nº de polos na origem → **tabela tipo × entrada** (tipo 0: degrau finito / rampa e parábola divergem; tipo 1: degrau nulo / rampa finita / parábola diverge; tipo 2: degrau e rampa nulos / parábola finita; tipo 3: tudo nulo) → **obtenção rápida**: forma expandida → `kp = k·b0/a0` etc. → **ressalvas**: usar a coluna certa (tipo), verificar convergência, fórmulas só valem para **P com realimentação unitária** → ↑k ↓erro, **mas** ganho demais desestabiliza.
- **⚠ Errata da legenda:** a transcrição diz "tipo 0 apresenta erro **infinito** para entrada degrau" — pelo contexto/tabela é **finito** (erro da legenda automática; corrigir no material).
- **Deduzido:** derivação de E(s) e das constantes. ✔ Conferido.

---

## Tópico 1.4 — Resposta ao Degrau de Sistemas de 2ª Ordem (7 vídeos)

### t1.4_v01 — "Por que 2ª ordem?"
- **Sequência:** por que o **degrau**? (1º entrada comum: mudança de velocidade, altitude, apontamento, braço robótico, antena; 2º **rampa/parábola para y ≡ degrau para ẏ/ÿ** — antena: rampa em posição = degrau em velocidade; foguete: parábola em altura = degrau em aceleração; 3º se não responde bem ao degrau, não responderá a entradas mais complexas) → por que **2ª ordem**? (1º resposta de 1ª ordem "não tem graça": constante − exponencial, ou diverge; 2º muitos sistemas aproximáveis por 2ª ordem) → **exemplo comparativo**: 2ª: **`1/(s²+s+1)`**; 3ª: **`5/[(s²+s+1)(s+5)]`**; 4ª: **`64/[(s²+s+1)(s²+12s+64)]`** → gráficos sobrepostos: **boas aproximações** → ressalva: aproximação para **análise**, não necessariamente para projeto; nem sempre válida → **contra-exemplo**: **`1/[(s²+s+1)(s+1)]`** → resposta bem diferente.
- ✔ Simulado: Mp 16,3 % (2ª) / 15,9 % (3ª polo −5) / 16,3 % (4ª) vs. Mp 8,1 %, tp 4,92 s (contra-exemplo). **Figuras:** 3 comparações (recriar por simulação).

### t1.4_v02 — "As Diferentes Respostas ao Degrau"
- **Sequência:** 3 tipos conforme os polos → **instável** (complexos Re>0 → diverge oscilando; reais positivos → diverge monotonicamente) — "não estamos interessados" → **superamortecida** (2 polos reais negativos; converge sem oscilar, parecida com 1ª ordem) → **criticamente amortecida** (polos reais iguais; caso particular, visualmente similar) → **subamortecida** (par complexo conjugado Re<0; oscilação de amplitude decrescente) → recapitulação → interesse na subamortecida (**vai mais rápido ao valor final**, mas sem oscilações grandes nem longas).
- Conceitual; figuras dos 3 tipos.

### t1.4_v03 — "Características da Resposta Subamortecida"
- **Sequência:** 3 sistemas: **`1/(s²+s+1)`, `64/(s²+12s+64)`, `25/(s²+4s+25)`** → respostas sobrepostas → brainstorm de características candidatas → **4 grandezas**: **`tp`** (instante de pico), **`tr`** (tempo de subida), **`ts`** (tempo de acomodação), **`Mp`** (overshoot — prefere o inglês) → definições no 3º sistema: `tp` = instante do valor máximo → **`tr` 0–100 %**: até a 1ª passagem pelo **valor final** (não da entrada!; coincidem se erro nulo; curso usa só 0–100 %) → **`ts`**: confinamento em faixa percentual do valor final; **curso usa 5 %** → **`Mp`** = ultrapassagem relativa ao valor final (%; com degrau unitário e erro nulo: `Mp = ymáx − 1`) → definições **relativas ao valor final** ⇒ independem da amplitude do degrau e do erro de regime.
- **Convenções do curso: tr(0–100 %), ts(±5 %).**

### t1.4_v04 — "Parametrização de 2ª Ordem"
- **Sequência:** tradução de requisitos ("rápido" → tr/tp/ts; "confortável" → Mp máx) → FT 2ª ordem **sem zeros**, erro nulo (zeros = outros cursos) → forma `a0/(s²+a1s+a0)` → y(t) "essa coisa aí que eu nem vou me entreter a falar" → **mudança de variáveis: `a0 = ωn²`, `a1 = 2ζωn`** → forma **`ωn²/(s²+2ζωn·s+ωn²)`**, `ωn = √a0`, `ζ = a1/(2√a0)` → **`y(t) = 1 − [e^{−σt}/√(1−ζ²)]·sen(ωd·t + φ)`**, com **`σ = ζωn`**, **`ωd = ωn√(1−ζ²)`**, `tg φ = √(1−ζ²)/ζ` → formas em σ e ωd: `(σ²+ωd²)/(s²+2σs+σ²+ωd²)` → **polos `−σ ± jωd`** → forma fatorada `(s+σ−jωd)(s+σ+jωd)` ("verifique com Bhaskara").
- **Notação:** csi (ζ), ômega n, ômega d, sigma, fi. **Deduzido:** parametrização e polos.

### t1.4_v05 — "Fórmulas de 2ª Ordem"
- **Sequência:** recapitulação → "acredite ou verifique" → **`tp = π/ωd = π/(ωn√(1−ζ²))`** (derivando y(t) e igualando a zero) → **`Mp = e^{−ζπ/√(1−ζ²)}`** (substituindo tp) → **Mp só depende de ζ** → faixas de ζ: <0 diverge; =0 não amortecido (polos ±jωn, oscilação sustentada); 0–1 subamortecido; =1 criticamente amortecido (Mp = 0); >1 superamortecido → **`tr = (π − β)/ωd`, `β = arccos ζ`** (= φ; mistério β×φ — "se souber, me avise") → **`ts(5 %) = 3/σ`** — **aproximação pela envoltória, fórmula pessimista** → **exemplo completo: `25/(s²+4s+25)`**: ωn = 5, ζ = 0,4 → **Mp = 25,4 %, tp = 0,69 s, tr = 0,43 s (β em radianos!), ts = 1,5 s** ("exatamente os valores da simulação") → nomes: ζ = fator/coeficiente/razão de amortecimento; **ωn = frequência natural não amortecida**; **ωd = frequência amortecida**; **σ = decaimento exponencial**.
- ✔ Simulado: Mp = 25,3 %, tp = 0,70 s, tr = 0,45 s; ts(5 %) medido ≈ 1,6–1,7 s (fórmula dá 1,5 s — apresentar como aproximação, como o próprio vídeo enfatiza).
- **⚠ Divergências v1:** (i) vídeo usa **`ts(5 %) = 3/σ`** — meu v1 usava `ts ≈ 4/σ` (critério 2 %); **adotar 3/σ**; (ii) vídeo usa **`tr = (π−β)/ωd` exato** — meu v1 usava `tr ≈ 1,8/ωn`; **adotar a exata**.

### t1.4_v06 — "Projeto para Requisito de Overshoot"
- **Sequência:** **ENUNCIADO-ÂNCORA: `G(s) = 1/[s(s+1)]`**, requisitos: **maior rejeição a perturbações possível + Mp ≤ 10 %** → `T(s) = k/(s²+s+k)` → `ωn = √k`, `ζ = 1/(2√k)` → ↑k ⇒ ↑rejeição; ↓ζ ⇒ ↑Mp → k-limite = o de Mp = 10 % → duas rotas (chutar ζ ou **inverter a fórmula**) → **dedução da inversa**: `ln Mp = −ζπ/√(1−ζ²)` → **`ζ = √(ln²Mp / (π² + ln²Mp))`** → **ζ(10 %) = 0,59** → **DICA: Mp na fórmula é fração (0–1)** → sugestão: montar **tabela ζ × Mp** (Mp: 5/10/15/20/25 %; ζ: 0,4/0,45/0,5/0,6/0,7) → `0,59 = 0,5/√k` → **`k = 0,718`** → `T(s) = 0,718/(s²+s+0,718)` → simulação confirma ≈10 % → **projeto literal**: `G = 1/[s(s+a)]` (tipo 1, erro nulo) → `ζ = a/(2√k)` → **`k = a²/(4ζ²)`** → atalho: substituir `ζ² = ln²Mp/(π²+ln²Mp)` direto.
- ✔ Simulado: k = 0,718 → **Mp = 10,1 %**.
- **⚠ Divergência v1 — PRINCIPAL DO MÓDULO:** o vídeo usa `1/[s(s+1)]` com **k = 0,718**; meu v1 usava `1/[s(s+4)]` com K = 11,45. **O exemplo do vídeo vira o principal**; o caso a = 4 vira exercício extra (pela fórmula literal: k = 16/(4·0,3494) = 11,45 ✓ consistente).

### t1.4_v07 — "Projeto para Requisito de Instante de Pico"
- **Sequência:** mesmo procedimento com tp → **requisito exemplo: tp = 3,14 s** → `ωd = π/tp = 1` → mesma planta `G = 1/[s(s+1)]` → `ωd = √k·√(1 − 0,25/k) = √(k − 0,25)` → **`k = 1,25`** → simulação: **tp ≈ 3,15 s, Mp = 20,8 %** → **CONFLITO DE REQUISITOS**: Mp = 10 % **e** tp = 3,14 s são incompatíveis com P simples → controladores mais elaborados (tópicos futuros) → **P não altera ts**: `σ = ζωn = 0,5` independentemente de k → **projeto literal**: `G = 1/[s(s+a)]` → `ωd = √(k − a²/4)` → **`k = π²/tp² + a²/4`**.
- ✔ Simulado: k = 1,25 → Mp = 20,7 %, polos −0,5 ± j1,0, tp ≈ 3,2 s (discretização; fórmula: 3,1416 s).
- **⚠ Divergência v1:** o vídeo usa tp = 3,14 s com **k = 1,25** na planta `1/[s(s+1)]`; meu v1 usava tp = 0,8 s com K = 19,42 na planta `1/[s(s+4)]`. **Vídeo vira principal**; a = 4 vira exercício extra.

---

## Consolidação: decisões propostas para a regeneração

1. **Exemplos dos vídeos = exemplos principais** em todos os tópicos (já todos validados por simulação):
   - Frações parciais: `2/[s(s+1)(s+2)]`, `20/[s(s+1)(s+10)]`, polos repetidos `2/[(s+1)²(s+2)]`.
   - BIBO: `1/s` + degrau; `1/(s²+1)` + cos t.
   - Routh: `s²+3s+2`, `s²+s−2`, `s³+6s²+11s+6`, `s³+6s²+11s+72`, 4ª ordem (coluna 1,2,−1,20,5), literais.
   - Faixa de estabilidade: `s³+6s²+11s+(6+k)` (−6<k<60); `10/(s³+8s²+12s+10)` (k<8,6); `10/(s³+11s²+8s−20)` (2<k<10,8); exemplos multiparamétricos.
   - Erro MA: `1/[(s+1)(s+2)]` (0,5), `2/[(s+1)(s+2)]` (0; rampa 1,5), `(s²+6s+9)/(s³+8s²+17s+10)` (0,1), pegadinha instável.
   - 2ª ordem: `1/(s²+s+1)`, `25/(s²+4s+25)`, `64/(s²+12s+64)`; aproximações `5/[(s²+s+1)(s+5)]`, `64/[(s²+s+1)(s²+12s+64)]`; contra-exemplo `1/[(s²+s+1)(s+1)]`.
   - **Projeto P: `G = 1/[s(s+1)]` → k = 0,718 (Mp = 10 %) e k = 1,25 (tp = 3,14 s)**.
2. **Minhas âncoras v1 viram exercícios extras** quando compatíveis: `1/[s(s+4)]` com K = 11,45 / K = 19,42; `s³+5s²+6s+K` (0<K<30); motor CC completo (0,11/(0,10 s+1)); `5/(2s+1)`.
3. **Fórmulas do vídeo prevalecem**: `ts(5 %) = 3/σ` (não 4/σ); `tr = (π−β)/ωd` exato (não 1,8/ωn); `tp = π/ωd`; `Mp = e^{−ζπ/√(1−ζ²)}}`; inversa `ζ = √(ln²Mp/(π²+ln²Mp))`; projeto literal `k = a²/(4ζ²)` e `k = π²/tp² + a²/4`.
4. **Modelo de motor do vídeo** (sem atrito, constante única): `ÿ + (R/L)ẏ + (k²/LJ)y = (k/LJ)u` para velocidade; posição → 3ª ordem (exercício proposto pelo próprio vídeo).
5. **Demonstrações físicas** (caixa de descarga/Ktesibius, servo didático 2 rad/s, túnel de vento) viram **texto descritivo + figuras recriadas**, sem qualquer referência a vídeos (alunos não têm acesso).
6. **Tom do professor preservado** nas notas de aula e roteiros de slides (informal, humor, "preguiçoso", "parcimonioso"), mantendo o material do aluno objetivo.
7. **Errata da legenda** a corrigir: "tipo 0 → erro infinito ao degrau" → **finito**.
8. **ts medido × fórmula**: apresentar `ts = 3/σ` como aproximação pessimista (como o vídeo enfatiza), mostrando na simulação que o valor medido pode diferir levemente (25/(s²+4s+25): fórmula 1,5 s, medido ≈ 1,7 s).
