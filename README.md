# Laboratório de Controle Automático — Engenharia Elétrica (Campus Guarapari) (2026/2)

Repositório da disciplina Laboratório de Controle Automático (7º período, 30 h, 2 aulas/semana). Pré-requisito: Controle Automático.

Este repositório está organizado como uma apostila de laboratório: cada módulo traz a teoria completa (conceitos do zero, para quem não tem os livros), os laboratórios computacionais em Python (notebooks executados e validados), as listas de exercícios com gabaritos detalhados e os exercícios resolvidos. Slides acompanham todas as aulas, e os trabalhos de bancada usam o kit Arduino + motor CC.

**Curso:** Engenharia Elétrica — 7º período — Ifes — campus Guarapari

**Carga horária:** 30 h (laboratório) — 2 aulas/semana, 15 semanas

**Pré-requisito:** Controle Automático

**Ferramenta computacional:** [python-control](https://python-control.readthedocs.io/) **0.10.2** (Python + Jupyter)

**Bancada:** Arduino + ponte H + motor CC + encoder magnético (Trabalhos 1 e 3, projeto final)

## Objetivos

**Geral (PPC):** desenvolver e testar, em um sistema real de controle, controladores analógicos e digitais para sistemas físicos dinâmicos.

**Específicos (PPC):** modelar e analisar um sistema de controle; obter o modelo matemático de um sistema físico real; projetar, implementar e testar controladores PID; utilizar software de simulação para desenvolver projeto de controladores.

Na prática, vamos buscar:

1. Modelar sistemas físicos (elétricos, mecânicos, eletromecânicos) por função de transferência e analisar sua resposta temporal;
2. Analisar estabilidade e erro em regime de sistemas realimentados (Routh-Hurwitz, constantes de erro);
3. Projetar controladores no plano-s (lugar das raízes: P, PD, avanço, atraso, PI, PID) e no domínio da frequência (Bode, Nichols-Black, Nyquist, margens);
4. Identificar experimentalmente uma planta real (PRBS → modelo FOPDT → aproximação de Padé);
5. Analisar não linearidades em malhas de controle (saturação, zona morta, histerese), o fenômeno de windup e suas soluções anti-windup, e prever ciclos-limite pela função descritiva;
6. Sintonizar (inclusive pelo experimento do relé), implementar embarcado e validar um controlador PID digital na planta real.

## Ementa (PPC)

Modelagem e análise de sistemas físicos. Estudo dos elementos essenciais em um sistema de
controle. Análise de não linearidades em malhas de controle. Projeto, sintonia e implementação
de controladores PID.

As quatro unidades do PPC e sua carga horária:

| Unidade | Tema | CH |
|---|---|---|
| I | Modelagem e análise de sistemas físicos | 6 h |
| II | Elementos essenciais em um sistema de controle | 4 h |
| III | Análise de não linearidades em malhas de controle | 4 h |
| IV | Projeto, sintonia e implementação de controladores PID | 16 h |

> **Nota sobre a ferramenta computacional.** O PPC menciona "MatLab e Simulink ou SCILAB"; este
> curso adota **[python-control](https://python-control.readthedocs.io/) 0.10.2** (Python,
> NumPy/SciPy, Jupyter) no lugar do MATLAB das edições anteriores, mantendo todos os conteúdos da
> ementa e alinhando a disciplina a uma ferramenta livre, gratuita e amplamente usada na
> indústria e na pesquisa. Nenhum material exige MATLAB.

## Plataformas

| Frente | Onde | Plataforma |
|---|---|---|
| Simulação e projeto | Todos os módulos (Labs 01–16) | **python-control 0.10.2** em notebooks Jupyter |
| Bancada (planta real) | Trabalhos 1 e 3, projeto final | **Arduino** + ponte H (L298N) + **motor CC** + **encoder magnético** |
| Aquisição de dados | Bancada | `firmware/telemetry.py` (pyserial → CSV) |

## Estrutura

```
lab-cont-2026-2/
├── README.md                          ← este arquivo (plano de ensino resumido)
├── modulo1_introducao/                ← semanas 1–5  · modelagem, Laplace, estabilidade, 2ª ordem, P
├── modulo2_plano_s/                   ← semanas 6–9  · plano-s, LGR, avanço, atraso/PI, PID, Padé
├── modulo3_frequencia/                ← semanas 10–14 · Bode, Nichols-Black, Nyquist, projeto
├── modulo4_nao_linearidades/          ← semana 15 · MÓDULO AUTÔNOMO (Unidade III do PPC)
│    (cada módulo contém:)
│    ├── teoria_moduloN.md             ← teoria completa, autossuficiente
│    ├── exercicios_resolvidos_moduloN.md
│    ├── listaN_moduloN.md + gabarito_listaN_moduloN.md
│    ├── labs/                         ← notebooks Jupyter (.ipynb)
│    └── slides/                       ← apresentação da aula
├── trabalhos/                         ← Trabalhos 1 e 3 (bancada motor CC)
├── projeto_final/                     ← enunciado, especificações e rubrica do projeto
├── firmware/                          ← sketches Arduino + telemetria Python
└── imagens/                           ← figuras geradas (m1_*, m2_*, m3_*, m4_*)
```

Detalhando cada item:

- `moduloN/teoria_moduloN.md` — **aula completa em texto**: conceitos explicados do zero, deduções,
  diagramas de blocos (Mermaid), figuras e exemplos numéricos resolvidos;
- `moduloN/exercicios_resolvidos_moduloN.md` — exercícios resolvidos passo a passo, no mesmo estilo
  das questões das listas (conta feita, unidade, conclusão);
- `moduloN/listaN_*.md` + `gabarito_listaN_*.md` — lista de exercícios e **gabarito detalhado**,
  com referência ao ponto exato da teoria em cada questão ("Consulte: teoria §X.Y");
- `moduloN/labs/` — **16 notebooks** computacionais (Lab 01–16), autocontidos e executados com 0 erros;
- `trabalhos/` — [Trabalho 1](trabalhos/trabalho1_identificacao_prbs_fopdt.md) (identificação
  PRBS/FOPDT, semanas 5–7) e [Trabalho 3](trabalhos/trabalho3_pid_posicao_motor_cc.md) (PID de
  posição, semanas 14–15);
- `projeto_final/` — [enunciado do projeto final](projeto_final/projeto_final_motor_cc.md):
  servo de posição que integra os Trabalhos 1 e 3, com especificações, rubrica e cronograma;
- `firmware/` — `prbs_aquisicao/` (PRBS + telemetria), `pid_motor/` (PID ISA 2DOF, derivada
  filtrada, anti-windup por clamping) e `telemetry.py` (coleta serial → CSV);
- `imagens/` — figuras geradas para a apostila (ver "Sobre as figuras", ao final);
- `00_planejamento/` — plano de ensino completo e mapas de conteúdo (documentos do professor).

## Como usar

Clone (ou sincronize) o repositório e instale o ambiente Python:

```bash
git clone https://github.com/fabiobento/lab-cont-2026-2.git
cd lab-cont-2026-2
pip install "control==0.10.2" numpy scipy matplotlib jupyter
```

Cada notebook de laboratório é autocontido: a primeira célula verifica as dependências e define as
funções utilitárias (métricas de resposta ao degrau etc.). Para começar:

```bash
jupyter notebook modulo1_introducao/labs/lab01_sistemas_e_modelos.ipynb
```

## Roteiro de leitura

**Módulo 1 — Introdução: modelos, Laplace, estabilidade e resposta temporal (semanas 1–5)**

| Semana | Teoria | Laboratório |
|---|---|---|
| 2 | [Sistemas de controle e modelos matemáticos](modulo1_introducao/teoria_modulo1.md) (§1.1) | [Lab 01 — sistemas e modelos](modulo1_introducao/labs/lab01_sistemas_e_modelos.ipynb) |
| 3 | Laplace e função de transferência (§1.2) | [Lab 02 — Laplace e FT](modulo1_introducao/labs/lab02_laplace_e_ft.ipynb) |
| 4 | Estabilidade e erro em regime (§1.3) | [Lab 03 — estabilidade e erro](modulo1_introducao/labs/lab03_estabilidade_e_erro.ipynb) |
| 5 | Resposta de 2ª ordem e projeto P (§1.4) — **lançamento do Trabalho 1** | [Lab 04 — resposta ao degrau e projeto P](modulo1_introducao/labs/lab04_resposta_2a_ordem_e_projeto_P.ipynb) |

**Módulo 2 — Projeto no plano-s (semanas 6–9)**

| Semana | Teoria | Laboratório |
|---|---|---|
| 6 | [Regiões do plano-s e aproximações](modulo2_plano_s/teoria_modulo2.md) (§2.1) | [Lab 05 — plano-s e aproximações](modulo2_plano_s/labs/lab05_plano_s_e_aproximacoes.ipynb) |
| 7 | Lugar das raízes (§2.2) — **entrega do Trabalho 1** | [Lab 06 — LGR](modulo2_plano_s/labs/lab06_lgr.ipynb) |
| 8 | Projeto de avanço de fase; PD (§2.3) | [Lab 07 — avanço de fase](modulo2_plano_s/labs/lab07_avanco_de_fase.ipynb) |
| 9 | Atraso de fase, PI; avanço-atraso, PID e atraso de transporte (§2.4–2.5) | [Lab 08 — atraso e PI](modulo2_plano_s/labs/lab08_atraso_e_pi.ipynb) · [Lab 09 — PID e Padé](modulo2_plano_s/labs/lab09_pid_e_atraso.ipynb) |

**Módulo 3 — Análise e projeto no domínio da frequência (semanas 10–14)**

| Semana | Teoria | Laboratório |
|---|---|---|
| 10 | [Resposta em frequência e Bode](modulo3_frequencia/teoria_modulo3.md) (§3.1) | [Lab 10 — Bode](modulo3_frequencia/labs/lab10_resposta_em_frequencia_e_bode.ipynb) |
| 11 | Carta de Nichols-Black (§3.2) | [Lab 11 — Nichols-Black](modulo3_frequencia/labs/lab11_carta_de_nichols_black.ipynb) |
| 12 | Nyquist e efeito do atraso (§3.3) | [Lab 12 — Nyquist](modulo3_frequencia/labs/lab12_nyquist_e_atraso.ipynb) |
| 13 | Projeto de avanço e atraso na frequência (§3.4) | [Lab 13 — projeto na frequência](modulo3_frequencia/labs/lab13_projeto_avanco_e_atraso.ipynb) |
| 14 | PD, PI e PID na frequência (§3.5) — **lançamento do Trabalho 3 / projeto final** | [Lab 14 — PD/PI/PID na frequência](modulo3_frequencia/labs/lab14_pd_pi_pid_na_frequencia.ipynb) |

**Módulo 4 — Não linearidades em malhas de controle (semana 15, módulo autônomo)**

| Semana | Teoria | Laboratório |
|---|---|---|
| 15 | [Não linearidades estáticas; windup e anti-windup; ciclos-limite, função descritiva e experimento do relé](modulo4_nao_linearidades/teoria_modulo4.md) (§4.1–4.3) — **apresentações do projeto final** | [Lab 15 — não linearidades em malha](modulo4_nao_linearidades/labs/lab15_nao_linearidades_em_malha.ipynb) · [Lab 16 — windup, ciclos-limite e relé](modulo4_nao_linearidades/labs/lab16_windup_ciclos_limite_e_rele.ipynb) |

**Listas de exercícios** (com gabarito detalhado, passo a passo)

| Lista | Conteúdo | Enunciado |
|---|---|---|
| 1 | Módulo 1 (semanas 1–5) | [lista 1](modulo1_introducao/lista1_modulo1.md) |(modulo1_introducao/
| 2 | Módulo 2 (semanas 6–9) | [lista 2](modulo2_plano_s/lista2_modulo2.md) |(modulo2_plano_s/
| 3 | Módulo 3 (semanas 10–14) | [lista 3](modulo3_frequencia/lista3_modulo3.md) |
| 4 | Módulo 4 (semana 15) | [lista 4](modulo4_nao_linearidades/lista4_modulo4.md) |

## Slides

Cada módulo traz seus decks em `slides/`: 4 apresentações no Módulo 1, 5 no Módulo 2, 5 no
Módulo 3 e 3 no Módulo 4 (aulas 15a–15c) — **17 apresentações** no total, uma por aula.

## Cronograma (15 semanas)

As unidades (U1–U4) seguem o PPC da disciplina.

| Semana | Unidade | Atividade |
|---|---|---|
| 1 | — | Apresentação da disciplina; ambiente computacional (Python + python-control) |
| 2 | U1 | Sistemas, sinais e modelos matemáticos (massa-mola, RLC, motor CC) — Lab 01 |
| 3 | U1 | Transformada de Laplace e função de transferência — Lab 02 |
| 4 | U2 | Estabilidade (BIBO, Routh), malha fechada e erro em regime — Lab 03 |
| 5 | U2 | Resposta de 2ª ordem e projeto proporcional — Lab 04 · **Trabalho 1 lançado** |
| 6 | U4 | Regiões do plano-s e aproximações de polos dominantes — Lab 05 |
| 7 | U4 | Lugar das raízes — Lab 06 · **Trabalho 1 entregue** |
| 8 | U4 | Projeto de avanço de fase; controlador PD — Lab 07 |
| 9 | U4 | Atraso de fase, PI; avanço-atraso, PID e atraso de transporte (Padé) — Labs 08–09 |
| 10 | U1/U4 | Resposta em frequência, diagrama de Bode e margens — Lab 10 |
| 11 | U4 | Pico de ressonância e carta de Nichols-Black — Lab 11 |
| 12 | U4 | Critério de Nyquist e efeito do atraso — Lab 12 |
| 13 | U4 | Projeto de avanço e atraso na frequência — Lab 13 |
| 14 | U4 | PD, PI e PID na frequência — Lab 14 · **Trabalho 3 / projeto final lançados** |
| 15 | U3/U4 | Não linearidades: saturação, zona morta, histerese; windup/anti-windup; ciclos-limite, função descritiva e experimento do relé — Labs 15–16 · **Lista 4** · **apresentações do projeto final** |

## Estratégias de aprendizagem

Conforme o PPC: aula expositiva; exercícios de análise e síntese; roteiros de laboratório; estudo
de caso; trabalhos em grupo; resolução de situações-problema.

Cada semana segue o ciclo: **(i)** exposição teórica pelo deck da aula (com exemplos resolvidos em
destaque); **(ii)** laboratório computacional em notebook (simulação guiada, com perguntas de
análise); **(iii)** discussão dos resultados; **(iv)** lista de exercícios do módulo, cujo
gabarito detalhado serve de revisão. Nos trabalhos de bancada, o ciclo se estende à planta real:
identificação → projeto → implementação embarcada → validação.

## Avaliação da aprendizagem

Instrumentos previstos no PPC: avaliação escrita (testes e provas); exercícios; elaboração e
apresentação de trabalhos. Neste curso, tomam a forma:

| Instrumento | Cobre | Como é entregue |
|---|---|---|
| Listas de exercícios (4) | Módulos 1–4 | Individuais, nos prazos indicados em aula; gabarito disponível para revisão |
| Trabalho 1 — identificação PRBS/FOPDT | Unidade I | Em grupo (até 3), apresentação presencial, semana 7 — 15 pontos |
| Trabalho 3 — PID de posição no motor CC | Unidade IV | Em grupo (até 2), apresentação presencial, semana 15 — 28 pontos |
| Projeto final — servo de posição | Unidades I–IV | Em grupo; integra os Trabalhos 1 e 3; rubrica em `projeto_final/` |

### Pesos dos instrumentos

A composição da nota semestral segue o plano de ensino da turma:

| Instrumento | Peso |
|---|---|
| Listas de exercícios | _a definir_ |
| Trabalho 1 | _a definir_ |
| Trabalho 3 | _a definir_ |
| Projeto final | _a definir_ |
| **Total** | **100 %** |

Dentro do **projeto final**, a distribuição já está definida em sua rubrica: identificação e
validação do modelo 20 %, projeto do controlador 25 %, atendimento às especificações na planta
real 30 %, demonstração do anti-windup/não linearidades 15 % e apresentação 10 % — ver o
[enunciado](projeto_final/projeto_final_motor_cc.md).

## Convenções usadas no texto

- **Exercício resolvido N.M** — contas e raciocínios completos, no mesmo estilo das questões das
  listas. Refazer sem olhar é a melhor preparação.
- **"Consulte: teoria §X.Y"** — nos gabaritos, cada questão indica o ponto exato da teoria onde o
  tema é desenvolvido.
- **Vírgula decimal** em textos, tabelas e figuras (padrão pt-BR).
- Diagramas de blocos em **Mermaid**, dentro dos próprios arquivos de teoria.
- Figuras numeradas por módulo: `m1_figXX_*`, `m2_figXX_*`, `m3_figXX_*`, `m4_figXX_*`.

## Bibliografia

**Referências deste curso:**

- OGATA, K. _Engenharia de Controle Moderno_. 5. ed. Pearson. **(referência principal)**
- NISE, N. S. _Engenharia de Sistemas de Controle_. 7. ed. LTC. **(referência principal)**
- DISTEFANO, J. J.; STUBBERUD, A. R.; WILLIAMS, I. J. _Schaum's Outline of Feedback and Control
  Systems_. 2. ed. McGraw-Hill. **(exercícios resolvidos)**
- Documentação do **python-control** — https://python-control.readthedocs.io/ **(referência
  computacional oficial; usar a versão 0.10.2)**

> As teorias de cada módulo são autossuficientes; as caixas 📖 ao longo dos textos indicam os
> capítulos específicos de cada livro para aprofundamento — este é o mapa de leituras detalhado,
> mantido junto ao conteúdo.

## Sobre as figuras

O diretório `imagens/` reúne as **figuras geradas computacionalmente** para esta apostila
(matplotlib/Python), usadas para fins didáticos nos arquivos de teoria — respostas ao degrau,
regiões do plano-s, lugares das raízes, diagramas de Bode/Nyquist/Nichols-Black, características
de não linearidades, respostas com windup e ciclos-limite simulados. Todas são referenciadas nos
textos por URL absoluta deste repositório.
