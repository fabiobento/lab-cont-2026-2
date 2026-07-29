# Unidade III — Não-linearidades em sistemas de controle

## Apostila completa e autossuficiente

**Carga: 4 h (semanas 8–9) · Labs 06 e 07 · Lista 3**

Toda a teoria das Unidades I–II supõe **linearidade**: dobrar a entrada dobra a saída, e a
soma de causas produz a soma dos efeitos. Nenhum sistema real é assim em toda a faixa de
operação. Esta unidade estuda as três não-linearidades onipresentes na bancada — saturação,
zona morta e histerese — e os dois fenômenos novos que elas criam: **windup** e
**ciclos-limite**. Sem esta unidade, o PID que funciona na simulação falha no kit.

Esta é a **versão expandida e autossuficiente**: todo o conteúdo das caixas 📖 "Onde
estudar" da versão original foi desenvolvido na íntegra aqui. Os livros clássicos de
graduação tratam não-linearidades de forma dispersa; as referências-âncora desta unidade
são **FBS** (Åström & Murray, caps. 5 e 11), **Åström & Hägglund** (*Advanced PID Control*)
e o capítulo de sistemas não lineares do **Schaum** (DiStefano et al., cap. 19), cujas
figuras e deduções foram incorporadas ao texto.

---

## 1. As três não-linearidades da bancada

*(Desenvolve Ogata, cap. 8; FBS, cap. 5 e cap. 11; Åström & Hägglund, cap. 3; Nise, cap. 2
— linearização; Schaum, §3.5 e cap. 19.)*

Antes dos três casos, uma distinção útil (Schaum, cap. 19): não-linearidades **"suaves"**
(como $f(e) = e^3$, atrito viscoso quadrático) aproximam-se bem por linearização no ponto de
operação; não-linearidades **"duras"** ou *essenciais* (saturação, zona morta, histerese,
relé) têm descontinuidades ou quinas que nenhuma reta tangente representa — são elas que
estudamos aqui.

### 1.1 Saturação

Todo atuador tem limites: o PWM vai de 0 a 100 %, a fonte entrega no máximo $V_{max}$, a
válvula abre no máximo até o fim. Modelo:

$$u_{sat} = \mathrm{sat}(v) = \begin{cases} u_{max}, & v > u_{max}\\ v, & u_{min} \le v \le u_{max}\\ u_{min}, & v < u_{min}\end{cases}$$

Na faixa linear o ganho é 1; fora dela o ganho efetivo cai (a saída "trava" no batente
enquanto a entrada continua crescendo). Consequência estrutural: **existe uma saída máxima
alcançável em regime**,
$$y_{max} = G(0)\,u_{max}.$$
Pedir mais que isso não é "sintonia ruim" — é fisicamente impossível, e o controlador que
não sabe disso entra em windup (§2).

### 1.2 Zona morta

Perto de zero, o atuador não responde: no kit, a ponte H + atrito estático exigem um PWM
mínimo para o motor sair do repouso. Modelo (banda $\pm\delta$):

$$u = \begin{cases} v - \delta, & v > \delta\\ 0, & |v| \le \delta\\ v + \delta, & v < -\delta\end{cases}$$

Consequência: com controlador P, a malha "desiste" quando o comando entra na banda — fica um
**erro residual** que nenhum aumento finito de $K_p$ elimina de todo. Note que zona morta e
atrito estático (Stribeck) são duas descrições do mesmo fenômeno físico: o torque de
"destravamento".

### 1.3 Histerese (com memória)

A saída depende do **caminho**: folga (*backlash*) de engrenagens, comparadores com
histerese, termostatos liga/desliga. É a única das três com **estado interno** — para
saber a saída não basta saber a entrada atual, é preciso saber de onde ela veio. Por isso
no Lab 06 ela é implementada como `ct.nlsys` **com estado**.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-19-10-schaum.png)

**Figura 3.1 — Característica de histerese (*backlash*): a saída segue ramos diferentes na
subida e na descida da entrada, formando um laço de largura $2d$; a inclinação dos ramos é
o ganho $K$.** (Fonte: DISTEFANO et al., Fig. 19-10, Cap. 19)

### Exercício resolvido 1 — o que a saturação torna impossível

