# Trabalho 3 — Controle PID de Posição Angular em Motor CC

**Laboratório de Controle Automático — Engenharia Elétrica — Ifes Campus Guarapari**
**Lançamento:** semana 14 · **Apresentações:** semana 15 · **Valor:** 28 pontos · **Grupos:** até 2 integrantes

---

## 1. Objetivos

1. Obter o modelo de **velocidade** do motor CC (pode ser o mesmo do Trabalho 1);
2. Obter o modelo de **posição** a partir do de velocidade, com ajuste do ganho de conversão $k'$;
3. **Sintonizar um PID** para a planta de posição e **justificar** a escolha da sintonia;
4. **Implementar e testar** o controlador na planta real (firmware `firmware/pid_motor/`), analisando o resultado.

## 2. Bancada e software

Mesma bancada do Trabalho 1 (Arduino + ponte H + motor CC + encoder magnético), agora com o firmware `pid_motor/`, que implementa embarcado:

- **PID em forma ISA com 2 graus de liberdade** (derivada e, opcionalmente, proporcional sobre a **medição** — evita o "chute derivativo" no degrau de referência);
- **derivada filtrada** ($N$ entre 5 e 20);
- **anti-windup por clamping** (congela o integrador quando o PWM satura e o erro tem o mesmo sinal — §4.2 da teoria do Módulo 4);
- telemetria serial (`t, referencia, angulo, pwm`) para análise em Python via `firmware/telemetry.py`.

> **Consulte:** teoria `modulo2_plano_s/teoria_modulo2.md` §2.5 (PID e suas realizações), `modulo3_frequencia/teoria_modulo3.md` §3.5 (PD/PI/PID na frequência) e `modulo4_nao_linearidades/teoria_modulo4.md` §4.2 (windup e anti-windup — **obrigatório** para o Passo 4).

## 3. Roteiro

**Passo 1 — Modelo de velocidade.** Se já tem o modelo do Trabalho 1, reutilize-o (pode-se desprezar o atraso para o projeto do controlador, mas mencione isso na justificativa). Caso contrário, repita o procedimento do Trabalho 1 (PRBS + ajuste FOPDT) para obter

$$G_v(s) = \frac{K}{\tau s + 1} \qquad [\text{velocidade}/\text{PWM}].$$

**Passo 2 — Modelo de posição.** A posição é a integral da velocidade, com um ganho de conversão $k'$ (unidades do encoder → graus ou radianos):

$$G_p(s) = \frac{K\,k'}{s(\tau s + 1)}.$$

Para medir $k'$: aplique um **PWM fixo de amplitude $A$** e grave o gráfico **ângulo × tempo**. Em regime, a velocidade é constante e o ângulo cresce linearmente com coeficiente angular $a = \dfrac{y_2 - y_1}{x_2 - x_1}$ (dois pontos da reta). Igualando $K\,k'\,A = a$:

$$k' = \frac{a}{K\,A}.$$

**Passo 3 — Sintonia do PID.** Com $G_p(s)$ identificada, sintonize o PID usando **os métodos do curso** — não há especificações impostas, mas o "bom" resultado deve ser **justificado**. Rotas aceitas (escolha uma principal e cite as demais):

- **Plano-s (Módulo 2):** projeto PD/PI/PID pelo LGR (posicionamento de polos, ângulo de contribuição);
- **Frequência (Módulo 3):** margem de fase alvo (sugestão: PM ≥ 50°), projeto de PD pelas fórmulas diretas e acréscimo de PI para erro nulo;
- **Relé/ZN (Módulo 4):** experimento do relé na planta real ou no modelo → $K_u = 4d/(\pi a)$, $P_u$ → tabela ZN → **refinamento** (reduzir $k_p$ e $k_i$, reforçar $k_d$), como no Lab 16.

Valide em simulação **antes** de ir para a bancada (`control.step_response` da malha fechada; inclua a saturação do PWM no modelo se usar `solve_ivp`, como no Lab 16).

**Passo 4 — Teste na planta real.** Programe os ganhos no firmware `pid_motor/`, aplique degraus de referência de posição (ex.: 0° → 90° → −90° → 0°) e colete a telemetria. Analise:

- sobressinal, tempo de estabelecimento e erro de regime **medidos × simulados** — explique as diferenças;
- **sinal de controle (PWM)**: saturou? Se sim, o anti-windup atuou corretamente? Compare com uma execução **sem anti-windup** (desabilite no firmware) e discuta o windup observado (§4.2);
- efeito do filtro da derivada e do ruído do encoder no PWM.

## 4. Entrega e avaliação

- **Apresentação presencial** (agendar com o professor), máximo **10 minutos**, com **todos os integrantes** participando;
- Entregar: CSVs da identificação e dos ensaios em malha fechada, notebook/script Python (modelo, sintonia, simulação × medição) e o firmware utilizado;
- Serão avaliados: correção dos modelos de velocidade e posição, **justificativa da sintonia** (método, números, margens), qualidade do ensaio real e a análise crítica (windup, saturação, ruído, diferenças modelo × planta).

**Bom trabalho!**
