# Unidade I — Modelagem e análise de sistemas físicos

## Apostila da Unidade I

**Carga: 6 h (semanas 2–4) · Labs 01, 02 e 03 · Lista 1**

Esta é a apostila da Unidade I. Todo o conteúdo
indicado nas caixas 📖 "Onde estudar" da versão original foi desenvolvido **na íntegra aqui
mesmo**: você encontrará as deduções completas, os desenvolvimentos matemáticos passo a
passo, exemplos adicionais resolvidos e tabelas de referência — sem necessidade de consultar
os livros da disciplina.

Os livros de referência sobre os quais esta apostila foi construída são: **Ogata**
(*Engenharia de Controle Moderno*, 5ª ed.), **Nise** (*Engenharia de Sistemas de Controle*),
**Schaum** (DiStefano et al., *Feedback and Control Systems*), **Penedo** (*Sistemas de
Controle: Matemática Aplicada a Projetos*) e **FBS** (Åström & Murray, *Feedback Systems*,
gratuito em <https://fbswiki.org>). As referências às figuras e capítulos originais foram
mantidas ao final de cada seção, para quem desejar conferir o material nas fontes.

---

## 1. O que é modelar um sistema dinâmico

Um **sistema dinâmico** é qualquer sistema cuja saída no instante $t$ depende não só da
entrada em $t$, mas da **história** das entradas — porque o sistema armazena energia (massa
em movimento, capacitor carregado, massa térmica aquecida). Modelar é traduzir a física em
uma **equação diferencial ordinária (EDO)** que relaciona entrada $u(t)$ e saída $y(t)$.

O procedimento é sempre o mesmo:

1. **Escolher entrada e saída** (o que manipulo? o que meço?);
2. **Aplicar a lei física de balanço**: 2ª lei de Newton (mecânica), leis de Kirchhoff
   (elétrica), balanço de energia/massa (térmica/fluídica);
3. **Escrever a EDO** com coeficientes dados pelos parâmetros físicos;
4. Se houver não-linearidades, **linearizar** em torno do ponto de operação (Unidade III
   aprofunda; o Lab 01 §6 mostra o fluxo completo).

Os três sistemas abaixo, de domínios diferentes, produzem EDOs com a **mesma estrutura** —
essa universalidade é o que torna a teoria de controle uma disciplina única:

| Sistema | Lei | EDO | Analogia |
|---|---|---|---|
| Massa–mola–amortecedor | Newton | $m\ddot{x} + b\dot{x} + kx = f$ | massa ↔ indutância ↔ inércia térmica |
| Circuito RLC série | Kirchhoff | $L\ddot{q} + R\dot{q} + q/C = v$ | amortecedor ↔ resistor |
| Tanque com restrição | balanço de massa | $A\dot{h} + h/R_v = q_i$ | mola ↔ capacitor (armazenam "posição") |

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-2-15-nise.png)

**Figura 1.1 — Sistema massa–mola–amortecedor e sua FT.** (Fonte: NISE, Figura 2.15, Cap. 2, §2.5)

---

### 1.1 Modelagem de sistemas mecânicos translacionais

*(Este tópico desenvolve o conteúdo de Ogata, cap. 3, e Nise, cap. 2, §2.5.)*

Os sistemas mecânicos translacionais são descritos por três elementos fundamentais:

| Elemento | Símbolo | Lei constitutiva | Energia armazenada |
|---|---|---|---|
| Massa | $m$ | $f = m\ddot{x}$ (2ª lei de Newton) | cinética: $\frac{1}{2}m\dot{x}^2$ |
| Amortecedor viscoso | $b$ | $f = b(\dot{x}_2 - \dot{x}_1)$ | nenhuma — **dissipa** energia |
| Mola linear | $k$ | $f = k(x_2 - x_1)$ | potencial: $\frac{1}{2}k\Delta x^2$ |

**Procedimento sistemático (método dos diagramas de corpo livre):**

1. Atribua uma coordenada de deslocamento $x_i(t)$ a **cada massa** (ou a cada ponto
   independente de movimento), medida a partir da posição de equilíbrio estático — assim
   a força peso fica automaticamente cancelada pela pré-deformação das molas e não
   precisa aparecer nas equações.
2. Desenhe o **diagrama de corpo livre** de cada massa, supondo todos os deslocamentos e
   velocidades positivos na mesma direção.
3. Aplique a 2ª lei de Newton a cada massa:
   $$m_i\ddot{x}_i = \sum_j f_j.$$
4. Observe que uma mola/amortecedor entre dois pontos transmite força proporcional à
   **diferença** de deslocamento (ou velocidade) entre eles: $k(x_1 - x_2)$,
   $b(\dot{x}_1 - \dot{x}_2)$.
5. **Normalize (forma mônica).** Agrupe por variável e divida a equação pelo coeficiente da
   derivada de maior ordem, deixando-o igual a 1. Essa forma normalizada é a que revela
   diretamente os parâmetros de projeto — a constante de tempo $\tau$ (1ª ordem) ou $\omega_n$ e
   $\zeta$ (2ª ordem), definidos na Seção 4.

> **Agrupar, normalizar (forma mônica) e reconhecer a forma padrão ideal.** Depois de escrever a
> EDO, faça sempre dois movimentos de arrumação:
> 1. **Agrupe por variável** — junte os termos de cada variável ($x_1$ com $x_1$, $x_2$ com
>    $x_2$, …), com todas as derivadas de uma mesma variável lado a lado.
> 2. **Normalize (forma mônica)** — divida tudo pelo coeficiente da derivada de maior ordem, que
>    passa a valer 1.
>
> A forma normalizada casa com as **formas padrão ideais** do curso (Seção 4):
> - **1ª ordem:** a forma ideal é a de *constante de tempo*, $\tau\dot{y} + y = Ku$ (obtida
>   dividindo pelo coeficiente de $y$); a mônica equivalente é
>   $\dot{y} + \tfrac{1}{\tau}y = \tfrac{K}{\tau}u$. Aqui $K$ é o ganho estático e $\tau$ a
>   constante de tempo.
> - **2ª ordem:** a forma ideal **já é mônica**: $\ddot{y} + 2\zeta\omega_n\dot{y} +
>   \omega_n^2 y = \omega_n^2 K\,u$, expondo a frequência natural $\omega_n$ e o coeficiente de
>   amortecimento $\zeta$.
>
> Adquira o hábito de **sempre normalizar**: é a ponte entre a física (massas, molas, $R$, $L$,
> $C$, $A$, $R_v$…) e o vocabulário de desempenho ($\tau$, $\omega_n$, $\zeta$) usado no resto do
> curso.

**Exemplo 1.1 — Sistema de duas massas (adaptado de Ogata, Ex. 3.4; Nise, Ex. 2.17–2.18).**
Duas massas $m_1$ e $m_2$ deslizam sobre superfície sem atrito; $m_1$ está ligada à parede
por mola $k_1$; entre as massas há, em paralelo, mola $k_2$ e amortecedor $b$; a força $f$ atua
em $m_2$ (Figura 1.2).

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/sistema_duas_massas.png)

**Figura 1.2 — Sistema mecânico translacional de duas massas.** Esquema correspondente às
equações desenvolvidas nesta seção. (Adaptado de OGATA, Figura 3.4, Cap. 3, que traz uma versão
com três molas $k_1,k_2,k_3$ e força de entrada $u$; aqui usamos $k_1$, $k_2$, o amortecedor $b$
e a força $f$, sem a terceira mola.)

Massa 1: $m_1\ddot{x}_1 = k_2(x_2 - x_1) + b(\dot{x}_2 - \dot{x}_1) - k_1x_1$.

Massa 2: $m_2\ddot{x}_2 = f - k_2(x_2 - x_1) - b(\dot{x}_2 - \dot{x}_1)$.

Reagrupando (agrupado por variável):

$$m_1\ddot{x}_1 + b\dot{x}_1 + (k_1+k_2)x_1 - b\dot{x}_2 - k_2x_2 = 0,$$
$$m_2\ddot{x}_2 + b\dot{x}_2 + k_2x_2 - b\dot{x}_1 - k_2x_1  = f.$$

Na **forma mônica** (normalizando cada equação pela massa que multiplica a maior derivada —
$m_1$ na primeira, $m_2$ na segunda):

$$\ddot{x}_1 + \frac{b}{m_1}\dot{x}_1 + \frac{k_1+k_2}{m_1}x_1 - \frac{b}{m_1}\dot{x}_2 - \frac{k_2}{m_1}x_2 = 0,$$
$$\ddot{x}_2 + \frac{b}{m_2}\dot{x}_2 + \frac{k_2}{m_2}x_2 - \frac{b}{m_2}\dot{x}_1 - \frac{k_2}{m_2}x_1 = \frac{1}{m_2}f.$$

Com o coeficiente de cada aceleração igual a 1, os agrupamentos $\tfrac{k}{m}$ e $\tfrac{b}{m}$
são exatamente o que reaparece como $\omega_n^2$ e $2\zeta\omega_n$ na Seção 4.

Note a **simetria estrutural**: a força que o elemento intermediário exerce em uma massa é
igual e oposta à que exerce na outra (3ª lei de Newton embutida na modelagem).

---

### 1.2 Modelagem de sistemas elétricos

*(Desenvolve Ogata, cap. 3, §3-3 e §3-5, e Nise, cap. 2, §2.3.)*

Os três elementos passivos e suas leis constitutivas:

| Elemento | Relação $`v`$–$`i`$ | Em termos da carga $q$ ($i = \dot{q}$) |
|---|---|---|
| Resistor $R$ | $v = Ri$ | $v = R\dot{q}$ |
| Indutor $L$ | $v = L\dfrac{di}{dt}$ | $v = L\ddot{q}$ |
| Capacitor $C$ | $i = C\dfrac{dv}{dt}$ | $v = q/C$ |

Duas técnicas de análise equivalentes:

- **Malhas (LK tensão)**: soma das tensões ao longo de cada malha fechada é zero.
  Adequada para circuitos série. Para o RLC série com fonte $v(t)$:
  $$L\ddot{q} + R\dot{q} + \frac{1}{C}q = v(t).$$
- **Nós (LK corrente)**: soma das correntes que saem de cada nó é zero. Adequada para
  circuitos com muitos ramos em paralelo. Escolhendo as tensões de nó $e_1, e_2, \dots$
  como variáveis, cada capacitor entre nós $i$ e $j$ contribui com
  $C(\dot{e}_i - \dot{e}_j)$ etc.

**Exemplo 1.2 — RLC série.** Aplicando LK tensão à malha única:

$$v_L + v_R + v_C = v(t)\;\Rightarrow\; L\frac{di}{dt} + Ri + \frac{1}{C}\int_0^t id\tau = v(t).$$

Com $i = \dot{q}$: $L\ddot{q} + R\dot{q} + q/C = v$. Se a variável de interesse for a
tensão no capacitor $v_C = q/C$, então:

$$LC\ddot{v}_C + RC\dot{v}_C + v_C = v(t).$$

Na **forma mônica** (dividindo por $LC$):

$$\ddot{v}_C + \frac{R}{L}\dot{v}_C + \frac{1}{LC}v_C = \frac{1}{LC}\,v(t),$$

de onde já se leem $\omega_n = 1/\sqrt{LC}$ e $2\zeta\omega_n = R/L$ (Seção 4): o mesmo $RLC$ é,
portanto, um sistema de 2ª ordem cujo amortecimento é ditado por $R$.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-3-7-ogata.png)

**Figura 1.3 — Circuito RLC série: a tensão de entrada é $e_i$ e a saída é a tensão $e_o$
sobre o capacitor.** (Fonte: OGATA, Figura 3.7, Cap. 3)

---

### 1.3 Analogias eletromecânicas: força–tensão e força–corrente

*(Desenvolve Ogata, cap. 3, §3-4 e §3-5.)*

Comparando as EDOs mecânicas e elétricas, obtemos duas analogias clássicas, que permitem
"pensar" um sistema de um domínio usando a intuição do outro:

**Analogia força–tensão (massa–indutor)** — vem de comparar Newton ($m\ddot{x}+b\dot{x}+kx=f$)
com LK tensão do RLC série ($L\ddot{q}+R\dot{q}+q/C=v$):