*Uma planta térmica $G(s) = \dfrac{2}{10s+1}$ (K em °C por unidade de potência, acima da
ambiente) tem atuador limitado a $0 \le u \le 1{,}5$. (a) Qual o maior aquecimento de regime
alcançável? (b) O que acontece se a referência pedir 4 °C acima do ambiente com um PI bem
sintonizado?*

**Solução.** (a) $y_{max} = G(0)\,u_{max} = 2 \times 1{,}5 = 3$ °C.
(b) Como $4 > 3$: a saída sobe e **estaciona em 3**; o atuador fica cravado em 1,5; o erro
fica preso em $e \to 1$ e o integrador do PI, que só descansa com $e = 0$, **cresce sem
limite** (windup extremo). Quando a referência voltar a um valor alcançável, a malha ainda
levará muito tempo "descarregando" o integrador antes de reagir. Diagnóstico correto:
problema de **dimensionamento do atuador**, não de sintonia.

### Exercício resolvido 2 — a banda de erro da zona morta

*No kit, a zona morta equivalente do conjunto ponte H + atrito é $\delta = 0{,}12$ (em fração
de PWM). Com controle proporcional $K_p = 3$ na malha de velocidade, qual a banda de erro
residual? E com $K_p = 12$?*

**Solução.** A malha para de agir quando o comando $v = K_pe$ cai na banda:
$K_p|e| \le \delta \Rightarrow |e| \le \delta/K_p$.
Com $K_p = 3$: $|e| \le 0{,}04$; com $K_p = 12$: $|e| \le 0{,}01$
— quatro vezes menor, mas **nunca zero**. Ação integral elimina o erro *médio*, porém ao
custo de uma oscilação lenta de baixa amplitude ("hunting"): o integrador acumula até vencer
a banda, o sistema corrige e ultrapassa, o erro troca de sinal e o ciclo recomeça. A solução
de engenharia é a **compensação de zona morta** — somar $\hat\delta\,\mathrm{sign}(v)$ ao
comando (implementada no firmware de posição, constante `DEADZONE_COMP`; cuidado com
supercompensação, que vira um mini-relé e gera vibração).

> 📖 **Referências originais desta seção (para conferência):** Ogata, cap. 8 (saturação no
> contexto do PID). FBS, cap. 5 (Dynamic Behavior) e cap. 11 (saturação em malhas PID).
> Åström & Hägglund, cap. 3 (efeitos de atuador). Nise, cap. 2 (linearização) e Schaum,
> §3.5 (ponto de operação) e cap. 19 (características das não-linearidades, Fig. 19-10).

---

## 2. Windup: quando o integrador "não sabe" da saturação

*(Desenvolve FBS, cap. 11 — "Integral Windup"; Åström & Hägglund, cap. 3; Ogata, cap. 8;
transparências CDS 110 L9-1/L9-2.)*

### 2.1 O mecanismo, passo a passo

Durante uma saturação prolongada (degrau grande, referência inalcançável, perturbação
forte):

1. o erro persiste (o atuador no batente não consegue eliminá-lo);
2. o integrador, **cego para o atuador**, continua acumulando o erro;
3. quando o erro finalmente inverte de sinal, o integrador está tão carregado que o comando
   segue saturado **no sentido errado**;
4. resultado: **sobressinal enorme e resposta lenta**.

A assinatura experimental do windup é a **saída cruzando a referência com o atuador ainda
no batente** — numa malha bem projetada, o comando deveria ter saído da saturação *antes*
do cruzamento.

### 2.2 A cura — back-calculation (FBS, cap. 11)

A ideia: informar ao integrador que o atuador saturou, e drenar o excesso. Compara-se o
comando pedido $v$ com o aplicado $u_{sat}$ e realimenta-se a diferença ao integrador com
ganho $1/T_t$:

$$\dot{I} = \frac{K_p}{T_i}e + \frac{1}{T_t}\left(u_{sat} - v\right).$$

**Análise dos dois regimes:**

- **Fora da saturação:** $u_{sat} = v$, o termo extra é nulo — o PID é exatamente o
  original. O anti-windup é *cirurgicamente invisível* na operação normal.
