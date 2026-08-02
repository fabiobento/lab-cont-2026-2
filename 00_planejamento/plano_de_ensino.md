# Laboratório de Controle Automático — Planejamento (Parte 1)

**Curso:** Engenharia Elétrica — 7º período — Ifes Campus Guarapari
**Carga horária:** 30 h de laboratório (2 aulas/semana × 15 semanas)
**Pré-requisito:** Controle Automático
**Ferramenta computacional:** Python Control Systems Library (`python-control` v0.10.2) + `numpy` + `matplotlib` (substituindo MATLAB/Simulink e SCILAB do PPC)
**Progressão de conteúdo:** segue estritamente a ordem dos pacotes de vídeo (`estrutura-de-arquivos-curso-ITA-VERSÃO-3.txt`), com um módulo autônomo adicional para a Unidade III do PPC (não linearidades), não coberta pelos vídeos.

> ### §0.1 — Nota de revisão (estrutura de referência VERSÃO 3 e regeneração guiada por legendas)
> Esta versão do repositório foi **regenerada do zero** a partir das **transcrições completas dos vídeos** (legendas `.vtt` da VERSÃO 3), para que o conteúdo fique o mais próximo possível do que é efetivamente falado em cada aula. A VERSÃO 3 mantém a sequência de vídeos da VERSÃO 2, acrescenta os arquivos de legenda, **2 vídeos novos no pacote 03** ("Nichols-Black-Bode de 2ª e 3ª ordem…" no tópico 3.2; "A margem de fase e o efeito do atraso no diagrama de Nyquist" no tópico 3.3) e reagrupa os vídeos de projeto P do tópico 1.4 sob o item "03 - Projeto de Controle Proporcional".
>
> **Diretrizes desta regeneração:**
> 1. **Os exemplos falados nos vídeos são os exemplos principais do material** (todos revalidados por simulação); os exemplos da versão anterior do repositório viram exercícios extras quando compatíveis. O mapa vídeo ↔ conteúdo do pacote 01 está consolidado em `mapa_conteudo_videos_pacote01.md` (documento do professor).
> 2. **Os alunos não têm acesso aos vídeos.** Todo o material do aluno (teoria, exercícios, labs, listas) é **autossuficiente e não contém nenhuma referência a vídeos**. O mapeamento por vídeo existe apenas em documentos do professor (este plano, as notas de aula e os roteiros dos slides) — os vídeos servem à preparação/revisão do professor.
> 3. **Convenções de notação e fórmulas adotadas dos vídeos** (substituem as da versão anterior):
>    - `ts` = tempo de acomodação **±5 %** do valor final → **`ts ≈ 3/σ`** (aproximação pela envoltória, pessimista);
>    - `tr` = tempo de subida **0–100 %** do valor final → **`tr = (π − β)/ωd`**, com `β = arccos ζ` (fórmula exata);
>    - `tp = π/ωd`; `Mp = e^(−ζπ/√(1−ζ²))`; inversa **`ζ = √(ln²Mp / (π² + ln²Mp))`** (Mp em fração, 0–1);
>    - planta-âncora do projeto proporcional: **`G(s) = 1/[s(s+1)]`** → `k = 0,718` (Mp = 10 %) e `k = 1,25` (tp = 3,14 s); projeto literal `G = 1/[s(s+a)]` → `k = a²/(4ζ²)` e `k = π²/tp² + a²/4`;
>    - `L(s)` = Função de Transferência de Malha; constantes de erro `kp`, `kv`, `ka`; **tipo numérico** = nº de polos na origem; estabilidade = **BIBO**; curso **SISO**; derivadas em notação de pontos (`ÿ`, `u⁗`).

---

## 1. Árvore do repositório

