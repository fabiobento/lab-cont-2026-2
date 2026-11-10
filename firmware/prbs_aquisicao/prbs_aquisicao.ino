/*
 * prbs_aquisicao.ino — Laboratório de Controle Automático (Ifes Guarapari)
 * Trabalho 1 — Identificação FOPDT do motor CC com PRBS
 *
 * Gera um PRBS no PWM (ponte H), estima a velocidade pelo encoder
 * magnético e envia pela serial linhas CSV:  t,u,y
 *   t [s], u = PWM aplicado [-255..255], y = velocidade [contas/janela]
 *
 * Kit MOTOR_REV07: L298N com IN1/IN2 em PWM nos pinos 9/10 (Timer1, 16 bits),
 * encoder C1 -> D2 (interrupção), C2 -> D4. Ajuste as constantes abaixo.
 *
 * Diferença em relação ao firmware MOTOR_REV07: lá um script no PC (Python ou
 * MATLAB) comandava o PWM e consultava a velocidade pela serial a cada
 * iteração, e o atraso dessa troca de mensagens aparecia no modelo (dezenas de
 * ms). Aqui o PRBS e a amostragem rodam no Arduino, com período fixo.
 */

// ---------------- Pinos (kit MOTOR_REV07) ----------------
const int PIN_IN1   = 9;    // L298N IN1 <- PWM (OC1A)
const int PIN_IN2   = 10;   // L298N IN2 <- PWM (OC1B)
const int PIN_ENC_A = 2;    // encoder C1 (interrupção)
const int PIN_ENC_B = 4;    // encoder C2

// ---------------- Parâmetros do experimento ----------------
unsigned long Tb_ms   = 200;      // período de cada bit do PRBS [ms]  (kit: tau ≈ 80 ms -> 100..300 ms)
unsigned long T_ms    = 30000;    // duração total do ensaio [ms]
const int  PWM_BASE   = 140;      // nível central do PRBS (0..255)
const int  PWM_AMP    = 80;       // amplitude do PRBS em torno do nível central
unsigned long Ts_ms   = 20;       // janela de amostragem/telemetria [ms]

// ---------------- Encoder ----------------
volatile long enc_count = 0;

// Contagem 2x (as duas bordas de C1; ≈ 474 contas/volta no kit) — a MESMA do
// pid_motor.ino, para que CONTAS_POR_GRAU valha nos dois firmwares.
// Sentido como no MOTOR_REV07: C1 == C2 -> +1; C1 != C2 -> -1.
void isr_enc() {
  if (digitalRead(PIN_ENC_A) == digitalRead(PIN_ENC_B)) enc_count++;
  else                                                  enc_count--;
}

// ---------------- PRBS (LFSR de 8 bits, polinômio x^8+x^6+x^5+x^4+1) ----------------
uint8_t lfsr = 0xA5;
uint8_t prbs_bit() {
  uint8_t bit = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 4)) & 1;
  lfsr = (lfsr >> 1) | (bit << 7);
  return bit;
}

// ---------------- Atuador: PWM de 16 bits no Timer1 (como no MOTOR_REV07) ----------------
void setupPWM16() {
  DDRB |= _BV(PB1) | _BV(PB2);
  TCCR1A = _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11);
  TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS10);
  ICR1 = 0xFFFF;
  OCR1A = 0;
  OCR1B = 0;
}

void aplica_pwm(int u) {                       // u em [-255, 255] -> 16 bits (×257)
  u = constrain(u, -255, 255);
  unsigned int d = (unsigned int)abs(u) * 257U;
  if (u >= 0) { OCR1B = 0; OCR1A = d; }
  else        { OCR1A = 0; OCR1B = d; }
}

void setup() {
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_ENC_A, INPUT);
  pinMode(PIN_ENC_B, INPUT);
  setupPWM16();
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_A), isr_enc, CHANGE);

  Serial.begin(115200);
  while (!Serial) { ; }
  Serial.println("# prbs_aquisicao — t[s],u[pwm],y[contas/janela]");

  unsigned long t0 = millis();
  unsigned long t_bit = t0;      // último instante de troca de bit
  unsigned long t_am  = t0;      // último instante de amostragem
  long enc_prev = 0;
  int u = PWM_BASE + PWM_AMP;    // primeiro nível
  aplica_pwm(u);                 // aplica já em t = 0 (antes, só era aplicado na 1ª troca de bit)

  while (millis() - t0 < T_ms) {
    unsigned long agora = millis();

    // troca o bit do PRBS a cada Tb
    if (agora - t_bit >= Tb_ms) {
      t_bit = agora;
      u = prbs_bit() ? (PWM_BASE + PWM_AMP) : (PWM_BASE - PWM_AMP);
      aplica_pwm(u);
    }

    // telemetria a cada Ts
    if (agora - t_am >= Ts_ms) {
      t_am = agora;
      noInterrupts();
      long c = enc_count;
      interrupts();
      long y = c - enc_prev;     // contas na janela = velocidade (escala constante)
      enc_prev = c;

      Serial.print((agora - t0) / 1000.0, 3);
      Serial.print(",");
      Serial.print(u);
      Serial.print(",");
      Serial.println(y);
    }
  }

  aplica_pwm(0);                 // fim do ensaio: desliga o motor
  Serial.println("# fim do ensaio");
}

void loop() {
  // ensaio único; resete a placa para repetir (após ajustar Tb/T se necessário)
}