| Mecânico translacional | Elétrico |
|---|---|
| Força $f$ | Tensão $v$ |
| Velocidade $\dot{x}$ | Corrente $i$ |
| Deslocamento $x$ | Carga $q$ |
| Massa $m$ | Indutância $L$ |
| Atrito viscoso $b$ | Resistência $R$ |
| Rigidez $k$ | Inverso da capacitância $1/C$ |

**Analogia força–corrente (massa–capacitor)** — vem de comparar Newton com LK corrente do
RLC paralelo ($C\ddot{\psi}+\dot{\psi}/R+\psi/L=i$, em termos do fluxo $\psi$):

| Mecânico translacional | Elétrico |
|---|---|
| Força $f$ | Corrente $i$ |
| Velocidade $\dot{x}$ | Tensão $v$ |
| Deslocamento $x$ | Fluxo concatenado $\psi$ |
| Massa $m$ | Capacitância $C$ |
| Atrito viscoso $b$ | Condutância $1/R$ |
| Rigidez $k$ | Inverso da indutância $1/L$ |

> **Como usar na prática:** dado um circuito mecânico, a analogia força–tensão constrói um
> circuito elétrico **em série** (malhas ↔ massas); a analogia força–corrente constrói o
> circuito **dual** (nós ↔ massas). Em ambos os casos, massas mecânicas correspondem a
> elementos que vão para o terra elétrico (referência de velocidade nula).

---

### 1.4 Sistemas de nível de líquido (fluídicos)

*(Desenvolve Ogata, cap. 4, §4-2 — a dedução do tanque usada no curso.)*

Considere um tanque de seção transversal constante $A$ [m²], com vazão de entrada $q_i$
[m³/s], nível $h$ [m] e saída através de uma válvula/restrição.

**Balanço de massa** (fluido incompressível): a taxa de acumulação de volume no tanque é a
diferença entre o que entra e o que sai:

$$A\frac{dh}{dt} = q_i - q_o.$$

**Lei da restrição.** A vazão de saída depende da pressão hidrostática $\rho g h$ no fundo.
Define-se a **resistência hidráulica** $R_v$:

- **Escoamento laminar** (tubos longos e finos): $q_o = \dfrac{\rho g h}{R_l}$ — relação
  **linear** entre vazão e nível. Então a EDO do tanque já é linear:
  $$A\dot{h} + \frac{1}{R_v}h = q_i,\qquad R_v \equiv \frac{R_l}{\rho g}.$$
- **Escoamento turbulento** (válvulas, orifícios): $q_o = K_v\sqrt{h}$ — relação
  **não-linear**.

**Capacitância hidráulica.** O tanque armazena volume; define-se a capacitância
$C_h = A = dV/dh$ [m²], análoga ao capacitor elétrico.

**Linearização da válvula turbulenta.** Se o ponto de operação é $(\bar{q}, \bar{h})$ com
$\bar{q} = K_v\sqrt{\bar{h}}$, expandimos em série de Taylor mantendo só o termo linear:

$$q_o \approx \bar{q} + \underbrace{\left.\frac{dq_o}{dh}\right|_{\bar h}}_{K_v/(2\sqrt{\bar h})}(h-\bar h)
\;\Rightarrow\; \Delta q_o = \frac{1}{R_v}\Delta h,\qquad
R_v = \frac{2\sqrt{\bar h}}{K_v} = \frac{2\bar h}{\bar q}.$$

A resistência hidráulica turbulente **depende do ponto de operação** — quanto maior o nível
de equilíbrio, maior a resistência equivalente. Em variáveis-desvio
($\Delta h = h - \bar h$, $\Delta q_i = q_i - \bar q$), a EDO linearizada é idêntica à do
caso laminar:

$$A\frac{d\Delta h}{dt} + \frac{1}{R_v}\Delta h = \Delta q_i,$$

Normalizando para a **forma padrão ideal de 1ª ordem** (dividindo pelo coeficiente de $\Delta h$,
isto é, por $1/R_v$):

$$\underbrace{AR_v}_{\tau}\,\frac{d\Delta h}{dt} + \Delta h = \underbrace{R_v}_{K}\,\Delta q_i
\qquad(\text{forma }\tau\dot{y} + y = Ku),$$

que, aplicando Laplace (Seção 2), produz a FT de 1ª ordem

$$\frac{\Delta H(s)}{\Delta Q_i(s)} = \frac{R_v}{AR_v s + 1} = \frac{K}{\tau s + 1},
\qquad K = R_v,\ \ \tau = AR_v.$$

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-1-ogata.png)

**Figura 1.4 — (a) Sistema de nível de líquido; (b) curva altura de nível × vazão, com a
tangente no ponto de operação $P$ definindo a resistência linearizada.** (Fonte: OGATA,
Figura 4.1, Cap. 4)

**Interpretação:** o ganho estático é a própria resistência (um aumento permanente de
$\Delta q_i$ na entrada eleva o nível de $R_v\Delta q_i$) e a constante de tempo é o produto
"capacitância × resistência", exatamente como o $RC$ elétrico.

---

### 1.5 Sistemas térmicos

*(Desenvolve Ogata, cap. 4, §4-3 — a dedução do sistema térmico usado no curso.)*

Considere um corpo de massa $M$ e calor específico $c$, a temperatura $\theta$ (uniforme,
modelo concentrado), trocando calor com o ambiente a $\theta_a$ por convecção através de
uma superfície de área $S$ e coeficiente de convecção $h_c$, e recebendo potência térmica
$q_{in}$ [W] de uma resistência elétrica.

**Balanço de energia:** taxa de acumulação = potência entrando − potência saindo:

$$Mc\frac{d\theta}{dt} = q_{in} - h_cS(\theta - \theta_a).$$

Definindo a **resistência térmica** $R_t = 1/(h_cS)$ [K/W] e a **capacitância térmica**
$C_t = Mc$ [J/K], em variáveis-desvio em torno do equilíbrio
($\Delta\theta = \theta - \bar\theta$):

$$C_t\frac{d\Delta\theta}{dt} + \frac{1}{R_t}\Delta\theta = \Delta q_{in}
\;\Rightarrow\;
\underbrace{R_tC_t}_{\tau}\frac{d\Delta\theta}{dt} + \Delta\theta = \underbrace{R_t}_{K}\Delta q_{in}
\;\Rightarrow\;
\frac{\Delta\Theta(s)}{\Delta Q_{in}(s)} = \frac{R_t}{R_tC_t\,s + 1}.$$

De novo uma 1ª ordem com $\tau = R_tC_t$ e $K = R_t$: **o ganho estático de um sistema
térmico é sua resistência térmica** (1 °C de aumento permanente exige $1/R_t$ watts
adicionais). É essa estrutura — 1ª ordem, muitas vezes com tempo morto devido ao transporte
do fluido/sensor — que faz do controle de temperatura o exemplo industrial por excelência
do modelo FOPDT da Seção 6.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-26-ogata.png)

**Figura 1.5 — (a) Sistema térmico (tanque aquecido e misturado); (b) diagrama de blocos
do sistema — repare a 1ª ordem $\frac{1}{RCs}$ dentro da malha.** (Fonte: OGATA,
Figura 4.26, Cap. 4)

**Analogia completa entre domínios:**

| Grandeza | Elétrico | Mecânico transl. | Mecânico rotac. | Hidráulico | Térmico |
|---|---|---|---|---|---|
| Esforço ("tensão") | $v$ | força $f$ | torque $T$ | pressão $p$ | temperatura $\theta$ |
| Fluxo ("corrente") | $i$ | veloc. $\dot{x}$ | veloc. ang. $\omega$ | vazão $q$ | fluxo de calor $\dot q$ |
| Resistência | $R$ | $b$ | $b_r$ | $R_v$ | $R_t$ |
| Capacitância | $C$ | $1/k$ | $1/k_r$ | $A$ ($=C_h$) | $Mc$ |
| Inércia | $L$ | $m$ | $J$ | inertância | — |

---

### 1.6 Exercícios resolvidos da Seção 1

**Exercício resolvido 1 — do sistema físico à EDO.**

*Um carrinho de massa $m = 1$ kg está preso a uma parede por uma mola de rigidez
$k = 5$ N/m e um amortecedor $b = 2$ N·s/m. A entrada é a força $f(t)$ aplicada; a saída é a
posição $x(t)$. Obtenha a EDO e identifique o que cada termo representa fisicamente.*

**Solução.** A 2ª lei de Newton diz que $m\ddot{x}$ = soma das forças. As forças sobre o
carrinho são: a força externa $f$, a força da mola $-kx$ (contrária ao deslocamento — a mola
"puxa de volta") e a do amortecedor $-b\dot{x}$ (contrária à velocidade — atrito viscoso):

$$m\ddot{x} = f - kx - b\dot{x} \quad\Longrightarrow\quad \ddot{x} + 2\dot{x} + 5x = f.$$

Como $m = 1$, a EDO **já está na forma mônica** (coeficiente de $\ddot{x}$ igual a 1): comparando
com a forma padrão de 2ª ordem $\ddot{y} + 2\zeta\omega_n\dot{y} + \omega_n^2 y$, lê-se de
imediato $\omega_n^2 = 5$ e $2\zeta\omega_n = 2$ (o §4 fecha as contas: $\omega_n=\sqrt5$,
$\zeta=1/\sqrt5$).

Cada termo tem leitura física: $\ddot{x}$ é a inércia (resiste a *mudar* de velocidade),
$2\dot{x}$ dissipa energia (o único termo que "gasta"), $5x$ armazena energia potencial e
tende a devolver o carrinho ao repouso. Veremos no §4 que esses três papéis reaparecem em
$\omega_n$ e $\zeta$.

**Exercício adicional 1.A — tanque aquecido.**
*Um tanque perfeitamente misturado, de seção $A = 2$ m², recebe vazão $q_i$ e perde por uma
restrição laminar $R_v = 0{,}5$ s/m². Encontre a FT entre vazão de entrada e nível, e
interprete $K$ e $\tau$ fisicamente.*

**Solução.** Direto das fórmulas do §1.4:
$$K = R_v = 0{,}5\ \text{s/m}^2,\qquad \tau = AR_v = 2 \times 0{,}5 = 1\ \text{s}.$$
$$\boxed{\frac{H(s)}{Q_i(s)} = \frac{0{,}5}{s+1}}$$
Leitura: dobrando permanentemente a vazão em $\Delta q_i$, o nível sobe em regime
$0{,}5\,\Delta q_i$ metros, levando cerca de $4\tau = 4$ s para se acomodar.

**Exercício adicional 1.B — tanque aquecido (térmico).**
*Um corpo é aquecido por uma resistência elétrica que injeta potência $q_{in}$ [W] e troca calor
com o ambiente por convecção. Valores didáticos: capacitância térmica $C_t = Mc = 200$ J/K e
resistência térmica $R_t = 0{,}5$ K/W. A entrada é a potência $q_{in}$ e a saída, a temperatura
$\theta$ (em desvio $\Delta\theta$ do ambiente). Ache a FT $\Delta\Theta(s)/\Delta Q_{in}(s)$ e
interprete $K$ e $\tau$.*

**Solução.** É a mesma 1ª ordem do §1.5, agora com números. Do balanço de energia, já na forma
padrão $\tau\dot{y} + y = Ku$:
$$R_tC_t\,\dot{\Delta\theta} + \Delta\theta = R_t\,\Delta q_{in}
\;\Rightarrow\; K = R_t = 0{,}5\ \text{K/W},\quad \tau = R_tC_t = 0{,}5 \times 200 = 100\ \text{s}.$$
$$\boxed{\frac{\Delta\Theta(s)}{\Delta Q_{in}(s)} = \frac{0{,}5}{100\,s+1}}$$
Leitura: 1 W permanente a mais eleva a temperatura, em regime, $0{,}5$ K, e a acomodação leva
$\approx 4\tau = 400$ s. É a **mesma estrutura** do tanque de nível (1.A) — muda só o significado
físico das grandezas e a escala de tempo (sistemas térmicos são lentos), exatamente a analogia
do §1.3.

> 📖 **Referências originais desta seção (para conferência):** Ogata, cap. 3 (sistemas
> mecânicos e elétricos, analogias força–tensão e força–corrente) e cap. 4 (sistemas
> fluídicos e térmicos). Nise, cap. 2 (modelagem no domínio da frequência, com exemplos
> eletromecânicos) e motor CC no cap. 2. Schaum, cap. 3 (EDOs: resposta livre §3.9 e
> forçada §3.10). Penedo, §1.3 (modelagem de sistemas físicos). FBS, cap. 3 (System
> Modeling) e cap. 4 (exemplos completos).