- **Dentro da saturação:** suponha $v > u_{max}$ com $e > 0$ ainda positivo. O termo
  $(u_{sat} - v)/T_t$ é negativo e cresce com o excesso $v - u_{max}$; em equilíbrio
  dinâmico ($\dot I \approx 0$), o excesso estabiliza em
  $v - u_{sat} \approx \dfrac{T_t K_p}{T_i}e$ — o comando fica **"colado" logo acima do
  batente**, em vez de subir sem limite. Ao inverter o erro, o comando sai da saturação
  quase imediatamente.

**Escolha de $T_t$ (tempo de rastreamento):** regra do curso $T_t = \sqrt{T_iT_d}$ (PID)
ou $T_i/2$ (PI). $T_t$ grande demais = anti-windup fraco (drena devagar, quase como não
ter); pequeno demais = integrador escravizado ao batente, com resposta preguiçosa ao sair
da saturação e sensibilidade a ruído de medição no sinal $u_{sat}$.

**Variante — clamping (parada condicional):** simplesmente congelar o integrador enquanto
$v$ estiver saturado e o erro tiver o mesmo sinal de $v$. Mais simples de implementar,
porém menos suave que o back-calculation (o integrador para "seco" e pode estacionar com
erro pequeno preso).

### Exercício resolvido 3 — a aritmética do windup

*Um PI com $K_p = 1{,}5$ e $T_i = 3$ s opera saturado enquanto o erro fica preso em
$e = +1$ por 4 s. (a) Quanto o integrador acumula? (b) Se depois o erro salta para
$e = -0{,}4$, quanto tempo leva para devolver o acúmulo sem anti-windup? (c) E o que muda
com back-calculation, $T_t = 1{,}5$ s?*

**Solução.** (a) $\Delta I = \dfrac{K_p}{T_i}\displaystyle\int_0^4 e\,dt = \dfrac{1{,}5}{3}\cdot 1\cdot 4 = 2{,}0$.
(b) Taxa de descarga: $\dot{I} = \dfrac{K_p}{T_i}e = 0{,}5\times(-0{,}4) = -0{,}2$/s ⟹
$t = 2{,}0/0{,}2 = \boxed{10\ \text{s}}$ — dois turnos e meio do tempo de carga, com a malha
inutilizada nesse intervalo.
(c) Com back-calculation, enquanto $v$ excede $u_{max}$ o termo $(u_{sat}-v)/T_t$ drena o
excesso na escala de $T_t = 1{,}5$ s — o integrador nunca chega a acumular os 2,0; ele para
de crescer assim que $v$ encosta no batente. O Lab 07 §1 mostra as duas curvas lado a lado
com o estado do integrador plotado.

> 📖 **Referências originais desta seção (para conferência):** FBS, cap. 11 (seção
> "Integral Windup" — inclui o diagrama de back-calculation usado no curso). Åström &
> Hägglund, cap. 3. Ogata, cap. 8 (PID modificados). Transparências CDS 110 L9-2 — o
> diagrama de blocos do anti-windup exatamente como implementado na classe `DigitalPID`
> (Lab 10) e no firmware do kit.

---

## 3. Retratos de fase: enxergar a dinâmica não linear inteira

*(Desenvolve FBS, cap. 5 — na íntegra; Schaum, cap. 19 (plano de fase); Ogata, cap. 2
(linearização); notebook CDS 110 L2.)*

### 3.1 O plano de fase e o campo de vetores

Para sistemas de 2ª ordem, o **retrato de fase** traça as trajetórias no plano
$(x_1, x_2)$ — tipicamente (posição, velocidade). Escrevendo o sistema como
$\dot x_1 = x_2$, $\dot x_2 = f(x_1, x_2)$, cada ponto do plano tem uma seta (o campo
$\dot{x} = f(x)$); as curvas seguem as setas. Eliminando o tempo entre as duas equações,
as trajetórias obedecem a $\dfrac{dx_2}{dx_1} = \dfrac{f(x_1,x_2)}{x_2}$ — uma EDO no
plano. O retrato mostra de uma vez o que dezenas de simulações temporais mostrariam, e é a
ferramenta que revela os fenômenos que **não existem** no mundo linear.

### 3.2 Pontos de equilíbrio e sua classificação (FBS, cap. 5)

