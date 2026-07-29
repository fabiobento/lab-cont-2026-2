# Unidade II — Malha fechada: elementos essenciais, estabilidade e desempenho

## Apostila completa e autossuficiente

**Carga: 4 h (semanas 5–7) · Labs 04 e 05 · Lista 2**

Pré-requisito: Unidade I (FT, polos, 1ª/2ª ordem, Bode — ver `apostila_unidade1_completa.md`).

Esta é a **versão expandida e autossuficiente** da apostila da Unidade II. Todo o conteúdo
indicado nas caixas 📖 "Onde estudar" da versão original foi desenvolvido **na íntegra
aqui mesmo**: deduções completas, tabelas de referência, casos especiais e exemplos
resolvidos adicionais — sem necessidade de consultar os livros da disciplina. As referências
aos capítulos originais (Nise, Ogata, Schaum, Penedo, FBS) foram mantidas ao final de cada
seção apenas para conferência.

---

## 1. Por que fechar a malha

*(Desenvolve Nise, cap. 1 e cap. 5; Ogata, cap. 2 e cap. 5; Schaum, caps. 2 e 7; Penedo,
cap. 6; FBS, cap. 2.)*

### 1.1 Malha aberta × malha fechada

Em **malha aberta**, o controlador calcula a entrada da planta "às cegas": qualquer erro de
modelo ou perturbação vai direto para a saída. Exemplo clássico (FBS, cap. 2): o controle de
velocidade de cruzeiro *sem* sensor de velocidade — calcula-se o ângulo do acelerador que
"deveria" dar 100 km/h; qualquer subida, vento ou mudança de carga desvia a velocidade real.
Em **malha fechada**, mede-se a saída, compara-se com a referência e o **erro**
$e = r - y$ comanda o controlador:

```
 r ──►(＋)──► C(s) ──► u ──►(＋d)──► G(s) ──┬──► y
       ▲(−)                                │
       └────────────────────────────────────┘
```

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-7-16-schaum.png)

**Figura 2.1 — O sistema de realimentação canônico: referência $R$, erro atuante $E$,
sinal realimentado $B$, caminho direto $G$ e caminho de realimentação $H$.** (Fonte:
DISTEFANO et al., Fig. 7-16, Cap. 7)

### 1.2 Os elementos da malha (Nise, cap. 1; Schaum, cap. 2)

Cada bloco da Figura 2.1 tem um papel físico definido:

| Elemento | Papel | No kit do laboratório |
|---|---|---|
| **Referência** $r$ | valor desejado da saída | setpoint no display/serial |
| **Somador** | gera o erro $e = r - b$ | subtração no firmware |
| **Controlador** $C(s)$ | calcula a ação de controle $u$ | o PID digital |
| **Atuador** | converte o comando em potência | ponte H L298N + PWM |
| **Planta** $G(s)$ | o sistema físico | motoredutor CC / sistema térmico |
| **Sensor** $H(s)$ | mede a saída | encoder de quadratura / LM35 |

Distinção clássica de terminologia (Schaum, cap. 2): **servomecanismo** = a referência
*muda* com o tempo e o objetivo é segui-la (controle de posição do kit); **regulador** = a
referência é *fixa* e o objetivo é rejeitar perturbações (controle de temperatura). As duas
tarefas têm exigências diferentes — essa tensão reaparece no 2DOF (Unidade IV, §6).

### 1.3 As duas funções de transferência que resumem tudo

A álgebra de blocos (Unidade I, §3) dá:

$$\underbrace{T(s) = \frac{Y}{R} = \frac{C G}{1 + CG}}_{\text{referência} \to \text{saída}}\qquad
\underbrace{T_{dy}(s) = \frac{Y}{D} = \frac{G}{1 + CG}}_{\text{perturbação} \to \text{saída}}$$

(pela superposição: com $D=0$ obtém-se $T$; com $R=0$, a perturbação entra depois de $C$,
logo o numerador é só $G$).

O denominador comum $1 + C(s)G(s)$ é o coração do curso: **os polos de malha fechada são as
raízes de $1 + CG = 0$**, a *equação característica*. Todo o resto da unidade é aprender a
prever onde essas raízes estão sem precisar calculá-las diretamente.

### 1.4 O que a realimentação compra — com dedução (FBS, cap. 2)

**(i) Redução do efeito de perturbações.** Em malha aberta, a perturbação $d$ somada na
entrada da planta aparece na saída como $G\cdot d$; em malha fechada aparece como
$\dfrac{G}{1+CG}\cdot d$ — dividida pelo fator $1 + CG$. O mesmo fator atenua o erro de
modelo: definindo a **sensibilidade** de $T$ a variações relativas de $G$,

$$S = \frac{\partial T/T}{\partial G/G} = \frac{G}{T}\frac{\partial T}{\partial G}
= \frac{G(1+CG)}{CG}\cdot\frac{C(1+CG) - C\cdot CG}{(1+CG)^2} = \boxed{\frac{1}{1+CG}}.$$

Ou seja: uma variação de 10 % nos parâmetros da planta produz, em malha fechada com
$|CG| = 9$, apenas ~1 % de variação na FT de malha fechada. É a dedução formal do "a
realimentação torna o sistema insensível ao modelo".

**(ii) Resposta mais rápida** — o Exercício 1 abaixo quantifica: a constante de tempo cai
de $1+K_pK$ vezes.

**(iii) Estabilização de plantas instáveis** — só a realimentação consegue mover polos do
semiplano direito para o esquerdo (§6 mostra o caso extremo).

**E o preço:** mal projetada, a malha fechada instabiliza um sistema que era estável em
malha aberta — daí a obsessão com estabilidade nesta unidade.

### Exercício resolvido 1 — o efeito do ganho na malha do motor

