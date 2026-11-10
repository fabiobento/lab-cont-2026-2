/*
 * pid_motor.ino — Laboratório de Controle Automático (Ifes Guarapari)
 * Projeto final / Trabalho 2 — servo de posição angular no motor CC
 *
 * Kit do laboratório (MOTOR_REV07): Arduino Uno + shield com OLED SSD1306 +
 * ponte H L298N (IN1/IN2 acionados por PWM nos pinos 9/10, ENA com jumper) +
 * motor JGA25-370 6 V 210 rpm com roda + encoder Hall (C1 -> D2, C2 -> D4).
 *
 * VERSÃO 2 (2026-11) — mudanças em relação à versão 1:
 *   - o laço trabalha em GRAUS (não em contas): os ganhos projetados com
 *     G_p(s) em [graus/PWM] entram DIRETO no firmware (kp em PWM/grau etc.);
 *   - 4 modos de ensaio (calibração, malha aberta, relé, malha fechada);
 *   - anti-windup selecionável: nenhum / clamping / back-calculation;
 *   - compensação opcional da zona morta da ponte H + motor;
 *   - PWM_MAX ajustável (para provocar a saturação no ensaio da espec. 4);
 *   - amostragem com micros() e relógio sem deriva;
 *   - telemetria com 5 colunas:  t,r,angle,pwm,u_pid
 *
 * Realização digital do PID (forma paralela, 2 graus de liberdade):
 *
 *   u_pid = kp*e + I + uD
 *   e     = r - y                         (proporcional sobre o ERRO)
 *   uD    = kd * N/(s+N) * s * (-y)       (derivada FILTRADA sobre a MEDIÇÃO —
 *                                          sem "chute derivativo"; teoria M2 §2.5.3)
 *   I     = ki * integral(e)              (integrador guardado em unidades de PWM)
 *
 *   Discretização (Euler progressivo, período Ts):
 *     dxf  = N*(-y - xf);   uD = kd*dxf;   xf += dxf*Ts
 *     clamping (M4 §4.2.3):      I += ki*e*Ts, EXCETO se saturado e o erro
 *                                empurra mais fundo na saturação
 *     back-calculation (§4.2.4): I += (ki*e + (u - u_pid)/TT)*Ts
 *
 * Telemetria serial (CSV, uma linha por amostra):
 *   t [s], r [graus], angle [graus], pwm [-255..255 — o que foi APLICADO],
 *   u_pid [PWM pedido pelo controlador ANTES da saturação e da compensação]
 *   Colete com:  python firmware/telemetry.py --porta COMx --saida ensaio.csv
 */

// =====================================================================
// 1) PINOS E HARDWARE (kit MOTOR_REV07 — não altere sem conferir a placa)
// =====================================================================
const int PIN_IN1   = 9;    // L298N IN1 <- PWM (OC1A, Timer1 16 bits)
const int PIN_IN2   = 10;   // L298N IN2 <- PWM (OC1B, Timer1 16 bits)
const int PIN_ENC_A = 2;    // encoder C1 (interrupção INT0)
const int PIN_ENC_B = 4;    // encoder C2 (só leitura — D4 não tem interrupção)

// Contagem do encoder: 1x = só borda de subida de C1 (como o MOTOR_REV07: 237
// contas/volta); 2x = as duas bordas de C1 (≈ 474 contas/volta, resolução 2x melhor).
const bool ENCODER_2X = true;

// Display OLED do shield: atualizar o SSD1306 leva dezenas de ms (I2C) e
// destruiria o período de amostragem — ele só é usado ANTES e DEPOIS do ensaio.
// Se a biblioteca Adafruit_SSD1306 não estiver instalada, troque para 0.
#define USAR_OLED 1

// =====================================================================
// 2) MODO DE ENSAIO
// =====================================================================
//   0 = CALIBRACAO   : motor desligado; gire o eixo À MÃO n voltas e leia as contas
//   1 = MALHA_ABERTA : degrau de PWM fixo (medição de k' / ganho de posição)
//   2 = RELE         : experimento do relé (Åström–Hägglund) em torno de REF_RELE
//   3 = MALHA_FECHADA: PID com o perfil de referências em degraus
const int MODO = 3;

// =====================================================================
// 3) CONVERSÃO CONTAS <-> GRAUS  (medir no modo 0 — Etapa 0 do projeto)
// =====================================================================
// contas_por_grau = (contas lidas após n voltas) / (360 * n)
// Referência do kit: 237 contas/volta em 1x (0,658) -> ≈ 474 em 2x (≈ 1,317). MEÇA a sua.
const float CONTAS_POR_GRAU = 1.0;   // AJUSTAR para a sua bancada