```
lab-controle-automatico/
├── README.md                            ← plano de ensino: ementa, cronograma, avaliação, mapa de leituras
│
├── ambiente/
│   ├── instalacao.md                    ← guia de instalação: Python, Jupyter, python-control 0.10.2
│   ├── lab00_introducao_python_control.ipynb
│   └── exemplos_python_control.md       ← exemplos oficiais da documentação ↔ aulas do curso
│
├── imagens/                             ← TODAS as figuras geradas pelo curso (PNG/SVG)
│                                         Convenção de link obrigatória (GitHub, caminho absoluto):
│                                         https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/<arquivo>
│
├── modulo1_introducao/                  ← MÓDULO 01 — pacote de vídeos "01 - Introdução ao Controle de Sistemas"
│   ├── teoria_modulo1.md                ← texto teórico completo e autossuficiente (tópicos 1.1–1.4)
│   ├── notas_de_aula/                   ← guias de quadro para o professor (passo a passo, linha a linha)
│   │   ├── nota_1_1_sistemas_controle_e_modelos.md        (tópico 1.1, 7 vídeos)
│   │   ├── nota_1_2_laplace_e_funcao_de_transferencia.md  (tópico 1.2, 3 vídeos)
│   │   ├── nota_1_3_estabilidade_e_erro_em_regime.md      (tópico 1.3, 6 vídeos)
│   │   └── nota_1_4_resposta_ao_degrau_e_controle_P.md    (tópico 1.4, 7 vídeos)
│   ├── exercicios_resolvidos_modulo1.md ← ≥ 3 exercícios por tópico, resolvidos passo a passo
│   ├── labs/
│   │   ├── lab01_sistemas_e_transformada_de_laplace.ipynb
│   │   ├── lab02_funcao_de_transferencia_e_saida.ipynb
│   │   ├── lab03_estabilidade_erro_e_diagramas_de_blocos.ipynb
│   │   └── lab04_resposta_ao_degrau_e_projeto_proporcional.ipynb
│   └── slides/
│       ├── slides_aula01_sistemas_e_controle.md           (conteúdo + placeholder de figura + roteiro falado)
│       ├── slides_aula02_laplace_e_ft.md
│       ├── slides_aula03_estabilidade_e_erro.md
│       └── slides_aula04_degrau_e_controle_P.md
│
├── modulo2_plano_s/                     ← MÓDULO 02 — pacote de vídeos "02 - Controle de Sistemas no Plano-s"
│   ├── teoria_modulo2.md                (tópicos 2.1–2.5)
│   ├── notas_de_aula/  (5 notas, uma por tópico)
│   ├── exercicios_resolvidos_modulo2.md
│   ├── labs/
│   │   ├── lab05_plano_s_e_regioes_de_desempenho.ipynb
│   │   ├── lab06_lugar_das_raizes.ipynb
│   │   ├── lab07_projeto_avanco_de_fase.ipynb
│   │   └── lab08_atraso_PI_PID_e_atraso_de_transporte.ipynb
│   └── slides/ (5 decks com roteiro falado)
│
├── modulo3_resposta_em_frequencia/      ← MÓDULO 03 — pacote de vídeos "03 - Controle Usando a Resposta em Frequência"
│   ├── teoria_modulo3.md                (tópicos 3.1–3.5, incluindo os 2 vídeos novos da VERSÃO 3)
│   ├── notas_de_aula/  (5 notas, uma por tópico)
│   ├── exercicios_resolvidos_modulo3.md
│   ├── labs/
│   │   ├── lab09_bode_e_margens_de_estabilidade.ipynb
│   │   ├── lab10_nichols_e_nyquist.ipynb
│   │   └── lab11_projeto_de_controladores_em_frequencia.ipynb
│   └── slides/ (5 decks com roteiro falado)
│
├── modulo4_nao_linearidades/            ← MÓDULO 04 — AUTÔNOMO (Unidade III do PPC, não coberta pelos vídeos)
│   ├── teoria_modulo4.md                ← zona morta, histerese, saturação; windup; ciclos-limite e função descritiva
│   ├── notas_de_aula/  (3 notas)
│   ├── exercicios_resolvidos_modulo4.md
│   ├── labs/
│   │   ├── lab12_nao_linearidades_em_malha.ipynb
│   │   └── lab13_windup_ciclos_limite_e_rele.ipynb
│   └── slides/ (3 decks com roteiro falado)
│
├── trabalhos/                           ← trabalhos de 2024/2 integrados e adaptados a python-control
│   ├── trabalho1_identificacao_prbs_fopdt.md      (PRBS, FOPDT, Padé)
│   └── trabalho3_pid_posicao_motor_cc.md          (PID de posição no motor CC)
│
├── projeto_final/
│   └── lab15_projeto_final.md           ← enunciado do projeto final (integra Trabalhos 1 e 3)
│
├── listas/
│   ├── lista1_modulo1.md
│   ├── lista2_modulo2.md
│   ├── lista3_modulo3.md
│   └── lista4_modulo4.md
│
└── firmware/                            ← Arduino do kit (motor CC: velocidade e posição; planta térmica)
    ├── prbs_aquisicao/                  ← geração de PRBS + telemetria serial (suporte ao Trabalho 1)
    ├── pid_motor/                       ← PID ISA 2DOF, derivada filtrada, anti-windup (suporte ao Trabalho 3)
    └── telemetry.py                     ← registrador serial → CSV lido nos notebooks
```