*O motor do curso, $G = \dfrac{5}{2s+1}$, é fechado com controlador proporcional $C = K_p = 3$
e realimentação unitária. Obtenha $T(s)$, a nova constante de tempo e o erro de regime ao
degrau.*

**Solução.**
$$T(s) = \frac{15/(2s+1)}{1 + 15/(2s+1)} = \frac{15}{2s+16} = \frac{0{,}9375}{0{,}125s+1}.$$
A malha fechada ainda é 1ª ordem, mas com $\tau_{mf} = 2/16 = 0{,}125$ s — **16× mais rápida**
— e ganho estático $0{,}9375 \ne 1$. O erro de regime ao degrau unitário:
$$e_{ss} = 1 - T(0) = 1 - \frac{15}{16} = \frac{1}{1+K_pK} = 6{,}25\,\%.$$
Aumentar $K_p$ melhora os dois... até o atuador saturar (Unidade III) ou, em plantas de ordem
maior, até a malha oscilar (§4). Este compromisso é o tema da unidade.

> 📖 **Referências originais desta seção (para conferência):** Nise, cap. 1 (elementos da
> malha) e cap. 5 (redução com realimentação). Ogata, cap. 2 (blocos) e cap. 5 (efeitos das
> ações de controle). Schaum, cap. 2 (terminologia: servomecanismo × regulador) e cap. 7
> (Fig. 7-16 e provas das fórmulas $C/R$, $E/R$, $B/R$). Penedo, cap. 6. FBS, cap. 2
> (*Feedback Principles* — inclui a dedução da sensibilidade).

---

## 2. Erro de regime permanente e o "tipo" do sistema

*(Desenvolve Nise, cap. 7 — na íntegra; Schaum, §9.4–9.9; Ogata, cap. 5, parte final;
FBS, caps. 7 e 12.)*

### 2.1 Dedução completa das constantes de erro (Nise, cap. 7)

Para malha fechada unitária estável, $E(s) = \dfrac{R(s)}{1 + L(s)}$, com $L = CG$ a FT
**de malha**. Pelo teorema do valor final:

$$e_{ss} = \lim_{s\to0} sE(s) = \lim_{s\to0} \frac{sR(s)}{1 + L(s)}.$$

**Degrau unitário** ($R = 1/s$):
$$e_{ss} = \lim_{s\to0}\frac{1}{1+L(s)} = \frac{1}{1 + \lim L(s)} = \frac{1}{1 + K_{pos}},
\qquad K_{pos} \equiv \lim_{s\to0} L(s).$$

**Rampa unitária** ($R = 1/s^2$):
$$e_{ss} = \lim_{s\to0}\frac{1}{s(1+L)} = \frac{1}{\lim sL(s)} = \frac{1}{K_v},
\qquad K_v \equiv \lim_{s\to0} sL(s).$$

**Parábola unitária** ($R = 1/s^3$):
$$e_{ss} = \frac{1}{K_a}, \qquad K_a \equiv \lim_{s\to0} s^2L(s).$$

O que decide se essas constantes são finitas ou infinitas é **quantos polos na origem**
(integradores puros $1/s$) existem em $L(s)$ — o **tipo** do sistema. Escrevendo
$L(s) = \dfrac{K\prod(s+z_i)}{s^n\prod(s+p_j)}$, o tipo é $n$. A tabela completa:

| Tipo de $L(s)$ | degrau | rampa | parábola | Constantes |
|---|---|---|---|---|
| 0 (nenhum $1/s$) | $\dfrac{1}{1+K_{pos}}$ | ∞ | ∞ | $K_{pos} = \lim L$; $K_v = K_a = 0$ |
| 1 (um $1/s$) | **0** | $1/K_v$ | ∞ | $K_{pos} = \infty$; $K_v = \lim sL$; $K_a = 0$ |
| 2 | 0 | **0** | $1/K_a$ | $K_{pos} = K_v = \infty$; $K_a = \lim s^2L$ |

**Por que o integrador zera o erro?** Leitura física: um integrador só "descansa" (sua
saída para de variar) quando sua entrada é zero — e a entrada do integrador é o erro. Se a
malha é estável e contém um integrador, em regime o erro *tem* que ser zero. É a razão de
ser da ação integral do PID (Unidade IV).

**Atenção à distinção que aparece no kit:** no controle de **velocidade** a planta é tipo 0,
logo o integrador precisa estar no controlador; no controle de **posição** o integrador já
está na planta ($\theta = \int\omega\,dt$), e o erro ao degrau já é nulo com P puro.

**Erro para perturbação na entrada da planta** (caso importante na bancada): com
$E/R$ não se calcula — usa-se $E(s) = -\dfrac{G(s)}{1+CG}D(s)$ e o TVF. Se a perturbação é
um degrau e o controlador tem integrador, o erro também vai a zero.

**Observação (Schaum, §9.9):** as fórmulas supõem malha fechada **estável** — o TVF não se
aplica a sistema instável, e um "erro de regime" calculado para malha instável é
matematicamente bonito e fisicamente inútil.

### Exercício resolvido 2 — projeto por especificação de erro

*Para $L(s) = \dfrac{K}{s(s+4)}$: (a) erro ao degrau e à rampa; (b) menor $K$ para erro de
rampa ≤ 2 %; (c) o custo dessa escolha.*

**Solução.** (a) Tipo 1 ⟹ $e_{degrau} = 0$; $K_v = \lim sL = K/4$ ⟹ $e_{rampa} = 4/K$.
(b) $4/K \le 0{,}02 \Rightarrow K \ge 200$.
(c) Malha fechada: $s^2 + 4s + K = 0 \Rightarrow \omega_n = \sqrt{K},\ \zeta = 2/\sqrt{K}$.
Com $K = 200$: $\zeta = 0{,}141$ ⟹ $M_p \approx 64\,\%$ — inaceitável. **Precisão de regime e
amortecimento conflitam** no controlador P; resolver esse conflito (com o zero do PD, ou
avanço de fase) é o que a Unidade IV faz.

