# Lista 4 — Unidade IV: Projeto, sintonia e implementação de PID

**Entrega:** fim da semana 12 (antes do projeto final) · Consulta liberada; trabalho individual. 🖥️ = verificar com `python-control`.

> 🖼️ Figuras de apoio para esta lista (consultar antes de resolver):
>
> - Ogata, **Tabela 8.1** — regra de sintonia de Ziegler–Nichols pelo 1º método (curva de reação: L e T). Cap. 8, §8.2, **p. 524** (p. 535 do PDF).
> - Ogata, **Tabela 8.2** — regra de sintonia de Ziegler–Nichols pelo 2º método ($K_{cr}$ e $P_{cr}$). Cap. 8, §8.2, **p. 525** (p. 536 do PDF).
> - Ogata, **Figura 8.3** — curva de resposta em forma de S, com a tangente no ponto de inflexão definindo o atraso L e a constante T. Cap. 8, §8.2, **p. 523** (p. 534 do PDF).
> - Ogata, **Figura 8.28** — sistema com controle I-PD (proporcional e derivada na medição — caso $b = 0$). Cap. 8, **p. 544** (p. 555 do PDF).
> - Nise, **Figura 13.4** — conversão A/D: sinal analógico, amostrador + segurador (ZOH) e amostras digitais. Cap. 13, p. 1039 do arquivo PDF (a cópia digital não exibe o nº impresso).

---

**Q1.** Converta o PID paralelo $C(s) = 6 + \dfrac{3}{s} + 1{,}5s$ para a forma ISA
$C(s) = K_p\!\left(1 + \dfrac{1}{T_is} + T_ds\right)$ e escreva a versão com derivada filtrada ($N = 10$).

**Q2.** Com o ponto crítico obtido na Lista 2 Q3 ($K_u = 60$, $T_u = 1{,}89$ s), calcule as sintonias de Ziegler–Nichols de malha fechada para P, PI e PID. 🖥️ Simule o degrau das três malhas (planta $\frac{1}{(s+1)(s+2)(s+3)}$) e compare $M_p$ e $t_s$.

**Q3.** Identificou-se em bancada o modelo FOPDT $G(s) = \dfrac{2\,e^{-2s}}{8s+1}$.
(a) Calcule as sintonias PI e PID por ZN de malha aberta.
(b) Calcule a sintonia PI por CHR 0 % (servo).
(c) Qual você recomendaria para um forno que não tolera ultrapassagem? Justifique.

**Q4.** Para a planta da Q3, sintonize um PI pelo método lambda com $\lambda = \tau$ e com $\lambda = \tau/2$. O que cada escolha prioriza? Estime qualitativamente o efeito sobre PM.

**Q5.** Um PID tem $K_p = 2$, $T_d = 1$ e derivada filtrada com constante $N$.
(a) Mostre que o ganho de alta frequência do ramo derivativo tende a $K_pN$.
(b) O sensor tem ruído de amplitude 0,01. Estime a contribuição do ruído no atuador para $N = 10$ e $N = 100$.
(c) Por que a derivada deve atuar sobre a **medição** e não sobre o erro? Que evento a torna crítica?

**Q6.** Implementação digital:
(a) Discretize $C(s) = \dfrac{s+1}{s}$ (PI com $K_p = 1$, $T_i = 1$) por Tustin com $h = 0{,}5$ s, obtendo $C(z)$.
(b) Para a malha da Q2 ($T_u = 1{,}89$ s), qual o maior período de amostragem recomendado?
(c) Escreva as equações a diferenças do PID de produção do curso (P ponderado, I com back-calculation, D filtrada sobre a medição).

**Q7.** No PI 2DOF com ponderação de referência $b$ ($u = K_p(br - y) + \frac{K_p}{T_i}\int e\,dt$):
(a) Mostre que os polos de malha fechada não dependem de $b$.
(b) Mostre onde $b$ aparece (zeros de $T_{ry}$) para $K_p = 2$, $T_i = 2$.
(c) Por que a resposta à perturbação de carga é idêntica para qualquer $b$?

**Q8.** *(Mini-projeto integrador)* No experimento do relé em uma planta de bancada mediu-se: amplitude do relé $d = 0{,}8$, amplitude da oscilação $a = 0{,}05$, período $T_u = 3$ s.
(a) Estime $K_u$.
(b) Sintonize um PI por ZN de malha fechada.
(c) Liste, na ordem correta, as verificações que você faria antes de embarcar esse PI no microcontrolador (cite os critérios numéricos do curso).