**Pontos de equilíbrio**: onde $f(x_e) = 0$ — o sistema parado ali fica ali. A
classificação local vem da **linearização**: $A = \left.\dfrac{\partial f}{\partial x}
\right|_{x_e}$ (jacobiano) e seus autovalores $\lambda_{1,2}$:

| Autovalores | Tipo de equilíbrio | Retrato local |
|---|---|---|
| reais, ambos negativos | **nó estável** | trajetórias entram direto, sem oscilar |
| reais, ambos positivos | nó instável | trajetórias saem direto |
| complexos, parte real negativa | **foco estável** | espiral que converge (oscilação amortecida) |
| complexos, parte real positiva | foco instável | espiral que diverge |
| um positivo, um negativo | **sela** | instável; duas separatrizes entram, duas saem |
| imaginários puros | centro | órbitas fechadas em torno do ponto |

(Teorema de Hartman–Grobman, enunciado no FBS: perto do equilíbrio, o retrato não linear é
qualitativamente igual ao da linearização — **exceto** quando há autovalor com parte real
nula, caso em que só a análise não linear decide.)

### 3.3 Região de atração: local × global

A **região de atração** de um equilíbrio é o conjunto de condições iniciais que converge a
ele. Em sistemas lineares estáveis é o plano inteiro; **com saturação ela encolhe** — o Lab
06 §6 mostra o pêndulo com controle P saturado escapando quando parte de longe: o comando
satura, o sistema "perde autoridade" e cai para outro equilíbrio. Estabilidade **local**
≠ **global**: distinção que não existe no mundo linear e que é central quando o atuador é
limitado. As fronteiras entre regiões de atração são as **separatrizes** das selas.

### 3.4 Ciclos-limite

Órbitas fechadas **isoladas** no plano de fase — ver §4.

### Exercício resolvido 4 — classificando equilíbrios do pêndulo

*Para $\dot{x}_1 = x_2$, $\dot{x}_2 = -\sin x_1 - 0{,}5x_2$ (pêndulo com atrito, normalizado):
encontre e classifique os equilíbrios.*

**Solução.** Equilíbrios: $x_2 = 0$ e $\sin x_1 = 0 \Rightarrow (k\pi, 0)$.
Jacobiano: $A = \begin{bmatrix}0 & 1\\ -\cos x_1 & -0{,}5\end{bmatrix}$.
Em $(0,0)$ (pêndulo para baixo): $\lambda^2 + 0{,}5\lambda + 1 = 0 \Rightarrow
\lambda = -0{,}25 \pm 0{,}97j$ — **foco estável**: trajetórias espiralam para dentro
(oscilação amortecida).
Em $(\pi, 0)$ (invertido): $\lambda^2 + 0{,}5\lambda - 1 = 0 \Rightarrow
\lambda = \{0{,}78; -1{,}28\}$ — **sela**: instável; as separatrizes que passam por ela
dividem o plano em regiões de atração dos equilíbrios estáveis vizinhos.
No Lab 06 este retrato é gerado com `ct.phase_plane_plot` — compare o esboço com o gráfico.

**Exercício adicional 4.A — linearização na prática (revisão do Lab 01).**
*Linearize $\ddot\theta = -\frac{g}{l}\sin\theta$ em torno de $\theta_e = \pi$ (invertido).*

**Solução.** Com $\theta = \pi + \tilde\theta$, $\sin(\pi + \tilde\theta) \approx
-\tilde\theta$: $\ddot{\tilde\theta} = +\frac{g}{l}\tilde\theta$ — polos em
$\pm\sqrt{g/l}$: instável (sela), coerente com a tabela. É por isso que o controle de
posição do kit é difícil em grandes ângulos: o modelo linear só vale perto do ponto de
operação — **validade local**.

> 📖 **Referências originais desta seção (para conferência):** FBS, cap. 5 (equilíbrios,
> linearização, retratos de fase, regiões de atração — referência do curso, gratuita
> online). Notebook CDS 110 **L2** (pêndulo invertido, versão computacional). Ogata, cap. 2
> (linearização). Schaum, §3.5 e cap. 19 (plano de fase, Exemplos 19.11 e ss.).

---

## 4. Ciclos-limite e a função descritiva