**Exercício adicional 2.A — erro com perturbação.**
*Na malha do Exercício 1 ($C = 3$, $G = 5/(2s+1)$), uma perturbação degrau unitário entra na
entrada da planta. Qual o efeito permanente na saída? E se o controlador for PI,
$C = 3(1 + 1/(2s))$?*

**Solução.** $T_{dy}(0) = \dfrac{G(0)}{1+C(0)G(0)} = \dfrac{5}{16} = 0{,}31$ — resta 31 % da
perturbação. Com PI, $C(0) \to \infty$ ⟹ $T_{dy}(0) = 0$: **o integrador rejeita totalmente
perturbações constantes** — por isso a bancada com atrito (perturbação de carga quase
constante) exige ação I.

> 📖 **Referências originais desta seção (para conferência):** Nise, cap. 7 (tipos,
> constantes de erro, tabelas e exemplos resolvidos). Schaum, §9.4–9.9 (classificação por
> tipo e constantes $K_p, K_v, K_a$ com resumo em tabela). Ogata, cap. 5 (parte final).
> FBS, cap. 7 (rastreamento) e cap. 12 (ação integral).

---

## 3. Estabilidade absoluta: o critério de Routh–Hurwitz

*(Desenvolve Nise, cap. 6 — incluindo os casos especiais; Ogata, cap. 5; Schaum, §5.3–5.4;
Penedo, §4.5.)*

Um sistema é **estável** (BIBO) se e só se todos os polos têm parte real negativa. O
critério de **Routh** responde "todas as raízes estão no semiplano esquerdo?" **sem
calcular as raízes** — só com os coeficientes da equação característica
$a_ns^n + a_{n-1}s^{n-1} + \dots + a_1s + a_0 = 0$.

### 3.1 O procedimento completo

**Passo 0 — condição necessária (mas não suficiente):** todos os coeficientes presentes
(nenhuma potência faltando) e de mesmo sinal. Se falhar, já existem raízes no semiplano
direito (ou sobre o eixo imaginário) e nem vale montar a tabela.

**Passo 1 — montar a tabela.** As duas primeiras linhas recebem os coeficientes
alternados:

| linha | 1ª col. | 2ª col. | 3ª col. |
|---|---|---|---|
| $s^n$ | $a_n$ | $a_{n-2}$ | $a_{n-4}$ |
| $s^{n-1}$ | $a_{n-1}$ | $a_{n-3}$ | $a_{n-5}$ |
| $s^{n-2}$ | $b_1$ | $b_2$ | $\dots$ |
| $s^{n-3}$ | $c_1$ | $\dots$ | |

Cada elemento novo vem do **determinante cruzado** das duas linhas imediatamente acima,
sempre usando a primeira coluna como pivô, com sinal trocado:

$$b_1 = \frac{-\begin{vmatrix}a_n & a_{n-2}\\ a_{n-1} & a_{n-3}\end{vmatrix}}{a_{n-1}}
= \frac{a_{n-1}a_{n-2} - a_n a_{n-3}}{a_{n-1}},\qquad
b_2 = \frac{a_{n-1}a_{n-4} - a_n a_{n-5}}{a_{n-1}},$$

$$c_1 = \frac{b_1a_{n-3} - a_{n-1}b_2}{b_1},\quad \dots$$

Duas simplificações legítimas (Nise, cap. 6): qualquer linha pode ser **multiplicada por
uma constante positiva** (limpa frações, sem alterar sinais); e a tabela termina quando só
restam zeros.

**Passo 2 — interpretar (o teorema):**

> **O número de raízes no semiplano direito = número de trocas de sinal na primeira
> coluna da tabela.** Estável ⟺ nenhuma troca de sinal.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/tab-6-3-nise.png)

**Figura 2.2 — Tabela de Routh completa do Exemplo 6.1 do Nise (polinômio
$s^3 + 10s^2 + 31s + 1030$): note o preenchimento por determinantes cruzados e as duas
trocas de sinal na primeira coluna ($1 \to 1 \to -72 \to 103$) — o sistema tem dois polos
no semiplano direito.** (Fonte: NISE, Tabela 6.3, Cap. 6)

### 3.2 Casos especiais (Nise, cap. 6, na íntegra)

**Caso especial 1 — zero na primeira coluna (com linha não nula).** Não se pode dividir por
zero. Solução prática: substitui-se o zero por $\varepsilon > 0$ pequeno, completa-se a
tabela e faz-se $\varepsilon \to 0^+$ observando os sinais. Se os sinais acima e abaixo do
$\varepsilon$ coincidirem, há raízes puramente imaginárias; se trocarem, há raízes no
semiplano direito.

**Caso especial 2 — linha inteira nula.** Indica raízes simétricas em relação à origem
(pares $\pm s$): raízes imaginárias conjugadas, ou pares reais opostos, ou quadrados
complexos. Procedimento:
1. Forme o **polinômio auxiliar** $P(s)$ com os coeficientes da linha *imediatamente acima*
   da linha nula — ele tem só potências pares de $s$;
2. Substitua a linha nula pelos coeficientes de $dP/ds$;
3. Continue a tabela normalmente.
As raízes de $P(s) = 0$ são exatamente as raízes simétricas — e é assim que se encontra a
frequência de oscilação no limite de estabilidade (ver Exercício 3).

### 3.3 O uso mais valioso: faixa estabilizante de ganho