---

## 2. A transformada de Laplace: por que ela domina a engenharia de controle

*(Desenvolve Schaum, cap. 4; Ogata, cap. 2; Nise, cap. 2; Penedo, §3.3.)*

Resolver EDOs no domínio do tempo é trabalhoso: cada ordem de derivada exige uma integração,
e acoplar sistemas significa eliminar variáveis entre EDOs. A **transformada de Laplace**

$$F(s) = \mathcal{L}\{f(t)\} = \int_0^\infty f(t)\,e^{-st}\,dt,\qquad s = \sigma + j\omega,$$

converte EDOs em **equações algébricas**: derivar no tempo vira multiplicar por $s$.

### 2.1 A propriedade fundamental: derivação

Aplicando integração por partes à definição:

$$\mathcal{L}\{\dot{f}(t)\} = sF(s) - f(0^-),$$
$$\mathcal{L}\{\ddot{f}(t)\} = s^2F(s) - sf(0^-) - \dot{f}(0^-).$$

Com **condições iniciais nulas** (hipótese padrão na definição de função de transferência,
§3):

$$\mathcal{L}\{\dot{y}\} = sY(s), \qquad \mathcal{L}\{\ddot{y}\} = s^2Y(s).$$

As condições iniciais representam energia acumulada; quando modelamos em
**variáveis-desvio** em torno de um ponto de operação (como fizemos no tanque e no sistema
térmico), elas são nulas por construção — é por isso que a teoria de controle trabalha
quase sempre com C.I. nulas.

### 2.2 Tabela de transformadas essenciais

As cinco que você deve memorizar, seguidas da tabela ampliada de uso contínuo:

| $f(t)$ | $F(s)$ | Uso típico |
|---|---|---|
| degrau unitário $1(t)$ | $1/s$ | ensaio de identificação |
| rampa $t$ | $1/s^2$ | erro de seguimento (Unidade II) |
| $e^{-at}$ | $1/(s+a)$ | resposta de 1ª ordem |
| $\sin(\omega t)$ | $\omega/(s^2+\omega^2)$ | resposta em frequência |
| $f(t-\theta)$ | $e^{-\theta s}F(s)$ | **tempo morto** (transporte, sensor) |

Tabela ampliada:

| # | $f(t)$, $t \ge 0$ | $F(s)$ |
|---|---|---|
| 1 | impulso $\delta(t)$ | $1$ |
| 2 | degrau $1(t)$ | $1/s$ |
| 3 | $t^n$ | $n!/s^{n+1}$ |
| 4 | $e^{-at}$ | $1/(s+a)$ |
| 5 | $te^{-at}$ | $1/(s+a)^2$ |
| 6 | $\sin(\omega t)$ | $\omega/(s^2+\omega^2)$ |
| 7 | $\cos(\omega t)$ | $s/(s^2+\omega^2)$ |
| 8 | $e^{-at}\sin(\omega t)$ | $\omega/[(s+a)^2+\omega^2]$ |
| 9 | $e^{-at}\cos(\omega t)$ | $(s+a)/[(s+a)^2+\omega^2]$ |
| 10 | $1 - e^{-t/\tau}$ | $\dfrac{1}{s(\tau s + 1)}$ |
| 11 | $\dfrac{\omega_n}{\sqrt{1-\zeta^2}}e^{-\zeta\omega_n t}\sin(\omega_n\sqrt{1-\zeta^2}\,t)$ | $\dfrac{\omega_n^2}{s(s^2+2\zeta\omega_n s+\omega_n^2)}$ (resposta ao degrau subamortecida, derivada) |

### 2.3 Propriedades operacionais

| Propriedade | Tempo | Frequência |
|---|---|---|
| Linearidade | $af(t) + bg(t)$ | $aF(s) + bG(s)$ |
| Derivação | $\dot{f}$ | $sF(s) - f(0^-)$ |
| Integração | $\int_0^t f\,d\tau$ | $F(s)/s$ |
| Deslocamento no tempo | $f(t-\theta)\,1(t-\theta)$ | $e^{-\theta s}F(s)$ |
| Deslocamento na frequência | $e^{-at}f(t)$ | $F(s+a)$ |
| Escalonamento | $f(t/a)$ | $aF(as)$ |
| Convolução | $f * g$ | $F(s)G(s)$ |
| **Valor inicial** | $\lim_{t\to0^+}f(t)$ | $\lim_{s\to\infty}sF(s)$ |
| **Valor final (TVF)** | $\lim_{t\to\infty}f(t)$ | $\lim_{s\to0}sF(s)$ |

Duas propriedades que usaremos o semestre inteiro:

- **Teorema do valor final (TVF):** $\displaystyle\lim_{t\to\infty} y(t) = \lim_{s\to 0} sY(s)$,
  válido **somente quando o limite existe** — ou seja, quando $sY(s)$ tem todos os polos no
  semiplano esquerdo (sistema estável). É como calculamos erro de regime sem simular.
  **Cuidado clássico:** para $y(t) = \sin(\omega t)$, o TVF indicaria valor final zero,
  o que é falso — os polos estão sobre o eixo imaginário e o teorema não se aplica.
- **Frações parciais:** para voltar ao tempo, decompõe-se $Y(s)$ em termos de tabela.

### 2.4 Frações parciais: os três casos (Schaum §4.7–4.8, na íntegra)

Dada $F(s) = N(s)/D(s)$ própria (grau de $N$ < grau de $D$; se não for, faça a divisão
polinomial primeiro — o quociente gera impulsos e suas derivadas):

**Caso 1 — polos reais e distintos.** $D(s) = (s+p_1)(s+p_2)\cdots(s+p_n)$:

$$F(s) = \sum_{i=1}^n \frac{A_i}{s+p_i},\qquad
A_i = \left.(s+p_i)F(s)\right|_{s=-p_i}.$$

A antitransformada é $f(t) = \sum_i A_i e^{-p_i t}$: cada polo real contribui um modo
exponencial cujo resíduo $A_i$ mede "quanto" daquele modo aparece.

**Caso 2 — polos reais repetidos.** Polo $-p$ com multiplicidade $r$:

$$\frac{A_1}{(s+p)} + \frac{A_2}{(s+p)^2} + \cdots + \frac{A_r}{(s+p)^r},
\qquad
A_k = \frac{1}{(r-k)!}\left.\frac{d^{r-k}}{ds^{r-k}}\Big[(s+p)^rF(s)\Big]\right|_{s=-p},$$

gerando termos $t^{k-1}e^{-pt}$ no tempo.

**Caso 3 — par de polos complexos conjugados** $s = -a \pm j\omega$. Duas rotas:

*(a) Resíduos complexos:* trate como o Caso 1; os resíduos de polos conjugados são
conjugados entre si, e no final os termos se combinam em uma senoide real amortecida.

*(b) Completar quadrados (rota preferida na prática):* reescreva
$(s+a)^2 + \omega^2$ no denominador e force o numerador na forma
$\alpha\,\frac{\omega}{(s+a)^2+\omega^2} + \beta\,\frac{s+a}{(s+a)^2+\omega^2}$,
que antitransforma para $e^{-at}[\alpha\sin(\omega t) + \beta\cos(\omega t)]$.

**Exemplo do Caso 3 (passo a passo).** Antitransformar
$F(s) = \dfrac{2s+3}{s^2+2s+5}$.

Completando quadrados: $s^2+2s+5 = (s+1)^2 + 4$, logo $a = 1$, $\omega = 2$. Forçamos o
numerador:

$$2s + 3 = 2(s+1) + 1 = 2(s+1) + \frac{1}{2}\cdot 2.$$

$$F(s) = 2\,\frac{s+1}{(s+1)^2+2^2} + \frac{1}{2}\,\frac{2}{(s+1)^2+2^2}
\;\Rightarrow\;
f(t) = e^{-t}\left[2\cos(2t) + \frac{1}{2}\sin(2t)\right].$$

### 2.5 O fluxo completo: EDO → Laplace → tempo

O roteiro que você usará nos Labs 01 e 02:

1. Escreva a EDO (Seção 1);
2. Aplique Laplace nos dois lados (C.I. nulas);
3. Resolva algebricamente para $Y(s)$;
4. Decomponha em frações parciais;
5. Antitransforme termo a termo pela tabela;
6. Verifique com o TVF (regime) e o teorema do valor inicial ($t = 0$).

### Exercício resolvido 2 — resposta ao degrau via Laplace

*A planta de referência do curso (o motor CC do kit, como veremos) é
$G(s) = \dfrac{5}{2s+1}$. Calcule $y(t)$ para degrau unitário na entrada, o valor final, e
o valor em $t = 2$ s.*

**Solução.** $Y(s) = G(s)\cdot\dfrac{1}{s} = \dfrac{5}{s(2s+1)}$. Frações parciais (Caso 1):

$$\frac{5}{s(2s+1)} = \frac{A}{s} + \frac{B}{2s+1};\quad A = \left.\frac{5}{2s+1}\right|_{s=0} = 5,\quad
B = \left.\frac{5}{s}\right|_{s=-1/2} = -10.$$

Logo $Y(s) = \dfrac{5}{s} - \dfrac{10}{2s+1} = \dfrac{5}{s} - \dfrac{5}{s+1/2}$ e, pela tabela,

$$\boxed{y(t) = 5\left(1 - e^{-t/2}\right)}.$$

Valor final pelo TVF: $\lim_{s\to0} s\,Y(s) = 5$ ✓ (coincide com $t\to\infty$ na expressão).
Em $t = 2$ s (uma constante de tempo, pois $\tau = 2$): $y = 5(1-e^{-1}) = 3{,}16$ —
**63,2 % do valor final**, o número mágico da identificação (§6).

**Exercício adicional 2.A — resposta ao impulso e rampa.**
*Para o mesmo sistema, obtenha (a) a resposta ao impulso unitário; (b) o valor final do
erro de seguimento à rampa unitária se a planta estiver em malha aberta.*

**Solução.** (a) Impulso: $Y(s) = G(s)\cdot 1 = \frac{5}{2s+1} = \frac{2{,}5}{s+0{,}5}$,
logo $y(t) = 2{,}5\,e^{-t/2}$ — note que a resposta ao impulso é a **derivada** da resposta
ao degrau (pois impulso é a derivada do degrau e o sistema é LTI).

(b) Rampa: $Y(s) = \frac{5}{s^2(2s+1)}$, então $y(t) = 5(t - 2 + 2e^{-t/2})$. A saída segue
a rampa com **atraso permanente** de $5\times 2 = 10$ unidades: sistemas de 1ª ordem puro
**não seguem rampa** em malha aberta — motivador do controle integral (Unidade II).

> 📖 **Referências originais desta seção (para conferência):** Schaum, cap. 4 (tabelas,
> §4.7–4.8 frações parciais com exemplos resolvidos). Ogata, cap. 2 (transformada e solução
> de EDOs). Nise, cap. 2 (revisão de Laplace no início). Penedo, §3.3 (passo a passo em
> português).

---

## 3. Função de transferência, polos e zeros

*(Desenvolve Nise, caps. 2 e 5; Ogata, cap. 2; Schaum, caps. 6 e 7; Penedo, §3.4–3.5;
FBS, cap. 9.)*

Aplicando Laplace à EDO com condições iniciais nulas, a razão saída/entrada vira uma função
racional de $s$ — a **função de transferência (FT)**:

$$m\ddot{x} + b\dot{x} + kx = f \;\xrightarrow{\ \mathcal{L}\ }\; G(s) = \frac{X(s)}{F(s)} = \frac{1}{ms^2 + bs + k}.$$

A FT é o "DNA" do sistema: contém tudo sobre seu comportamento entrada–saída. Quatro
propriedades fundamentais (Nise, cap. 2):

1. A FT é definida apenas para **sistemas lineares e invariantes no tempo (LTI)**;
2. A FT é **independente da entrada** — é uma propriedade do sistema;
3. Pressupõe **condições iniciais nulas** (variáveis-desvio);
4. A resposta a **qualquer** entrada é $Y(s) = G(s)U(s)$: convolução no tempo vira
   produto em $s$.

