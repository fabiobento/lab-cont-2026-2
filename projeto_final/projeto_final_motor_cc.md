# Projeto Final — Servo de Posição com Motor CC: da Identificação à Malha Fechada Real

**Laboratório de Controle Automático — Engenharia Elétrica — Ifes Campus Guarapari**
**Lançamento:** semana 14 (junto ao Trabalho 2) · **Apresentações:** semana 15 (semana de seminários, conforme calendário) · **Grupos:** até 2 integrantes

---

## 1. Visão geral

O projeto final **integra os Trabalhos 1 e 3** e fecha o ciclo completo da disciplina sobre o mesmo hardware (Arduino + ponte H + motor CC + encoder magnético):

```
identificação (PRBS/FOPDT)  →  projeto do controlador (plano-s e/ou frequência)
     Trabalho 1                    Módulos 2 e 3
                                   ↓
     validação final  ←  implementação embarcada (PID digital + anti-windup)
     semana 15                 Trabalho 2 + Módulo 4
```

Cada grupo deverá projetar, implementar e validar um **servo de posição angular**: dado um perfil de referências (degraus 0° → 90° → −90° → 0°), a posição do eixo deve segui-lo atendendo às especificações da Seção 3, com o controlador **rodando no Arduino** (firmware `firmware/pid_motor/`).

## 2. Relação com os trabalhos

| Entrega anterior | O que entra no projeto |
|---|---|
| Trabalho 1 | Modelo FOPDT de velocidade $G_v(s) = Ke^{-Ls}/(\tau s+1)$, dados e código de identificação |
| Trabalho 2 | Modelo de posição $G_p(s) = Kk'/[s(\tau s+1)]$, sintonia do PID e primeiros ensaios |
| **Projeto final** | **Versão final** de ambos + atendimento às especificações + análise de robustez + demonstração ao vivo |

Quem já entregou os Trabalhos 1 e 3 **reutiliza** os resultados (corrigindo o que foi apontado); quem não entregou deve executar os roteiros completos dos dois trabalhos.

## 3. Especificações de desempenho

Para o degrau de referência de 90° (posição angular do eixo):

1. **Erro de regime nulo** ($|e_{ss}| < 2°$, resolução do encoder);
2. **Sobressinal** $M_p \le 15\%$;
3. **Tempo de estabelecimento** $t_s \le 2{,}5$ s (critério de ±5%);
4. **Sem windup visível**: com o PWM saturando durante o degrau, o sobressinal não pode crescer mais que 5 pontos percentuais em relação ao ensaio sem saturação — o anti-windup deve estar ativo e demonstrado (ligado × desligado).

As especificações 1–3 devem ser mostradas **em simulação** (modelo identificado) e **na planta real** (telemetria). Divergências entre os dois devem ser explicadas.

## 4. Conteúdo mínimo do relatório/presentação

1. **Identificação** (T1): PRBS, modelo FOPDT, validação modelo × dados, discussão do atraso;
2. **Modelo de posição** (T3): medição de $k'$, modelo final $G_p(s)$;
3. **Projeto do controlador**: método escolhido (LGR, frequência ou relé/ZN + refinamento), contas principais, margens de ganho/fase da malha projetada (`control.margin`);
4. **Realização digital**: equações de recorrência implementadas no firmware (PID ISA 2DOF, derivada filtrada sobre a medição, anti-windup por clamping ou back-calculation), período de amostragem escolhido e justificativa;
5. **Validação experimental**: gráficos referência × posição × PWM; tabela de métricas medidas × simuladas; demonstração do anti-windup (especificação 4);
6. **Discussão de não linearidades** (Módulo 4): saturação do PWM, zona morta da ponte H/motor e resolução do encoder — onde cada uma aparece nos seus dados e como foi contornada;
7. **Conclusão**: o que faria diferente; limitações do modelo FOPDT.

## 5. Cronograma e avaliação

| Semana | Marco |
|---|---|
| 14 | Lançamento (com o Trabalho 2); revisão do modelo e projeto do controlador |
| 15 | Ensaios finais, ajustes e **apresentação** (10 min + 5 min de arguição) |

**Avaliação (rubrica):**

| Critério | Peso |
|---|---|
| Identificação e validação do modelo | 20% |
| Projeto do controlador (método, contas, margens) | 25% |
| Atendimento às especificações na planta real | 30% |
| Demonstração e discussão do anti-windup/não linearidades | 15% |
| Apresentação e arguição | 10% |

> **Consulte (roteiro de estudos para o projeto):**
> - Identificação/Padé — `teoria_modulo2.md` §2.5.6 e Lab 09;
> - Projeto PD/PI/PID — `teoria_modulo2.md` §2.3–2.5 (plano-s) ou `teoria_modulo3.md` §3.4–3.5 (frequência);
> - PID digital, saturação e anti-windup — `teoria_modulo4.md` §4.1–4.2 e Lab 16;
> - Sintonia alternativa pelo relé — `teoria_modulo4.md` §4.3 e Lab 16, Parte 4.

**Bom projeto!**
