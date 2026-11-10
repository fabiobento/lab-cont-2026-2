/*
 * pid_motor.ino — Laboratório de Controle Automático (Ifes Guarapari)
 * Projeto final — servo de posição angular no motor CC
 *
 * Kit do laboratório (MOTOR_REV07): Arduino Uno + shield com OLED SSD1306 +
 * ponte H L298N (IN1/IN2 acionados por PWM nos pinos 9/10, ENA com jumper) +
 * motor JGA25-370 6 V 210 rpm com roda + encoder Hall (C1 -> D2, C2 -> D4).
 *
 * VERSÃO 3 (2026-11): GRAVE UMA VEZ E CONFIGURE PELO NOTEBOOK.
 *   Ao ligar (ou quando o PC abre a porta serial, o que reinicia o Uno), o
 *   firmware escreve "# pronto" e espera ~2,5 s por linhas "CHAVE=valor"
 *   terminadas por "GO". A função coletar() de projeto_final/ferramentas_projeto.py
 *   faz isso por você:
 *       coletar("ma_p100", PORTA, MODO=1, PWM_MA=100, CPG=1.3167)
 *   Sem configuração (ex.: firmware/telemetry.py), valem os padrões abaixo.
 *
 * MODOS (chave MODO):
 *   0 CALIBRAÇÃO   motor desligado; gire a roda À MÃO; 5ª coluna = contas brutas
 *   1 MALHA ABERTA degrau de PWM_MA entre MA_INI e MA_FIM [ms]
 *   2 RELÉ         u = ±D (histerese H [graus]) em torno de REF [graus]
 *   3 PID          perfil de degraus R (graus) nos instantes TR (ms)
 *   4 PARTIDA      rampa lenta de PWM (RAMPA PWM/s, SINAL ±1) até o eixo se mover
 *   5 PRBS         PRBS entre BASE±AMP, bit de TB ms; 5ª coluna = contas na janela
 *                  de 20 ms (velocidade) — identificação do Trabalho 1
 *
 * Telemetria (CSV, 1 linha a cada 20 ms):  t, r, angle, pwm, u_pid
 *   t [s], r [graus], angle [graus], pwm [-255..255, o APLICADO],
 *   u_pid [PWM pedido pelo PID antes da saturação/compensação]
 *   (modo 0: contas brutas; modo 5: contas na janela)
 *
 * PID (2 graus de liberdade): u = kp·e + I − kd·N/(s+N)·s·y   (e = r − y)
 *   Euler:  dxf = N(−y − xf); uD = kd·dxf; xf += dxf·Ts
 *   clamping (AW=1): I += ki·e·Ts, exceto se saturado e o erro empurra mais fundo
 *   back-calculation (AW=2): I += (ki·e + (u_sat − u_c)/TT)·Ts
 *   compensação de zona morta: u_c = u_pid ± ZM quando |e| > EM
 */

// ---------------- hardware (kit MOTOR_REV07 — não altere) ----------------
const int PIN_IN1   = 9;    // L298N IN1 <- PWM (OC1A, Timer1 16 bits)
const int PIN_IN2   = 10;   // L298N IN2 <- PWM (OC1B, Timer1 16 bits)
const int PIN_ENC_A = 2;    // encoder C1 (interrupção INT0)
const int PIN_ENC_B = 4;    // encoder C2 (só leitura — D4 não tem interrupção)
const bool ENCODER_2X = true;   // as duas bordas de C1 (≈ 474 contas/volta)

// Display: atualizar o SSD1306 leva dezenas de ms — só antes e depois do ensaio.
// Se a biblioteca Adafruit_SSD1306 não estiver instalada, troque para 0.
#define USAR_OLED 1

const unsigned long Ts_us = 20000UL;   // período de amostragem (20 ms)

// ---------------- parâmetros configuráveis (padrões) ----------------
int   MODO = 3;
float CPG  = 1.0;         // contas por grau (Etapa de calibração)
float KP = 1.0, KI = 0.0, KD = 0.0, NF = 30.0;
int   PWM_MAX = 255, AW = 1, ZM = 0;
float TT = 0.2, EM = 0.0;
int   PWM_MA = 100;  unsigned long MA_INI = 500, MA_FIM = 2500;
int   D_RELE = 120;  float H_RELE = 1.0, REF_RELE = 0.0;
float RAMPA = 10.0;  int SINAL = 1;
int   BASE = 140, AMP = 80;  unsigned long TB = 200;
unsigned long T_MS = 0;   // duração; 0 = padrão do modo

const int MAX_DEG = 8;
int   N_DEG = 4;
float R_DEG[MAX_DEG]          = { 0, 90, -90, 0 };
unsigned long TR_MS[MAX_DEG]  = { 0, 2000, 7000, 12000 };

// ---------------- estado ----------------
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