Com o ganho $K$ como incógnita literal, a primeira coluna vira um conjunto de desigualdades
em $K$ — Routh entrega a **faixa estabilizante** e o **ganho crítico** $K_u$. No limite, a
linha que zera fornece, via polinômio auxiliar, a frequência da oscilação sustentada
$\omega_u$. Esse par $(K_u, \omega_u)$ alimenta a sintonia de Ziegler–Nichols na
Unidade IV.

### Exercício resolvido 3 — Routh na planta de 3ª ordem do curso

*Para $L(s) = \dfrac{K}{(s+1)(s+2)(s+4)}$ em malha fechada unitária, determine a faixa
estabilizante de $K$, o ganho crítico e a frequência de oscilação.*

**Solução.** Característica: $(s+1)(s+2)(s+4) + K = s^3 + 7s^2 + 14s + (8+K) = 0$. Tabela:

| | | |
|---|---|---|
| $s^3$ | $1$ | $14$ |
| $s^2$ | $7$ | $8+K$ |
| $s^1$ | $\dfrac{7\cdot14 - (8+K)}{7} = \dfrac{90-K}{7}$ | $0$ |
| $s^0$ | $8+K$ | |

Primeira coluna positiva ⟺ $\dfrac{90-K}{7} > 0$ **e** $8+K > 0$ ⟹ $\boxed{-8 < K < 90}$.
No limite $K = K_u = 90$ a linha $s^1$ zera (Caso especial 2): o **polinômio auxiliar** vem
da linha $s^2$:
$$7s^2 + 98 = 0 \Rightarrow s = \pm j\sqrt{14}, \quad\text{ou seja}\quad
\omega_u = \sqrt{14} \approx 3{,}74\ \text{rad/s},\qquad T_u = \frac{2\pi}{\omega_u} \approx 1{,}68\ \text{s}.$$
Guarde $K_u = 90$ e $T_u = 1{,}68$ s: reaparecem no experimento do relé (Lab 07) e nas
tabelas de Ziegler–Nichols (Lab 09) — é a espinha dorsal numérica do curso.

**Exercício adicional 3.A — o caso da linha nula com oscilação.**
*Verifique a estabilidade de $s^4 + 2s^3 + 3s^2 + 2s + 2$... veja o que acontece na linha
$s^1$: os dois elementos zeram. Linha auxiliar: $2s^2 + 2$ ⟹ $dP/ds = 4s$; a tabela
continua ($s^1$: 4; $s^0$: 2), sem trocas de sinal — mas as raízes de $2s^2+2 = 0$ são
$\pm j$: o sistema é **marginalmente estável**, com oscilação de frequência 1 rad/s. Lição:
linha nula + nenhuma troca de sinal ⟹ não é instável, mas tem polos sobre o eixo
imaginário.*

> 📖 **Referências originais desta seção (para conferência):** Nise, cap. 6 (procedimento,
> TABELA 6.3, zero na primeira coluna §6.4, linha nula §6.5). Ogata, cap. 5 (critério de
> Routh). Schaum, §5.3 (procedimento resumido + muitos resolvidos; §5.4 determinantes de
> Hurwitz). Penedo, §4.5.

---

## 4. Lugar das raízes: como os polos "andam" quando o ganho varia

*(Desenvolve Nise, cap. 8 e cap. 9; Ogata, cap. 6 — na íntegra; Schaum, caps. 13 e 14;
Penedo, caps. 5 e 7.)*

### 4.1 Definição e as duas condições fundamentais (Ogata, cap. 6)

O **lugar geométrico das raízes (LGR)** é o mapa das raízes de $1 + K\,L_0(s) = 0$ quando
$K$ varia de 0 a ∞. Reescrevendo a equação característica:

$$L_0(s) = -\frac{1}{K}\;\;(\text{real negativo})\;\Rightarrow\;
\begin{cases}\textbf{condição angular:} & \angle L_0(s) = \pm 180°(2k+1)\\[2mm]
\textbf{condição de módulo:} & |L_0(s)| = 1/K\end{cases}$$

A condição angular decide **se um ponto pertence ao LGR**; a condição de módulo diz **qual
ganho** corresponde a esse ponto. Os ângulos se calculam vetorialmente: cada polo/zero de
malha aberta contribui com o ângulo do vetor que vai dele ao ponto de teste — soma dos
ângulos dos zeros menos soma dos ângulos dos polos.

### 4.2 Regras de esboço (Nise, cap. 8 — conjunto completo usado no curso)

1. **Número de ramos** = número de polos de malha aberta $n_p$. Os ramos **começam nos
   polos** de $L_0$ ($K = 0$) e **terminam nos zeros** ($K \to \infty$) — os $n_p - n_z$
   ramos sem zero finito terminam no infinito.
2. **Simetria:** o LGR é simétrico em relação ao eixo real (raízes complexas vêm em pares
   conjugados).
3. **Eixo real:** um ponto do eixo real pertence ao LGR se há um número **ímpar** de
   polos+zeros reais à sua direita (polos/zeros complexos contribuem ângulos que se
   cancelam aos pares — por isso só os reais contam).
4. **Assíntotas:** os $n_p - n_z$ ramos que vão ao infinito o fazem ao longo de retas com
   ângulos $\theta_k = \dfrac{(2k+1)180°}{n_p-n_z}$, $k = 0, 1, \dots$, partindo do
   **centroide**
   $$\sigma_a = \frac{\sum \text{polos} - \sum \text{zeros}}{n_p - n_z}.$$
5. **Pontos de saída/entrada no eixo real (*breakaway/break-in*):** onde dois ramos se
   encontram e se tornam complexos (ou voltam ao eixo real). Resolve-se $dK/ds = 0$ com
   $K = -1/L_0(s)$ expresso em função de $s$ reais, mantendo só as soluções que estão no
   LGR.
