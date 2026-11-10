# Projeto Final — Servo de Posição com Motor CC

**Laboratório de Controle Automático — Engenharia Elétrica — Ifes Campus Guarapari**
**5 aulas de 1h40:** 11/11 · 18/11 · 25/11 · 03/12 · 10/12 · **Avaliação por bancada**

---

## 1. O que vamos fazer

Projetar, implementar e validar um **servo de posição**: o Arduino mede o ângulo da roda do motor
e comanda o PWM para que ela siga uma referência em degraus — 0° → 90° → −90° → 0°, um degrau a
cada 5 s —, atendendo às especificações da Seção 3.

O projeto inteiro é feito **em sala, em 5 aulas**. Cada aula tem um **roteiro em notebook**
(Seção 4) que conduz a bancada passo a passo — ensaio, conta, simulação, discussão — e traz, no
ponto em que é usada, a teoria necessária (caixas 📘). **Não é preciso estudar fora do horário de
aula.** O material teórico dos módulos continua no repositório para quem quiser se aprofundar.

O projeto **inclui os Trabalhos 1 e 2**: o Trabalho 1 (identificação) termina na Aula 2 e o
Trabalho 2 (PID de posição) na Aula 4 (Seção 6).

## 2. A bancada

O kit do laboratório: Arduino Uno com shield e display OLED, ponte H L298N, motor JGA25-370 de
6 V / 210 rpm com redução, encoder Hall e uma roda no eixo.

| Ligação | Pino do Arduino |
|---|---|
| L298N IN1 / IN2 (PWM; ENA com jumper) | D9 / D10 |
| encoder C1 / C2 | D2 (interrupção) / D4 |
| OLED SSD1306 (I²C) | A4 / A5 |

**Software** (tudo no repositório):

| Arquivo | O que é |
|---|---|
| `firmware/pid_motor/pid_motor.ino` | **o único firmware do projeto**: gravado **uma vez**, na Aula 1. Cada ensaio é configurado pelo notebook |
| `projeto_final/ferramentas_projeto.py` | `coletar()` (ensaio na bancada), `simular()` (o mesmo ensaio no gêmeo digital), métricas oficiais, gráficos |
| `projeto_final/aula1_…ipynb` a `aula5_…ipynb` | os **roteiros** das aulas |

**Para rodar:** Python com `pip install "control==0.10.2" numpy scipy matplotlib jupyter pyserial`,
e a Arduino IDE com a biblioteca *Adafruit SSD1306*. Os notebooks ficam em `projeto_final/` e
salvam os dados em `projeto_final/dados/`.

## 3. Especificações

Para o **degrau de 90°** do perfil (0° → 90°):

| # | Especificação | Valor |
|---|---|---|
| 1 | erro de regime | $\|e_{ss}\| < 2°$ |
| 2 | sobressinal | $`M_p \le 15\%`$ |
| 3 | tempo de acomodação (critério de ±5 %) | $t_s \le 2{,}5$ s |
| 4 | sem *windup* visível | com o PWM limitado a ±80, o sobressinal cresce no máximo **5 pontos percentuais** em relação ao ensaio nominal, com o anti-windup ligado |

**Como se mede** (função `metricas_ensaio()` — a mesma para todas as bancadas):

- $M_p$ — quanto o ângulo passa da referência final, em % da amplitude do degrau;
- $t_s$ — último instante em que o ângulo está fora de ±5 % da amplitude (±4,5°), contado a
  partir do degrau;
- $e_{ss}$ — média de (referência − ângulo) no último 1 s do trecho;
- cada ensaio nominal é feito **3 vezes** e vale o **pior** dos três.

## 4. Cronograma — os roteiros

| Aula | Data | Roteiro | O que a bancada faz | Checkpoint |
|---|---|---|---|---|
| 1 | 11/11 | `aula1_bancada_e_modelo_de_velocidade.ipynb` | grava o firmware, testa o sentido, calibra o encoder, faz o ensaio PRBS e ajusta o modelo de velocidade (FOPDT) | ✅ 1 |
| 2 | 18/11 | `aula2_modelo_de_posicao_e_primeiro_projeto.ipynb` | mede o modelo de posição, a zona morta e o atrito estático; monta o gêmeo digital; faz o 1º projeto pelo lugar das raízes e o testa na bancada | ✅ 2 — **fim do Trabalho 1** |
| 3 | 25/11 | `aula3_pid_rele_e_compensacao.ipynb` | projeta o PID pelo lugar das raízes, confere com o relé (Ziegler-Nichols), escolhe a compensação de zona morta e faz o 1º ensaio do controlador final | ✅ 3 |
| 4 | 03/12 | `aula4_validacao_e_antiwindup.ipynb` | 3 ensaios nominais (especificações 1–3), ensaios com e sem anti-windup (especificação 4), medido × simulado | ✅ 4 — **fim do Trabalho 2** |
| 5 | 10/12 | `aula5_fechamento_e_apresentacao.ipynb` | painel de resultados, tabela das não linearidades e **apresentação** | — |

