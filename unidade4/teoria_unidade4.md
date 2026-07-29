# Unidade IV — PID: síntese, sintonia e implementação

## Apostila completa e autossuficiente

**Carga: 3 h (semanas 10–12) · Labs 08, 09, 10 e 11 · Lista 4**

Pré-requisitos: Unidades I (modelos e frequência), II (estabilidade e margens) e III
(saturação e anti-windup) — ver as apostilas completas correspondentes.

O PID responde pela maioria das malhas industriais do mundo. Compreendê-lo exige juntar
toda a teoria das três unidades anteriores: modelos (para sintonia), margens e sensibilidade
(para robustez) e não-linearidades (para implementação real e digital). Esta é a **versão
expandida e autossuficiente** — todo o conteúdo das caixas 📖 "Onde estudar" foi
desenvolvido na íntegra aqui, com deduções completas, tabelas de sintonia, exemplos
resolvidos adicionais e as figuras originais de Ogata, Nise e Schaum.

---

## 1. O algoritmo PID e o efeito de cada ação

*(Desenvolve Ogata, cap. 5 e cap. 8; Nise, cap. 9; FBS, cap. 11; Schaum, cap. 4 e cap. 20;
Penedo, cap. 9.)*

### 1.1 A forma padrão

$$u(t) = K_p\left(e(t) + \frac{1}{T_i}\int_0^t e(\tau)\,d\tau + T_d\frac{de}{dt}\right)
\qquad\Longleftrightarrow\qquad
C(s) = K_p\left(1 + \frac{1}{T_i s} + T_d s\right)$$

Forma equivalente ("paralela"): $u = K_pe + K_i\int e\,dt + K_d\dot e$. As três ações:

- **P (proporcional):** força imediata contra o erro — define a rapidez básica e a banda da
  malha. Preço: com plantas tipo 0, deixa erro de regime $\dfrac{1}{1+K_pG(0)}$ (Unidade II,
  §2) e, alto demais, derruba o amortecimento (Exercício 2 da Unidade II).
- **I (integral):** acumula o erro — só descansa quando $e = 0$ (Unidade II, §2.1):
  **elimina o erro de regime** e rejeita perturbações constantes. Preço: atraso de fase
  (até $-90°$ em baixa frequência) ⟹ derruba a PM; e, com saturação, windup (Unidade III).
- **D (derivativa):** antecipação — age sobre a *taxa de variação* do erro, adianta fase e
  acrescenta amortecimento. Preço: amplifica ruído de medição e não age sobre erros
  constantes (sozinha, não controla nada).

### 1.2 O efeito de cada ação demonstrado (Ogata, cap. 5, na íntegra)

**Ação integral sobre a 1ª ordem.** Planta $K/(\tau s+1)$ com controlador I $K_i/s$: a malha
fechada é
$$T(s) = \frac{K_iK}{\tau s^2 + s + K_iK},\qquad e_{degrau} = 0.$$
O erro sumiu, mas repare no numerador do coeficiente de $s$: o amortecimento é
$2\zeta\omega_n = 1/\tau$ — **fixo**; aumentar $K_i$ só aumenta $\omega_n = \sqrt{K_iK/\tau}$,
logo $\zeta = \frac{1}{2\sqrt{K_iK\tau}}$ **cai**. O integrador zerou o erro *e* cobrou seu
preço em amortecimento — exatamente o que a PM prevê.

**Ação derivativa acrescentando amortecimento.** Planta de posição $K/[s(\tau s+1)]$ com PD
$K_p(1+T_ds)$: característica $\tau s^2 + (1 + KK_pT_d)s + KK_p = 0$. O termo derivativo
aparece multiplicando $s$: **é ele quem aumenta o amortecimento** ($2\zeta\omega_n =
(1+KK_pT_d)/\tau$) sem mexer no ganho de regime. É a demonstração algébrica do "D melhora
o transitório".

**Efeitos de um olhar só (Ogata, cap. 8):**

| Ação | Tempo de subida | Sobressinal | Tempo de acomodação | Erro de regime |
|---|---|---|---|---|
| $K_p\uparrow$ | diminui | aumenta | pequena mudança | diminui (não zera) |
| $K_i\uparrow$ ($T_i\downarrow$) | diminui | aumenta | aumenta | **elimina** |
| $K_d\uparrow$ ($T_d\uparrow$) | pequena mudança | **diminui** | diminui | nenhum |

### 1.3 O sistema completo

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-1-ogata.png)

**Figura 4.1 — Diagrama de blocos do sistema de controle PID básico: a referência é
comparada com a saída e o PID age sobre o erro.** (Fonte: OGATA, Figura 8.1, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-25-ogata.png)

**Figura 4.2 — O PID no mundo real: (a) a malha com distúrbio $D(s)$ na entrada da planta
e ruído $N(s)$ na medição — os dois sinais "invisíveis" que o projeto deve enfrentar;
(b) o diagrama de blocos equivalente com as três ações em paralelo.** (Fonte: OGATA,
Figura 8.25, Cap. 8)