6. **Cruzamento do eixo $j\omega$:** por Routh (como no Exercício 3) — dá $K_u$ e
   $\omega_u$.
7. **Ângulos de partida/chegada** (polos/zeros complexos): o ramo sai de um polo complexo
   $p_c$ com ângulo $\theta_p = 180° + \sum\angle(\text{zeros}) - \sum\angle(\text{outros polos})$,
   medido a partir de $p_c$; análogo para chegada a zeros complexos. No curso (plantas com
   polos reais) raramente é necessário, mas é a regra que falta para o caso geral.
8. **Ganho num ponto do LGR:** $K = \dfrac{\prod \text{distâncias aos polos}}
   {\prod \text{distâncias aos zeros}}$ — a condição de módulo lida graficamente.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-6-3-ogata.png)

**Figura 2.3 — Sistema do Exemplo 6.1 do Ogata: $G(s) = \dfrac{K}{s(s+1)(s+2)}$ com
realimentação unitária.** (Fonte: OGATA, Figura 6.3, Cap. 6)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-6-6-ogata.png)

**Figura 2.4 — O lugar das raízes completo desse sistema: três ramos, assíntotas a
$\pm 60°$ e $180°$ com centroide em $-1$, saída do eixo real em $s = -0{,}42$, cruzamento
com o eixo imaginário em $\pm j\sqrt{2}$ quando $K = 6$, e o projeto $\zeta = 0{,}5$ no
ponto $K = 1{,}0383$ (linha tracejada de $60°$).** (Fonte: OGATA, Figura 6.6, Cap. 6)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-13-2-schaum.png)

**Figura 2.5 — Um LGR de dois ramos calculado analiticamente
($GH = \dfrac{K(s+1)}{s(s+2)}$): cada raiz de malha fechada foi fatorada em função de $K$
— um ramo vai do polo 0 ao zero $-1$, o outro do polo $-2$ ao "zero no infinito".**
(Fonte: DISTEFANO et al., Fig. 13-2, Cap. 13)

### 4.3 Intuições de projeto (Nise, cap. 9)

- **Acrescentar um polo empurra o lugar para a direita** (piora estabilidade — é o que o
  tempo morto e filtros extras fazem na prática);
- **Acrescentar um zero puxa para a esquerda** (melhora amortecimento — é o que a ação
  derivativa faz: o PD acrescenta um zero em $-1/T_d$);
- Pontos do LGR sobre uma mesma reta a partir da origem têm o mesmo $\zeta$ — o projeto de
  ganho por especificação é: desenhar a reta do $\zeta$ desejado, achar a interseção com o
  LGR e ler $K$ pela condição de módulo (é o que a Figura 2.4 mostra para $\zeta = 0{,}5$).

### Exercício resolvido 4 — esboço completo

*Esboce o LGR de $L(s) = \dfrac{K}{s(s+2)(s+4)}$ e determine o $K$ do cruzamento com o eixo
imaginário.*

**Solução.** Polos em $0, -2, -4$; sem zeros; $n_p - n_z = 3$.
Eixo real: LGR entre $0$ e $-2$ (um polo à direita) e à esquerda de $-4$ (três à direita).
Assíntotas: ângulos $\pm60°$ e $180°$, centroide $\sigma_a = (0-2-4)/3 = -2$.
Saída do eixo real: $K = -s(s+2)(s+4) = -(s^3+6s^2+8s)$;
$dK/ds = -(3s^2 + 12s + 8) = 0 \Rightarrow s = -0{,}845$ (a raiz $-3{,}15$ está fora do
trecho válido).
Cruzamento $j\omega$: característica $s^3+6s^2+8s+K$; Routh dá $K < 6\cdot8 = 48$ e a linha
auxiliar $6s^2 + 48 = 0 \Rightarrow \omega = \sqrt{8} = 2{,}83$ rad/s.
Esboço: dois ramos saem de $0$ e $-2$, encontram-se em $-0{,}845$, tornam-se complexos e
cruzam o eixo em $\pm j2{,}83$ quando $K = 48$; o terceiro ramo vai de $-4$ para $-\infty$.

> 📖 **Referências originais desta seção (para conferência):** Nise, cap. 8 (técnicas,
> regra a regra, com exemplos de cada caso) e cap. 9 (projeto via LGR — inclusive PID).
> Ogata, cap. 6 (inteiro: condições angular/de módulo e o Exemplo 6.1 completo, FIGURAS
> 6.3–6.6). Schaum, cap. 13 (análise, FIG. 13-2) e cap. 14 (projeto). Penedo, caps. 5 e 7
> (em português).

---

## 5. Estabilidade relativa: margens de ganho e de fase

*(Desenvolve Ogata, cap. 7 — estabilidade relativa; Nise, cap. 10 e cap. 11; Schaum,
caps. 10, 15 e 16; FBS, caps. 10 e 12.)*

Routh e LGR dizem *se* a malha é estável; as **margens** dizem *quão longe* da instabilidade
ela opera — essencial porque o modelo nunca é exato. A fronteira da instabilidade, no
domínio da frequência, é o ponto $L(j\omega) = -1$: ganho 1 com fase $-180°$ (o sinal
realimentado volta somado a si mesmo). As margens medem a distância a esse ponto por dois
"caminhos" diferentes, ambos lidos no Bode de $L(j\omega)$:

- **Margem de ganho (GM):** na frequência $\omega_{180}$ em que a fase cruza $-180°$, quanto
  falta para o ganho chegar a 1:
  $$GM = \frac{1}{|L(j\omega_{180})|}\quad\text{(em dB: } GM_{dB} = -20\log_{10}|L(j\omega_{180})|\text{)}.$$
  É **por quanto o ganho da planta pode crescer** antes de instabilizar. GM = 2 (6 dB)
  significa: se o ganho real for o dobro do modelado, a malha entra em oscilação.