// =====================================================================
// 4) PID — ganhos em unidades de GRAUS (resultado do seu projeto)
// =====================================================================
float kp = 1.0;     // [PWM/grau]
float ki = 0.0;     // [PWM/(grau.s)]
float kd = 0.0;     // [PWM.s/grau]
const float N_FILT = 30.0;   // polo do filtro da derivada [rad/s] (teoria M2 §2.5.3)

// =====================================================================
// 5) REALIZAÇÃO
// =====================================================================
const unsigned long Ts_us = 20000UL;  // período de amostragem [us] (20 ms)
int PWM_MAX = 255;                    // limite do PWM — reduza (ex.: 100) no ensaio da espec. 4
const int AW_MODO = 1;                // 0 = sem anti-windup, 1 = clamping, 2 = back-calculation
const float TT = 0.2;                 // constante de rastreamento da back-calculation [s]
const int ZM_COMP = 0;                // compensação da zona morta [PWM] (0 = desligada)
const float E_MORTO = 0.0;            // |e| abaixo disto [graus] -> não aplica a compensação

// =====================================================================
// 6) PERFIS DE ENSAIO
// =====================================================================
// MODO 3: perfil de referências (degraus, em graus)
const int N_DEGRAUS = 4;
float perfil_graus[N_DEGRAUS]        = { 0, 90, -90, 0 };
unsigned long degrau_ms[N_DEGRAUS]   = { 0, 2000, 7000, 12000 };   // instantes de troca
unsigned long T_FIM_MS = 17000;

// MODO 1: degrau de PWM em malha aberta
const int  PWM_MA       = 150;     // amplitude A do degrau de PWM
const unsigned long MA_INICIO_MS = 500;    // instante do degrau
const unsigned long MA_FIM_MS    = 2500;   // instante em que o PWM volta a zero
// (o ensaio continua por mais 1 s para registrar a desaceleração)

// MODO 2: relé  u = +D_RELE se e > H_RELE ; -D_RELE se e < -H_RELE ; mantém entre os dois
const int   D_RELE   = 120;     // amplitude do relé [PWM]  (bem acima da zona morta!)
const float H_RELE   = 1.0;     // histerese [graus] (>= 1 resolução do encoder)
const float REF_RELE = 0.0;     // referência [graus]
const unsigned long RELE_FIM_MS = 6000;

// MODO 0: duração da calibração (gire o eixo à mão durante esse tempo)
const unsigned long CAL_FIM_MS = 30000;

// =====================================================================
// ESTADO
// =====================================================================
#if USAR_OLED
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
Adafruit_SSD1306 display(128, 64, &Wire, -1);
void oled(const char* l1, const char* l2) {
  display.clearDisplay(); display.setTextSize(2); display.setTextColor(WHITE);
  display.setCursor(0, 0);  display.println(l1);
  display.setCursor(0, 24); display.println(l2);
  display.display();
}
#else
void oled(const char*, const char*) {}
#endif

volatile long enc_count = 0;
float I  = 0.0;      // termo integral [PWM]
float xf = 0.0;      // estado do filtro da derivada [graus]
int   u_rele = 0;    // estado do relé

// Mesma convenção de sentido do MOTOR_REV07: borda de subida de C1 com C2 em
// nível alto -> conta para cima. No modo 2x, a borda de descida de C1 com C2
// em nível baixo também conta para cima (C1 == C2 -> +1; C1 != C2 -> -1).
void isr_enc() {
  bool c1 = digitalRead(PIN_ENC_A), c2 = digitalRead(PIN_ENC_B);
  if (ENCODER_2X) { if (c1 == c2) enc_count++; else enc_count--; }
  else            { if (c2) enc_count++; else enc_count--; }
}

// PWM de 16 bits no Timer1 (fast PWM, TOP = 0xFFFF, ~244 Hz), como no MOTOR_REV07
void setupPWM16() {
  DDRB |= _BV(PB1) | _BV(PB2);
  TCCR1A = _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11);
  TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS10);
  ICR1 = 0xFFFF;
  OCR1A = 0;
  OCR1B = 0;
}

// u em [-255, 255] (mesma escala de PWM do Trabalho 1) -> 16 bits (×257)
void aplica_pwm(int u) {
  u = constrain(u, -255, 255);
  unsigned int d = (unsigned int)abs(u) * 257U;
  if (u >= 0) { OCR1B = 0; OCR1A = d; }     // IN1 = PWM, IN2 = 0
  else        { OCR1A = 0; OCR1B = d; }     // IN1 = 0,   IN2 = PWM
}

float referencia_em(unsigned long t_ms) {
  float r = perfil_graus[0];
  for (int i = 0; i < N_DEGRAUS; i++)
    if (t_ms >= degrau_ms[i]) r = perfil_graus[i];
  return r;
}