**Em cada roteiro:** ⏱️ tempo sugerido de cada parte · 📘 teoria para ler antes de fazer · 🔧
passo na bancada · 💻 passo no notebook · ✏️ linha de código para completar · ❓ pergunta para a
bancada responder no próprio notebook · ✅ checkpoint — chame o professor.

**Os resultados passam de uma aula para a outra** no arquivo `dados/parametros_bancada.json`
(funções `salvar_parametros()` / `carregar_parametros()`). **Não apaguem a pasta `dados/`** e usem
sempre o mesmo computador ou levem a pasta junto.

## 5. Organização da bancada

- A bancada trabalha junta e é avaliada junta.
- **Papéis, trocados a cada aula:** 🔧 **operador(a)** (hardware e firmware), 💻
  **programador(a)** (notebook), ✍️ **relator(a)** (respostas ❓ e conferência dos números). Com
  mais de 3 pessoas, os papéis são divididos em dupla; com 2, o relator acumula com o programador.
- Na apresentação (Aula 5) **todos falam**, e qualquer integrante pode ser perguntado sobre
  qualquer parte.

## 6. Avaliação (por bancada)

| Nota | O que é avaliado | Quando |
|---|---|---|
| **Trabalho 1** | roteiros das Aulas 1 e 2: firmware e teste de sentido, calibração, FOPDT com e sem desvio, modelo de posição, zona morta e atrito, gêmeo validado, iteração 1 e a explicação da falha | Checkpoint 2 (18/11) |
| **Trabalho 2** | roteiros das Aulas 3 e 4: PID pelo lugar das raízes, relé e Ziegler-Nichols, compensação e robustez, especificações 1–4 na bancada, medido × simulado | Checkpoint 4 (03/12) |
| **Projeto final** | os 5 roteiros completos + apresentação e arguição | Aula 5 (10/12) |

**Critérios em cada nota:**

| Critério | Peso | Excelente | Suficiente | Insuficiente |
|---|---|---|---|---|
| Ensaios e dados | 25 % | todos os ensaios do roteiro feitos, CSVs na pasta `dados/`, gráficos coerentes | falta algum ensaio secundário | faltam ensaios principais |
| Contas e código | 25 % | linhas ✏️ corretas e resultados conferidos | algum erro corrigido no checkpoint | resultados sem sentido físico não percebidos |
| Respostas ❓ | 30 % | explicam o "porquê" com os números da própria bancada | corretas, mas genéricas | ausentes ou erradas |
| Especificações | 20 % | atendidas (ou a falha diagnosticada com os dados) | atendidas parcialmente | não atendidas e sem diagnóstico |

Na nota do **projeto final**, a apresentação e a arguição valem 30 % e os roteiros, 70 %.

**Entrega:** ao final da Aula 5, a pasta `projeto_final/` da bancada com os 5 notebooks **salvos
com as saídas** e a pasta `dados/` completa, no local indicado pelo professor.

## 7. Problemas frequentes na bancada

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `coletar()` diz que o Arduino não respondeu | firmware antigo gravado; porta errada; Monitor Serial da IDE aberto | grave o `pid_motor.ino`; confira `PORTA`; feche o Monitor Serial |
| erro de compilação na `Adafruit_SSD1306` | biblioteca não instalada | instale-a pelo Gerenciador de Bibliotecas, ou troque `#define USAR_OLED 1` por `0` |
| no teste de sentido, a posição diminui | sentido do motor × sentido do encoder | desligue a fonte e inverta os fios do motor em OUT1/OUT2 (não troque C1/C2) |
| em malha fechada, o motor dispara girando sem parar | realimentação positiva (o teste de sentido não foi feito ou foi desfeito) | desligue e refaça o teste de sentido |
| o ângulo de 90° vira ≈ 45° ou 180° | `CPG` errado | refaça a calibração da Aula 1 |
| erro de regime de vários graus | atrito/zona morta | é o assunto das Aulas 2 e 3 |
| oscilação lenta em torno da referência | integrador forte demais + atrito estático | reduza $k_i$; confira `ZM` e `EM` |
| PWM "trepidando", motor zumbindo parado | compensação de zona morta sem a faixa `EM` | Aula 3, Parte 3 |
| `KeyError` ao abrir um roteiro | falta um resultado de aula anterior em `dados/parametros_bancada.json` | rode o roteiro anterior (ou chame o professor) |

## 8. Para se aprofundar (opcional)

| Assunto | Teoria | Laboratório |
|---|---|---|
| modelos de 1ª ordem, identificação | M1 §1.2; `trabalhos/trabalho1_…md` | Lab 02 |
| atraso de transporte, Padé | M2 §2.5.4–2.5.5 | Lab 09 |
| plano-s, lugar das raízes, PD/PI/PID | M2 §2.1–2.5 | Labs 05–09 |
| margens de ganho e de fase | M3 §3.1.8–3.1.9 | — |
| saturação, zona morta, atrito | M4 §4.1 | Lab 15 |
| windup e anti-windup | M4 §4.2 | Lab 16, Parte 1 |
| relé e Ziegler-Nichols | M4 §4.3.7–4.3.8 | Lab 16, Parte 4 |
