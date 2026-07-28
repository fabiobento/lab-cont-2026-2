# Lista 1 — Unidade I: Modelagem e análise de sistemas físicos

**Entrega:** fim da semana 4 · **Peso:** compõe os 20 % de listas · Consulta liberada (livros e notebooks); trabalho individual.

Instruções: resolva analiticamente e, quando indicado com 🖥️, **verifique com `python-control`** anexando o código e o gráfico. Use notação SI.

> 🖼️ Figuras de apoio para esta lista (consultar antes de resolver):
>
> - Ogata, **Figura 5.2** — curva de resposta exponencial ao degrau, com a tangente inicial e as marcas em T, 2T, 3T, 4T. Cap. 5, §5.2, **p. 148** (p. 159 do PDF).
> - Ogata, **Figura 5.8** — especificações de resposta transitória ($t_d, t_r, t_p, M_p, t_s$) sobre a curva ao degrau. Cap. 5, seção 'Especificações de resposta transitória', **p. 154** (p. 165 do PDF).
> - Nise, **Figura 2.15** — sistema massa–mola–amortecedor e sua FT (exemplo 'Uma Equação de Movimento'). Cap. 2, §2.5, p. 107–108 do arquivo PDF (a cópia digital não exibe o nº impresso).
> - Nise, **Figura 2.35** — servomotor CC controlado pela armadura: esquema e diagrama para a dedução da FT. Cap. 2, seção de sistemas eletromecânicos, p. 127–128 do arquivo PDF (a cópia digital não exibe o nº impresso).
> - Penedo, **Figura 4.4** — localização dos polos complexos conjugados de 2ª ordem no plano complexo. Cap. 4, p. 42 do arquivo PDF.

---

**Q1.** Um sistema massa–mola–amortecedor tem $m = 2$ kg, $b = 8$ N·s/m e $k = 50$ N/m, com força $f(t)$ como entrada e posição $x(t)$ como saída.
(a) Escreva a EDO e obtenha $G(s) = X(s)/F(s)$.
(b) Calcule $\omega_n$, $\zeta$ e o ganho estático. Classifique o amortecimento.
(c) 🖥️ Simule o degrau unitário e confira o valor final pelo teorema do valor final.

**Q2.** Para o circuito RC série (saída = tensão no capacitor) com $R = 10\ \text{k}\Omega$ e $C = 100\ \mu\text{F}$: obtenha $G(s)$, a constante de tempo, e esboce à mão a resposta ao degrau de 5 V marcando $\tau$ e o tempo de acomodação (critério de 2 %).

**Q3.** Um tanque tem área $A = 2\ \text{m}^2$, vazão de entrada $q_i$ (entrada) e vazão de saída linearizada $q_o = h/R_v$, com $R_v = 50\ \text{s/m}^2$.
(a) Deduza a EDO do nível $h(t)$ e $G(s) = H(s)/Q_i(s)$.
(b) Identifique $K$ e $\tau$ e interprete fisicamente cada um.

**Q4.** Para o motor CC do Lab 01 ($R_a = 2\ \Omega$, $L_a \approx 0$, $K_t = K_e = 0{,}1$, $J = 0{,}02$, $b_m = 0{,}005$): deduza o modelo de 1ª ordem $\omega(s)/V_a(s) = K_m/(\tau_m s + 1)$ e calcule $K_m$ e $\tau_m$. Compare com a FT usada no curso.

**Q5.** Usando transformada de Laplace (sem simulação), obtenha $y(t)$ para o degrau unitário aplicado a $G(s) = \dfrac{5}{2s+1}$ e calcule $y(2)$ e $y(4)$ (isto é, em $t = \tau$ e $t = 2\tau$).

**Q6.** Escreva o sistema da Q1 em espaço de estados com $x_1 = x$ e $x_2 = \dot{x}$ (matrizes $A$, $B$, $C$, $D$) e mostre, calculando $C(sI - A)^{-1}B$, que a FT resultante coincide com a da Q1.

**Q7.** Em um ensaio senoidal de uma planta de 1ª ordem desconhecida mediu-se: ganho estático $M(0) = 2$; em $\omega = 3$ rad/s, ganho $M = 0{,}632$ e fase $\phi = -71{,}6°$. Determine $K$ e $\tau$ e escreva $G(s)$. 🖥️ Confirme com `ct.frequency_response`.

**Q8.** O Bode experimental de uma planta de 2ª ordem subamortecida apresenta pico de ressonância $M_r = 2{,}55$ (relativo ao ganho estático) em $\omega_r = 9{,}59$ rad/s. Determine $\zeta$ e $\omega_n$ e escreva a FT normalizada. 🖥️ Verifique o pico no Bode.