// convenção do MOTOR_REV07: subida de C1 com C2 alto -> +1 (2x: C1 == C2 -> +1)
void isr_enc() {
  bool c1 = digitalRead(PIN_ENC_A), c2 = digitalRead(PIN_ENC_B);
  if (ENCODER_2X) { if (c1 == c2) enc_count++; else enc_count--; }
  else            { if (c2) enc_count++; else enc_count--; }
}

void setupPWM16() {                       // fast PWM 16 bits, ~244 Hz (como no MOTOR_REV07)
  DDRB |= _BV(PB1) | _BV(PB2);
  TCCR1A = _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11);
  TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS10);
  ICR1 = 0xFFFF;
  OCR1A = 0;
  OCR1B = 0;
}

void aplica_pwm(int u) {                  // u em [-255, 255] -> 16 bits (×257)
  u = constrain(u, -255, 255);
  unsigned int d = (unsigned int)abs(u) * 257U;
  if (u >= 0) { OCR1B = 0; OCR1A = d; }
  else        { OCR1A = 0; OCR1B = d; }
}

// ---------------- configuração pela serial ----------------
void le_lista_float(char* v, float* dst, int* n) {
  int k = 0; char* sp; char* tok = strtok_r(v, ",", &sp);
  while (tok && k < MAX_DEG) { dst[k++] = atof(tok); tok = strtok_r(NULL, ",", &sp); }
  *n = k;
}
void le_lista_ul(char* v, unsigned long* dst) {
  int k = 0; char* sp; char* tok = strtok_r(v, ",", &sp);
  while (tok && k < MAX_DEG) { dst[k++] = strtoul(tok, NULL, 10); tok = strtok_r(NULL, ",", &sp); }
}

void aplica_cfg(const char* k, char* v) {
  if      (!strcmp(k, "MODO"))    MODO = atoi(v);
  else if (!strcmp(k, "CPG"))     CPG = atof(v);
  else if (!strcmp(k, "KP"))      KP = atof(v);
  else if (!strcmp(k, "KI"))      KI = atof(v);
  else if (!strcmp(k, "KD"))      KD = atof(v);
  else if (!strcmp(k, "N"))       NF = atof(v);
  else if (!strcmp(k, "PWM_MAX")) PWM_MAX = atoi(v);
  else if (!strcmp(k, "AW"))      AW = atoi(v);
  else if (!strcmp(k, "TT"))      TT = atof(v);
  else if (!strcmp(k, "ZM"))      ZM = atoi(v);
  else if (!strcmp(k, "EM"))      EM = atof(v);
  else if (!strcmp(k, "PWM_MA"))  PWM_MA = atoi(v);
  else if (!strcmp(k, "MA_INI"))  MA_INI = strtoul(v, NULL, 10);
  else if (!strcmp(k, "MA_FIM"))  MA_FIM = strtoul(v, NULL, 10);
  else if (!strcmp(k, "D"))       D_RELE = atoi(v);
  else if (!strcmp(k, "H"))       H_RELE = atof(v);
  else if (!strcmp(k, "REF"))     REF_RELE = atof(v);
  else if (!strcmp(k, "RAMPA"))   RAMPA = atof(v);
  else if (!strcmp(k, "SINAL"))   SINAL = atoi(v) >= 0 ? 1 : -1;
  else if (!strcmp(k, "BASE"))    BASE = atoi(v);
  else if (!strcmp(k, "AMP"))     AMP = atoi(v);
  else if (!strcmp(k, "TB"))      TB = strtoul(v, NULL, 10);
  else if (!strcmp(k, "T"))       T_MS = strtoul(v, NULL, 10);
  else if (!strcmp(k, "R"))       le_lista_float(v, R_DEG, &N_DEG);
  else if (!strcmp(k, "TR"))      le_lista_ul(v, TR_MS);
  else { Serial.print("# chave desconhecida: "); Serial.println(k); }
}

void recebe_configuracao() {
  char buf[48];
  Serial.setTimeout(2500);                 // espera o PC por até 2,5 s
  while (true) {
    size_t n = Serial.readBytesUntil('\n', buf, sizeof(buf) - 1);
    if (n == 0) return;                    // ninguém mandou nada: usa os padrões
    buf[n] = 0;
    if (n > 0 && buf[n - 1] == '\r') buf[n - 1] = 0;
    if (!strcmp(buf, "GO")) return;
    char* eq = strchr(buf, '=');
    if (eq) { *eq = 0; aplica_cfg(buf, eq + 1); }
  }
}

unsigned long duracao_ms() {
  if (T_MS > 0) return T_MS;
  switch (MODO) {
    case 0: return 30000;
    case 1: return MA_FIM + 1000;
    case 2: return 6000;
    case 4: return 15000;
    case 5: return 30000;
    default: return 17000;
  }
}

float referencia_em(unsigned long t_ms) {
  float r = R_DEG[0];
  for (int i = 0; i < N_DEG; i++)
    if (t_ms >= TR_MS[i]) r = R_DEG[i];
  return r;
}

