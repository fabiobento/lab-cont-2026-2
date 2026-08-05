/*
 * prbs_aquisicao.ino — Laboratório de Controle Automático (Ifes Guarapari)
 * Trabalho 1 — Identificação FOPDT do motor CC com PRBS
 *
 * Gera um PRBS no PWM (ponte H), estima a velocidade pelo encoder
 * magnético e envia pela serial linhas CSV:  t,u,y
 *   t [s], u = PWM aplicado [-255..255], y = velocidade [contas/janela]
 *
 * Ajuste as constantes abaixo conforme a bancada.
 */

// ---------------- Pinos (ajuste para a sua ponte H / encoder) ----------------
const int PIN_PWM   = 9;    // ENA da ponte H (PWM)
const int PIN_IN1   = 7;    // IN1 (sentido)
const int PIN_IN2   = 8;    // IN2 (sentido)
const int PIN_ENC_A = 2;    // encoder canal A (interrupção)
const int PIN_ENC_B = 3;    // encoder canal B (interrupção)

// ---------------- Parâmetros do experimento ----------------
unsigned long Tb_ms   = 500;      // período de cada bit do PRBS [ms]  (regra: tau/5 .. tau/2)
unsigned long T_ms    = 60000;    // duração total do ensaio [ms]
const int  PWM_BASE   = 140;      // nível central do PRBS (0..255)
const int  PWM_AMP    = 80;       // amplitude do PRBS em torno do nível central
unsigned long Ts_ms   = 20;       // janela de amostragem/telemetria [ms]

// ---------------- Encoder ----------------
volatile long enc_count = 0;

void isr_enc() {
  // quadratura simples: sentido pelo canal B
  if (digitalRead(PIN_ENC_B)) enc_count++;
  else                        enc_count--;
}

// ---------------- PRBS (LFSR de 8 bits, polinômio x^8+x^6+x^5+x^4+1) ----------------
uint8_t lfsr = 0xA5;
uint8_t prbs_bit() {
  uint8_t bit = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 4)) & 1;
  lfsr = (lfsr >> 1) | (bit << 7);
  return bit;
}

// ---------------- Atuador ----------------
void aplica_pwm(int u) {
  u = constrain(u, -255, 255);
  if (u >= 0) { digitalWrite(PIN_IN1, HIGH); digitalWrite(PIN_IN2, LOW); }
  else        { digitalWrite(PIN_IN1, LOW);  digitalWrite(PIN_IN2, HIGH); }
  analogWrite(PIN_PWM, abs(u));
}

void setup() {
  pinMode(PIN_PWM, OUTPUT);
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_ENC_A, INPUT_PULLUP);
  pinMode(PIN_ENC_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_A), isr_enc, RISING);

  Serial.begin(115200);
  while (!Serial) { ; }
  Serial.println("# prbs_aquisicao — t[s],u[pwm],y[contas/janela]");

  unsigned long t0 = millis();
  unsigned long t_bit = t0;      // último instante de troca de bit
  unsigned long t_am  = t0;      // último instante de amostragem
  long enc_prev = 0;
  int u = PWM_BASE + PWM_AMP;    // primeiro nível

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
