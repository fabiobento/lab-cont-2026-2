# Lista de Exercícios 4 — Não Linearidades em Malhas de Controle

**Laboratório de Controle Automático — Engenharia Elétrica — Ifes Campus Guarapari**
**Módulo 4 (semana 15): não linearidades estáticas, windup/anti-windup, ciclos-limite, função descritiva e experimento do relé**

> **Instruções.** Resolva à mão sempre que possível e **valide por simulação** (python-control) quando indicado. Os Labs 15 e 16 contêm funções prontas que podem ser reutilizadas (`sim_p_sat`, `sim_dz`, `sim_termostato`, `sim_pi_windup`, `sim_rele`, `fd_numerica`, `fd_sat_teo`). Entregue os códigos utilizados junto com as respostas.
>
> **Teoria de referência:** `teoria_modulo4.md` — §4.1 (não linearidades estáticas), §4.2 (windup e anti-windup), §4.3 (ciclos-limite, função descritiva e experimento do relé).

---

## Questão 1 — Saturação: característica estática e ganho efetivo

Um amplificador de potência tem ganho $k = 5$ e satura em $\pm 10$ V (isto é, $u_{\max} = 10$ V).

a) Esboce a característica estática $u(e)$ e determine a **maior amplitude de entrada** para a qual o amplificador ainda se comporta linearmente.

b) Calcule a saída para $e = 1{,}5$ V e para $e = 3$ V.

c) Para uma entrada senoidal $e(t) = 4\sen(\omega t)$ (amplitude $A = 4$ V), calcule o **ganho descritivo** $N(A)$ do amplificador saturado, usando

$$N(A) = \frac{2k}{\pi}\left[\arcsen\left(\frac{s}{A}\right) + \frac{s}{A}\sqrt{1-\left(\frac{s}{A}\right)^2}\right], \qquad s = \frac{u_{\max}}{k}.$$

d) Interprete: quanto vale, em percentual, a redução de ganho efetivo em relação a $k$? O que isso sugere sobre o comportamento de uma malha cujo controlador "conta" com o ganho $k$?

---

## Questão 2 — Zona morta e erro de regime

Um atuador apresenta zona morta de largura $d = 0{,}3$ (não responde a comandos com $|u| < 0{,}3$) na entrada de uma planta de ganho unitário em regime, controlada em malha fechada por um proporcional $C(s) = k_p$, com referência constante $r = 1{,}5$.

a) Mostre que, em regime permanente, a saída fica **confinada no intervalo**

$$\frac{k_p r - d}{1 + k_p} \;\le\; y_{ss} \;\le\; \frac{k_p r + d}{1 + k_p}$$

e que o erro de regime satisfaz $|e_{ss}| \le \dfrac{r + d}{1 + k_p}$ (adote a solução de fronteira $y_{ss} = \dfrac{k_p r - d}{1+k_p}$).

b) Calcule $y_{ss}$ e o erro para $k_p = 6$.

c) Determine o **menor $k_p$ inteiro** que garante $|e_{ss}| \le 0{,}05$. Comente: por que nenhum ganho finito zera o erro? Que elemento de controlador resolveria o problema, e qual novo risco ele traria (§4.2)?

---

## Questão 3 — Termostato: período exato da oscilação

Um forno é modelado por $G(s) = \dfrac{1}{5s+1}$ e controlado por um relé com histerese (termostato) de saída $\pm 1$ e banda de histerese $h = 0{,}2$ (o relé comuta quando $y$ atinge $\pm h$ em torno do setpoint, considerado nulo).

a) Mostre que o período exato da oscilação em regime é

$$T = 2\tau \ln\!\left(\frac{1+h}{1-h}\right), \qquad \tau = 5\ \text{s},$$

e calcule $T$.

b) Recalcule para $h = 0{,}5$. A temperatura oscila mais ou menos? E a frequência de comutação do relé? Discuta o compromisso prático (conforto térmico × desgaste do contator).

c) **Simulação:** valide os dois períodos com a função `sim_termostato` do Lab 15 (adapte $\tau$ para 5 s).

---

## Questão 4 — Windup: a aritmética do transbordamento do integrador

Considere $G(s) = \dfrac{1}{5s+1}$ com PI $k_p = 1$, $k_i = 0{,}5$ ($T_i = k_p/k_i = 2$ s), saturação do atuador em $\pm 1{,}2$ e degrau de referência $r = 1$.

a) Calcule o valor de regime do sinal de controle, $u_{ss}$, necessário para $y_{ss} = r$. A saturação é atingida durante o transitório?

b) Enquanto o atuador permanece saturado em $u = 1{,}2$, a saída evolui como $y(t) = 1{,}2\left(1 - e^{-t/5}\right)$. Determine o instante $t^*$ em que $y$ alcança $r$.