*(Desenvolve FBS, cap. 5 e cap. 10; Schaum, cap. 19 (§19.5 — função descritiva, na
íntegra); Åström & Hägglund, cap. 4; Ogata, cap. 7 e cap. 8.)*

### 4.1 Ciclo-limite × oscilação marginal linear

Um **ciclo-limite** é uma oscilação periódica com **amplitude e período próprios do
sistema**, independentes da condição inicial: no plano de fase, uma órbita fechada
**isolada e atratora** (trajetórias de dentro e de fora convergem para ela). Compare com a
oscilação marginal linear ($\zeta = 0$): lá as órbitas são uma família contínua de elipses
concêntricas, a amplitude depende de onde se começou, e qualquer perturbação de parâmetro a
destrói. O ciclo-limite é robusto — por isso aparece tanto (e por isso é útil: §4.3).

### 4.2 Função descritiva: definição e dedução do relé ideal (Schaum, §19.5)

**Definição.** Excita-se o elemento não linear com $e = a\sin\omega t$; a saída periódica
$f(e(t))$ é expandida em série de Fourier $\sum_n B_n\sin(n\omega t + \phi_n)$. A
**função descritiva** é o "ganho equivalente ao primeiro harmônico":

$$N(a, \omega) = \frac{B_1 e^{j\phi_1}}{a},$$

a razão entre a componente fundamental da saída e a amplitude da entrada. Para elementos
sem memória e ímpares, $N$ não depende de $\omega$ e é real.

**Dedução para o relé ideal.** Relé de amplitude $d$: $f(e) = d\,\mathrm{sign}(e)$. Com
$e = a\sin\omega t$, a saída é uma onda quadrada $\pm d$ em fase com a senoide. O primeiro
harmônico de uma onda quadrada de amplitude $d$ tem amplitude $4d/\pi$ (coeficiente de
Fourier clássico: $B_1 = \frac{2}{\pi}\int_0^\pi d\sin\theta\,d\theta = \frac{4d}{\pi}$).
Como não há defasagem ($\phi_1 = 0$):

$$\boxed{N(a) = \frac{4d}{\pi a}}$$

**Condição de ciclo-limite** (balanço harmônico) numa malha relé + planta $G$: a oscilação
se sustenta quando o sinal, ao dar uma volta completa na malha, retorna igual a si mesmo:

$$N(a)\,G(j\omega) = -1 \quad\Longleftrightarrow\quad
\boxed{G(j\omega) = -\frac{1}{N(a)} = -\frac{\pi a}{4d}}$$

Graficamente: a oscilação ocorre na **interseção da curva de Nyquist de $G(j\omega)$ com o
lugar de $-1/N(a)$** (que, para o relé, é o eixo real negativo de $0^-$ a $-\infty$).
Como $-1/N$ é real, a oscilação acontece **na frequência em que a fase de $G$ é $-180°$**
— exatamente $\omega_u$ da Unidade II! — e com amplitude $a$ tal que o ganho do relé
"complete" o ganho crítico.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-19-12-schaum.png)

**Figura 3.2 — A malha padrão da análise por função descritiva: um único elemento não
linear em cascata com a planta linear $G(\omega)$.** (Fonte: DISTEFANO et al., Fig. 19-12,
Cap. 19)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-19-13-schaum.png)

**Figura 3.3 — O critério gráfico: traçam-se no plano polar $G(\omega)$ e $-1/N(A)$; as
interseções dão amplitude e frequência das oscilações. Neste exemplo (saturação +
$G = 8/[j\omega(j\omega+2)^2]$) não há interseção — o sistema não oscila.** (Fonte:
DISTEFANO et al., Fig. 19-13, Cap. 19)

### 4.3 O experimento do relé (identificação automática de $K_u$, $T_u$)

Essa é a joia da unidade (Åström–Hägglund, 1984 — usado em autotuning industrial até
hoje): substituindo temporariamente o controlador por um relé de amplitude $d$, a malha
entra sozinha num ciclo-limite pequeno e seguro. Medem-se a amplitude $a$ da oscilação da
**saída** e o período $T_u$, e então

$$\boxed{K_u = \frac{4d}{\pi a}},\qquad T_u\ \text{lido direto do registro.}$$