**Observações sobre a árvore:**

- A pasta `imagens/` concentra todos os recursos visuais gerados (gráficos matplotlib/python-control em PNG e diagramas). Diagramas de blocos e fluxos de sinal usam **Mermaid.js** embutido no Markdown (blocos ```` ```mermaid ````), sem necessidade de imagem.
- Toda referência de figura no material usa o formato absoluto do GitHub, ex.:
  `https://github.com/fabiobento/lab-cont-2026-2/blob/main/imagens/fig_bode_motor_cc.png`
- Os Trabalhos 1 e 3 de 2024/2 foram adaptados: MATLAB/IDENT/tfest → `python-control` (estimação FOPDT por ajuste de curva e `control.pade` para aproximação do atraso), mantendo o hardware (Arduino + ponte H + motor CC + encoder) e o método (PRBS).

---

## 2. Mapa vídeo ↔ conteúdo — Pacote 01 (referência do professor)

Extraído das transcrições (detalhamento completo em `mapa_conteudo_videos_pacote01.md`). **Esta tabela não aparece no material do aluno.**

| # | Vídeo (pacote 01) | Conteúdo falado | Âncoras numéricas do vídeo (validadas) |
|---|---|---|---|
| 1.1.1 | O que é Sistema? | Etimologia; Ktesibius e o relógio de água; boia + válvula (caixa de descarga) | — (narrativo) |
| 1.1.2 | Exemplos de Sistemas | Sistema = parte do universo; bloco entrada/saída; perturbações; SISO; relação direta/oposta | — |
| 1.1.3 | O Objetivo do Controle | Modificar a relação e-s de forma eficiente; requisitos de desempenho; elevador | — |
| 1.1.4 | O Gráfico da Saída | Gráfico y×t; referência; erro e = r − y; requisitos no gráfico | forno 180 °C → 160 °C (erro 20 °C); carro 0–100 km/h em 8 s, faixa ±10 % |
| 1.1.5 | Análise e Projeto | Análise × projeto; MA × MF; servo didático; realimentação humana | referência 2 rad/s; massas → velocidade cai ~metade em MA |
| 1.1.6 | Exemplo de Malha Fechada | u = k·e; ajuste do ganho (túnel de vento); importância dos modelos | — (demonstração) |
| 1.1.7 | Modelos Matemáticos | Modelo parcimonioso; 3 modelagens → mesma forma ÿ + a1ẏ + a0y = b0u | massa-mola-amortecedor; RLC série; motor CC sem atrito: ÿ + (R/L)ẏ + (k²/LJ)y = (k/LJ)u |
| 1.2.1 | Transformada de Laplace | Linearidade; invariância; LIT; definição; propriedades; TVF | L{f″} = s²F(s) deduzido |
| 1.2.2 | Função de Transferência | G(s) = Y/U copiando coeficientes; polos e zeros; Bhaskara; forma fatorada | 1/(s²+2s+3); 2/(s³+8s²+4s); (2s+1)/(s²+3s+5); (s+3)/[(s+1)(s+2)] |
| 1.2.3 | Calculando a Saída | Tabela de TL; frações parciais; truque dos resíduos; polos repetidos | 2/[s(s+1)(s+2)] → 1−2e⁻ᵗ+e⁻²ᵗ; 20/[s(s+1)(s+10)] → 2−(20/9)e⁻ᵗ+(2/9)e⁻¹⁰ᵗ |
| 1.3.1 | BIBO Estabilidade | Definição BIBO; padrão dos polos; condição necessária e suficiente | 1/s + degrau → rampa; 1/(s²+1) + cos t → (t/2)·sen t |
| 1.3.2 | Critério de Routh-Hurwitz | Tabela de Routh; 2ª/3ª/4ª ordem; literais; nº de trocas = nº de raízes RHP | s²+3s+2 ✓; s²+s−2 ✗; s³+6s²+11s+6 (1,6,10,6) ✓; s³+6s²+11s+72 (1,6,−1,72) ✗; 4ª ordem (1,2,−1,20,5) → 2 raízes RHP |
| 1.3.3 | Vantagens da Realimentação | FTMF T = kG/(1+kG); estabilização; sensibilidade; perturbação | 1/(s−1) estável k>1; erro de modelo 20 %: 17 % (MA) → 1,5 % (MF, kA=10) / 5,6 % (kA=2) |
| 1.3.4 | Faixa de Estabilidade | Routh com parâmetros; casos-limite; múltiplos parâmetros | s³+6s²+11s+(6+k) → −6<k<60 (k=60 → ±j√11); 10/(s³+8s²+12s+10) → k<8,6; 10/(s³+11s²+8s−20) → 2<k<10,8 |
| 1.3.5 | Erro em Malha Aberta | ess para degrau/rampa/parábola; TVF; cascata de coeficientes | 1/[(s+1)(s+2)] → 0,5; 2/[(s+1)(s+2)] → 0 (rampa: 1,5); (s²+6s+9)/(s³+8s²+17s+10) → 0,1; pegadinha instável |
| 1.3.6 | Erro em Malha Fechada | L(s) = kG; kp, kv, ka; tipo numérico; tabela tipo × entrada | kp = k·b0/a0 etc.; ⚠ errata da legenda: tipo 0 → erro ao degrau **finito** |
| 1.4.1 | Por que 2ª ordem? | Por que degrau; por que 2ª ordem; aproximações visuais | 1/(s²+s+1) vs 5/[(s²+s+1)(s+5)] vs 64/[(s²+s+1)(s²+12s+64)]; contra-exemplo polo em −1 |
| 1.4.2 | Diferentes Respostas | Instável / superamortecida / criticamente amortecida / subamortecida | — |
| 1.4.3 | Características Subamortecida | tp, tr (0–100 %), ts (±5 %), Mp; relativas ao valor final | 1/(s²+s+1); 64/(s²+12s+64); 25/(s²+4s+25) |
| 1.4.4 | Parametrização de 2ª ordem | ζ, ωn, σ, ωd, φ; polos −σ ± jωd | y(t) = 1 − e^(−σt)/√(1−ζ²) · sen(ωd t + φ) |
| 1.4.5 | Fórmulas de 2ª ordem | tp, Mp, tr, ts; nomes dos parâmetros | 25/(s²+4s+25): ζ=0,4 → Mp=25,4 %, tp=0,69 s, tr=0,43 s, ts=1,5 s |
| 1.4.6 | Projeto p/ Overshoot | Inversão ζ(Mp); tabela ζ×Mp; projeto literal | **G = 1/[s(s+1)], Mp = 10 % → ζ = 0,59 → k = 0,718**; G = 1/[s(s+a)] → k = a²/(4ζ²) |
| 1.4.7 | Projeto p/ Instante de Pico | ωd = π/tp; conflito de requisitos; σ fixo no P | **G = 1/[s(s+1)], tp = 3,14 s → k = 1,25 (Mp = 20,8 %)**; k = π²/tp² + a²/4 |

*Os mapas dos pacotes 02 e 03 serão construídos da mesma forma a partir de `legendas_02.txt` e `legendas_03.txt` antes da regeneração dos Módulos 02 e 03.*

---

## 3. Plano de ensino remapeado — semana a semana (15 semanas × 2 h)

| Sem. | Módulo / Unidade PPC | Conteúdo teórico (ordem estrita dos vídeos) | Prática / entregas |
|---|---|---|---|
| 1 | — | Apresentação da disciplina; ambiente computacional | **Lab 00** — instalação e introdução à `python-control` |
| 2 | **M01** §1.1 (U.I) | O que é sistema; exemplos entrada/saída; SISO e perturbações; objetivo do controle; referência e erro; análise × projeto; MA × MF; controle proporcional; modelos matemáticos (massa-mola-amortecedor, RLC, motor CC) | **Lab 01** — sistemas e Transformada de Laplace em Python |
| 3 | **M01** §1.2 (U.I) | Linearidade e invariância (LIT); Transformada de Laplace e propriedades; TVF; função de transferência; polos e zeros; tabela de TL; frações parciais e resíduos; polos repetidos | **Lab 02** — FT e resposta temporal (`step_response`, frações parciais com `scipy.signal.residue`) |
| 4 | **M01** §1.3 (U.II) | Estabilidade BIBO; Routh–Hurwitz; FTMF e vantagens da realimentação; faixa de estabilidade; erro em regime MA/MF; L(s), kp/kv/ka, tipo numérico | **Lab 03** — estabilidade, erro e constantes de erro |
| 5 | **M01** §1.4 (U.II/IV) | Por que degrau/2ª ordem; tipos de resposta; tp, tr, ts, Mp; parametrização ζωn; fórmulas; **projeto P para overshoot (k = 0,718) e para instante de pico (k = 1,25) na planta 1/[s(s+1)]** | **Lab 04** — resposta ao degrau e projeto P. **Lançamento do Trabalho 1** (identificação PRBS/FOPDT do motor CC) |
| 6 | **M02** §2.1 (U.II) | Plano-s; regiões de desempenho (Mp, tp, ts, tr no plano-s); aproximações (3ª→2ª, 2ª→1ª, efeito de zero) | **Lab 05** — plano-s e regiões de desempenho |
| 7 | **M02** §2.2 (U.II) | Polos em malha fechada; o que é o LGR; regras de esboço; exemplos 3ª e 4ª ordem | **Lab 06** — LGR com `control.root_locus`. **Entrega do Trabalho 1** |
| 8 | **M02** §2.3 (U.IV) | Alterando a forma do LGR; projeto do controlador de avanço de fase; controlador PD | **Lab 07** — projeto de avanço de fase |
| 9 | **M02** §2.4–2.5 (U.IV) | Controlador de atraso de fase; PI; avanço-atraso e PID; atraso de transporte e projeto com atraso | **Lab 08** — atraso/PI/PID e aproximação de Padé |
| 10 | **M03** §3.1 (U.II/IV) | Resposta em frequência de sistemas LIT; diagrama de Bode; esboços; margem de fase; ajuste de ganho; relação MF × sobressinal | **Lab 09** — Bode e margens (`control.bode_plot`, `control.margin`) |
| 11 | **M03** §3.2–3.3 (U.II) | Carta de Nichols-Black; **Nichols-Black-Bode de 2ª e 3ª ordem (vídeo novo V3)**; diagrama de Nyquist; princípio do argumento; critério de Nyquist; margem de ganho; **margem de fase e efeito do atraso no Nyquist (vídeo novo V3)** | **Lab 10** — Nichols e Nyquist (`control.nichols_plot`, `control.nyquist_plot`) |
| 12 | **M03** §3.4–3.5 (U.IV) | Efeito de polo/zero no Bode; compensadores de avanço e atraso em frequência; PD, PI e PID no domínio da frequência | **Lab 11** — projeto de controladores em frequência. **Lançamento do Trabalho 3 / Projeto final** |
| 13 | **M04** §4.1–4.2 (U.III) | Não linearidades estáticas: saturação, zona morta, histerese; efeitos na malha; windup do integrador e anti-windup | **Lab 12** — não linearidades em malha (simulação) |
| 14 | **M04** §4.3 (U.III) | Ciclos-limite; função descritiva; experimento do relé (Ku = 4d/πa) e sintonia a partir dele | **Lab 13** — windup, ciclos-limite e relé |
| 15 | U.IV | Projeto final: implementação do PID de posição no motor CC (Trabalho 3 adaptado), testes e ajustes | **Apresentações do projeto final** (seminários, 10 min/grupo) |

---

## 4. Amarração com o PPC

| Unidade PPC (CH) | Onde é coberta no novo plano |
|---|---|
| **I — Modelagem e análise de sistemas físicos (6 h)** | M01 §1.1–1.2 (semanas 2–3) + identificação experimental (Trabalho 1, semanas 5–7) + resposta em frequência (M03 §3.1) |
| **II — Elementos essenciais em um sistema de controle (4 h)** | M01 §1.3–1.4 (semanas 4–5): estabilidade, malha fechada, erro, resposta ao degrau; reforçado em M02 §2.1–2.2 e M03 §3.3 |
| **III — Análise de não linearidades em malhas de controle (4 h)** | **M04 autônomo** (semanas 13–14): zona morta, histerese, saturação, windup, ciclos-limite |
| **IV — Projeto, sintonia e implementação de PID (16 h)** | Distribuída: projeto P (sem. 5), avanço/PD (sem. 8), atraso/PI/PID no plano-s (sem. 9), margens e projeto em frequência (sems. 10–12), PID digital/implementação e sintonia via Trabalho 3 + firmware (sems. 12–15) |

## 5. Convenções de produção (valem para todas as partes seguintes)

1. **Fidelidade às transcrições**: sequência de tópicos, exemplos, números e notação seguem os vídeos; divergências são sempre sinalizadas em nota (documentos do professor). Os exemplos trazidos de fora (versão anterior do repositório) entram como exercícios extras, nunca como exemplo principal.
2. **Material do aluno sem referências a vídeos**: teoria, exercícios, labs e listas são autossuficientes; apoio bibliográfico em caixas 📖 (Ogata, Nise, Schaum).
3. **Notas de aula**: desenvolvimento matemático linha a linha, sem saltos algébricos, pronto para transcrição no quadro branco, seguindo a sequência falada dos vídeos; incluem o mapeamento por vídeo (documento do professor) e falas sugeridas no tom das aulas.
4. **Exercícios resolvidos**: no mínimo 3 por tópico, com passo a passo completo e verificação computacional quando aplicável.
5. **Figuras**: código Python (`matplotlib` + `python-control`) com `plt.savefig('fig_x.png')`; inserção sempre por link absoluto do GitHub na pasta `imagens/`.
6. **Diagramas de blocos**: Mermaid.js em bloco ```` ```mermaid ````.
7. **Notebooks**: Markdown explicando a teoria antes de cada bloco de código; código comentado linha por linha; todos os números de exemplo conferidos por simulação em `python-control` 0.10.2.
8. **Slides**: conteúdo na tela (tópicos curtos) + placeholder de figura/diagrama + roteiro falado (speaker notes), espelhando a progressão dos vídeos.
9. **Fórmulas oficiais do curso**: `ts ≈ 3/σ` (±5 %), `tr = (π−β)/ωd`, `tp = π/ωd`, `Mp = e^(−ζπ/√(1−ζ²))`, `ζ = √(ln²Mp/(π²+ln²Mp))`, projeto P literal `k = a²/(4ζ²)` e `k = π²/tp² + a²/4` para `G = 1/[s(s+a)]`.
