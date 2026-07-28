# Lista 3 — Unidade III: Não-linearidades em malhas de controle

**Entrega:** fim da semana 9 · Consulta liberada; trabalho individual. 🖥️ = verificar com `python-control` (`ct.nlsys`/`ct.interconnect`).

> 🖼️ Figuras de apoio para esta lista (consultar antes de resolver):
>
> - Ogata, **Figura 8.4** — malha fechada apenas com ganho proporcional para obter $K_{cr}$ (2º método de ZN). Cap. 8, §8.2, **p. 524** (p. 535 do PDF).
> - Ogata, **Figura 8.5** — oscilação sustentada com período $P_{cr}$. Cap. 8, §8.2, **p. 524** (p. 535 do PDF).
> - Transparências CDS 110 **L9-1** (29/05/2024), **slide 15** — 'Windup and Anti-Windup Compensation': diagrama de blocos do back-calculation com as respostas com/sem anti-windup.

---

**Q1.** A planta térmica $G(s) = \dfrac{2}{10s+1}$ tem atuador saturado em $0 \le u \le 1{,}5$.
(a) Qual a maior referência de regime alcançável?
(b) Aplica-se degrau de referência $r = 4$ com controlador PI bem sintonizado. Descreva o que acontece com a saída, com o atuador e com o integrador ao longo do tempo.
(c) 🖥️ Simule e mostre as três curvas ($y$, $u$, parcela integral).

**Q2.** Um atuador tem zona morta $\delta = 0{,}2$ e a malha usa controlador P com $K_p = 4$.
(a) Mostre que existe uma **banda de erro residual** e calcule sua largura.
(b) Por que a ação integral elimina o erro médio mas pode gerar oscilação lenta (ciclo-limite) em torno da referência? Explique o mecanismo.

**Q3.** Explique, com um diagrama entrada×saída, a diferença entre zona morta, saturação e histerese, e dê um exemplo físico de cada uma presente nas plantas do projeto final (kit motor CC — velocidade e posição — e sistema térmico).

**Q4.** No experimento do relé sobre a planta de 3ª ordem do curso ($G = \dfrac{1}{(s+1)(s+2)(s+4)}$, cujo ponto crítico é $K_u = 90$, $\omega_u = \sqrt{14}$ rad/s), usa-se relé de amplitude $d = 1$.
(a) Pela função descritiva $N(a) = \dfrac{4d}{\pi a}$, calcule a amplitude $a$ do ciclo-limite previsto.
(b) Calcule o período $T_u$ esperado.
(c) Se o relé passar a $d = 0{,}5$, o que muda em $a$, $T_u$ e na estimativa de $K_u$? Por que isso torna o método robusto?

**Q5.** Um PI com $K_p = 2$ e $T_i = 4$ opera saturado ($u_{max} = 1$) enquanto o erro fica preso em $e = 1$ durante 3 s.
(a) De quanto cresce a parcela integral nesse intervalo?
(b) Ao fim, o erro salta para $e = -0{,}5$ e lá permanece. Quanto tempo o integrador leva para devolver o excesso acumulado (sem anti-windup)?
(c) Com back-calculation ($T_t = 1$), escreva a equação do integrador durante a saturação e explique por que a "devolução" é muito mais rápida.

**Q6.** No anti-windup por back-calculation, discuta os efeitos de escolher $T_t$ muito grande e muito pequeno, e justifique a regra prática $T_t = \sqrt{T_iT_d}$ (ou $T_i/2$ para PI).

**Q7.** Para o pêndulo $\dot{x}_1 = x_2$, $\dot{x}_2 = -\sin x_1 - 0{,}5x_2$:
(a) Encontre todos os pontos de equilíbrio.
(b) Linearize em $(0, 0)$ e em $(\pi, 0)$ e classifique cada equilíbrio pelos autovalores.
(c) 🖥️ Gere o retrato de fase com `ct.phase_plane_plot` e identifique visualmente as classificações do item (b).

**Q8.** Diferencie **oscilação marginal linear** (polos sobre o eixo $j\omega$) de **ciclo-limite não linear** quanto a: dependência da condição inicial, robustez a perturbações e assinatura no plano de fase. Cite um exemplo de cada visto nos Labs 05–07.