### 3.1 Polos e zeros

Escrevendo a FT em forma fatorada:

$$G(s) = K_g\,\frac{(s+z_1)(s+z_2)\cdots(s+z_m)}{(s+p_1)(s+p_2)\cdots(s+p_n)}.$$

- **Polos** = raízes do denominador. Cada polo $p$ contribui com um modo $e^{pt}$ na
  resposta: polo real negativo → exponencial que decai; par complexo
  $-\sigma \pm j\omega_d$ → oscilação amortecida $e^{-\sigma t}\sin(\omega_d t)$;
  **qualquer polo com parte real positiva → resposta cresce sem limite (instável)**.
  Por isso "estabilidade = todos os polos no semiplano esquerdo" (estabilidade BIBO).
  Polos sobre o eixo imaginário (oscilação pura) são o caso limite: *marginalmente
  estável*.
- **Zeros** = raízes do numerador. Não criam modos, mas moldam *quanto* de cada modo
  aparece (alteram os resíduos das frações parciais); um zero em $j\omega_0$ bloqueia
  completamente senoides naquela frequência (pois $G(j\omega_0) = 0$). Zeros no semiplano
  direito (**sistemas de fase não mínima**) produzem a resposta que "primeiro vai para o
  lado errado" — típica de caldeiras e aviões.
- **Ganho estático** $= G(0)$: valor final da resposta ao degrau unitário (pelo TVF).

**Exemplo 3.1 — efeito de um zero (Nise, cap. 4).** Compare
$$G_1(s) = \frac{1}{(s+1)(s+2)},\qquad G_2(s) = \frac{(s+3)}{(s+1)(s+2)}.$$
Ambas têm os mesmos polos $-1, -2$, logo os mesmos modos $e^{-t}, e^{-2t}$. Mas os
resíduos mudam: para degrau unitário,
$$Y_1(s) = \frac{1/2}{s} - \frac{1}{s+1} + \frac{1/2}{s+2},\qquad
Y_2(s) = \frac{3/2}{s} - \frac{2}{s+1} + \frac{1/2}{s+2}.$$
O modo rápido ganhou o mesmo peso, o modo lento dobrou de peso — a resposta de $G_2$ é
visivelmente mais rápida no início. **O zero não muda os modos; muda a mixagem deles.**

### 3.2 Estabilidade e a localização dos polos (Penedo, §3.5)

Resumo visual do plano $s$:

| Localização do polo | Modo temporal | Classificação |
|---|---|---|
| Real, semiplano esquerdo ($p < 0$) | $e^{-|p|t}$ decai | estável |
| Complexos conjugados, SPE | oscilação amortecida | estável |
| Sobre o eixo imaginário | oscilação permanente / valor constante | marginal |
| Qualquer um no semiplano direito | cresce sem limite | **instável** |

### 3.3 Diagramas de blocos: as regras de redução (Nise, cap. 5, na íntegra)

Diagramas de blocos representam graficamente o fluxo de sinais: cada bloco é uma FT, cada
linha é um sinal, cada somador combina sinais ($\pm$) e cada ponto de derivação (*pickoff*)
copia um sinal sem atenuá-lo.

**Regra 1 — Cascata (série).** Blocos em série multiplicam:
$$G_{eq} = G_1G_2\cdots G_n \qquad\text{(vale a ordem; para SISO a ordem não altera o produto)}.$$

**Regra 2 — Paralelo.** Blocos alimentados pelo mesmo sinal e somados na saída somam:
$$G_{eq} = G_1 \pm G_2.$$

**Regra 3 — Malha fechada (realimentação).** A fórmula mais importante do curso:
$$T(s) = \frac{G(s)}{1 + G(s)H(s)}\quad(\text{malha fechada com realimentação } H),$$
com sinal **$+$ no denominador para realimentação negativa** e $-$ para positiva. A
Unidade II vive dentro dessa fórmula. Caso particular frequente: realimentação unitária
($H = 1$) dá $T = G/(1+G)$.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-5-6-nise.png)

**Figura 1.6 — (a) Sistema de controle com realimentação típico; (b) modelo simplificado;
(c) função de transferência equivalente de malha fechada.** (Fonte: NISE, Figura 5.6,
Cap. 5)

**Regra 4 — Deslocamento de somadores.** Um somador pode "atravessar" um bloco $G$ desde
que se compense:
- Mover o somador para **depois** do bloco: o ramo movido passa a ter $G$ em série.
- Mover o somador para **antes** do bloco: o ramo movido passa a ter $1/G$ em série.

**Regra 5 — Deslocamento de pontos de derivação.**
- Mover o ponto de derivação para **depois** do bloco: o ramo derivado ganha $1/G$.
- Mover o ponto de derivação para **antes** do bloco: o ramo derivado ganha $G$.

As Figuras 1.7 e 1.8 mostram graficamente as equivalências das Regras 4 e 5 — verifique
cada uma seguindo os sinais da entrada até a saída nos dois lados do sinal "$\equiv$":

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-5-7-nise.png)

**Figura 1.7 — Álgebra de diagramas de blocos para junções de soma: formas equivalentes
para mover um bloco (a) para a esquerda e (b) para a direita, passando uma junção de
soma.** (Fonte: NISE, Figura 5.7, Cap. 5)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-5-8-nise.png)

**Figura 1.8 — Álgebra de diagramas de blocos para pontos de ramificação: formas
equivalentes para mover um bloco (a) para a esquerda e (b) para a direita, passando um
ponto de derivação.** (Fonte: NISE, Figura 5.8, Cap. 5)

A estratégia geral de redução (Schaum, cap. 7): (i) reduza as malhas mais internas com a
Regra 3; (ii) mova somadores/derivações para "destravar" malhas aninhadas; (iii) repita
até restar um único bloco.

**Exemplo 3.2 — malha com perturbação.** Um sistema clássico: referência $R(s)$ entra no
somador, segue o controlador $C(s)$, depois uma perturbação $D(s)$ é somada antes da planta
$P(s)$, e a saída $Y(s)$ realimenta negativamente. Superposição (sistema linear):

- Com $D = 0$: $\dfrac{Y}{R} = \dfrac{C P}{1 + CP}$.
- Com $R = 0$: $\dfrac{Y}{D} = \dfrac{P}{1 + CP}$.

Logo $Y = \dfrac{CP}{1+CP}R + \dfrac{P}{1+CP}D$. **Lição central:** o mesmo fator
$1 + CP$ (a "função sensibilidade") aparece nos dois denominadores — fechar a malha com
ganho alto atenua o efeito de perturbações na saída, exatamente o motivo de existir
controle realimentado.

**Exemplo 3.3 — redução completa (Schaum, cap. 7).**
Reduza $Y/R$ do sistema com $G_1$ no caminho direto, $G_2$ em cascata, realimentação interna
$H_1$ em torno de $G_2$ apenas, e realimentação externa unitária.

1. Malha interna: $G_2' = \dfrac{G_2}{1 + G_2H_1}$.
2. Cascata: $G = G_1G_2'$.
3. Malha externa ($H = 1$): $\boxed{\dfrac{Y}{R} = \dfrac{G_1G_2}{1 + G_2H_1 + G_1G_2}}$.

> 📖 **Referências originais desta seção (para conferência):** Nise, cap. 2 (FT a partir da
> física) e cap. 5 (redução de diagramas de blocos, regra por regra). Ogata, cap. 2 (FT e
> álgebra de blocos). Schaum, cap. 6 (propriedades da FT, §6.4 resposta temporal) e cap. 7
> (diagramas de blocos — dezenas de exercícios resolvidos). Penedo, §3.4 (polos e zeros) e
> §3.5 (estabilidade). FBS, cap. 9 (Transfer Functions).

---

## 4. Sistemas de 1ª e 2ª ordem: o vocabulário do curso

*(Desenvolve Nise, cap. 4; Ogata, cap. 5, primeira metade; Schaum, §4.13; Penedo, cap. 4;
FBS, cap. 6.)*

Sistemas reais podem ter dezenas de polos, mas uma fração enorme da prática de controle se
entende (e se projeta) com apenas dois modelos: a 1ª e a 2ª ordem. Eles são o "vocabulário"
do engenheiro de controle: especificações como sobressinal, tempo de subida e tempo de
acomodação são todas definidas sobre essas duas respostas canônicas.

### 4.1 Primeira ordem

$$G(s) = \frac{K}{\tau s + 1}\qquad\Longrightarrow\qquad y_{degrau}(t) = K\left(1 - e^{-t/\tau}\right)$$

**Dedução completa.** Para degrau unitário, $Y(s) = \dfrac{K}{s(\tau s+1)}$. Frações
parciais: $\dfrac{K}{s(\tau s + 1)} = \dfrac{K}{s} - \dfrac{K\tau}{\tau s + 1} =
\dfrac{K}{s} - \dfrac{K}{s + 1/\tau}$. Antitransformando termo a termo:

$$y(t) = K - Ke^{-t/\tau} = K\left(1 - e^{-t/\tau}\right).\qquad\blacksquare$$

Só dois parâmetros, com significado direto:

- $K$ (**ganho estático**): quanto a saída vale em regime por unidade de entrada;
- $\tau$ (**constante de tempo**): em $t = \tau$ a resposta atingiu $1 - e^{-1} = $
  **63,2 %**; em $t = 2\tau$, 86,5 %; em $t = 3\tau$, 95 %; em $4\tau$, 98 %
  (**tempo de acomodação a 2 %**: $t_s \approx 4\tau$).

**A tangente na origem** (truque gráfico útil na bancada): derivando em $t = 0$,
$\dot y(0) = K/\tau$ — ou seja, se a resposta continuasse com sua inclinação inicial,
atingiria o valor final exatamente em $t = \tau$. Na bancada, trace a tangente no início
da curva registrada e leia onde ela cruza o valor final: ali está $\tau$, sem conta alguma.

**Resposta ao impulso** (FT da entrada = 1): $y(t) = \dfrac{K}{\tau}e^{-t/\tau}$ — salta
para $K/\tau$ e decai; é a derivada da resposta ao degrau.

**Resposta à rampa:** $y(t) = K\left(t - \tau + \tau e^{-t/\tau}\right)$ — em regime a
saída segue a rampa com **atraso constante de $K\tau$**: erro permanente de seguimento,
que motivará o controle integral na Unidade II.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-5-1-ogata.png)

**Figura 1.9 — Diagramas de blocos do sistema de 1ª ordem. (a) Diagrama de blocos de um
sistema de primeira ordem; (b) diagrama de blocos simplificado.** (Fonte: OGATA, Figura 5.1,
Cap. 5, p. 147)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-5-2-ogata.png)

**Figura 1.10 — Curva de resposta exponencial ao degrau, com a tangente inicial e as marcas
em T, 2T, 3T, 4T.** (Fonte: OGATA, Figura 5.2, Cap. 5, p. 147)

> **Nota — de onde vem a forma $1/(\tau s + 1)$?** Um integrador puro realimentado
> unitariamente: $\dfrac{1/s}{1 + 1/s}\cdot\frac{1}{\tau}$… Mais diretamente: qualquer
> sistema com um único acumulador de energia (um capacitor, um tanque, uma massa térmica,
> um motor CC sem indutância) e um único dissipador gera exatamente essa FT, com
> $\tau$ = "capacitância × resistência" do domínio correspondente (§1.4–1.5).

### 4.2 Segunda ordem padrão

$$G(s) = \frac{K\,\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

- $\omega_n$ (**frequência natural não amortecida**): a "velocidade" do sistema — a
  frequência com que ele oscilaria se não houvesse dissipação;
- $\zeta$ (**fator de amortecimento**): a "forma" da resposta.

**Os cinco regimes de amortecimento** (pelas raízes de $s^2 + 2\zeta\omega_n s + \omega_n^2$):

| Caso | Polos | Resposta ao degrau |
|---|---|---|
| $\zeta > 1$: superamortecido | dois polos reais distintos $-\zeta\omega_n \pm \omega_n\sqrt{\zeta^2-1}$ | subida lenta, sem oscilação |
| $\zeta = 1$: criticamente amortecido | polo real duplo em $-\omega_n$ | subida mais rápida possível sem sobressinal |
| $0 < \zeta < 1$: **subamortecido** | $s = -\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2}$ | oscilação amortecida com sobressinal |
| $\zeta = 0$: não amortecido | $\pm j\omega_n$ | oscilação permanente |
| $\zeta < 0$ | polos no semiplano direito | oscilação crescente — **instável** |