unsigned long duracao_ms() {
  if (MODO == 0) return CAL_FIM_MS;
  if (MODO == 1) return MA_FIM_MS + 1000;
  if (MODO == 2) return RELE_FIM_MS;
  return T_FIM_MS;
}

void setup() {
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_ENC_A, INPUT);
  pinMode(PIN_ENC_B, INPUT);
  setupPWM16();
  aplica_pwm(0);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_A), isr_enc, ENCODER_2X ? CHANGE : RISING);

  Serial.begin(115200);
  while (!Serial) { ; }
#if USAR_OLED
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
#endif
  {
    char l2[12];
    snprintf(l2, sizeof(l2), "MODO %d", MODO);
    oled("ENSAIO", l2);                           // o display NÃO é atualizado durante o ensaio
  }
  Serial.print("# pid_motor v2 — MODO=");
  Serial.print(MODO);
  Serial.print(" kp="); Serial.print(kp, 4);
  Serial.print(" ki="); Serial.print(ki, 4);
  Serial.print(" kd="); Serial.print(kd, 4);
  Serial.print(" N=");  Serial.print(N_FILT, 1);
  Serial.print(" PWM_MAX="); Serial.print(PWM_MAX);
  Serial.print(" AW="); Serial.print(AW_MODO);
  Serial.print(" ZM_COMP="); Serial.println(ZM_COMP);
  Serial.println("# t[s],r[graus],angle[graus],pwm,u_pid");

  const float Ts = Ts_us / 1.0e6;
  const unsigned long T_FIM = duracao_ms();
  unsigned long t0 = micros();
  unsigned long t_am = t0;

  while (true) {
    if ((unsigned long)(micros() - t_am) < Ts_us) continue;
    t_am += Ts_us;                                   // relógio sem deriva
    unsigned long t_ms = (t_am - t0) / 1000UL;
    if (t_ms > T_FIM) break;

    noInterrupts();
    long c = enc_count;
    interrupts();
    float y = c / CONTAS_POR_GRAU;                   // posição [graus]
    float r = 0.0, u_pid = 0.0;
    int u = 0;

    if (MODO == 0) {                                 // ---- CALIBRAÇÃO ----
      u = 0;
      u_pid = (float)c;                              // 5ª coluna = contas brutas
    }
    else if (MODO == 1) {                            // ---- MALHA ABERTA ----
      u = (t_ms >= MA_INICIO_MS && t_ms < MA_FIM_MS) ? PWM_MA : 0;
      u_pid = u;
    }
    else if (MODO == 2) {                            // ---- RELÉ ----
      r = REF_RELE;
      float e = r - y;
      if (e >  H_RELE) u_rele =  D_RELE;
      if (e < -H_RELE) u_rele = -D_RELE;
      if (u_rele == 0) u_rele = D_RELE;              // partida
      u = u_rele;
      u_pid = u;
    }
    else {                                           // ---- MALHA FECHADA (PID) ----
      r = referencia_em(t_ms);
      float e = r - y;

      // derivada filtrada sobre a medição
      float dxf = N_FILT * (-y - xf);
      float uD = kd * dxf;
      xf += dxf * Ts;

      // PID antes do limitador
      u_pid = kp * e + I + uD;

      // compensação da zona morta (opcional): soma ZM_COMP no sentido do comando
      float u_c = u_pid;
      if (ZM_COMP > 0 && fabs(e) > E_MORTO) {
        if (u_pid > 0) u_c += ZM_COMP;
        else if (u_pid < 0) u_c -= ZM_COMP;
      }

      // limitador DENTRO do controlador (M4 §4.2.5, obs. 1)
      float u_sat = constrain(u_c, -PWM_MAX, PWM_MAX);

      // anti-windup
      if (AW_MODO == 1) {                            // clamping
        bool empurra = (u_c >= PWM_MAX && e > 0) || (u_c <= -PWM_MAX && e < 0);
        if (!empurra) I += ki * e * Ts;
      } else if (AW_MODO == 2) {                     // back-calculation
        I += (ki * e + (u_sat - u_c) / TT) * Ts;
      } else {                                       // sem proteção (demonstração do windup)
        I += ki * e * Ts;
      }
      u = (int)u_sat;
    }

    aplica_pwm(u);

    Serial.print((t_am - t0) / 1.0e6, 3); Serial.print(",");
    Serial.print(r, 2);                   Serial.print(",");
    Serial.print(y, 2);                   Serial.print(",");
    Serial.print(u);                      Serial.print(",");
    Serial.println(u_pid, 1);
  }

  aplica_pwm(0);
  Serial.println("# fim do ensaio");
  {
    noInterrupts(); long c = enc_count; interrupts();
    char l2[16];
    snprintf(l2, sizeof(l2), "%ld cts", c);
    oled("FIM", l2);                              // MODO 0: contas totais da calibração
  }
}

void loop() {
  // ensaio único; resete a placa para repetir
}