- **Margem de fase (PM):** na frequência de cruzamento de ganho $\omega_{gc}$ (onde
  $|L| = 1$), quanto falta para a fase chegar a $-180°$:
  $$PM = 180° + \angle L(j\omega_{gc}).$$
  É **quanto atraso de fase extra** a malha tolera — e atraso de fase é o que tempo morto,
  amostragem e dinâmicas não modeladas acrescentam.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-10-37-nise.png)

**Figura 2.6 — Leitura das margens no diagrama de Bode: desce-se de $\omega_{\Phi_M}$
(onde o ganho é 0 dB) para ler a margem de fase $\Phi_M$; desce-se de $\omega_{G_M}$ (onde
a fase é $-180°$) para ler a margem de ganho $G_M$.** (Fonte: NISE, Figura 10.37, Cap. 10)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-10-1-schaum.png)

**Figura 2.7 — As mesmas margens em escala linear de ganho: a margem de ganho é a distância
de $|GH(j\omega_{\varphi})|$ até 1, e a margem de fase é o ângulo que falta para $-180°$ em
$\omega_1$ (ganho unitário).** (Fonte: DISTEFANO et al., Fig. 10-1, Cap. 10)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-7-67-ogata.png)

**Figura 2.8 — Margens de ganho e de fase de sistemas estáveis e instáveis: (a) nos
diagramas de Bode; (b) nos diagramas polares (plano $G$); (c) no diagrama módulo (dB) ×
fase. Nos casos instáveis as margens são "negativas".** (Fonte: OGATA, Figura 7.67, Cap. 7)

### 5.1 A ponte margens ↔ resposta no tempo

Duas regras de bolso que amarram frequência e tempo (usadas o curso inteiro):

$$\zeta \approx \frac{PM\ [°]}{100}\quad(PM \lesssim 70°),\qquad
\text{banda da malha fechada} \approx \omega_{gc}.$$

A primeira vem da 2ª ordem: para $G = \omega_n^2/[s(s+2\zeta\omega_n)]$, calcula-se
exatamente $PM = \arctan\dfrac{2\zeta}{\sqrt{\sqrt{1+4\zeta^4}-2\zeta^2}}$, que é quase
perfeitamente linear em $\zeta$ até $\zeta \approx 0{,}7$ — daí $PM \approx 100\zeta$.
Assim, **PM = 45° ⟺ $\zeta \approx 0{,}45$ ⟺ $M_p \approx 20\,\%$**.

**Critério de aceitação do curso: PM ≥ 45° e GM ≥ 6 dB.**

A PM tem uma consequência prática direta: a **margem de atraso**
$$\theta_{max} = \frac{PM_{rad}}{\omega_{gc}}\ \text{[s]}$$
— o maior tempo morto adicional tolerável antes de a fase no cruzamento passar de $-180°$.
É ela que o período de amostragem consome no controle digital (atraso médio $\approx h/2$,
Unidade IV).

### Exercício resolvido 5 — margens à mão e no critério do curso

*Para $L(s) = \dfrac{4}{(s+1)^3}$: calcule GM analiticamente, obtenha PM (numericamente) e
julgue pelo critério do curso.*

**Solução.** Fase: $\angle L = -3\arctan\omega$. Cruza $-180°$ quando
$\arctan\omega = 60° \Rightarrow \omega_{180} = \tan 60° = \sqrt{3}$ rad/s.
$$|L(j\sqrt{3})| = \frac{4}{\left(\sqrt{1+3}\right)^3} = \frac{4}{8} = 0{,}5
\;\Rightarrow\; GM = 2 = 6{,}0\ \text{dB}.$$
Numericamente (Lab 05, `ct.margin`): $\omega_{gc} = 1{,}23$ rad/s e $PM = 27{,}1°$.
**Veredito:** GM passa raspando (6 dB), PM reprova (27° < 45°) — a malha é estável mas
oscilaria demais ($\zeta \approx 0{,}27$ pela regra de bolso ⟹ $M_p \approx 40\,\%$).
Moral: **as margens se avaliam em conjunto**; uma boa e outra ruim = projeto ruim.

> 📖 **Referências originais desta seção (para conferência):** Ogata, cap. 7 (estabilidade
> relativa: GM/PM no Bode e no polar, FIGURA 7.67). Nise, cap. 10 (margens, FIGURA 10.37)
> e cap. 11 (projeto por margens). Schaum, cap. 10 (FIG. 10-1), caps. 15–16. FBS, caps. 10
> e 12 — e as transparências CDS 110 L7-2 (slide "Robust stability: gain and phase
> margins").

---

## 6. O critério de Nyquist: a ferramenta definitiva

*(Desenvolve Ogata, cap. 7 — seção do critério; Nise, cap. 10; Schaum, cap. 11 e cap. 12;
FBS, cap. 10.)*

Bode + margens bastam quando a planta é estável e de fase "comportada". O caso geral —
inclusive **plantas com polo na origem** (o controle de posição do kit!) e plantas instáveis
— exige o **critério de Nyquist**. A curva de Nyquist é $L(j\omega)$ traçada no plano
complexo para $\omega$ de $-\infty$ a $+\infty$.

### 6.1 O mapeamento por trás do critério (Schaum, cap. 11)

A ideia central é o **mapeamento de contornos**: quando $s$ percorre um contorno fechado no
plano $s$, a função $F(s) = 1 + L(s)$ percorre um contorno fechado no plano $F$. O
**princípio do argumento** (análise complexa) diz que

$$N = Z - P,$$

onde: $Z$ = nº de **zeros** de $F$ dentro do contorno; $P$ = nº de **polos** de $F$ dentro
do contorno; $N$ = nº de **envolvimentos horários da origem** pela curva $F(s)$.

**De onde vem isso?** O argumento de $F(s)$ é $\sum\angle(s - z_i) - \sum\angle(s - p_i)$.
Quando $s$ dá uma volta completa no contorno, cada zero *dentro* dele contribui $+360°$ ao
argumento total e cada polo dentro contribui $-360°$; os de fora contribuem 0° líquido. A
variação total do argumento é $2\pi(Z - P)$ — e cada $360°$ de variação é exatamente uma
volta da curva em torno da origem.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-11-3-schaum.png)

