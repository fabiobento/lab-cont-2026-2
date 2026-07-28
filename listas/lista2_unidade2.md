# Lista 2 — Unidade II: Malha fechada, estabilidade e desempenho

**Entrega:** fim da semana 7 · Consulta liberada; trabalho individual. 🖥️ = verificar com `python-control`.

> 🖼️ Figuras de apoio para esta lista (consultar antes de resolver):
>
> - Schaum (DiStefano), **Fig. 7-16** — o sistema de realimentação canônico (base de toda a álgebra de blocos). Cap. 7, **p. 164** (p. 175 do PDF).
> - Nise, **Tabela 6.3** — tabela de Routh completa do Exemplo 6.1 (modelo de preenchimento passo a passo). Cap. 6, p. 456 do arquivo PDF (a cópia digital não exibe o nº impresso).
> - Ogata, **Figura 6.3** — sistema do Exemplo 6.1 e a construção completa do seu lugar das raízes na sequência. Cap. 6 (Exemplo 6.1), **p. 249** (p. 260 do PDF).
> - Ogata, **Figura 7.67** — definição gráfica das margens de ganho e de fase (sistemas estáveis × instáveis). Cap. 7, **p. 426** (p. 437 do PDF).
> - Ogata, **Figura 7.47** — contorno de Nyquist no plano $s$ (eixo $j\omega$ + semicírculo de raio infinito). Cap. 7, **p. 411** (p. 422 do PDF).

---

**Q1.** A planta $G(s) = \dfrac{5}{2s+1}$ (motor do curso) é realimentada com controlador proporcional $K_p = 3$ e realimentação unitária.
(a) Obtenha a FT de malha fechada e a nova constante de tempo.
(b) Calcule o erro de regime ao degrau unitário.
(c) O que acontece com $\tau_{mf}$ e $e_{ss}$ quando $K_p \to \infty$? Que fenômeno prático impede esse limite?

**Q2.** Especifica-se para uma malha de 2ª ordem padrão: $M_p \le 10\,\%$ e $t_s(2\%) \le 2$ s.
(a) Traduza as especificações em restrições sobre $\zeta$ e $\sigma = \zeta\omega_n$.
(b) Desenhe a região admissível dos polos no plano $s$.
(c) Proponha um par de polos que atenda com folga e calcule $M_p$ e $t_s$ resultantes.

**Q3.** Para $L(s) = \dfrac{K}{(s+1)(s+2)(s+3)}$ em realimentação unitária:
(a) Monte a tabela de Routh e determine a faixa de $K$ que estabiliza a malha.
(b) Determine o ganho crítico $K_u$ e a frequência $\omega_u$ da oscilação sustentada (linha auxiliar de Routh).
(c) 🖥️ Confirme com `ct.root_locus_plot` e simulando o degrau com $K = K_u$.

**Q4.** Para $L(s) = \dfrac{K}{s(s+2)}$:
(a) Classifique o tipo do sistema e calcule $e_{ss}$ para degrau e para rampa unitária (em função de $K$).
(b) Determine o menor $K$ para erro de rampa $\le 5\,\%$.
(c) Esse aumento de $K$ tem custo. Qual, em termos de amortecimento? Justifique pelos polos de malha fechada.

**Q5.** Para $L(s) = \dfrac{K}{s(s+1)^2}$ com $K = 1$:
(a) Calcule analiticamente a frequência de cruzamento de fase $\omega_{180}$ e a margem de ganho.
(b) 🖥️ Obtenha PM e $\omega_{gc}$ com `ct.margin` e verifique se a malha atende ao critério do curso (PM ≥ 45°, GM ≥ 6 dB).
(c) Qual o maior $K$ que mantém GM ≥ 6 dB?

**Q6.** Esboce à mão o lugar das raízes de $L(s) = \dfrac{K(s+4)}{s(s+2)}$: segmentos no eixo real, pontos de saída/entrada e comportamento assintótico. O sistema pode instabilizar para algum $K > 0$? 🖥️ Compare com `ct.root_locus_plot`.

**Q7.** A planta **instável** $P(s) = \dfrac{1}{s-1}$ é controlada por $C(s) = K$.
(a) Aplique o critério de Nyquist ($Z = N + P$): quantos envolvimentos de $-1$ são necessários para estabilizar?
(b) Esboce o Nyquist de $L = K/(s-1)$ e determine a faixa de $K$ estabilizante.
(c) Confirme algebricamente pelo polo de malha fechada.

**Q8.** Uma malha tem PM = 45° na frequência de cruzamento $\omega_{gc} = 2$ rad/s. Qual o maior tempo morto adicional $\theta$ que ela tolera antes de instabilizar (margem de atraso)? Comente a relevância para controle via rede/serial no projeto final.