É o modo `M 2` do firmware do kit. Note a diferença de papéis em relação ao método clássico
de Ziegler–Nichols (Figuras 3.4 e 3.5): lá, ajusta-se o ganho proporcional **na mão** até a
oscilação sustentada — demorado e potencialmente inseguro; aqui, o relé leva a malha ao
mesmo ponto crítico **automaticamente**, com amplitude controlável por $d$.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-4-ogata.png)

**Figura 3.4 — Malha fechada apenas com ganho proporcional: o arranjo clássico para obter
$K_{cr}$ (2º método de Ziegler–Nichols). O experimento do relé substitui $K_p$ pelo relé
de amplitude $d$ e chega ao mesmo ponto crítico automaticamente.** (Fonte: OGATA, Figura
8.4, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-5-ogata.png)

**Figura 3.5 — Oscilação sustentada com período $P_{cr}$: o registro que se obtém tanto no
2º método de ZN quanto no experimento do relé (neste, lendo também a amplitude $a$).**
(Fonte: OGATA, Figura 8.5, Cap. 8)

### Exercício resolvido 5 — prevendo e usando o ciclo do relé

*Na planta de 3ª ordem do curso ($K_u = 90$, $\omega_u = \sqrt{14}$, do Exercício 3 da
Unidade II), instala-se um relé de amplitude $d = 2$. (a) Preveja a amplitude e o período do
ciclo-limite. (b) Na bancada mediu-se $a = 0{,}031$: qual o $K_u$ estimado e o erro?*

**Solução.** (a) $a = \dfrac{4d}{\pi K_u} = \dfrac{8}{\pi\cdot 90} = 0{,}0283$;
$T_u = 2\pi/\sqrt{14} = 1{,}68$ s.
(b) $\hat{K}_u = \dfrac{4\cdot2}{\pi\cdot 0{,}031} = 82{,}1$ — erro de ~9 % em relação a 90.
Erros dessa ordem são normais: a função descritiva ignora os harmônicos superiores da onda
quadrada (a planta os filtra parcialmente — quanto mais polos, melhor a aproximação).
Para as tabelas de sintonia (Unidade IV) essa precisão é mais que suficiente.
**Bônus conceitual:** dobrar $d$ dobra $a$ mas **não muda** $T_u$ nem $\hat{K}_u$ — a
frequência do ciclo é propriedade da planta (o ponto de fase $-180°$), não do relé. É isso
que torna o método robusto e ajustável à segurança da bancada (relé pequeno ⟹ oscilação
pequena).

### 4.4 Relé com histerese: o termostato

Acrescentando histerese $\pm h$ ao relé (liga abaixo de $r - h$, desliga acima de $r + h$)
obtém-se o controle liga/desliga clássico. O ciclo-limite agora é **intencional**: a
temperatura oscila numa banda em torno da referência. Reduzir $h$ estreita a banda mas
**aumenta a frequência de comutação** — desgaste de contatos/chaveamento é o preço; por isso
$h \to 0$ não se usa. Pela função descritiva, a histerese acrescenta **atraso de fase** ao
elemento ($N(a)$ passa a ser complexa — Figura 3.1 mostra a característica e o Schaum
Fig. 19-11 traz $|\bar N|$ e $\phi_1(A)$ normalizados), o que desloca a interseção com
$G(j\omega)$ e permite ajustar o ponto do ciclo — usado no autotuning para obter outros
pontos da curva de Nyquist. O Lab 06 §5 simula o termostato como `ct.nlsys` com estado.

> 📖 **Referências originais desta seção (para conferência):** FBS, cap. 5 (ciclos-limite)
> e cap. 10 (a leitura de $G(j\omega) = -1/N$ como interseção com o Nyquist). Schaum,
> cap. 19, §19.5 (definição de função descritiva, Eq. 19.35–19.36, exemplos 19.17–19.20
> resolvidos, FIGS. 19-10 a 19-13). Åström & Hägglund, cap. 4 (dedução completa do
> experimento do relé, inclusive com histerese). Ogata, cap. 7 (base de $G(j\omega)$) e
> cap. 8 (FIGURAS 8.4 e 8.5).

---

## 5. Resumo da unidade e conexão com os labs