---

## 2. O PID "de verdade": o que difere do livro-texto

*(Desenvolve Ogata, cap. 8 — PID modificado; FBS, cap. 11; Åström & Hägglund, cap. 3;
Nise, cap. 9 e cap. 13.)*

O PID ideal tem três problemas práticos que toda implementação séria precisa tratar.

### 2.1 Filtro derivativo — dedução completa

A derivada ideal $T_ds$ tem ganho $T_d\omega$, que cresce sem limite com a frequência: um
amplificador de ruído perfeito. A solução universal é derivar **com filtro**:

$$C_{PID}(s) = K_p\left(1 + \frac{1}{T_i s} + \frac{T_d s}{1 + T_d s/N}\right).$$

**O que o filtro faz, em números:** o termo derivativo
$\dfrac{T_ds}{1 + T_ds/N}$ tem ganho em alta frequência limitado a
$$\lim_{\omega\to\infty}\left|\frac{j\omega T_d}{1 + j\omega T_d/N}\right| = N.$$
Com $N = 10$ (padrão do curso), a derivada amplifica o ruído de alta frequência no máximo
$N\cdot K_p = 10K_p$ vezes — contra infinito no caso ideal. Em baixa frequência o termo se
comporta como $T_ds$ (derivada ideal); o canto do filtro fica em $\omega_f = N/T_d$,
acima da banda da malha, para não estragar a ação derivativa útil. Note que agora o PID é
**próprio** (realizável): numerador e denominador com o mesmo grau.

### 2.2 Derivada na medição — o "derivative kick"

A referência quase sempre muda em degraus; derivar $e = r - y$ deriva o degrau da referência
⟹ **um impulso no comando** a cada mudança de setpoint (o *derivative kick*). Como o
objetivo da ação D é amortecer a **resposta da planta**, deriva-se apenas $-y$:

$$u = K_p\left(e + \frac{1}{T_i}\int e\,dt\right) - K_pT_d\frac{dy}{dt}.$$

Os polos de malha fechada não mudam (o denominador de $1 + CG$ é o mesmo — a referência só
aparece no numerador); o que muda é o **zero** que o $T_ds$ criava no caminho da referência
— e era ele o causador do sobressinal extra a degraus de setpoint. Derivando a medição, o
transitório de referência fica mais suave. É a versão "pobre" do 2DOF (§6) — e é o modo
`D on measurement` de qualquer controlador industrial.

### 2.3 PI-D: a forma do curso (Ogata, cap. 8)

Juntando as duas ideias (D na medição, com filtro) obtém-se o **PI-D**, a arquitetura usada
nos Labs 08–11 e no firmware do kit — a Figura 4.3 mostra exatamente a topologia: P e I
agindo no erro, D agindo na medição realimentada.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-26-ogata.png)

**Figura 4.3 — Sistema com controle PI-D: os termos $1$ (proporcional) e $1/(T_is)$
(integral) agem sobre o erro $E(s)$; o termo $T_ds$ (derivativo) age sobre o sinal medido
$B(s)$, não sobre a referência.** (Fonte: OGATA, Figura 8.26, Cap. 8)

**Ainda falta uma coisa** — o anti-windup do §2.2 da Unidade III. A forma final
(implementada na classe `DigitalPID` do Lab 10 e no firmware, arquivo
`pid_controller.cpp`) é: **PI-D + filtro derivativo + anti-windup por back-calculation**.

### Exercício resolvido 1 — lendo o filtro derivativo no Bode

*Para $C = 2\left(1 + \dfrac{1}{4s} + \dfrac{0{,}8s}{1 + 0{,}08s}\right)$: identifique os
parâmetros, o canto do filtro e o ganho de alta frequência do termo derivativo. Por que o
filtro é indispensável no kit?*

**Solução.** $K_p = 2$; $T_i = 4$ s; $T_d = 0{,}8$ s; $N = 0{,}8/0{,}08 = 10$.
Canto do filtro: $\omega_f = N/T_d = 12{,}5$ rad/s — deve ficar **acima** da banda da malha
($\omega_{gc}$ típica de 2–5 rad/s no kit) para não destruir a ação derivativa onde ela
importa, e abaixo da frequência do ruído do encoder.
Ganho máximo do termo derivativo: $K_pN = 20$ — contra ∞ sem filtro.
No kit, a velocidade vem de **diferenças do encoder** (ruído de quantização intenso); sem
filtro, a ação D injetaria esse ruído amplificado direto no PWM, aquecendo o motor e
gastando a bateria — efeito mensurável no Lab 08.

> 📖 **Referências originais das Seções 1–2 (para conferência):** Ogata, cap. 5 (efeitos
> das ações P, I, D com deduções) e cap. 8 (PID modificado, PI-D — FIGURAS 8.1, 8.25 e
> 8.26). Nise, cap. 9 (projeto de PID por LGR). FBS, cap. 11 (o PID com todas as
> modificações práticas). Åström & Hägglund, cap. 3. Schaum, cap. 4 e cap. 20. Penedo,
> cap. 9.