A Figura 1.11 mostra a família de respostas subamortecidas com o eixo do tempo normalizado
por $\omega_n$: repare que $\zeta$ controla **a forma** (quanto oscila) enquanto $\omega_n$
apenas **estica ou comprime o tempo** — a mesma curva serve para qualquer $\omega_n$.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-13-nise.png)

**Figura 1.11 — Respostas de segunda ordem subamortecidas para diferentes valores do fator
de amortecimento $\zeta$ (eixo do tempo normalizado, $\omega_n t$).** (Fonte: NISE,
Figura 4.13, Cap. 4)

### 4.3 Dedução completa da resposta subamortecida (Nise, cap. 4)

Para $0 < \zeta < 1$ e degrau unitário (tomamos $K = 1$ sem perda de generalidade):

$$Y(s) = \frac{\omega_n^2}{s(s^2 + 2\zeta\omega_n s + \omega_n^2)}.$$

Completando quadrados no denominador quadrático (Caso 3 do §2.4):
$s^2 + 2\zeta\omega_n s + \omega_n^2 = (s+\zeta\omega_n)^2 + \omega_n^2(1-\zeta^2)$.
Definindo a **frequência natural amortecida** $\omega_d = \omega_n\sqrt{1-\zeta^2}$ e
$\sigma = \zeta\omega_n$, a decomposição em frações parciais dá:

$$Y(s) = \frac{1}{s} - \frac{s + 2\zeta\omega_n}{(s+\sigma)^2 + \omega_d^2}
= \frac{1}{s} - \frac{s+\sigma}{(s+\sigma)^2+\omega_d^2} - \frac{\zeta}{\sqrt{1-\zeta^2}}\,\frac{\omega_d}{(s+\sigma)^2+\omega_d^2}.$$

Antitransformando pelos itens 8–9 da tabela:

$$y(t) = 1 - e^{-\zeta\omega_n t}\left[\cos(\omega_d t) + \frac{\zeta}{\sqrt{1-\zeta^2}}\sin(\omega_d t)\right],$$

ou, na forma de senoide única com ângulo de fase $\phi = \arccos\zeta$:

$$\boxed{\;y(t) = 1 - \frac{e^{-\zeta\omega_n t}}{\sqrt{1-\zeta^2}}\,
\sin\!\Big(\omega_d t + \arccos\zeta\Big)\;}$$

A resposta é uma oscilação de frequência $\omega_d$ envolvida pelo **envelope exponencial**
$e^{-\zeta\omega_n t}$: a parte real do polo manda no decaimento; a parte imaginária manda
na frequência das oscilações.

### 4.4 Dedução das especificações de desempenho ($M_p$, $t_p$, $t_s$, $t_r$)

**Tempo de pico $t_p$** — instante do primeiro (e maior) máximo. Derivando $y(t)$ e
igualando a zero, os fatores trigonométricos se cancelam e resta
$\sin(\omega_d t) = 0$, cuja primeira raiz positiva é $\omega_d t = \pi$:

$$t_p = \frac{\pi}{\omega_d} = \frac{\pi}{\omega_n\sqrt{1-\zeta^2}}.$$

**Sobressinal percentual $M_p$** — avaliando $y(t_p)$: o seno em $\omega_d t_p + \arccos\zeta
= \pi + \arccos\zeta$ vale $-\sin(\arccos\zeta) = -\sqrt{1-\zeta^2}$, logo

$$y(t_p) = 1 + e^{-\zeta\omega_n t_p}\;\Rightarrow\;
\boxed{\;M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}\times 100\,\%\;}$$

e sua inversa (usada em projeto — "dado o $M_p$ desejado, qual $\zeta$?"):

$$\zeta = \frac{|\ln(M_p/100)|}{\sqrt{\pi^2 + \ln^2(M_p/100)}}.$$

A curva $M_p \times \zeta$ (Figura 1.12) é uma das mais consultadas do curso: lendo na
horizontal o sobressinal desejado, obtém-se verticalmente o $\zeta$ necessário — e vice-versa.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-15-nise.png)

**Figura 1.12 — Ultrapassagem (sobressinal) percentual em função do fator de
amortecimento.** (Fonte: NISE, Figura 4.15, Cap. 4)

**Tempo de acomodação $t_s$** — instante a partir do qual a resposta permanece dentro de
$\pm 2\%$ do valor final. Como a amplitude do termo oscilatório é limitada pelo envelope
$e^{-\zeta\omega_n t}/\sqrt{1-\zeta^2}$, impomos que o envelope caia a 2 %
($\approx$ 4 constantes de tempo do envelope; a aproximação clássica usa o envelope
simples $e^{-\zeta\omega_n t}$):

$$t_s(2\%) \approx \frac{4}{\zeta\omega_n} = \frac{4}{\sigma},\qquad
t_s(5\%) \approx \frac{3}{\zeta\omega_n}.$$

**Tempo de subida $t_r$** (10 % → 90 % do valor final) — não tem fórmula fechada exata;
aproximações úteis (Nise, cap. 4):

$$t_r \approx \frac{1{,}8}{\omega_n}\quad(\zeta \approx 0{,}5\ \text{a}\ 0{,}8),
\qquad\text{ou}\qquad t_r \approx \frac{2{,}16\zeta + 0{,}60}{\omega_n}\quad(0{,}3\le\zeta\le 0{,}8).$$

**Síntese das fórmulas de desempenho** (usadas até o fim do curso):

$$M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \times 100\,\%,\qquad
t_p = \frac{\pi}{\omega_n\sqrt{1-\zeta^2}},\qquad
t_s(2\%) \approx \frac{4}{\zeta\omega_n}.$$

**Valores de referência para memorizar:** $\zeta = 0{,}7 \Rightarrow M_p \approx 4{,}3\%$;
$\zeta = 0{,}5 \Rightarrow M_p \approx 16\%$; $\zeta = 0{,}3 \Rightarrow M_p \approx 37\%$.

### 4.5 A geometria do plano $s$ (leitura fundamental para a Unidade II)

Para o par de polos $s = -\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2}$:

- **Distância à origem** $= \sqrt{(\zeta\omega_n)^2 + \omega_n^2(1-\zeta^2)} = \omega_n$:
  todos os polos com a mesma $\omega_n$ estão sobre um mesmo **círculo**;
- **Ângulo com o eixo real negativo** $\theta$: $\cos\theta = \dfrac{\zeta\omega_n}{\omega_n}
  = \zeta$: polos sobre uma mesma **reta** a partir da origem têm o mesmo $\zeta$ — e
  portanto o mesmo $M_p$;
- **Parte real** $\sigma = \zeta\omega_n$ manda no tempo de acomodação
  ($t_s = 4/\sigma$): polos sobre uma mesma **reta vertical** acomodam igual;
- **Parte imaginária** $\omega_d$ manda na frequência das oscilações e no $t_p$.

**Tradução de especificações em regiões do plano $s$** (a base do lugar das raízes,
Unidade II): exigir $M_p \le M_0$ limita os polos a um cone ($\theta \le \arccos\zeta_0$);
exigir $t_s \le T$ empurra os polos para a esquerda de $\sigma = 4/T$; exigir $t_p \le T_p$
exige $\omega_d \ge \pi/T_p$. Projetar um controlador é, literalmente, mover os polos de
malha fechada para dentro da região permitida.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-17-nise.png)

**Figura 1.13 — Diagrama de polos de um sistema de segunda ordem subamortecido: a
distância radial é $\omega_n$, $\cos\theta = \zeta$, a parte real $-\zeta\omega_n = -\sigma_d$
manda no tempo de acomodação e a parte imaginária $\pm j\omega_d$ manda no tempo de
pico.** (Fonte: NISE, Figura 4.17, Cap. 4)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-5-2-ogata.png)

**Figura 1.14 — Especificações de resposta transitória ($t_d, t_r, t_p, M_p, t_s$) sobre a
curva ao degrau.** (Fonte: OGATA, Figura 5.2, Cap. 5, p. 154)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-5-22-ogata.png)

**Figura 1.15 — Família de respostas ao degrau unitário para $\zeta = 0; 0{,}2; \dots; 1$
($\omega_n = 1$).** (Fonte: OGATA, Figura 5.22, Cap. 5, p. 174)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-10-nise.png)

**Figura 1.16 — Respostas ao degrau superpostas dos quatro casos de amortecimento.** (Fonte:
NISE, Figura 4.10, Cap. 4)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-14-nise.png)

**Figura 1.17 — Especificações da resposta subamortecida de 2ª ordem ($T_r, T_p, \%UP,
T_s$).** (Fonte: NISE, Figura 4.14, Cap. 4)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-1-penedo.png)

**Figura 1.18 — Especificações de desempenho caracterizadas graficamente.** (Fonte: PENEDO,
Figura 4.1, Cap. 4)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-4-4-penedo.png)

**Figura 1.19 — Localização dos polos complexos conjugados de 2ª ordem no plano complexo.**
(Fonte: PENEDO, Figura 4.4, Cap. 4)

### 4.6 Aproximação de sistemas de ordem superior (Nise, §4.7–4.8)

Sistemas reais têm mais de dois polos, mas muitas vezes se comportam como 2ª ordem. Duas
ferramentas de análise:

- **Polos dominantes:** polos com parte real 5× (ou mais) menor em módulo que os demais
  decaem 5× mais devagar e dominam a resposta — os rápidos "morrem" antes. As fórmulas de
  2ª ordem podem então ser aplicadas aos polos dominantes.
- **Cancelamento aproximado polo–zero:** um zero muito próximo de um polo quase anula o
  resíduo daquele modo, removendo-o da resposta — por isso nem todo polo aparece de fato
  na saída.

### Exercício resolvido 3 — caracterizando um sistema de 2ª ordem

*Para o carrinho do Exercício 1 ($\ddot{x} + 2\dot{x} + 5x = f$): calcule $\omega_n$, $\zeta$,
o ganho estático, classifique o amortecimento e estime $M_p$ e $t_s$ ao degrau.*

**Solução.** Comparando $s^2 + 2s + 5$ com $s^2 + 2\zeta\omega_n s + \omega_n^2$:
$$\omega_n = \sqrt{5} = 2{,}24\ \text{rad/s};\qquad 2\zeta\omega_n = 2 \Rightarrow \zeta = \frac{1}{\sqrt{5}} = 0{,}447.$$
Ganho estático: $G(0) = 1/5 = 0{,}2$ m/N. Como $0 < \zeta < 1$: **subamortecido**.
$$M_p = e^{-\pi(0{,}447)/\sqrt{1-0{,}2}} = e^{-1{,}571} \approx 20{,}8\,\%;\qquad
t_s \approx \frac{4}{\zeta\omega_n} = \frac{4}{1} = 4\ \text{s}.$$
Os polos estão em $s = -1 \pm 2j$: parte real $-1$ ⟹ envelope $e^{-t}$ ⟹ acomoda em ~4 s ✓.

**Exercício adicional 4.A — projeto por especificação (prévia da Unidade II).**
*Deseja-se resposta ao degrau com $M_p \le 10\%$ e $t_s \le 1$ s. Em que região do plano $s$
devem estar os polos dominantes?*

**Solução.** Pela inversa do sobressinal:
$\zeta \ge \dfrac{|\ln 0{,}1|}{\sqrt{\pi^2 + \ln^2 0{,}1}} = \dfrac{2{,}303}{\sqrt{9{,}87 + 5{,}30}} = 0{,}59$
⟹ ângulo máximo $\theta = \arccos 0{,}59 = 53{,}8°$ com o eixo real negativo.
Por $t_s$: $\sigma = \zeta\omega_n \ge 4/1 = 4$ rad/s.
**Região:** semiplano esquerdo, à esquerda da reta vertical $\mathrm{Re}(s) = -4$ e dentro
do cone de $53{,}8°$.

> 📖 **Referências originais desta seção (para conferência):** Nise, cap. 4 (dedução de
> $M_p$, $t_p$, $t_s$, com a geometria do plano $s$). Ogata, cap. 5, primeira metade
> (resposta transitória). Schaum, §4.13. Penedo, cap. 4 (§4.2 especificações; §4.3–4.4
> primeira e segunda ordens). FBS, cap. 6 (Linear Systems).