| Conceito | Onde está nesta apostila | Onde pratica | Livro-âncora |
|---|---|---|---|
| Saturação, alcançabilidade | §1.1 + Ex. 1 | Lab 06 §3 | FBS 11; Å&H 3 |
| Zona morta e compensação | §1.2 + Ex. 2 | Lab 06 §4 + firmware `DEADZONE_COMP` | FBS 5 |
| Histerese/termostato | §1.3, §4.4 | Lab 06 §5 | Schaum 19; Å&H 4 |
| Retratos de fase, região de atração | §3 (tabela de classificação) | Lab 06 §6 | FBS 5; CDS 110 L2 |
| Windup e back-calculation | §2 (dedução dos dois regimes) | Lab 07 §1 → Lab 10 e firmware | FBS 11 |
| Ciclo-limite × oscilação marginal | §4.1 | Labs 05×07 | FBS 5 |
| Função descritiva do relé | §4.2 (dedução completa) | Lab 07 §2 | Schaum 19; Å&H 4 |
| Experimento do relé, $K_u = 4d/\pi a$ | §4.3 + Ex. 5 | Lab 07 §2 → projeto final | Å&H 4 |

**Autoavaliação antes da Lista 3:** você deve conseguir (i) calcular a maior referência
alcançável dada a saturação; (ii) explicar o mecanismo do windup em 4 passos e escrever a
equação do back-calculation; (iii) classificar equilíbrios por linearização (tabela de
autovalores); (iv) deduzir de onde vem $K_u = 4d/(\pi a)$ e aplicá-la a dados de bancada;
(v) justificar por que o período do relé não depende de $d$; (vi) interpretar a condição
$G(j\omega) = -1/N(a)$ como interseção no plano de Nyquist.

---

## Mapa das fórmulas da Unidade III (folha de consulta)

| Tema | Fórmulas-chave |
|---|---|
| Alcançabilidade | $y_{max} = G(0)\,u_{max}$ |
| Zona morta | banda de erro residual $|e| \le \delta/K_p$; compensação $+\hat\delta\,\mathrm{sign}(v)$ |
| Anti-windup | $\dot I = \frac{K_p}{T_i}e + \frac{1}{T_t}(u_{sat}-v)$; $T_t = \sqrt{T_iT_d}$ ou $T_i/2$ |
| Equilíbrios | $f(x_e) = 0$; classificação pelos autovalores do jacobiano |
| Função descritiva | $N(a) = B_1e^{j\phi_1}/a$; relé ideal: $N(a) = 4d/(\pi a)$ |
| Balanço harmônico | $G(j\omega) = -1/N(a)$: oscilação na fase $-180°$ |
| Experimento do relé | $K_u = 4d/(\pi a)$; $T_u$ medido; $a \propto d$, $T_u$ independente de $d$ |

---

## Leituras dirigidas da Unidade III

**Esta apostila cobre integralmente o conteúdo abaixo.** Atenção: os livros de graduação
tratam não-linearidades de forma dispersa — aqui o FBS e o Åström & Hägglund são as fontes
principais.

| Prioridade | Fonte | O que ler | Onde está aqui |
|---|---|---|---|
| essencial | **FBS**, caps. 5 e 11 | comportamento dinâmico (equilíbrios, retratos de fase, regiões de atração, ciclos-limite) e a seção "Integral Windup" | §2, §3, §4.1 |
| essencial | **Åström & Hägglund**, caps. 3–4 | efeitos de atuador, anti-windup e o experimento do relé completo (inclusive com histerese) | §1, §2, §4.3–4.4 |
| essencial | **Schaum**, cap. 19 | características das não-linearidades e função descritiva (§19.5, FIGS. 19-10 a 19-13) com exercícios resolvidos | §1.3, §4.2 |
| apoio | **Ogata**, cap. 8 | saturação no contexto do PID e PID modificados (FIGURAS 8.4 e 8.5) | §1, §4.3 |
| apoio | **Nise**, cap. 2 · **Schaum**, §3.5 | linearização e ponto de operação | §3.4 |
| computacional | **CDS 110** L2 e L4a · doc. `python-control` | fase plana do pêndulo, ciclo-limite do predador–presa e o exemplo oficial *Describing function analysis* | Labs 06–07 |
| slides | **CDS 110** L9-1, slide 15 | diagrama de blocos do anti-windup por back-calculation | §2.2 |