// LFSR de 8 bits do PRBS (mesmo do prbs_aquisicao.ino)
uint8_t lfsr = 0xA5;
int bit_prbs() {
  uint8_t b = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 4)) & 1;
  lfsr = (lfsr >> 1) | (b << 7);
  return b;
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
  oled("PRONTO", "aguarda PC");
#endif
  Serial.println("# pronto pid_motor v3");
  recebe_configuracao();

  Serial.print("# MODO="); Serial.print(MODO);
  Serial.print(" CPG="); Serial.print(CPG, 4);
  Serial.print(" KP="); Serial.print(KP, 4);
  Serial.print(" KI="); Serial.print(KI, 4);
  Serial.print(" KD="); Serial.print(KD, 4);
  Serial.print(" N="); Serial.print(NF, 1);
  Serial.print(" PWM_MAX="); Serial.print(PWM_MAX);
  Serial.print(" AW="); Serial.print(AW);
  Serial.print(" ZM="); Serial.print(ZM);
  Serial.print(" EM="); Serial.println(EM, 2);
  Serial.println("# t[s],r[graus],angle[graus],pwm,u_pid");
  {
    char l2[12];
    snprintf(l2, sizeof(l2), "MODO %d", MODO);
    oled("ENSAIO", l2);
  }

  const float Ts = Ts_us / 1.0e6;
  const unsigned long T_FIM = duracao_ms();
  float I = 0.0, xf = 0.0;
  int u_rele = 0;
  int u_prbs = BASE + AMP;
  unsigned long t_bit = TB;
  long c_prev = 0;
  bool moveu = false;
  unsigned long t_moveu = 0;

  noInterrupts(); enc_count = 0; interrupts();
  if (MODO == 5) aplica_pwm(u_prbs);           // PRBS: primeiro nível já em t = 0

  unsigned long t0 = micros();
  unsigned long t_am = t0;

  while (true) {
    if ((unsigned long)(micros() - t_am) < Ts_us) continue;
    t_am += Ts_us;                                    // relógio sem deriva
    unsigned long t_ms = (t_am - t0) / 1000UL;
    if (t_ms > T_FIM) break;

    noInterrupts();
    long c = enc_count;
    interrupts();
    float y = c / CPG;
    float r = 0.0, u_pid = 0.0;
    int u = 0;

    if (MODO == 0) {                                  // ---- CALIBRAÇÃO ----
      u_pid = (float)c;
    }
    else if (MODO == 1) {                             // ---- MALHA ABERTA ----
      u = (t_ms >= MA_INI && t_ms < MA_FIM) ? PWM_MA : 0;
      u_pid = u;
    }
    else if (MODO == 2) {                             // ---- RELÉ ----
      r = REF_RELE;
      float e = r - y;
      if (e >  H_RELE) u_rele =  D_RELE;
      if (e < -H_RELE) u_rele = -D_RELE;
      if (u_rele == 0) u_rele = D_RELE;
      u = u_rele;
      u_pid = u;
    }
    else if (MODO == 4) {                             // ---- PARTIDA (rampa) ----
      if (!moveu && labs(c) >= 3) { moveu = true; t_moveu = t_ms; }
      if (moveu) { u = 0; if (t_ms > t_moveu + 300) break; }
      else {
        float a = RAMPA * (t_ms / 1000.0);
        if (a > 150) a = 150;
        u = SINAL * (int)a;
      }
      u_pid = u;
    }
    else if (MODO == 5) {                             // ---- PRBS ----
      u_pid = (float)(c - c_prev);                    // contas na janela que terminou
      c_prev = c;
      if (t_ms >= t_bit) { u_prbs = bit_prbs() ? BASE + AMP : BASE - AMP; t_bit += TB; }
      u = u_prbs;
    }
    else {                                            // ---- PID ----
      r = referencia_em(t_ms);
      float e = r - y;
      float dxf = NF * (-y - xf);
      float uD = KD * dxf;
      xf += dxf * Ts;
      u_pid = KP * e + I + uD;
      float u_c = u_pid;
      if (ZM > 0 && fabs(e) > EM) {
        if (u_pid > 0) u_c += ZM;
        else if (u_pid < 0) u_c -= ZM;
      }
      float u_sat = constrain(u_c, -PWM_MAX, PWM_MAX);
      if (AW == 1) {
        bool empurra = (u_c >= PWM_MAX && e > 0) || (u_c <= -PWM_MAX && e < 0);
        if (!empurra) I += KI * e * Ts;
      } else if (AW == 2) {
        I += (KI * e + (u_sat - u_c) / TT) * Ts;
      } else {
        I += KI * e * Ts;
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
    oled("FIM", l2);
  }
}

void loop() {
  // ensaio único; o próximo coletar() reinicia a placa ao abrir a porta
}