---

## 3. Sintonia: onde os números saem

*(Desenvolve Ogata, cap. 8 — na íntegra; FBS, cap. 11; Åström & Hägglund, caps. 4–5;
Nise, cap. 9.)*

Sintonizar = escolher $(K_p, T_i, T_d)$. Quatro famílias de métodos, do mais histórico ao
recomendado no curso:

### 3.1 Ziegler–Nichols pelo ponto crítico (2º método — 1942)

A malha é levada ao limite de oscilação com ganho proporcional puro (ou pelo relé,
Unidade III): registra-se o **ganho crítico** $K_u$ ($K_{cr}$ na notação do Ogata) e o
**período crítico** $T_u$ ($P_{cr}$). A Tabela 4.1 dá os parâmetros.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-4-ogata.png)

**Figura 4.4 — Arranjo do 2º método de ZN: malha fechada apenas com ganho proporcional,
que é aumentado até a oscilação sustentada.** (Fonte: OGATA, Figura 8.4, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-5-ogata.png)

**Figura 4.5 — A oscilação sustentada de período $P_{cr}$ no ganho crítico $K_{cr}$.** (Fonte:
OGATA, Figura 8.5, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/tab-8-2-ogata.png)

**Tabela 4.1 — Regras de sintonia de Ziegler–Nichols baseadas no ganho crítico $K_{cr}$ e
no período crítico $P_{cr}$ (2º método).** (Fonte: OGATA, Tabela 8.2, Cap. 8)

Em fórmulas: P: $K_p = 0{,}5K_u$; PI: $K_p = 0{,}45K_u$, $T_i = T_u/1{,}2$; PID:
$K_p = 0{,}6K_u$, $T_i = T_u/2$, $T_d = T_u/8$.

**Advertências (Åström & Hägglund):** o ZN clássico mira **razão de decaimento 1/4**
($\zeta \approx 0{,}2$) — oscilatório demais para a maioria das aplicações, e foi projetado
para rejeição de perturbações, não para seguimento de referência. Uso recomendado no curso:
obter $K_u, T_u$ com segurança **pelo relé** (Lab 07), e usar ZN apenas como ponto de
partida grosseiro a ser melhorado.

### 3.2 Ziegler–Nichols pela curva de reação (1º método)

Se a planta admite ensaio de degrau em malha aberta e a resposta é em S (FOPDT, Unidade I,
§6): medem-se $K$, o tempo morto $L$ ($\theta$) e a constante $T$ ($\tau$), e aplica-se a
Tabela 4.2.

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-2-ogata.png)

**Figura 4.6 — Ensaio de degrau da planta em malha aberta: a base experimental do 1º
método.** (Fonte: OGATA, Figura 8.2, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-3-ogata.png)

**Figura 4.7 — A curva em S com a tangente no ponto de inflexão definindo $L$ e $T$.**
(Fonte: OGATA, Figura 8.3, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/tab-8-1-ogata.png)

**Tabela 4.2 — Regras de sintonia de Ziegler–Nichols baseadas na resposta ao degrau
(1º método).** (Fonte: OGATA, Tabela 8.1, Cap. 8)

Em fórmulas: P: $K_p = T/(KL)$; PI: $K_p = 0{,}9T/(KL)$, $T_i = L/0{,}3$; PID:
$K_p = 1{,}2T/(KL)$, $T_i = 2L$, $T_d = 0{,}5L$. Note que o PID inteiro é função de
$K, L, T$ — o modelo FOPDT do Lab 02 *é* a sintonia.

### 3.3 CHR (Chien–Hrones–Reswick, 1952)

Corrige o principal defeito do ZN distinguindo explicitamente as duas tarefas da malha:
**servo** (seguir referência) e **regulatório** (rejeitar perturbação), com duas variantes
cada: resposta mais rápida sem sobressinal, ou com sobressinal de 20 %. A Tabela 3 do
Lab 09 §3.4 traz as fórmulas completas (todas em função de $K$, $\tau$ e $\theta$ do FOPDT).
CHR-0 % é frequentemente a melhor sintonia "de tabela" para a bancada quando a referência
importa mais que a perturbação.

### 3.4 Lambda (IMC) — a recomendação do curso, com a dedução

Baseado no modelo FOPDT $G = \dfrac{Ke^{-\theta s}}{\tau s+1}$, fecha a malha pedindo uma
resposta de 1ª ordem com constante de tempo escolhida $\lambda$ — **um único botão de
ajuste**: $\lambda$ pequeno ⟹ malha rápida e agressiva; grande ⟹ suave e robusto.