---

## 5. Espaço de estados: a representação que o computador prefere

*(Desenvolve Nise, cap. 3; Ogata, cap. 2 (seção de espaço de estados) e cap. 3 (motor CC);
Penedo, caps. 2 e 10; FBS, caps. 3 e 6.)*

A FT descreve a relação entrada–saída de um sistema SISO linear. A **representação em
espaço de estados** faz o mesmo — e mais: lida naturalmente com múltiplas entradas e saídas
(MIMO), com condições iniciais e com não-linearidades, e é a forma que todo simulador
numérico usa internamente.

### 5.1 Definições (Nise, cap. 3)

- **Variáveis de estado:** o conjunto **mínimo** de variáveis $x_1, \dots, x_n$ tal que,
  conhecendo seus valores em $t_0$ e a entrada $u(t)$ para $t \ge t_0$, todo o futuro do
  sistema fica determinado. A escolha não é única, mas o número $n$ (a **ordem** do
  sistema) é.
- **Vetor de estado:** $x = [x_1\ \cdots\ x_n]^T$ — resume a **história** do sistema:
  posições e velocidades; cargas e correntes; níveis e temperaturas.
- **Equações de estado e de saída:**

$$\dot{x} = Ax + Bu,\qquad y = Cx + Du,$$

com $A$ ($n\times n$, dinâmica), $B$ ($n\times 1$, entrada), $C$ ($1\times n$, saída) e
$D$ (transmissão direta, quase sempre 0 em sistemas físicos estritamente próprios).

**Quantas variáveis de estado?** Tantas quantos forem os **armazenadores independentes de
energia**: cada massa com velocidade própria (1), cada mola (1), cada capacitor (1), cada
indutor (1), cada tanque (1), cada corpo térmico (1). Cuidado com os casos dependentes:
dois capacitores em paralelo contam como um só.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-3-5-nise.png)

**Figura 1.20 — Circuito elétrico para representação em espaço de estados: dois
armazenadores independentes ($L$ e $C$) ⟹ duas variáveis de estado, $i_L$ e $v_C$ —
as grandezas que aparecem derivadas nas leis constitutivas.** (Fonte: NISE, Figura 3.5,
Cap. 3)

### 5.2 Da EDO ao espaço de estados

Para o carrinho $\ddot{x} + \frac{b}{m}\dot{x} + \frac{k}{m}x = \frac{f}{m}$, a escolha
canônica é a **variável de fase**: $x_1 = x$ (posição), $x_2 = \dot{x}$ (velocidade).
Então $\dot{x}_1 = x_2$ (definição) e, pela EDO,
$\dot{x}_2 = -\frac{k}{m}x_1 - \frac{b}{m}x_2 + \frac{1}{m}f$. Em matrizes:

$$A = \begin{bmatrix}0 & 1\\ -k/m & -b/m\end{bmatrix},\quad
B = \begin{bmatrix}0\\ 1/m\end{bmatrix},\quad C = [1\ \ 0],\quad D = 0.$$

Note o padrão: a primeira linha de $A$ é $[0\ \ 1]$ (cadeia de integradores), e a última
linha traz os coeficientes da EDO com sinais trocados — essa é a **forma companheira**,
que generaliza para qualquer ordem. A Figura 1.21 mostra a mesma ideia em diagrama de
blocos para o sistema massa–amortecedor $M\dot v + Dv = f$: cada variável de estado é a
**saída de um integrador**.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-3-4-nise.png)

**Figura 1.21 — Diagrama de blocos de uma massa e amortecedor: o segundo bloco integra a
velocidade para produzir o deslocamento — incluir a posição como variável adicional
aumenta a ordem do sistema de 1 para 2.** (Fonte: NISE, Figura 3.4, Cap. 3)

### 5.3 Do espaço de estados à FT

Aplicando Laplace a $\dot{x} = Ax + Bu$ com C.I. nulas:
$sX(s) = AX(s) + BU(s) \Rightarrow (sI - A)X(s) = BU(s) \Rightarrow X(s) = (sI-A)^{-1}BU(s)$.
Substituindo em $Y(s) = CX(s) + DU(s)$:

$$\boxed{\;G(s) = C(sI-A)^{-1}B + D\;}$$

Como $(sI-A)^{-1} = \mathrm{adj}(sI-A)/\det(sI-A)$, o denominador de $G(s)$ é
$\det(sI - A)$ — o **polinômio característico de $A$**. Conclusão fundamental:

$$\textbf{Os polos da FT são os autovalores de } A.$$

Isso fecha o círculo: estabilidade ↔ autovalores no semiplano esquerdo; modos $e^{\lambda t}$
↔ autovalores $\lambda$; $\omega_n, \zeta$ ↔ geometria do par de autovalores.

**Exemplo 5.1 — do carrinho à FT.** Com $m=1$, $b=2$, $k=5$:
$\det(sI - A) = \det\begin{bmatrix}s & -1\\ 5 & s+2\end{bmatrix} = s^2 + 2s + 5$,
e $C(sI-A)^{-1}B = \dfrac{1}{s^2+2s+5}$ — exatamente a FT do §3. ✓

### 5.4 Solução no tempo e a matriz de transição (FBS, cap. 6)

A solução da equação de estado é

$$x(t) = e^{At}x(0) + \int_0^t e^{A(t-\tau)}Bu(\tau)\,d\tau,$$

onde $e^{At}$ é a **exponencial de matriz** (matriz de transição de estado). O primeiro
termo é a resposta livre (às condições iniciais); o segundo é a convolução com a entrada
— a versão matricial de $Y(s) = G(s)U(s)$. Na prática, ninguém calcula $e^{At}$ à mão:
usa-se `scipy.linalg.expm` ou, melhor, simula-se com `python-control`.

### 5.5 Modelagem completa do motor CC controlado pela armadura (Nise, cap. 2; Ogata, cap. 3)

O servomotor CC é a planta de referência do laboratório — a dedução a seguir é a que você
deve saber refazer de memória.

**Física (duas equações + dois acoplamentos):**

1. **Circuito de armadura (LK tensão):**
   $$v_a = R_a i_a + L_a\frac{di_a}{dt} + e_b,$$
   com $R_a$ resistência e $L_a$ indutância de armadura, $e_b$ a força contraeletromotriz.
2. **Conversão eletromecânica (dois lados do mesmo fenômeno):**
   - torque motor proporcional à corrente: $T_m = K_t i_a$;
   - f.c.e.m. proporcional à velocidade: $e_b = K_e\omega$.
   No SI, $K_t = K_e$ (conservação de energia: potência elétrica $e_b i_a$ = mecânica
   $T_m\omega$).
3. **Dinâmica mecânica do eixo (Newton rotacional):**
   $$J\dot{\omega} = T_m - b_m\omega = K_t i_a - b_m\omega,$$
   com $J$ o momento de inércia total (rotor + carga refletida pela redução) e $b_m$ o
   atrito viscoso.

**Caso completo (3 polos → 2 polos).** Com $L_a \ne 0$, aplicando Laplace e eliminando
$I_a(s)$: da elétrica, $I_a = \dfrac{V_a - K_e\Omega}{R_a + L_as}$; na mecânica,
$(Js + b_m)\Omega = K_t I_a$. Resultado:

$$\frac{\Omega(s)}{V_a(s)} = \frac{K_t}{(R_a + L_as)(Js + b_m) + K_tK_e}
= \frac{K_t/(L_aJ)}{s^2 + \left(\frac{R_a}{L_a} + \frac{b_m}{J}\right)s + \frac{R_ab_m + K_tK_e}{L_aJ}}.$$

Sistema de **2ª ordem**: um polo "elétrico" (rápido, $\approx R_a/L_a$) e um "mecânico"
(lento). Estado correspondente: $x = [\omega\ \ i_a]^T$.

**Caso reduzido ($L_a \approx 0$) — o modelo do curso.** A dinâmica elétrica é ordens de
grandeza mais rápida que a mecânica; desprezando $L_a$, a corrente "acompanha
instantaneamente" a tensão: $i_a = (v_a - K_e\omega)/R_a$. Substituindo na mecânica:

$$J\dot{\omega} = \frac{K_t}{R_a}v_a - \left(b_m + \frac{K_tK_e}{R_a}\right)\omega.$$

**Leitura física notável:** a f.c.e.m. **age como atrito extra** ($K_tK_e/R_a$) — o motor
se autofreia ao girar, o que garante estabilidade intrínseca. Na forma padrão de 1ª ordem:

$$\frac{\Omega(s)}{V_a(s)} = \frac{K_m}{\tau_m s + 1},\qquad
K_m = \frac{K_t}{R_ab_m + K_tK_e},\qquad
\tau_m = \frac{R_aJ}{R_ab_m + K_tK_e}.$$

**Se a saída for posição** $\theta$ em vez de velocidade, basta acrescentar um integrador
($\omega = \dot\theta$):

$$\frac{\Theta(s)}{V_a(s)} = \frac{K_m}{s(\tau_m s + 1)}$$

— um **integrador em série com uma 1ª ordem**: o modelo clássico de servoposicionador.

### Exercício resolvido 4 — o motor CC do kit, da física ao modelo de 1ª ordem

*O motoredutor do kit do laboratório tem (valores nominais didáticos) $R_a = 2\ \Omega$,
$L_a \approx 0$, $K_t = K_e = 0{,}1$ (SI), $J = 0{,}02$ kg·m², $b_m = 0{,}005$ N·m·s.
Entrada: tensão $v_a$; saída: velocidade $\omega$. Obtenha o modelo.*

**Solução.** Pela fórmula deduzida acima:

$$K_m = \frac{K_t}{R_ab_m + K_tK_e} = \frac{0{,}1}{2(0{,}005) + (0{,}1)(0{,}1)} = \frac{0{,}1}{0{,}01 + 0{,}01} = 5,$$
$$\tau_m = \frac{R_aJ}{R_ab_m + K_tK_e} = \frac{2(0{,}02)}{0{,}02} = 2\ \text{s}.$$

$\boxed{G(s) = \dfrac{5}{2s+1}}$ — a planta de referência de todo o curso. No projeto final,
$K_m$ e $\tau_m$ do **seu** kit serão identificados por ensaio (§6), não calculados.

**Espaço de estados do motor (velocidade):** $\dot{\omega} = -\frac{1}{\tau_m}\omega +
\frac{K_m}{\tau_m}v_a$, i.e., $A = -0{,}5$, $B = 2{,}5$, $C = 1$.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-2-35-nise.png)

**Figura 1.22 — Servomotor CC controlado pela armadura: esquema e diagrama para a dedução
da FT.** (Fonte: NISE, Figura 2.35, Cap. 2)

### 5.6 No computador

No `python-control`:

```python
import control as ct
sys_ss = ct.ss(A, B, C, D)      # espaço de estados
sys_tf = ct.ss2tf(sys_ss)       # conversão EE → FT
sys_ss2 = ct.tf2ss(num, den)    # conversão FT → EE (realização)
t, y = ct.step_response(sys_tf) # resposta ao degrau
```

> 📖 **Referências originais desta seção (para conferência):** Nise, cap. 3 (modelagem no
> domínio do tempo) e motor CC no cap. 2. Ogata, cap. 2 (espaço de estados) e cap. 3
> (motor CC). Penedo, cap. 2 (revisão de matrizes/autovalores) e cap. 10. FBS, caps. 3 e 6.

---

## 6. Identificação experimental: o modelo que vem da bancada

*(Desenvolve Ogata, cap. 4 e cap. 8 — curva de reação / 1º método de Ziegler–Nichols.)*

Na prática (e no projeto final) os parâmetros não são conhecidos — são **medidos**. O ensaio
mais simples é o **degrau em malha aberta**: com o processo estabilizado em um ponto de
operação, aplica-se um degrau de amplitude $\Delta u$ na entrada e registra-se $y(t)$ até o
novo regime. Trabalhe sempre em **variáveis-desvio**:
$\Delta y(t) = y(t) - y_0$.

### 6.1 O modelo FOPDT

Muitos processos industriais (térmicos, nível, vazão) têm resposta ao degrau em forma de
"S" — subida suave com ponto de inflexão — bem descrita por um modelo de 1ª ordem **com
tempo morto** (*First Order Plus Dead Time*):

$$G(s) = \frac{K\,e^{-\theta s}}{\tau s + 1}.$$