**Figura 2.9 — Contorno fechado no plano complexo: o ponto de partida do mapeamento que
leva ao critério de Nyquist.** (Fonte: DISTEFANO et al., Fig. 11-3, Cap. 11)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-7-47-ogata.png)

**Figura 2.10 — O contorno de Nyquist no plano $s$: o eixo $j\omega$ inteiro mais o
semicírculo de raio infinito, percorrido no sentido horário — ele envolve todo o semiplano
direito.** (Fonte: OGATA, Figura 7.47, Cap. 7)

Aplicando ao **contorno de Nyquist** (Figura 2.10), que envolve todo o semiplano direito:
os zeros de $F = 1 + L$ no SPD são **os polos de malha fechada** (pois $T = L/(1+L)$) e os
polos de $F$ são os polos de malha aberta. Como $F = 1 + L$, envolver a origem no plano $F$
é o mesmo que envolver o ponto $-1$ no plano $L$. Resultado:

> **Teorema (Nyquist).** Sejam $P$ = nº de polos de $L$ no semiplano direito (SPD),
> $N$ = nº de envolvimentos **horários** do ponto $-1$ pela curva de Nyquist, e $Z$ = nº de
> polos de malha fechada no SPD. Então $\boxed{Z = N + P}$; a malha fechada é estável
> ⟺ $Z = 0$.

### 6.2 Como a curva é construída (Nise, cap. 10)

Na prática (e no `ct.nyquist_plot`): (1) traça-se $L(j\omega)$ para $\omega: 0^+ \to +\infty$
via Bode — cada ponto tem módulo e fase; (2) espelha-se em relação ao eixo real (é o trecho
$\omega < 0$, pois $L(-j\omega) = \overline{L(j\omega)}$); (3) fecha-se no infinito — para
plantas estritamente próprias, o semicírculo infinito mapeia na origem. A Figura 2.11
mostra a construção vetorial completa de um caso de 3 polos.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-10-27-nise.png)

**Figura 2.11 — Cálculo vetorial do diagrama de Nyquist para $G(s) = \dfrac{500}
{(s+1)(s+3)(s+10)}$: (a) vetores de cada polo ao ponto de teste em frequência baixa;
(b) vetores ao longo do arco infinito; (c) o diagrama de Nyquist resultante.** (Fonte:
NISE, Figura 10.27, Cap. 10)

Intuição física: $L(j\omega) = -1$ significa ganho 1 com fase $-180°$ — o sinal volta
somado a si mesmo e cresce a cada volta na malha. O critério conta, via princípio do
argumento, quantas raízes de $1 + L$ caíram do lado errado.

### 6.3 Três consequências para o curso

1. **Planta estável ($P = 0$):** estável ⟺ a curva **não envolve** $-1$; a distância mínima
   da curva a $-1$ resume a robustez — é a **margem de estabilidade**
   $s_m = \min_\omega|1+L(j\omega)| = 1/M_s$ (a terceira margem, Lab 05 §7.3);
2. **Planta instável ($P > 0$):** a curva **precisa** envolver $-1$ anti-horário $P$ vezes
   — envolver é obrigação, não defeito (Lab 05 §7.2);
3. **Polo na origem** (posição no kit): o contorno de Nyquist é deformado para contornar o
   polo com um pequeno semicírculo de raio $\varepsilon \to 0$ pela direita; esse desvio
   mapeia num **arco infinito** que fecha a curva — o raciocínio $Z = N + P$ é o único
   confiável nesses casos (ler "margens" no Bode de uma planta tipo 1 sem esse cuidado leva
   a erros de interpretação).

### Exercício resolvido 6 — quando ganho ALTO estabiliza

*A planta instável $P(s) = \dfrac{2}{s-2}$ é controlada por $C = K$. Use Nyquist para achar a
faixa estabilizante de $K$ e confirme algebricamente.*

**Solução.** $P = 1$ polo no SPD ⟹ para $Z = N + P = 0$ é preciso $N = -1$: **um envolvimento
anti-horário** de $-1$. A curva de $L(j\omega) = \dfrac{2K}{j\omega - 2}$ parte de $-K$
($\omega = 0$), tende a 0 ($\omega\to\infty$) e forma um círculo no semiplano esquerdo.
Ela envolve $-1$ (anti-horário, uma vez) se e só se o ponto inicial está à esquerda de $-1$:
$-K < -1 \Rightarrow \boxed{K > 1}$.
Confirmação: $1 + L = 0 \Rightarrow s = 2 - 2K$: negativo ⟺ $K > 1$ ✓.
**Note a inversão da intuição:** aqui ganho baixo instabiliza — o oposto do Exercício 3.
Nenhuma "regra de Bode" pega isso; Nyquist pega sempre.

**Exercício adicional 6.A — lendo $s_m$.**
*Para a malha do Exercício 5 ($L = 4/(s+1)^3$), sabe-se que $M_s = \max|S| \approx 2{,}2$.
Qual a distância mínima da curva de Nyquist a $-1$ e o que isso diz?*