**De onde sai a fórmula (IMC, Internal Model Control):** pede-se que a malha fechada
seja $T_{desejada} = \dfrac{e^{-\theta s}}{\lambda s + 1}$ (o tempo morto é imbatível — ele
fica na malha fechada). Invertendo $T = CG/(1+CG)$ para o controlador:
$C = \dfrac{1}{G}\cdot\dfrac{T}{1-T}$. Substituindo e aproximando
$e^{-\theta s} \approx 1 - \theta s$ (Padé de 1ª ordem):
$$C(s) = \frac{\tau s + 1}{K(\lambda + \theta)s},$$
que é **exatamente um PI** com
$$\boxed{K_p = \frac{1}{K}\cdot\frac{\tau}{\lambda + \theta},\qquad T_i = \tau.}$$

**Regras práticas (Labs 09–11):** $\lambda = \max(\theta,\ \tau/3)$ é o ponto de partida;
$T_d = \theta/2$ quando a derivada ajuda (temperatura, pouco ruído) — a robustez se
verifica sempre com PM ≥ 45° e GM ≥ 6 dB **depois** de sintonizar (§5).

### Exercício resolvido 2 — três sintonias, mesma planta

*Para a planta B do curso, $G(s) = \dfrac{3e^{-1{,}5s}}{4s+1}$ ($K = 3$, $\tau = 4$,
$\theta = 1{,}5$), calcule as sintonias PI por ZN-1 e por lambda com $\lambda = \tau/3$, e
compare $K_p$ e $T_i$.*

**Solução.**
ZN-1 (PI): $K_p = \dfrac{0{,}9T}{KL} = \dfrac{0{,}9\cdot4}{3\cdot1{,}5} = 0{,}8$;
$T_i = L/0{,}3 = 5$ s.
Lambda: $\lambda = 4/3 = 1{,}33$; $K_p = \dfrac{1}{3}\cdot\dfrac{4}{1{,}33+1{,}5} = 0{,}47$;
$T_i = 4$ s.
O lambda é **mais conservador** (menor ganho, integração mais lenta) — coerente com a
filosofia: ZN mira decaimento 1/4 (agressivo), lambda mira robustez ajustável. No Lab 09,
simule as duas e compare o sobressinal e o tempo de acomodação.

**Exercício adicional 3.A — e quando a planta é um integrador puro?**
*A malha de posição do kit tem $G(s) = \dfrac{K_m}{s(\tau_m s+1)}$ — não é FOPDT. Como
sintonizar?*

**Solução.** Não se aplica ZN-1/lambda diretamente. Caminho do curso: LGR (Unidade II, §4)
ou loop shaping (§4) sobre a planta de posição, ou fechar primeiro a malha de velocidade
(cascata, Lab 11 §6). É um bom exercício de auditoria: liste qual método serve para qual
arquitetura e por quê.

> 📖 **Referências originais desta seção (para conferência):** Ogata, cap. 8 (os dois
> métodos de ZN completos, com as FIGURAS 8.2–8.5 e TABELAS 8.1–8.2 — e a frase "essas
> regras são apenas ponto de partida"). Åström & Hägglund, cap. 4 (o contexto histórico e
> as críticas ao ZN) e cap. 5 (lambda/IMC). FBS, cap. 11 (PID Design).

---

## 4. Projeto por *loop shaping*: moldar o Bode da malha

*(Desenvolve FBS, cap. 12 — na íntegra; Ogata, cap. 7; Nise, cap. 11; Schaum, caps. 15–16;
Penedo, cap. 10.)*

### 4.1 A ideia em três frases

Tudo o que a malha precisa fazer está escrito no **Bode de** $L = CG$:

- **baixa frequência:** $|L|$ alto ⟹ $S = 1/(1+L)$ pequena ⟹ bom seguimento de referência,
  erro de regime pequeno e rejeição de perturbações;
- **média frequência (perto de $\omega_{gc}$):** a inclinação e a fase definem as margens —
  crossover suave, idealmente $-20$ dB/década, dá PM folgada (a fase de uma inclinação
  $-20$ dB/dec sustentada é $\approx -90°$; de $-40$ dB/dec, $\approx -180°$ — relação
  ganho–fase de Bode, FBS cap. 12);
- **alta frequência:** $|L|$ caindo rápido ⟹ pouca injeção de ruído de medição e robustez
  a dinâmicas não modeladas.

Como $C$ multiplica $G$, seu Bode **soma** ao da planta: *loop shaping* é escolher $C$ para
"mover" as curvas de $L$ até essas três exigências.

### 4.2 Lendo o PID como shaping

Cada termo do PID aparece no Bode de $L$ como uma "região":

- **$K_p$:** desloca o módulo inteiro para cima/baixo — posiciona $\omega_{gc}$;
- **$1/(T_is)$:** sobe o ganho em baixa frequência (+20 dB/dec abaixo de $1/T_i$) — garante
  seguimento; custa fase perto do crossover se $1/T_i$ estiver perto de $\omega_{gc}$
  (regra: $1/T_i \lesssim \omega_{gc}/5$, i.e., $T_i$ não pequeno demais);
- **$T_ds$ (filtrado):** adianta a fase **no crossover** (até $+90°$ antes do canto do
  filtro) — compra PM; o filtro $N$ limita o preço em alta frequência.