O tempo morto $\theta$ modela atrasos de transporte (fluido percorrendo tubulação), atraso
de medição do sensor e, na prática, também o efeito acumulado das dinâmicas de ordem
superior desprezadas — é ele que "arredonda" o início da curva em S.

Sua resposta ao degrau de amplitude $\Delta u$, partindo de $y_0$:

$$y(t) = y_0 + K\Delta u\left(1 - e^{-(t-\theta)/\tau}\right)\,1(t-\theta).$$

### 6.2 Método da tangente no ponto de inflexão (Ziegler–Nichols, Ogata cap. 8)

O método clássico sobre a curva de reação:

1. Trace a **tangente no ponto de inflexão** da curva em S;
2. O cruzamento dessa tangente com o valor inicial $y_0$ marca $\theta = L$;
3. O intervalo até o cruzamento com o valor final marca $\tau = T$;
4. $K = \Delta y_{regime}/\Delta u$.

É rápido e visual, mas **sensível ao traçado da tangente** — pequenas diferenças de
inclinação mudam muito $L$ e $T$, e o ruído de medição atrapalha a localização da inflexão.

### 6.3 Método dos dois pontos (28,3 % e 63,2 %) — o usado no curso

Mais robusto a ruído, usa dois pontos da curva em vez de uma reta traçada "no olho".
Do registro do degrau:

1. $K = \Delta y_{regime}/\Delta u$;
2. Medem-se os instantes em que a resposta atinge **28,3 %** e **63,2 %** da variação
   total:
   $$\tau = 1{,}5\,(t_{63} - t_{28}),\qquad \theta = t_{63} - \tau.$$

**De onde vêm os números?** Na resposta FOPDT, a fração da variação atingida é
$1 - e^{-(t-\theta)/\tau}$. Os dois pontos foram escolhidos para dar equações limpas:

- $1 - e^{-1/3} = 0{,}283$ ⟹ em $t_{28}$: $t_{28} - \theta = \tau/3$;
- $1 - e^{-1} = 0{,}632$ ⟹ em $t_{63}$: $t_{63} - \theta = \tau$.

Subtraindo: $t_{63} - t_{28} = \tau - \tau/3 = \frac{2}{3}\tau$ ⟹ $\tau = 1{,}5(t_{63}-t_{28})$;
e $\theta = t_{63} - \tau$. $\blacksquare$ Usar dois pontos separa $\tau$ de $\theta$ —
com um ponto só e a tangente inicial, os dois parâmetros se confundem.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-2-ogata.png)

**Figura 1.23 — Ensaio de resposta ao degrau unitário da planta (1º método de
Ziegler–Nichols).** (Fonte: OGATA, Figura 8.2, Cap. 8, p. 523)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-3-ogata.png)

**Figura 1.24 — Curva de resposta em forma de S, com a tangente no ponto de inflexão
definindo o atraso L e a constante T.** (Fonte: OGATA, Figura 8.3, Cap. 8, p. 523)

### 6.4 Boas práticas de ensaio (essenciais na bancada)

- **Amplitude do degrau:** grande o suficiente para vencer o ruído (relação
  sinal-ruído alta), pequena o suficiente para o sistema permanecer na região linear
  (e sem saturar o atuador);
- **Registre tempo suficiente:** o ensaio só termina quando a saída claramente atingiu o
  novo regime — estimar $\Delta y_{regime}$ "por projeção" é a maior fonte de erro em $K$;
- **Repita com outra amplitude e nos dois sentidos** (subida e descida): diferenças
  sistemáticas revelam não-linearidades e histerese;
- **Filtre com parcimônia:** média móvel curta ajuda; filtro agressivo distorce o início
  da curva e contamina $\theta$;
- **Valide o modelo:** simule o FOPDT identificado com **outro** degrau (não o usado na
  identificação) e compare com um segundo ensaio — RMSE pequeno = modelo confiável.

### Exercício resolvido 5 — identificação pelos dois pontos

*Um ensaio de degrau unitário estabiliza em $y_\infty = 3{,}0$. A resposta cruza 28,3 % da
variação em $t_{28} = 2{,}83$ s e 63,2 % em $t_{63} = 5{,}50$ s. Identifique o modelo FOPDT.*

**Solução.** $K = 3{,}0/1 = 3$.
$$\tau = 1{,}5(5{,}50 - 2{,}83) = 1{,}5 \times 2{,}67 = 4{,}0\ \text{s};\qquad
\theta = 5{,}50 - 4{,}0 = 1{,}5\ \text{s}.$$

$\boxed{G(s) = \dfrac{3\,e^{-1{,}5s}}{4s+1}}$ — exatamente a "planta B" usada nos Labs 02 e
09–11. **Sempre valide**: simule o modelo com um degrau de outra amplitude e compare com um
segundo ensaio (RMSE pequeno = modelo confiável). O Lab 02 automatiza todo esse fluxo.

**Exercício adicional 6.A — e se não houver tempo morto?**
*Um ensaio no motor do kit (degrau de 2 V) estabiliza em $\Delta\omega_\infty = 10$ rad/s,
atingindo 6,32 rad/s em $t = 0{,}5$ s. Identifique o modelo e compare com o nominal.*

**Solução.** A resposta cruza 63,2 % em $0{,}5$ s **desde o início do degrau** — logo
$\theta \approx 0$ e $\tau = 0{,}5$ s; $K = 10/2 = 5$ rad/s/V. Modelo:
$G(s) = \dfrac{5}{0{,}5s+1}$. O ganho bate com o nominal; a constante de tempo menor indica
que o kit real tem menos inércia equivalente que o valor didático — típico: o $J$ nominal
inclui folga de segurança.

> 📖 **Referências originais desta seção (para conferência):** Ogata, cap. 4 (processos
> térmicos/fluídicos) e cap. 8 (curva de reação, 1º método de Ziegler–Nichols, Figuras 8.2
> e 8.3). O método dos dois pontos é a variação moderna padrão em textos de controle de
> processos (cf. FBS, cap. 11, para o uso de $K, \tau, \theta$ no projeto PID).

---

## 7. Resposta em frequência: a outra janela para o mesmo sistema

*(Desenvolve Ogata, cap. 7; Nise, cap. 10; Schaum, cap. 15 e §6.5; Penedo, cap. 8;
FBS, cap. 9.)*

### 7.1 O teorema fundamental

Se a entrada é senoidal $u = A\sin(\omega t)$ e o sistema é **linear e estável**, a saída
em regime permanente é **outra senoide, na mesma frequência**, apenas com amplitude e fase
alteradas:

$$y_{ss}(t) = A\,\underbrace{|G(j\omega)|}_{\text{ganho}}\,\sin\!\big(\omega t + \underbrace{\angle G(j\omega)}_{\text{fase}}\big).$$

**Por quê?** Escrevendo a entrada como parte imaginária de $Ae^{j\omega t}$ e usando
$Y(s) = G(s)U(s)$, a decomposição em frações parciais mostra que os termos dos polos de
$G(s)$ decaem (sistema estável), restando apenas os termos dos polos da entrada em
$\pm j\omega$, que se combinam na senoide acima. Avaliar a FT em $s = j\omega$ dá, para
cada frequência, o par (ganho, fase) — a **resposta em frequência** do sistema.

Consequência prática imediata: a resposta em frequência é **mensurável experimentalmente**
sem conhecer a FT — excita-se o sistema com senoides de várias frequências e mede-se o par
(ganho, fase) em cada uma. É o que o Lab 03 faz.

### 7.2 O diagrama de Bode

O **diagrama de Bode** traça duas curvas contra $\log_{10}\omega$:

- **Módulo:** $20\log_{10}|G(j\omega)|$, em decibéis (dB). Em dB, produtos viram somas:
  o Bode de uma cascata é a **soma** dos Bodes dos blocos.
- **Fase:** $\angle G(j\omega)$, em graus (escala linear).

Referências rápidas de dB: ganho 2 → +6 dB; 10 → +20 dB; $1/\sqrt2 \approx 0{,}707$ → −3 dB;
0,1 → −20 dB.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-10-4-nise.png)

**Figura 1.25 — Diagramas de resposta em frequência para $G(s) = 1/(s+2)$: magnitude
(superior) e fase (inferior), ambos contra $\log\omega$.** (Fonte: NISE, Figura 10.4,
Cap. 10)

### 7.3 Os blocos construtivos e suas assíntotas (Nise, cap. 10; Ogata, cap. 7)

Como FTs fatoradas viram somas em dB, basta conhecer quatro tijolos:

**1. Ganho constante $K$:** reta horizontal em $20\log_{10}K$ dB; fase $0°$ ($K>0$) ou
$\pm 180°$ ($K<0$).

**2. Integrador $1/s$ (e derivador $s$):** $|G| = 1/\omega$ ⟹ reta de **−20 dB/década**
cruzando 0 dB em $\omega = 1$; fase constante **−90°**. O derivador é o espelho:
+20 dB/dec, +90°.

**3. Polo real $1/(\tau s + 1)$:**
$$|G|_{dB} = -10\log_{10}\!\big(1 + \omega^2\tau^2\big),\qquad
\angle G = -\arctan(\omega\tau).$$
Assíntotas: 0 dB para $\omega \ll 1/\tau$; **−20 dB/década** para $\omega \gg 1/\tau$. Na
**frequência de canto** $\omega_c = 1/\tau$: valor exato −3 dB e fase **−45°**. A fase vai
de 0° a −90°, concentrada (aproximadamente) na faixa $0{,}1\,\omega_c$ a $10\,\omega_c$ —
a assíntota de fase padrão cai 45°/década nesse intervalo. Erro máximo das assíntotas de
módulo: 3 dB, exatamente no canto.

**4. Zero real $(\tau s + 1)$:** o oposto do polo: +20 dB/década após $1/\tau$, fase de 0°
a +90° (+45° no canto). **Atenção:** zero no semiplano direito (fase não mínima) tem o
mesmo módulo do zero normal, mas fase **negativa** como se fosse um polo — daí o nome.

**5. Par de polos complexos (2ª ordem)** $\omega_n^2/(s^2 + 2\zeta\omega_n s + \omega_n^2)$:
assíntotas 0 dB e **−40 dB/década** após $\omega_n$; fase de 0° a −180° (−90° em
$\omega_n$). Mas perto do canto a curva real **depende fortemente de $\zeta$**: quanto
menor o amortecimento, maior o **pico de ressonância** — as assíntotas podem errar por
mais de 10 dB se $\zeta$ for pequeno. A Figura 1.26 mostra as assíntotas normalizadas e a
Figura 1.27, adiante, mostra o quanto a curva real se afasta delas para cada $\zeta$.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-10-13-nise.png)

**Figura 1.26 — Assíntotas de Bode para o polinômio de segunda ordem normalizado e
escalonado ($\omega/\omega_n$): (a) magnitude; (b) fase.** (Fonte: NISE, Figura 10.13,
Cap. 10)

### 7.4 Pico de ressonância e largura de banda

Em 2ª ordem subamortecida, derivando $|G(j\omega)|$ e igualando a zero obtém-se a
frequência de ressonância e o pico:

$$\omega_r = \omega_n\sqrt{1-2\zeta^2},\qquad
M_r = \frac{1}{2\zeta\sqrt{1-\zeta^2}}\qquad(\text{existe apenas se } \zeta < 0{,}707).$$

Note que $\omega_r < \omega_d < \omega_n$: a ressonância acontece um pouco **antes** da
frequência natural amortecida. A **largura de banda** $\omega_{BW}$ é a frequência onde o
ganho cai a −3 dB; ela mede a "rapidez" do sistema no domínio da frequência
($\omega_{BW}\uparrow \Rightarrow t_r\downarrow$) e aumenta com $\omega_n$ e diminui com
$\zeta$ (faixa usual de projeto).

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-10-14-nise.png)

**Figura 1.27 — Magnitude da resposta normalizada e escalonada para
$s^2 + 2\zeta\omega_n s + \omega_n^2$, para diversos valores de $\zeta$: os vales/picos
perto de $\omega/\omega_n = 1$ crescem à medida que $\zeta$ diminui — é o pico de
ressonância $M_r$ aparecendo.** (Fonte: NISE, Figura 10.14, Cap. 10)