**Solução.** $s_m = 1/M_s \approx 0{,}45 < 0{,}5$ — confirma o veredito do Exercício 5: a
curva passa "perto demais" de $-1$; qualquer erro de modelo de ~45 % já pode provocar
envolvimento. O critério $M_s \le 2$ (Unidade IV, §5) é a versão moderna e mais completa
das margens GM/PM.

> 📖 **Referências originais desta seção (para conferência):** Ogata, cap. 7 (critério de
> Nyquist com o contorno completo, FIGURA 7.47). Nise, cap. 10 (dedução gráfica, FIGURA
> 10.27). Schaum, cap. 11 (análise por Nyquist — definições 11.2–11.6, FIG. 11-3, passo a
> passo) e cap. 12 (projeto). FBS, cap. 10 (a formulação $Z = N + P$ usada no curso) — e as
> transparências CDS 110 L7-2 (slides 5 e 10).

---

## 7. Resumo da unidade e conexão com os labs

| Conceito | Onde está nesta apostila | Onde pratica | Livro-âncora |
|---|---|---|---|
| Malha fechada, $T$, $T_{dy}$, sensibilidade | §1 (deduções completas) | Lab 04 | Nise 5; FBS 2 |
| Erro de regime e tipo | §2 (dedução das constantes) | Lab 04/05, Lista 2 | Nise 7; Schaum 9 |
| Routh, $K_u$, $\omega_u$ | §3 (inclui casos especiais) | Lab 05 §1–2 | Nise 6; Ogata 5 |
| Lugar das raízes | §4 (regras 1–8 + exemplos) | Lab 05 §3 | Nise 8; Ogata 6 |
| GM, PM, critério do curso | §5 (leitura no Bode) | Lab 05 §4–6 | Ogata 7; Nise 10–11 |
| Nyquist $Z = N + P$, $s_m = 1/M_s$ | §6 (mapeamento deduzido) | Lab 05 §7 | FBS 10; Schaum 11 |

**Autoavaliação antes da Lista 2:** você deve conseguir (i) obter $T(s)$ e o erro de regime
de qualquer malha simples; (ii) montar uma tabela de Routh com $K$ literal e extrair
$K_u, \omega_u$, incluindo tratar a linha nula; (iii) esboçar um LGR de 3 polos com
assíntotas, breakaway e cruzamento; (iv) ler GM e PM num Bode e julgar pelo critério
PM ≥ 45°/GM ≥ 6 dB; (v) aplicar $Z = N + P$ inclusive com planta instável.

---

## Mapa das fórmulas da Unidade II (folha de consulta)

| Tema | Fórmulas-chave |
|---|---|
| Malha fechada | $T = \frac{CG}{1+CG}$; $T_{dy} = \frac{G}{1+CG}$; $S = \frac{1}{1+CG}$ |
| Erro de regime | $e_{ss} = \lim sE$; $K_{pos} = \lim L$, $K_v = \lim sL$, $K_a = \lim s^2L$ |
| Tipos | tipo 0: $1/(1+K_{pos})$; tipo 1: rampa $1/K_v$; tipo 2: parábola $1/K_a$ |
| Routh | trocas de sinal na 1ª coluna = polos no SPD; linha nula → polinômio auxiliar $P(s)$, derivar |
| LGR | condição angular $\pm180°(2k+1)$; assíntotas $\frac{(2k+1)180°}{n_p-n_z}$; centroide $\frac{\sum p - \sum z}{n_p-n_z}$; breakaway $dK/ds = 0$ |
| Margens | $GM = 1/|L(j\omega_{180})|$; $PM = 180° + \angle L(j\omega_{gc})$; $\zeta \approx PM/100$ |
| Margem de atraso | $\theta_{max} = PM_{rad}/\omega_{gc}$ |
| Nyquist | $Z = N + P$ (N horário); $s_m = \min|1+L| = 1/M_s$ |
| Critério do curso | PM ≥ 45°, GM ≥ 6 dB, $M_s \le 2$ |

---

## Leituras dirigidas da Unidade II

**Esta apostila cobre integralmente o conteúdo abaixo** — use a tabela apenas se quiser
conferir a formulação original em cada fonte:

| Prioridade | Fonte | O que ler | Onde está aqui |
|---|---|---|---|
| essencial | **Nise**, caps. 5–8 e 10 | redução de blocos, erro de regime (cap. 7 inteiro), Routh (TABELA 6.3), lugar das raízes e margens (FIGURAS 10.27 e 10.37) | §1–§6 |
| essencial | **Ogata**, caps. 5–7 | Routh, lugar das raízes (Exemplo 6.1, FIGURAS 6.3 e 6.6), Nyquist (FIGURA 7.47) e margens (FIGURA 7.67) | §3–§6 |
| exercícios | **Schaum**, caps. 5, 7, 9–13 | estabilidade (§5.3), constantes de erro (§9.4–9.9), Nyquist (cap. 11, FIG. 11-3), LGR (cap. 13, FIG. 13-2), malha canônica (FIG. 7-16) | §1–§6 |
| em português | **Penedo**, caps. 4–5 e 7 | estabilidade, LGR e projeto por lugar das raízes | §3–§4 |
| aprofundamento | **FBS**, caps. 2, 10 e 12 | princípios da realimentação, critério de Nyquist na forma $Z = N + P$ e robustez | §1, §6 |
| slides | **CDS 110** L7-1 e L7-2 | análise em pequenos sinais; critério de Nyquist (slide 5) e margens (slide 10) | §5–§6 |

## Referências bibliográficas

Ver a lista completa ao final de `apostila_unidade1_completa.md` (Ogata, Nise, DiStefano et
al., Penedo, Åström & Murray/FBS, CDS 110, `python-control`).