O FBS (cap. 12) enfatiza ainda os **limites fundamentais**: o efeito "waterbed" da
sensibilidade ($S$ pequena numa faixa ⟹ grande em outra, por $\int\log|S|\,d\omega = 0$
para plantas estáveis), e o compromisso inescapável entre banda alta e robustez/ruído. Não
existe malha boa em todas as frequências — existe malha bem distribuída.

### 4.3 A receita do curso (Lab 10)

1. Marcar a $\omega_{gc}$ alvo: a mais alta compatível com o tempo morto
   ($\omega_{gc} \lesssim 1/\theta$, pois o tempo morto come $PM/\omega$ de margem);
2. **D:** $T_d$ para adiantar a fase no crossover até PM ≥ 45°–60°;
3. **I:** $T_i$ com canto $1/T_i$ bem abaixo de $\omega_{gc}$;
4. **P:** $K_p$ para colocar $|L| = 0$ dB na $\omega_{gc}$ alvo;
5. **Auditar** (§5): PM/GM/$M_s$ + simulação de degrau e perturbação.

---

## 5. Auditoria de robustez: a "gang of four"

*(Desenvolve FBS, caps. 10–12; Åström & Hägglund, cap. 5.)*

Com $L = CG$, definem-se a **sensibilidade** $S = \dfrac{1}{1+L}$ e a **sensibilidade
complementar** $T = \dfrac{L}{1+L}$ (note $S + T = 1$). Quatro funções de transferência
respondem às quatro combinações (referência/perturbação × saída/comando) — a *gang of
four*:

$$S = \frac{1}{1+CG},\qquad T = \frac{CG}{1+CG},\qquad
T_{du} = \frac{C}{1+CG} = CS,\qquad T_{dy} = \frac{G}{1+CG} = GS.$$

$T_{du}$ (perturbação/ruído → **comando**) mede o esforço de controle — é ela que revela
sinais de comando violentos que não aparecem na saída; $T_{dy}$ é a rejeição de
perturbações na entrada da planta. A auditoria do curso se resume a:

$$\boxed{PM \ge 45°,\qquad GM \ge 6\ \text{dB},\qquad M_s = \max_\omega|S(j\omega)| \le 2}$$

$M_s$ é a **mais completa** das três: $M_s \le 2$ garante $PM \ge 29°$ e $GM \ge 2$
automaticamente, e seu inverso é a distância mínima da curva de Nyquist ao ponto $-1$
($s_m = 1/M_s$, Unidade II, §6). Leitura de $M_s$ no tempo: $M_s$ grande ⟹ resposta
"reboteante" a perturbações — a saída volta à referência com oscilação pronunciada.

---

## 6. Dois graus de liberdade (2DOF): seguir sem chutar

*(Desenvolve Ogata, cap. 8 — PID de dois graus de liberdade, na íntegra; FBS, cap. 11;
Åström & Hägglund, cap. 4.)*

### 6.1 O conflito servo × regulatório

Com um único controlador na malha (um grau de liberdade, Figura 4.10), os polos de malha
fechada que atendem à perturbação são os mesmos que atendem à referência — e o zero do PID
(caminho da referência) provoca sobressinal a mudanças de setpoint mesmo quando a rejeição
de perturbações está perfeita. O 2DOF separa as duas tarefas: o **caminho da realimentação**
cuida de estabilidade/perturbação; um **pré-filtro da referência** cuida do seguimento.

### 6.2 O 2DOF do curso: dedução completa

Tome o PID (com D na medição) e pese a referência na ação proporcional por $b \in [0,1]$:

$$u = K_p\left(b\,r - y\right) + \frac{K_p}{T_i}\int e\,dt - K_pT_d\frac{dy}{dt}.$$

**Polos invariantes:** como o termo $b\,r$ entra somado *antes* dos mesmos blocos de $-y$
na malha, o denominador de $1 + CG$ **não contém $b$** — os polos de malha fechada não
mudam com $b$. A estabilidade e a rejeição de perturbações ficam intactas.

**O zero muda:** a FT de referência fica com numerador proporcional a
$\left(b + \dfrac{1}{T_is}\right) = \dfrac{bT_is + 1}{T_is}$ — um zero em
$s = -\dfrac{1}{bT_i}$. Com $b < 1$ o zero se afasta da origem e **sua contribuição ao
sobressinal cai**: $b = 1$ recupera o PID cheio; $b = 0$ remove totalmente o chute
proporcional à referência. Ajuste típico: $b \approx 0{,}3$–$0{,}5$ quando o setpoint muda
em degraus grandes.

### 6.3 As arquiteturas clássicas (Ogata, cap. 8)

O PI-D (D na medição, Figura 4.3) e o 2DOF acima são casos particulares de uma família —
as Figuras 4.10–4.13 mostram as formas do Ogata:

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-28-ogata.png)

**Figura 4.10 — Sistema de controle com um grau de liberdade: um único controlador
$G_c(s)$ decide sozinho entre referência e perturbação.** (Fonte: OGATA, Figura 8.28,
Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-27-ogata.png)

