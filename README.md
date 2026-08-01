# Laboratório de Controle Automático

Este é o repositório da disciplina **Laboratório de Controle Automático** (Engenharia Elétrica,
7º período). Ele está organizado como uma **apostila**: cada unidade traz a **teoria em formato
tutorial** (conceitos deduzidos do zero, para quem não tem os livros em mãos), os **roteiros de
laboratório** em Jupyter e o **firmware** do projeto final. Slides de teoria e de prática acompanham todas as aulas.

**Curso:** Engenharia Elétrica — 7º período — Ifes — campus Guarapari

**Carga horária:** 30 h de laboratório (2 aulas/semana, 15 semanas)

**Pré-requisito:** Controle Automático

**Ferramenta principal:** [Python Control Systems Library](https://python-control.readthedocs.io/en/0.10.2/index.html) (`python-control`)

> Este material adota Python + `python-control` como alternativa livre e gratuita ao MATLAB/Simulink e SCILAB previstos no PPC, seguindo o modelo do curso [CDS 110 — Analysis and Design of Feedback Control Systems (Caltech)](https://murray.cds.caltech.edu/CDS_110/ChE_105,_Spring_2024), ministrado pelo [Prof. Richard Murray](https://www.linkedin.com/in/murrayrm) com a mesma biblioteca.

---

## Objetivos

**Geral:** desenvolver e testar, em um sistema real de controle, controladores analógicos e digitais para sistemas físicos dinâmicos.

**Específicos:**

1. Modelar e analisar um sistema de controle;
2. Obter o modelo matemático de um sistema físico real;
3. Projetar, implementar e testar controladores PID;
4. Utilizar software de computação numérica (Python + `python-control`) para desenvolver projetos de controladores.

## Ementa

Modelagem e análise de sistemas físicos. Estudo dos elementos essenciais em um sistema de controle. Análise de não-linearidades em malhas de controle. Projeto, sintonia e implementação de controladores PID.

As quatro unidades e sua carga horária:

| Unidade | Tema | Apostila | Labs | CH |
|:---:|---|---|---|:---:|
| **I** | Modelagem e análise de sistemas físicos | [`teoria_unidade1.md`](unidade1/teoria_unidade1.md) | 01–03 | 6 h |
| **II** | Elementos essenciais de um sistema de controle (malha fechada, estabilidade, desempenho) | [`teoria_unidade2.md`](unidade2/teoria_unidade2.md) | 04–05 | 4 h |
| **III** | Não-linearidades em malhas de controle | [`teoria_unidade3.md`](unidade3/teoria_unidade3.md) | 06–07 | 4 h |
| **IV** | Projeto, sintonia e implementação de PID | [`teoria_unidade4.md`](unidade4/teoria_unidade4.md) | 08–11 + projeto | 16 h |

## Estrutura do material

```
lab-controle-automatico/
├── README.md                          ← este arquivo (plano de ensino)
├── ambiente/
│   ├── instalacao.md                  ← guia de instalação do ambiente
│   ├── lab00_introducao_python_control.ipynb
│   └── exemplos_python_control.md     ← exemplos oficiais da biblioteca ↔ labs do curso
├── unidade1/                          ← Modelagem e análise de sistemas físicos (6 h)
│   ├── teoria_unidade1.md
│   ├── lab01_modelagem_edo.ipynb
│   ├── lab02_resposta_temporal.ipynb
│   └── lab03_resposta_em_frequencia.ipynb
├── unidade2/                          ← Elementos essenciais de um sistema de controle (4 h)
│   ├── teoria_unidade2.md
│   ├── lab04_sistemas_1a_2a_ordem.ipynb
│   └── lab05_estabilidade_malha_fechada.ipynb
├── unidade3/                          ← Não-linearidades em malhas de controle (4 h)
│   ├── teoria_unidade3.md
│   ├── lab06_nao_linearidades.ipynb
│   └── lab07_windup_e_ciclos_limite.ipynb
├── unidade4/                          ← Projeto, sintonia e implementação de PID (16 h)
│   ├── teoria_unidade4.md
│   ├── lab08_pid_fundamentos.ipynb
│   ├── lab09_sintonia_pid.ipynb
│   ├── lab10_pid_digital_implementacao.ipynb
│   ├── lab11_controle_2dof.ipynb
│   └── lab12_projeto_final_expandido.md         ← enunciado do projeto final
└── listas/                            ← listas de exercícios
└── slides/                            ← 8 decks (teoria + prática de cada unidade)
```

Detalhando cada item do repositório:

- **`unidadeX/teoria_unidadeX.md`** — a **apostila da unidade**: explica os conceitos do zero,
  com deduções completas, **exercícios resolvidos passo a passo** e caixas 📖 indicando
  capítulo/seção de cada livro (Ogata, Nise, Schaum, Penedo e FBS) para aprofundamento. Cada
  apostila termina com uma seção **"Resumo da unidade e conexão com os labs"** — o mapa
  detalhado conceito → seção → lab, reproduzido de forma consolidada [logo abaixo](#roteiro-de-leitura-da-teoria-à-prática).
- **`unidadeX/labYY_*.ipynb`** — o **roteiro de laboratório** correspondente: demonstração
  guiada, prática do estudante e discussão dos resultados, todo em `python-control`.
- **`ambiente/`** — `instalacao.md` prepara o Python antes da primeira aula;
  `lab00_introducao_python_control.ipynb` apresenta a sintaxe básica da biblioteca; e
  `exemplos_python_control.md` mapeia os exemplos oficiais da `python-control` 0.10.2 para os
  labs (função descritiva no Lab 07; cruise control, retratos de fase, `interconnect` e
  simulação híbrida como leitura paralela) e lista o que fica além da ementa.
- **`slides/`** — oito apresentações: para cada unidade, um deck de **teoria** e um de
  **prática** separados (a aula começa pela exposição teórica e depois passa ao laboratório),
  com referências aos livros no rodapé de cada slide, exercícios resolvidos em destaque e
  **roteiro falado** nas notas do apresentador.
- **`listas/`** — `lista1_unidade1.md` … `lista4_unidade4.md`: enunciados para os estudantes.
- **`firmware/`** — código Arduino do **projeto final** (PID ISA com 2DOF, derivada filtrada e
  anti-windup) para as três plantas do kit (motor CC em velocidade, motor em posição e planta
  térmica), além do registrador serial `telemetry.py` que gera o CSV lido nos notebooks.

## Como usar este repositório

Cada unidade segue sempre o mesmo fluxo — **teoria → laboratório → lista**:

1. **Antes da primeira aula:** rode `ambiente/instalacao.md` e o `lab00` para confirmar a
   versão da `python-control`.
2. **A cada unidade:** leia a **apostila** (`unidadeX/teoria_unidadeX.md`) até o ponto indicado
   no roteiro da semana; depois abra o **notebook do laboratório** e execute a prática guiada;
   ao fim da unidade, resolva a **lista de exercícios** correspondente.
3. **Nas semanas finais:** use o `firmware/` e o `lab12_projeto_final_expandido.md` para identificar,
   projetar e implementar o PID na planta física.

A seção seguinte é o mapa que amarra esses três passos: mostra, **seção a seção da apostila,
onde cada conceito é praticado**.

## Entrega das duplas no GitHub (ao longo de todo o semestre)

A avaliação de laboratório (Labs 01–11) **não** é uma prova única no fim: ela é o **fluxo
contínuo de entregas** que cada dupla acumula no próprio repositório GitHub, laboratório após
laboratório. Esse histórico é parte central da nota de relatórios — e começa já no Lab 01.

**Como funciona:**

- **No Lab 01**, cada dupla cria um repositório **privado** `lab-controle-dupla-XX` (XX = número
  da bancada) e adiciona o colega **e o professor** como colaboradores. A dupla vale para o
  semestre inteiro.
- A estrutura é **uma pasta por laboratório** (`lab-01/`, `lab-02/`, …), cada uma com o
  **notebook executado** (`.ipynb` com as saídas salvas), um `relatorio.md` com a análise dos
  resultados e os arquivos pedidos na seção **Entrega** daquele laboratório (por exemplo, o CSV
  de bancada usado no notebook).
- Cada laboratório tem prazo **até a próxima aula prática** e é entregue **por commit** no
  repositório da dupla — não por e-mail nem por outro canal.

**Sincronizar o material oficial antes de cada lab.** O material da disciplina (este
repositório) é atualizado ao longo do semestre; puxe a versão da semana antes de começar:

```
# uma vez, no Lab 00:
git clone https://github.com/fabiobento/lab-cont-2026-2.git

# no início de cada laboratório:
cd lab-cont-2026-2 && git pull
```

Trabalhe **sempre no repositório da sua dupla**, copiando para lá o notebook da semana — assim o
`git pull` do material oficial nunca sobrescreve o seu trabalho.

**Por que isso importa (e pesa na nota):**

- O **notebook executado + análise**, entregue por commit a cada semana, é exatamente o que
  compõe os **Relatórios de laboratório (40 %)** da tabela de [Avaliação](#avaliação-da-aprendizagem).
  O mesmo hábito de versionamento evolui naturalmente para o **relatório técnico + código** do
  **Projeto final (30 %)**, congelado com a tag `v1.0` na semana 15.
- Commits **pequenos, frequentes e com mensagens descritivas** desde a primeira semana valem mais
  do que um único commit na véspera (facilmente detectável). Exemplo de boa mensagem:
  `lab02: identificação FOPDT pelos dois pontos — RMSE 3,1%`; exemplo ruim: `update`.
- O histórico de commits também dá base objetiva para a **nota individual** dentro da dupla: quem
  fez o quê fica registrado.

> **Em resumo:** o repositório da dupla é o seu **caderno de laboratório versionado**. Mantê-lo
> vivo, semana a semana, é a forma de entrega da disciplina e uma fração relevante da avaliação —
> não deixe para o fim.

> **Nota para o professor:** esta seção descreve um fluxo de entrega **sugerido** (repositório
> privado por dupla + colaborador professor). Ajuste o nome do repositório-modelo, a
> obrigatoriedade e os prazos ao plano de ensino da turma antes de publicar.

---

## Roteiro de leitura: da teoria à prática

Esta é a relação **explícita entre as seções das apostilas de teoria e os laboratórios**. Para
cada unidade, a tabela indica em que **seção** o conceito é deduzido, em **qual lab** ele é
praticado e o **livro-âncora** para aprofundar. As tabelas espelham (e consolidam num único
lugar) as seções "Resumo da unidade e conexão com os labs" de cada apostila.

> **Como ler:** a coluna *Seção da apostila* usa a numeração interna de cada
> `teoria_unidadeX.md` (§1, §2.3, …); a coluna *Onde pratica* aponta o notebook do laboratório
> (e, quando útil, o projeto final ou o firmware).

### Unidade I — Modelagem e análise de sistemas físicos → Labs 01–03

Apostila: [`unidade1/teoria_unidade1.md`](unidade1/teoria_unidade1.md)

| Seção da apostila | Conceito | Onde pratica | Livro-âncora |
|---|---|---|---|
| **§1** (1.1–1.4) | Física → EDO (mecânico, elétrico, fluídico); linearização em §1.4; FT a partir do §3; térmico deduzido em §6.1 | [Lab 01](unidade1/lab01_modelagem_edo.ipynb) | Ogata 3–4; Nise 2 |
| **§2** | Transformada de Laplace e frações parciais (os três casos) | [Lab 01](unidade1/lab01_modelagem_edo.ipynb) / [Lab 02](unidade1/lab02_resposta_temporal.ipynb), Lista 1 | Schaum 4 |
| **§3** | Função de transferência, polos/zeros e redução de diagramas de blocos | [Labs 01–03](unidade1/) (e Lab 04) | Nise 2 e 5; Schaum 7 |
| **§4** | Sistemas de 1ª e 2ª ordem: $M_p$, $t_s$, geometria do plano $s$ | [Lab 02](unidade1/lab02_resposta_temporal.ipynb) e [Lab 04](unidade2/lab04_sistemas_1a_2a_ordem.ipynb) | Nise 4; Penedo 4 |
| **§5** (esp. §5.5) | Espaço de estados; motor CC deduzido linha a linha | [Lab 01](unidade1/lab01_modelagem_edo.ipynb) → projeto final | Nise 3; Ogata 2–3 |
| **§6** | Identificação experimental por degrau (FOPDT, método dos dois pontos) | [Lab 02](unidade1/lab02_resposta_temporal.ipynb) → projeto final | Ogata 4 e 8 |
| **§7** | Resposta em frequência e Bode (assíntotas, ressonância, tempo morto) | [Lab 03](unidade1/lab03_resposta_em_frequencia.ipynb) | Ogata 7; Nise 10; Schaum 15 |

### Unidade II — Malha fechada: estabilidade e desempenho → Labs 04–05

Apostila: [`unidade2/teoria_unidade2.md`](unidade2/teoria_unidade2.md)

| Seção da apostila | Conceito | Onde pratica | Livro-âncora |
|---|---|---|---|
| **§1** | Malha aberta × fechada; funções $T$, $T_{dy}$ e sensibilidade | [Lab 04](unidade2/lab04_sistemas_1a_2a_ordem.ipynb) | Nise 5; FBS 2 |
| **§2** | Erro de regime permanente e o "tipo" do sistema | [Lab 04](unidade2/lab04_sistemas_1a_2a_ordem.ipynb) / [Lab 05](unidade2/lab05_estabilidade_malha_fechada.ipynb), Lista 2 | Nise 7; Schaum 9 |
| **§3** | Estabilidade absoluta: critério de Routh–Hurwitz e faixa de ganho | [Lab 05](unidade2/lab05_estabilidade_malha_fechada.ipynb) §1–2 | Nise 6; Ogata 5 |
| **§4** | Lugar das raízes (regras de esboço + intuições de projeto) | [Lab 05](unidade2/lab05_estabilidade_malha_fechada.ipynb) §3 | Nise 8; Ogata 6 |
| **§5** | Estabilidade relativa: margens de ganho e de fase | [Lab 05](unidade2/lab05_estabilidade_malha_fechada.ipynb) §4–6 | Ogata 7; Nise 10–11 |
| **§6** | Critério de Nyquist ($Z = N + P$, $s_m = 1/M_s$) | [Lab 05](unidade2/lab05_estabilidade_malha_fechada.ipynb) §7 | FBS 10; Schaum 11 |

### Unidade III — Não-linearidades em malhas de controle → Labs 06–07

Apostila: [`unidade3/teoria_unidade3.md`](unidade3/teoria_unidade3.md)

| Seção da apostila | Conceito | Onde pratica | Livro-âncora |
|---|---|---|---|
| **§1** (1.1–1.3) | Não-linearidades estáticas: saturação, zona morta e histerese | [Lab 06](unidade3/lab06_nao_linearidades.ipynb) §3–5 (+ firmware `DEADZONE_COMP`) | FBS 5 e 11; Å&H 3–4 |
| **§2** | Windup do integrador e a cura por *back-calculation* | [Lab 07](unidade3/lab07_windup_e_ciclos_limite.ipynb) §1 → Lab 10 e firmware | FBS 11 |
| **§3** | Retratos de fase, equilíbrios e região de atração | [Lab 06](unidade3/lab06_nao_linearidades.ipynb) §6 | FBS 5; CDS 110 L2 |
| **§4** | Ciclos-limite e função descritiva; **experimento do relé** ($K_u = 4d/\pi a$) | [Lab 07](unidade3/lab07_windup_e_ciclos_limite.ipynb) §2 → projeto final | Schaum 19; Å&H 4 |

### Unidade IV — Projeto, sintonia e implementação de PID → Labs 08–11 + projeto

Apostila: [`unidade4/teoria_unidade4.md`](unidade4/teoria_unidade4.md)

| Seção da apostila | Conceito | Onde pratica | Livro-âncora |
|---|---|---|---|
| **§1** | Algoritmo PID e o efeito de cada ação (P, I, D) | [Lab 08](unidade4/lab08_pid_fundamentos.ipynb) | Ogata 5 e 8 |
| **§2** | O PID "de verdade": filtro derivativo, derivada na medição, PI-D | [Lab 08](unidade4/lab08_pid_fundamentos.ipynb) → [Lab 10](unidade4/lab10_pid_digital_implementacao.ipynb) | FBS 11; Ogata 8 |
| **§3** | Sintonia: Ziegler–Nichols (1º e 2º métodos), CHR e lambda (IMC) | [Lab 09](unidade4/lab09_sintonia_pid.ipynb) | Ogata 8; Å&H 4–5 |
| **§4** | Projeto por *loop shaping* (moldar o Bode da malha) | [Lab 09](unidade4/lab09_sintonia_pid.ipynb) → [Lab 10](unidade4/lab10_pid_digital_implementacao.ipynb) | FBS 12 |
| **§5** | Auditoria de robustez: *gang of four* e $M_s$ | [Lab 08](unidade4/lab08_pid_fundamentos.ipynb) e [Lab 10](unidade4/lab10_pid_digital_implementacao.ipynb) | FBS 10–12 |
| **§6** | Dois graus de liberdade (2DOF) / *setpoint weighting* | [Lab 11](unidade4/lab11_controle_2dof.ipynb) | Ogata 8; FBS 11 |
| **§7** | PID digital: amostragem, aliasing, Euler × Tustin, anti-windup | [Lab 10](unidade4/lab10_pid_digital_implementacao.ipynb) + firmware | Nise 13; CDS 110 L9-2 |
| **§8** | O procedimento completo (a receita do curso) | Projeto final (semanas 13–15) | — |

> **Observação sobre a Unidade IV:** o **Lab 10** trata do **PID digital** e o **Lab 11**, do
> **controle 2DOF** (conforme os notebooks e o cronograma). O *loop shaping* e a *gang of four*
> aparecem já no bloco de fundamentos/sintonia (Labs 08–09) e são retomados na implementação
> digital (Lab 10).

### Panorama semana a semana

Amarra o cronograma às **seções da apostila** estudadas em cada encontro:

| Sem. | Un. | Teoria (seções) | Laboratório |
|---:|:---:|---|---|
| 1  | — | — (ambiente) | [Lab 00 — introdução à `python-control`](ambiente/lab00_introducao_python_control.ipynb) |
| 2  | I | §1, §3, §5 | [Lab 01 — modelagem por EDO (FT e espaço de estados)](unidade1/lab01_modelagem_edo.ipynb) |
| 3  | I | §2, §4, §6 | [Lab 02 — resposta temporal e identificação FOPDT](unidade1/lab02_resposta_temporal.ipynb) |
| 4  | I | §7 | [Lab 03 — resposta em frequência (Bode experimental)](unidade1/lab03_resposta_em_frequencia.ipynb) |
| 5  | II | §1, §2 (+ U1 §4) | [Lab 04 — sistemas de 1ª e 2ª ordem em malha](unidade2/lab04_sistemas_1a_2a_ordem.ipynb) |
| 6  | II | §3, §4, §5, §6 | [Lab 05 — estabilidade: Routh, LGR, margens, Nyquist](unidade2/lab05_estabilidade_malha_fechada.ipynb) |
| 7  | III | §1, §3 | [Lab 06 — não-linearidades e retratos de fase](unidade3/lab06_nao_linearidades.ipynb) |
| 8  | III | §2, §4 | [Lab 07 — windup e ciclos-limite (experimento do relé)](unidade3/lab07_windup_e_ciclos_limite.ipynb) |
| 9  | IV | §1, §2, §5 | [Lab 08 — PID: ações P, I e D](unidade4/lab08_pid_fundamentos.ipynb) |
| 10 | IV | §3, §4 | [Lab 09 — sintonia: ZN, CHR e lambda](unidade4/lab09_sintonia_pid.ipynb) |
| 11 | IV | §7 (+ §2) | [Lab 10 — PID digital: discretização e anti-windup](unidade4/lab10_pid_digital_implementacao.ipynb) |
| 12 | IV | §6 | [Lab 11 — controle com dois graus de liberdade (2DOF)](unidade4/lab11_controle_2dof.ipynb) |
| 13–15 | IV | §8 (+ U1 §6, U3 §4) | [Projeto final](unidade4/lab12_projeto_final_expandido.md) — identificação, projeto e implementação na planta real |

---

## Cronograma (15 semanas × 2 h)

| Semana | Unidade | Atividade | CH |
|-------:|---------|-----------|---:|
| 1  | — | **Lab 00** — Ambiente Python, Jupyter e introdução à `python-control` | 2 h |
| 2  | I | **Lab 01** — Modelagem por equações diferenciais: FT e espaço de estados | 2 h |
| 3  | I | **Lab 02** — Simulação e resposta temporal (degrau, impulso, entrada arbitrária) | 2 h |
| 4  | I | **Lab 03** — Resposta em frequência e identificação experimental (Bode) | 2 h |
| 5  | II | **Lab 04** — Sistemas de 1ª e 2ª ordem: polos, amortecimento, especificações | 2 h |
| 6  | II | **Lab 05** — Estabilidade em malha fechada: lugar das raízes, margens de ganho e fase | 2 h |
| 7  | III | **Lab 06** — Não-linearidades estáticas: saturação, zona morta, histerese | 2 h |
| 8  | III | **Lab 07** — Efeitos em malha fechada: windup do integrador e ciclos-limite | 2 h |
| 9  | IV | **Lab 08** — Algoritmo PID: ações P, I e D e seus efeitos | 2 h |
| 10 | IV | **Lab 09** — Sintonia: Ziegler–Nichols, CHR e método lambda (IMC) | 2 h |
| 11 | IV | **Lab 10** — PID digital: discretização, filtro derivativo, anti-windup | 2 h |
| 12 | IV | **Lab 11** — Controle com dois graus de liberdade (2DOF) | 2 h |
| 13 | IV | **Projeto final** — identificação do sistema físico real | 2 h |
| 14 | IV | **Projeto final** — projeto, sintonia e implementação do PID | 2 h |
| 15 | IV | **Projeto final** — testes, relatório e apresentação de seminários | 2 h |

---

## Convenções usadas no material

Ao longo das apostilas e dos notebooks, alguns recursos se repetem:

- **Exercício resolvido N** — contas e raciocínios completos, no mesmo estilo das questões das
  listas. Refazer sem olhar é a melhor preparação (são 24 exercícios resolvidos no total).
- **Autoavaliação** — ao fim de cada apostila, a lista do que você deve conseguir fazer antes
  de tentar a lista de exercícios da unidade.
- **Observação** — detalhe de implementação ou armadilha clássica de bancada.
- 📖 — caixa "Onde estudar": aponta capítulo/seção/figura de cada livro (Ogata, Nise, Schaum,
  Penedo, FBS) para aprofundar. **As apostilas são autossuficientes**; as caixas 📖 são opcionais.
- Cada apostila fecha com um **"Mapa das fórmulas"** (folha de consulta) e uma tabela de
  **"Leituras dirigidas"** para quem quiser conferir a formulação original nas fontes.

**Plantas de referência do curso** (usadas de forma consistente em toda a apostila):

- Planta principal — motor CC do kit: **$G(s) = 5/(2s+1)$**.
- Planta de 3ª ordem (estabilidade/sintonia): **$1/[(s+1)(s+2)(s+4)]$**, com $K_u = 90$,
  $\omega_u = \sqrt{14}$, $T_u \approx 1{,}68$ s — obtidos por Routh (Lab 05), reencontrados
  pelo relé (Lab 07) e usados nas tabelas de Ziegler–Nichols (Lab 09).
- Planta FOPDT (identificação/sintonia): **$3\,e^{-1{,}5s}/(4s+1)$**.
- Critério de aceitação de projeto: **PM ≥ 45°**, **GM ≥ 6 dB**, **$M_s \le 2$**.

---

## Estratégias de aprendizagem

Aula expositiva; demonstração prática realizada pelo professor; laboratório (prática realizada pelo estudante); trabalho em grupo; exercícios de análise e síntese; estudo de caso; resolução de situações-problema.

Cada encontro segue o ciclo: **(i)** exposição teórica breve (≈20 min); **(ii)** demonstração guiada no notebook; **(iii)** prática do estudante nos exercícios do notebook; **(iv)** discussão dos resultados.

## Avaliação da aprendizagem

| Instrumento | Peso | Observações |
|---|---:|---|
| Relatórios de laboratório (Labs 01–11, em duplas) | 40 % | Notebook executado + análise, por commit no repositório da dupla — ver [Entrega das duplas no GitHub](#entrega-das-duplas-no-github-ao-longo-de-todo-o-semestre) |
| Listas de exercícios de análise e síntese | 20 % | Individuais, ao fim de cada unidade |
| Projeto final (sistema real) | 30 % | Relatório técnico + código |
| Seminário de apresentação do projeto | 10 % | Apresentação em grupo (15 min) |

Critérios priorizados (PPC): articulação entre o saber estudado e a solução de problemas reais; capacidade de análise crítica; iniciativa e criatividade; assiduidade e pontualidade; organização e clareza na expressão de conceitos.

### As listas de exercícios

São **quatro listas individuais**, uma por unidade, com questões no mesmo estilo dos
**Exercícios resolvidos** das apostilas. Cada lista consolida a unidade antes de a próxima
começar e prepara para o relatório e para o projeto.

| Lista | O quê estudar | Enunciado | Entregar até |
|:---:|---|---|---|
| 01 | Unidade I (Labs 01–03) | [`lista1_unidade1.md`](listas/lista1_unidade1.md) | semana 4 |
| 02 | Unidade II (Labs 04–05) | [`lista2_unidade2.md`](listas/lista2_unidade2.md) | semana 7 |
| 03 | Unidade III (Labs 06–07) | [`lista3_unidade3.md`](listas/lista3_unidade3.md) | semana 9 |
| 04 | Unidade IV (Labs 08–11) | [`lista4_unidade4.md`](listas/lista4_unidade4.md) | semana 12 |

## Bibliografia

**Básica (PPC):**

- OGATA, K. *Engenharia de Controle Moderno*. 5. ed. Rio de Janeiro: Pearson Brasil, 2006.
- DORF, R. C.; BISHOP, R. H. *Sistemas de Controle Modernos*. 8. ed. Rio de Janeiro: LTC, 2017.
- FELÍCIO, L. C. *Modelagem da Dinâmica de Sistemas e Estudo da Resposta*. São Carlos, 2008.

**Complementar (PPC):**

- CASTRUCCI, P. de L.; BITTAR, A.; SALES, R. M. *Controle Automático*. 2. ed. Rio de Janeiro: LTC, 2018.
- CAMPOS, M. M. de; TEIXEIRA, H. C. G. *Controles Típicos de Equipamentos e Processos Industriais*.

**Referência principal deste material:**

- ÅSTRÖM, K. J.; MURRAY, R. M. *Feedback Systems: An Introduction for Scientists and Engineers*. 2. ed. Princeton University Press. Disponível gratuitamente em <https://fbswiki.org>.
- MURRAY, R. M. *CDS 110 / ChE 105 — Analysis and Design of Feedback Control Systems*, Caltech, Spring 2024: <https://murray.cds.caltech.edu/CDS_110/ChE_105,_Spring_2024>.
- Documentação da `python-control` 0.10.x: <https://python-control.readthedocs.io/en/0.10.2/index.html> — repositório: <https://github.com/python-control/python-control>.
- ÅSTRÖM, K. J.; HÄGGLUND, T. *Advanced PID Control*. ISA, 2006 (referência para a Unidade IV).

**Apoio adicional recomendado aos estudantes:**

- NISE, N. S. *Engenharia de Sistemas de Controle*. LTC (excelente para modelagem — Unidade I — e lugar das raízes — Unidade II).
- DISTEFANO, J. J.; STUBBERUD, A. R.; WILLIAMS, I. J. *Sistemas de Retroação e Controle* (Coleção Schaum) — banco de exercícios resolvidos para todas as unidades.
- PENEDO, S. R. M. *Sistemas de Controle: Matemática Aplicada a Projetos*. Érica (reforço matemático em pt-BR: Laplace, diagramas de blocos).

> Cada apostila fecha com uma seção **"Leituras dirigidas"** que indica os capítulos e figuras
> específicos de cada livro para aquele tema — o mapa de leituras detalhado, mantido junto ao
> conteúdo. A tabela abaixo é a visão por laboratório desse mesmo mapa.

## Mapa de leituras por laboratório

Enquanto o [Roteiro de leitura](#roteiro-de-leitura-da-teoria-à-prática) liga cada **seção da
apostila** ao laboratório, a tabela abaixo dá a visão complementar: os **capítulos dos livros**
correspondentes a cada laboratório.

| Lab | FBS (Åström & Murray) | Ogata 5. ed. | Nise | Material CDS 110 |
|---|---|---|---|---|
| 00–01 | caps. 2–3 (modelagem, exemplos) | caps. 2–3 | caps. 1–2 | L1 (servomecanismo), L2 (pêndulo invertido) |
| 02 | cap. 6 (resposta) | cap. 4 | cap. 4 | L3 (sistemas LTI) |
| 03 | cap. 9 (resposta em frequência) | cap. 7 | cap. 10 | L7-1 (análise em pequenos sinais) |
| 04 | caps. 6–7 | cap. 5 | caps. 4, 8 | L3 |
| 05 | caps. 10 (Nyquist) e 12 (margens) | caps. 5, 7, 8 | caps. 6, 8, 10 | L7-2 (critério de Nyquist, Z = N + P) |
| 06–07 | caps. 5 (retratos de fase) e 11 (windup) | cap. 10 | — | L2 (fase plana), L9-2 (anti-windup) |
| 08–09 | caps. 11 (PID) e 12 (loop shaping) | cap. 10 (regras de sintonia) | cap. 9 | L9-1/L9-2 (PID e loop shaping) |
| 10–11 | cap. 11 (implementação, 2DOF) | cap. 10 | cap. 13 (digital) | L9-2 |
| Projeto | caps. 11–12 | cap. 10 | — | todos |