**Ponte tempo ↔ frequência** (use nos dois sentidos): $M_r$ alto ⟺ $\zeta$ baixo ⟺
$M_p$ alto no degrau; $\omega_{BW}$ alta ⟺ $\omega_n$ alta ⟺ resposta rápida. As
especificações de projeto podem assim ser dadas em qualquer um dos dois domínios.

### 7.5 Tempo morto em frequência

$$G_{tm}(j\omega) = e^{-j\omega\theta}\;\Rightarrow\; |G_{tm}| = 1\ \text{(0 dB)},\qquad
\angle G_{tm} = -\omega\theta\ \text{rad}.$$

O tempo morto **não altera o módulo**, mas sua fase cresce (em módulo) sem limite com
$\omega$ — no gráfico semilog é uma queda cada vez mais íngreme. É por isso que ele é o
grande inimigo da estabilidade em malha fechada (margens de fase, Unidades II e IV): ele
"consome" fase sem dar nenhum aviso no gráfico de módulo.

### 7.6 Construção de um Bode por assíntotas — exemplo completo

**Exemplo 7.1.** Esboce o Bode de $G(s) = \dfrac{100(s+2)}{(s+1)(s+10)}$.

1. **Fatore na forma de Bode** (cada termo como $(\tau s + 1)$):
   $G(s) = \dfrac{100 \cdot 2(0{,}5s+1)}{1\cdot(s+1)\cdot 10(0{,}1s+1)} = \dfrac{20(0{,}5s+1)}{(s+1)(0{,}1s+1)}$.
2. **Ganho de Bode:** $K_b = 20$ ⟹ $20\log_{10}20 = 26$ dB; fase base 0°.
3. **Cantos:** zero em $2$ rad/s; polos em $1$ e $10$ rad/s.
4. **Módulo por trechos:** começa plano em 26 dB; em $\omega = 1$, −20 dB/dec; em
   $\omega = 2$, o zero devolve +20 ⟹ volta a ficar plano; em $\omega = 10$, cai a
   −20 dB/dec definitivamente.
5. **Fase por trechos:** soma de $-\arctan(\omega/1) + \arctan(\omega/2) - \arctan(\omega/10)$.
   Limites: 0° → em frequências médias o zero "adianta" e a fase sobe (chega a ficar
   menos negativa) → termina em $-90°$ (dois polos − um zero).

Esse procedimento — fatorar, marcar cantos, somar inclinações — resolve qualquer Bode à mão
com precisão de ~3 dB, e é a habilidade cobrada na Lista 1.

### 7.7 Identificação por ensaio senoidal

Como $|G(j\omega)|$ e $\angle G(j\omega)$ são diretamente medíveis, a resposta em
frequência é também ferramenta de identificação:

- **1ª ordem:** $K$ é o ganho em baixa frequência; $\tau$ sai da fase
  ($\tan|\phi| = \omega\tau$) ou do ponto de −3 dB ($\omega_c = 1/\tau$);
- **2ª ordem subamortecida:** $\zeta$ sai do pico de ressonância pela fórmula inversa de
  $M_r$; $\omega_n$ sai da posição do pico ($\omega_r$);
- **Tempo morto:** diferença entre a fase medida e a fase esperada do modelo racional,
  dividida por $-\omega$.

**Dica de bancada (detecção síncrona):** em vez de medir amplitude "no olho" em sinal
ruidoso, multiplique a saída por $\sin(\omega t)$ e por $\cos(\omega t)$ e integre por
vários períodos — as médias dão diretamente as componentes em fase e em quadratura, logo
ganho e fase, com forte rejeição a ruído. O Lab 03 implementa isso.

### Exercício resolvido 6 — do ensaio senoidal ao modelo

*Uma planta desconhecida, sabidamente de 1ª ordem, dá ganho estático 2. Excitada com senoide
de $\omega = 3$ rad/s, a saída em regime tem ganho $0{,}632$ e atraso de fase de $71{,}6°$.
Identifique $G(s)$.*

**Solução.** Para $G = K/(\tau s+1)$: $K = 2$ (ganho em $\omega \to 0$). A fase é
$\phi = -\arctan(\omega\tau)$:
$$-71{,}6° \Rightarrow \tan(71{,}6°) = 3 = \omega\tau = 3\tau \Rightarrow \tau = 1\ \text{s}.$$
Verificação pelo ganho: $|G(j3)| = 2/\sqrt{1+9} = 0{,}632$ ✓. $\boxed{G(s) = \dfrac{2}{s+1}}$.
O Lab 03 implementa esse ensaio ponto a ponto (com detecção síncrona) e a identificação pelo
pico de ressonância.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-15-3-distefano.png)

**Figura 1.28 — Exemplo de diagrama de Bode (módulo e fase).** (Fonte: DISTEFANO,
Figura 15.3, Cap. 15)

> 📖 **Referências originais desta seção (para conferência):** Ogata, cap. 7, primeira
> parte (Bode, assíntotas, ressonância). Nise, cap. 10 (construção de Bode passo a passo,
> tabelas de assíntotas). Schaum, cap. 15 (Bode analysis, exercícios resolvidos) e §6.5.
> Penedo, cap. 8 (Bode em português). FBS, cap. 9 (frequency response) — e as
> transparências CDS 110 L7-1.

---

## 8. Resumo da unidade e conexão com os labs

| Conceito | Onde está nesta apostila | Onde pratica | Livro-âncora |
|---|---|---|---|
| Física → EDO → FT | §1 (1.1–1.5, todos os domínios) | Lab 01 | Ogata 3–4; Nise 2 |
| Laplace e frações parciais | §2 (inclui os 3 casos resolvidos) | Lab 01/02, Lista 1 | Schaum 4 |
| FT, polos/zeros, blocos | §3 (regras de redução 1–5) | Labs 01–04 | Nise 2 e 5; Schaum 7 |
| 1ª/2ª ordem, $M_p$, $t_s$ | §4 (deduções completas + geometria) | Labs 02 e 04 | Nise 4; Penedo 4 |
| Espaço de estados | §5 (conversões + autovalores) | Lab 01 | Nise 3; Ogata 2 |
| Motor CC completo | §5.5 (dedução linha a linha) | Lab 01 → projeto final | Nise 2; Ogata 3 |
| Identificação por degrau (FOPDT) | §6 (tangente + dois pontos + validação) | Lab 02 → projeto final | Ogata 4 e 8 |
| Resposta em frequência / Bode | §7 (assíntotas, ressonância, tempo morto) | Lab 03 | Ogata 7; Nise 10; Schaum 15 |
| Não linear → linearizado | §1.4 (válvula turbulenta, Taylor) | Lab 01 §6 | FBS 3 e 5 |

**Autoavaliação antes da Lista 1:** você deve conseguir (i) deduzir a FT do motor CC de
memória entendendo cada passo (§5.5); (ii) esboçar a resposta ao degrau de $K/(\tau s+1)$
marcando $\tau$ e $4\tau$ (§4.1); (iii) calcular $\zeta$, $\omega_n$, $M_p$ e $t_s$ de
qualquer 2ª ordem (§4.4); (iv) identificar um FOPDT a partir de dois pontos da curva (§6.3);
(v) extrair $K$ e $\tau$ de um par (ganho, fase) medido (§7.7); (vi) esboçar o Bode de
uma FT fatorada por assíntotas (§7.6); (vii) converter EDO ↔ espaço de estados ↔ FT e dizer
por que os polos são os autovalores de $A$ (§5.3).

---

## Mapa das fórmulas da Unidade I (folha de consulta)

| Tema | Fórmulas-chave |
|---|---|
| 1ª ordem | $y_{degrau}(t) = K(1-e^{-t/\tau})$; $y(\tau) = 0{,}632K$; $t_s \approx 4\tau$ |
| 2ª ordem | $G(s) = \frac{K\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$; polos $-\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2}$ |
| Desempenho | $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$; $t_p = \frac{\pi}{\omega_n\sqrt{1-\zeta^2}}$; $t_s \approx \frac{4}{\zeta\omega_n}$ |
| Geometria plano $s$ | $\cos\theta = \zeta$; $|s| = \omega_n$; $\mathrm{Re} = -\zeta\omega_n$ manda no $t_s$ |
| Laplace | $\mathcal{L}\{\dot f\} = sF(s)$; TVF: $\lim y = \lim_{s\to0}sY(s)$; tempo morto: $e^{-\theta s}$ |
| Malha fechada | $T = \frac{G}{1+GH}$ (realimentação negativa) |
| Espaço de estados | $G(s) = C(sI-A)^{-1}B + D$; polos = autovalores de $A$ |
| Motor CC ($L_a\!\approx\!0$) | $K_m = \frac{K_t}{R_ab_m + K_tK_e}$; $\tau_m = \frac{R_aJ}{R_ab_m + K_tK_e}$ |
| FOPDT | $G(s) = \frac{Ke^{-\theta s}}{\tau s+1}$; $\tau = 1{,}5(t_{63}-t_{28})$; $\theta = t_{63} - \tau$ |
| Bode | polo: −20 dB/dec após $1/\tau$, fase → −90°; zero: espelho; $1/s$: −20 dB/dec, −90°; tempo morto: 0 dB, fase $-\omega\theta$ |
| Ressonância | $M_r = \frac{1}{2\zeta\sqrt{1-\zeta^2}}$ ($\zeta<0{,}707$); $\omega_r = \omega_n\sqrt{1-2\zeta^2}$ |

---

## Leituras dirigidas da Unidade I

**Esta apostila cobre integralmente o conteúdo abaixo** — use a tabela apenas se quiser
conferir a formulação original em cada fonte:

| Prioridade | Fonte | O que ler | Onde está aqui |
|---|---|---|---|
| essencial | **Nise**, caps. 2–4 | modelagem no domínio da frequência (FIG. 2.15 massa–mola; FIG. 2.35 motor CC), espaço de estados e resposta transitória (FIGS. 4.10 e 4.14) | §1, §3, §5, §4 |
| essencial | **Ogata**, caps. 2–5 e 7 | Laplace, modelagem mecânica/elétrica/térmica, resposta transitória (FIGS. 5.1, 5.2, 5.22) e Bode | §2, §1, §4, §7 |
| essencial | **Ogata**, cap. 8 | curva de reação / 1º método de Ziegler–Nichols (FIGS. 8.2 e 8.3) | §6 |
| revisão matemática | **Schaum**, caps. 3–4 e 15 | EDOs, Laplace com frações parciais (§4.7–4.8) e Bode (FIG. 15-3) | §2, §7 |
| em português | **Penedo**, caps. 3–4 e 8 | Laplace, especificações de desempenho (FIGS. 4.1 e 4.4) e resposta em frequência | §2, §4, §7 |
| aprofundamento | **FBS** (gratuito), caps. 3, 4, 6 e 9 | modelagem, exemplos completos, sistemas lineares e resposta em frequência | §1, §5, §7 |
| computacional | **CDS 110** notebooks L1, L2, L3 | servomecanismo, pêndulo invertido (fluxo `nlsys → find_eqpt → linearize`) e ferramentas para sistemas LTI | Labs 01–03 |

## Referências bibliográficas

- OGATA, K. *Engenharia de Controle Moderno*. 5. ed. Rio de Janeiro: Pearson Brasil, 2006.
- NISE, N. S. *Engenharia de Sistemas de Controle*. LTC (excelente para modelagem — Unidade I — e lugar das raízes — Unidade II).
- DISTEFANO, J. J.; STUBBERUD, A. R.; WILLIAMS, I. J. *Sistemas de Retroação e Controle* (Coleção Schaum) — banco de exercícios resolvidos para todas as unidades.
- PENEDO, S. R. M. *Sistemas de Controle: Matemática Aplicada a Projetos*. Érica (reforço matemático em pt-BR: Laplace, diagramas de blocos).
- ÅSTRÖM, K. J.; MURRAY, R. M. *Feedback Systems: An Introduction for Scientists and Engineers*. 2. ed. Princeton University Press. Disponível gratuitamente em <https://fbswiki.org>.
- MURRAY, R. M. *CDS 110 / ChE 105 — Analysis and Design of Feedback Control Systems*, Caltech, Spring 2024: <https://murray.cds.caltech.edu/CDS_110/ChE_105,_Spring_2024>.
- Documentação da `python-control` 0.10.x: <https://python-control.readthedocs.io/en/0.10.2/index.html> — repositório: <https://github.com/python-control/python-control>.