**Figura 4.11 — Sistema com controle I-PD: a ação integral fica no caminho direto sobre o
erro, enquanto P e D atuam na realimentação — a referência entra "limpa", sem zero
derivativo nem proporcional.** (Fonte: OGATA, Figura 8.27, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-29-ogata.png)

**Figura 4.12 — Sistema de controle com dois graus de liberdade: $G_{c1}$ na realimentação
garante estabilidade e rejeição; $G_{c2}$ (à frente da malha) molda a resposta à
referência.** (Fonte: OGATA, Figura 8.29, Cap. 8)

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-8-30-ogata.png)

**Figura 4.13 — Outra realização de 2DOF, com $G_{c2}$ atuando sobre o sinal de saída
$B(s)$ medido — forma conveniente quando há ruído de medição a filtrar.** (Fonte: OGATA,
Figura 8.30, Cap. 8)

> 📖 **Referências originais das Seções 4–6 (para conferência):** FBS, cap. 12 (loop
> shaping, gang of four, limites fundamentais) e cap. 11 (2DOF, setpoint weighting).
> Ogata, cap. 7 (frequência) e cap. 8 (PID modificado e 2DOF — FIGURAS 8.27–8.30). Nise,
> cap. 11 (projeto em frequência). Schaum, caps. 15–16. Penedo, cap. 10. Åström &
> Hägglund, caps. 4–5.

---

## 7. PID digital: do contínuo ao microcontrolador

*(Desenvolve Nise, cap. 13; Ogata, cap. 8; FBS, cap. 11; Åström & Hägglund, cap. 3;
transparências CDS 110 L9-2.)*

### 7.1 Amostragem, aliasing e o custo oculto de $h$

O computador só vê o sinal em instantes discretos $t = kh$. Duas consequências:

- **Aliasing (Nise, cap. 13):** frequências acima de $\omega_s/2$ (Nyquist da amostragem)
  são indistinguíveis de frequências mais baixas — um sinal de $3\omega_s/4$ aparece nos
  dados como se fosse de $\omega_s/4$. Consequência prática: **filtrar antes de amostrar**
  (o filtro derivativo e o filtro de medição do kit fazem esse papel) e escolher
  $\omega_s$ bem acima da banda da malha.
- **O ZOH atrasa (Nise, cap. 13):** entre amostras, o comando fica congelado (*zero-order
  hold*). O segurador de ordem zero tem FT
  $$G_{ZOH}(s) = \frac{1 - e^{-sh}}{s},$$
  e sua resposta a qualquer entrada é a entrada **atrasada em média de meio período**:
  na faixa da malha, o ZOH se comporta aproximadamente como um tempo morto $e^{-sh/2}$
  — verificável expandindo $(1-e^{-sh})/(sh) \approx e^{-sh/2}$ para $sh$ pequeno.
  Somando o atraso de cálculo, o controle digital adiciona ~$h$ de tempo morto efetivo.
  Daí a regra do curso: **$h \le \tau_{dominante}/20$** (e conferir a PM: o atraso $h/2$
  consome $\omega_{gc}h/2$ radianos de margem — mais um motivo para o margem de atraso da
  Unidade II, §5.1).

