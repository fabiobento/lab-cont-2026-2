# Laboratório de Controle Automático

**Engenharia Elétrica — 7º período — Ifes Campus Guarapari**
Prof. Fábio Bento · 30 h (15 semanas × 2 h) · 2026/2

Repositório completo da disciplina: teoria, laboratórios em Python (python-control), listas com gabaritos detalhados, exercícios resolvidos, notas de aula, slides, trabalhos, projeto final e firmware para a bancada (Arduino + ponte H + motor CC + encoder magnético).

> **Ferramenta oficial do curso:** [python-control](https://python-control.readthedocs.io/) **0.10.2** (substitui o MATLAB das edições anteriores). Nenhum material exige MATLAB.

---

## Estrutura do repositório

```
lab-controle-automatico/
├── README.md                          ← este arquivo
│
firmware/
├── pid_motor
│   └── pid_motor.ino
├── prbs_aquisicao
│   └── prbs_aquisicao.ino
└── telemetry.py
│
├── modulo1_introducao/                ← semanas 1–5 · modelagem, Laplace, estabilidade, 2ª ordem, P
│   ├── teoria_modulo1.md
│   ├── lista1_modulo1.md
│   ├── labs/      lab01…lab04 (.ipynb)
│   └── slides/          (aulas 01–04)
│
├── modulo2_plano_s/                   ← semanas 6–9 · plano-s, LGR, avanço, atraso/PI, PID, Padé
│   ├── teoria_modulo2.md
│   ├── lista2_modulo2.md
│   └── labs/      lab05…lab09 (.ipynb)
│
├── modulo3_frequencia/                ← semanas 10–14 · Bode, Nichols-Black, Nyquist, projeto
│   ├── teoria_modulo3.md
│   ├── lista3_modulo3.md
│   └── labs/      lab10…lab14 (.ipynb)
│
├── modulo4_nao_linearidades/          ← semana 15 · MÓDULO AUTÔNOMO (Unidade III do PPC)
│   ├── teoria_modulo4.md              ← saturação, zona morta, histerese; windup/anti-windup;
│   │                                    ciclos-limite, função descritiva, experimento do relé
│   ├── lista4_modulo4.md
│   └── labs/      lab15, lab16 (.ipynb)
│
├── trabalhos/
│   ├── trabalho1_identificacao_prbs_fopdt.md    (semanas 5–7 · 15 pts)
│   └── trabalho3_pid_posicao_motor_cc.md        (semanas 14–15 · 28 pts)
│
├── projeto_final/
│   └── projeto_final_motor_cc.md      ← integra T1+T3; especificações, rubrica, cronograma
│
└── imagens/                           ← figuras geradas (m1_*, m2_*, m3_*, m4_*), usadas pela teoria
```

## Semana a semana (resumo)

| Sem. | Módulo | Conteúdo | Lab | Marcos |
|---|---|---|---|---|
| 1–5 | **M01** | Sistemas e modelos; Laplace e FT; estabilidade e erro; resposta de 2ª ordem; projeto P | 01–04 | **Trabalho 1** lançado (sem. 5) |
| 6–9 | **M02** | Plano-s e aproximações; LGR; avanço de fase; atraso/PI; avanço-atraso, PID e Padé | 05–09 | **Trabalho 1 entregue** (sem. 7) |
| 10–14 | **M03** | Resposta em frequência e Bode; Nichols-Black; Nyquist e atraso; projeto avanço/atraso; PD/PI/PID na frequência | 10–14 | **Trabalho 3 / Projeto final** lançados (sem. 14) |
| 15 | **M04** (autônomo) | Não linearidades estáticas; windup e anti-windup; ciclos-limite; função descritiva; experimento do relé | 15–16 | **Lista 4**; **apresentações do projeto final** |

## Como executar os laboratórios

```bash
pip install "control==0.10.2" numpy scipy matplotlib jupyter
jupyter notebook modulo1_introducao/labs/lab01_sistemas_e_modelos.ipynb
```

Cada notebook é autocontido: a primeira célula instala/verifica as dependências e define as funções utilitárias (métricas de resposta ao degrau etc.). Todos os labs foram executados e validados com 0 erros.

## Bancada (Trabalhos 1 e 3 / Projeto final)

1. Grave `firmware/prbs_aquisicao/prbs_aquisicao.ino` no Arduino (identificação) ou `firmware/pid_motor/pid_motor.ino` (malha fechada);
2. Ajuste pinos e constantes no topo de cada sketch (`Tb_ms`, ganhos PID, `CONTAS_POR_GRAU`…);
3. Colete os dados: `python firmware/telemetry.py --porta /dev/ttyUSB0 --saida dados.csv`;
4. Analise o CSV seguindo o roteiro do trabalho correspondente.

## Convenções

- **Vírgula decimal** em textos, tabelas e figuras (pt-BR);
- Figuras referenciadas por URL absoluta do GitHub (`github.com/fabiobento/lab-cont-2026-2`);
- Diagramas de blocos em Mermaid dentro dos próprios `.md`;

## Licença / uso

Material didático da disciplina. Uso livre para fins educacionais, citando a fonte.