c) Durante a saturação, o integrador acumula $\dot{x}_i = e = r - y$. Calcule $x_i(t^*)$ e compare com o valor necessário em regime, $x_{i,ss} = u_{ss}/k_i$. Qual o **excesso** acumulado (em percentual)?

d) Explique, com base no item (c), por que a saída ultrapassa a referência depois de $t^*$ (windup), e por que o sobressinal só desaparece depois que o integrador "devolve" o excesso.

---

## Questão 5 — Anti-windup: conceitos e implementação

a) Escreva a **regra de clamping** (condicional) para o integrador de um PI digital, indicando claramente em que condição a integração é congelada.

b) Na estratégia de **back-calculation**, o integrador evolui como $\dot{x}_i = e + \dfrac{1}{T_t}(u - u_{PI})$. Explique o papel do termo de realimentação e como escolher $T_t$ para um PI e para um PID.

c) Por que o limitador deve ser implementado **dentro do software do controlador** (e não apenas existir fisicamente no atuador)? O que acontece com qualquer esquema anti-windup se o controlador "não souber" que o atuador saturou?

---

## Questão 6 — Previsão de ciclo-limite por balanço harmônico

Um sistema $G(s) = \dfrac{4}{s(s+1)(s+2)}$ é realimentado por um relé ideal de amplitude $d = 1$ (sem histerese).

a) Determine a frequência $\omega_c$ para a qual $\angle G(j\omega_c) = -180°$ e calcule $|G(j\omega_c)|$.

b) Com a função descritiva do relé, $N(A) = \dfrac{4d}{\pi A}$, determine a **amplitude $A$ e a frequência** do ciclo-limite previsto, resolvendo $1 + N(A)\,G(j\omega) = 0$.

c) Mostre que o ganho crítico previsto pelo experimento do relé, $K_u = \dfrac{4d}{\pi A}$, **coincide exatamente** com o ganho crítico obtido pelo critério de Routh-Hurwitz para a malha com controlador proporcional $K$ no lugar do relé. Explique por que essa coincidência não é acidental.

d) **Simulação:** valide com `sim_rele` do Lab 16 (adapte a planta) e compare amplitude e período medidos com a previsão.

---

## Questão 7 — Sintonia Ziegler-Nichols a partir do relé

Usando os resultados da Questão 6 ($K_u$ e $P_u = 2\pi/\omega_c$), determine os parâmetros das sintonias Ziegler-Nichols de ciclo-limite:

a) Controlador **P**: $k_p$.

b) Controlador **PI**: $k_p$ e $T_i$.

c) Controlador **PID**: $k_p$, $T_i$ e $T_d$.

d) A sintonia PID de Ziegler-Nichols costuma produzir sobressinal elevado. Cite a estratégia de refinamento usada no Lab 16 e o resultado obtido lá.

---

## Questão 8 — Saturação não sustenta ciclo-limite em malha linear estável

Uma malha contém uma saturação ($k = 1$, nível $s = 1$) em cascata com $G(s) = \dfrac{K}{s(s+1)(s+2)}$ e realimentação unitária.

a) Esboce qualitativamente o lugar geométrico de $-1/N(A)$ para a saturação ($N(A)$ real, decrescendo de $1$ a $0$ quando $A$ cresce de $s$ a $\infty$). Em que intervalo do eixo real ele se encontra?

b) Para $K = 4$: calcule o ponto de cruzamento do Nyquist de $G(j\omega)$ com o eixo real e conclua que **não há ciclo-limite** possível.

c) Para $K = 12$: determine a condição de interseção, o valor de $N(A)$ requerido e resolva numericamente para a amplitude $A$ do ciclo-limite previsto.

d) Interprete fisicamente: por que a saturação só produz oscilação sustentada quando o ganho da malha linear já seria capaz de desestabilizar o sistema?

---

## Questão bônus — Relé com histerese: cuidado com interseções espúrias

Um relé com histerese ($d = 1$, $h = 0{,}2$) controla $G(s) = \dfrac{1}{(s+1)^2}$.

a) Mostre que o lugar geométrico de $-1/N(A)$ é uma **semirreta horizontal** em $\mathrm{Im} = -\dfrac{\pi h}{4d}$, e calcule esse valor.

b) Mostre que $\mathrm{Im}\,G(j\omega) = -\dfrac{2\omega}{(1+\omega^2)^2}$ atinge esse valor em **duas** frequências ($\omega \approx 0{,}08$ e $\omega \approx 2{,}02$ rad/s), mas que apenas **uma** delas satisfaz o balanço harmônico completo (módulo **e** fase). Identifique o erro de raciocinar apenas pela parte imaginária.

c) Determine a amplitude e o período do ciclo-limite previsto pela função descritiva.

d) **Simulação:** confirme com a simulação por eventos (adaptar `sim_termostato`/Lab 15 para a planta de 2ª ordem). Qual cruzamento o sistema "escolhe"?

---

**Bons estudos!** Na dúvida, rode a simulação — neste módulo, ela é parte da teoria.