![](https://github.com/fabiobento/lab-cont-2026-2/raw/main/imagens/fig-13-4-nise.png)

**Figura 4.14 — O segurador de ordem zero: (a) amostragem ideal; (b) o sinal reconstruído
em degraus; (c) a saída efetiva — a entrada atrasada de, em média, meio período de
amostragem.** (Fonte: NISE, Figura 13.4, Cap. 13)

### 7.2 Discretização: Euler × Tustin

Duas receitas para converter $C(s)$ em equações a diferenças:

- **Euler regressivo:** $s \to \dfrac{1 - z^{-1}}{h}$ — derivada vira diferença para trás,
  $\dot e[k] \approx (e[k] - e[k-1])/h$. Simples e estável para o PID nas taxas do curso.
- **Tustin (trapezoidal):** $s \to \dfrac{2}{h}\dfrac{1 - z^{-1}}{1 + z^{-1}}$ — a
  aproximação por trapézios da integração. Preserva o mapeamento do semiplano esquerdo no
  círculo unitário e a resposta em frequência de $C$ (com *prewarping* no crossover, se a
  precisão importar). O `ct.sample_system(sys, h, method='tustin')` usa esta.

### 7.3 O PID digital do curso, deduzido

Partindo do PI-D filtrado (§2) e integrando o termo integral por Euler:

$$I[k] = I[k-1] + \frac{K_p h}{T_i}e[k],\qquad
D[k] = \alpha\big(y[k] - y[k-1]\big) + (1-\alpha)D[k-1],\quad
\alpha = \frac{NT_d}{NT_d + h},$$

$$u[k] = K_p\big(e[k] + T_dD[k]\big) + I[k]\quad\text{(antes da saturação e do anti-windup)}.$$

A forma recursiva do $D$ é exatamente a discretização por Euler do filtro
$\dfrac{T_ds}{1 + T_ds/N}$ — verifique substituindo $D = T_d\,\dot y_{filtrada}$. A
**saturação** se aplica depois do somatório; o **anti-windup** (back-calculation, Unidade
III, §2.2) entra como $\frac{h}{T_t}(u_{sat} - v)$ somado ao $I[k]$; a **transição sem
solavanco** (*bumpless transfer*) ao ligar a malha ou trocar de modo zera/reinicializa
$I$ para que $u$ comece no valor atual do atuador.

**Efeitos de $h$ na bancada (Lab 11 §4):** $h$ grande demais degrada a ação D (a diferença
fica ruidosa e atrasada), atrasa a malha (PM cai $\omega_{gc}h/2$ rad) e torna o anti-windup
lerdo; $h$ pequeno demais satura a CPU e torna as diferenças do encoder dominadas pela
quantização.

### Exercício resolvido 3 — escolhendo $h$

*A malha de temperatura do kit tem $\tau \approx 60$ s; a de velocidade, $\tau \approx 0{,}1$
s. Escolha $h$ para cada uma e estime a perda de PM.*

**Solução.** Temperatura: $h \le 60/20 = 3$ s ⟹ $h = 0{,}5$ s é folgado (o projeto sugere
0,1–0,5 s); com $\omega_{gc} \approx 0{,}1$ rad/s, perda de PM $\approx \omega_{gc}h/2 =
0{,}025$ rad $\approx 1{,}4°$ — desprezível.
Velocidade: $h \le 0{,}1/20 = 5$ ms ⟹ $h = 10$ ms **já é o dobro do recomendado**; com
$\omega_{gc} \approx 20$ rad/s, perda $\approx 20\times0{,}005 = 0{,}1$ rad $\approx 5{,}7°$
— pequena, mas não nula; na margem, soma-se ao atraso de cálculo. Conclusão prática: a malha
de velocidade é a mais exigente do kit em taxa de amostragem — é por isso que o firmware a
roda no laço mais rápido.

**Exercício adicional 7.A — Tustin na mão.**
*Discretize $C(s) = \dfrac{1}{s+1}$ por Tustin com $h = 0{,}1$ s e escreva a equação a
diferenças.*

**Solução.** $s \to \dfrac{2}{0{,}1}\dfrac{1-z^{-1}}{1+z^{-1}} = 20\dfrac{1-z^{-1}}{1+z^{-1}}$:
$$C(z) = \frac{1+z^{-1}}{20(1-z^{-1}) + (1+z^{-1})} = \frac{1+z^{-1}}{21 - 19z^{-1}}
\;\Rightarrow\; u[k] = \frac{19}{21}u[k-1] + \frac{1}{21}\big(e[k] + e[k-1]\big).$$
Confira no Lab 11 com `ct.sample_system(ct.tf([1],[1,1]), 0.1, method='tustin')`.

> 📖 **Referências originais desta seção (para conferência):** Nise, cap. 13 (sistemas
> digitais: amostragem, aliasing, ZOH — FIGURA 13.4 — e estabilidade no plano $z$). Ogata,
> cap. 8 (implementação). FBS, cap. 11 (implementação do PID) — transparências CDS 110 L9-2
> (código anti-windup e referência do `python-control`). Åström & Hägglund, cap. 3.

---

## 8. O procedimento completo (a receita do curso)

Do modelo ao código, na ordem em que os labs a constroem:

1. **Modelar/identificar** (Unidade I): FOPDT do seu kit por ensaio de degrau, validado
   contra um segundo ensaio;
2. **Sintonizar** (§3): lambda ($\lambda = \max(\theta, \tau/3)$) ou CHR, conforme a tarefa;
3. **Implementar direito** (§2): PI-D + filtro derivativo $N = 10$ + anti-windup por
   back-calculation + bumpless;
4. **Discretizar** (§7): $h \le \tau/20$; Euler ou Tustin; atraso de $h/2$ incluído na PM;
5. **Auditar** (§5): PM ≥ 45°, GM ≥ 6 dB, $M_s \le 2$, simulação de degrau, perturbação e
   comando; e se a malha ainda oscilar ou chutar na referência, revisitar §4 (shaping) e
   §6 (2DOF).

---

## 9. Resumo da unidade e conexão com os labs

| Conceito | Onde está nesta apostila | Onde pratica | Livro-âncora |
|---|---|---|---|
| P, I, D e seus efeitos | §1 (deduções Ogata cap. 5) | Lab 08 | Ogata 5 e 8 |
| Filtro D, derivada na medição | §2 (deduções completas) | Lab 08 §4–5 → Lab 10 | FBS 11; Ogata 8 |
| ZN por $K_u,T_u$ | §3.1 (tabela completa) | Lab 09 §3.2 (dados do relé) | Ogata 8; Å&H 4 |
| ZN por $K,\tau,\theta$ | §3.2 (tabela completa) | Lab 09 §3.3 | Ogata 8 |
| CHR / lambda | §3.3–3.4 (dedução IMC) | Lab 09 §3.4–3.5 | Å&H 5 |
| Loop shaping | §4 (receita) | Lab 10 §1 | FBS 12 |
| Gang of four e $M_s$ | §5 | Lab 10 §4 | FBS 10–12 |
| 2DOF / setpoint weighting | §6 (dedução) | Lab 10 §5 | Ogata 8; FBS 11 |
| Amostragem, aliasing, ZOH | §7.1 | Lab 11 §2–4 | Nise 13 |
| Equações a diferenças | §7.3 (deduzidas) | Lab 11 §5 + firmware | CDS 110 L9-2 |

**Autoavaliação antes da Lista 4:** você deve conseguir (i) escrever as três formas do PID
(ideal, filtrado, digital) e dizer por que cada modificação existe; (ii) sintonizar por ZN-1,
ZN-2 e lambda e comparar; (iii) auditar uma malha por PM/GM/$M_s$ e pela simulação das
quatro respostas da gang of four; (iv) explicar o que o $b$ do 2DOF preserva e o que ele
muda; (v) escolher e justificar $h$; (vi) escrever o PID digital completo com anti-windup.

---

## Mapa das fórmulas da Unidade IV (folha de consulta)

| Tema | Fórmulas-chave |
|---|---|
| PID ISA | $C = K_p(1 + 1/(T_is) + T_ds)$ |
| PID filtrado | $C = K_p\left(1 + \frac{1}{T_is} + \frac{T_ds}{1+T_ds/N}\right)$; ganho máx. do D: $K_pN$ |
| ZN-2 (frequência) | P: $0{,}5K_u$; PI: $0{,}45K_u$, $T_u/1{,}2$; PID: $0{,}6K_u$, $T_u/2$, $T_u/8$ |
| ZN-1 (curva de reação) | P: $T/(KL)$; PI: $0{,}9T/(KL)$, $L/0{,}3$; PID: $1{,}2T/(KL)$, $2L$, $0{,}5L$ |
| Lambda (PI, FOPDT) | $K_p = \frac{1}{K}\frac{\tau}{\lambda+\theta}$; $T_i = \tau$; $\lambda = \max(\theta, \tau/3)$ |
| Gang of four | $S = \frac{1}{1+L}$; $T = \frac{L}{1+L}$; $CS$; $GS$; $M_s = \max\|S\| \le 2$ |
| 2DOF | $u = K_p(br - y) + \frac{K_p}{T_i}\int e - K_pT_d\dot y$; zero em $-1/(bT_i)$; polos inalterados |
| Anti-windup | $\dot I = \frac{K_p}{T_i}e + \frac{1}{T_t}(u_{sat}-v)$; $T_t = \sqrt{T_iT_d}$ |
| Digital | ZOH ≈ atraso $h/2$; $h \le \tau/20$; Euler $s\to(1-z^{-1})/h$; Tustin $s\to\frac{2}{h}\frac{1-z^{-1}}{1+z^{-1}}$ |
| D digital | $D[k] = \alpha(y[k]-y[k-1]) + (1-\alpha)D[k-1]$, $\alpha = \frac{NT_d}{NT_d+h}$ |

---

## Leituras dirigidas da Unidade IV

**Esta apostila cobre integralmente o conteúdo abaixo** — use a tabela apenas para conferir
a formulação original:

| Prioridade | Fonte | O que ler | Onde está aqui |
|---|---|---|---|
| essencial | **Ogata**, cap. 8 | PID, métodos de sintonia (TABELAS 8.1–8.2, FIGURAS 8.1–8.5), PID modificado (FIGURAS 8.25–8.27) e 2DOF (FIGURAS 8.28–8.30) | §1–§3, §6 |
| essencial | **FBS**, caps. 11–12 | PID completo (filtro, windup, 2DOF) e projeto por loop shaping com a gang of four | §2, §4–§6 |
| essencial | **Nise**, cap. 13 | amostragem, aliasing, segurador de ordem zero (FIGURA 13.4) e plano $z$ | §7 |
| apoio | **Åström & Hägglund**, caps. 3–5 | implementação real, experimento do relé, métodos modernos (CHR, lambda) | §2–§3 |
| apoio | **Ogata**, cap. 5 · **Nise**, cap. 9 | efeitos das ações de controle; PID por lugar das raízes | §1, §4 |
| exercícios | **Schaum**, caps. 4, 15, 16 e 20 | Laplace, Bode, projeto em frequência e temas avançados | §1, §4 |
| computacional | **CDS 110** L9-1 e L9-2 | exercícios de PID com `python-control`; o código de referência do PID digital com anti-windup | Labs 08–11 |

## Referências bibliográficas

Ver a lista completa ao final de `apostila_unidade1_completa.md`, acrescentando:
- ÅSTRÖM, K. J.; HÄGGLUND, T. *Advanced PID Control*. ISA, 2006.
