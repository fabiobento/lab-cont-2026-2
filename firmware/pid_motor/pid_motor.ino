/*
 * pid_motor.ino — Laboratório de Controle Automático (Ifes Guarapari)
 * Trabalho 2 / Projeto final — PID de posição angular no motor CC
 *
 * Realização digital (forma ISA, 2 graus de liberdade):
 *   - derivada FILTRADA sobre a MEDIÇÃO:  xf' = N*(-y - xf);  uD = kd*xf'
 *     (evita o "chute derivativo" em degraus de referência — ver teoria M2 §2.5)
 *   - anti-windup por CLAMPING: congela o integrador quando o PWM está
 *     saturado E o erro tem o mesmo sinal da saturação (teoria M4 §4.2)
 *   - perfil de referências em degraus: 0° -> 90° -> -90° -> 0°
 *
 * Telemetria serial (CSV):  t,r,angle,pwm
 *   t [s], r = referência [contas de encoder], angle = posição [contas],
 *   pwm = comando aplicado [-255..255]
 */

// ---------------- Pinos ----------------
const int PIN_PWM   = 9;
const int PIN_IN1   = 7;
const int PIN_IN2   = 8;
const int PIN_ENC_A = 2;
const int PIN_ENC_B = 3;

// ---------------- Ganhos do PID (AJUSTAR com a sua sintonia — Trabalho 2) ----------------
float kp = 2.0;
float ki = 0.5;
float kd = 1.0;

// ---------------- Parâmetros da realização ----------------
const float N_FILT = 10.0;        // filtro da derivada (5..20)
const float Ts_ms  = 20.0;        // período de amostragem [ms]
const int   PWM_MAX = 255;
const bool  ANTI_WINDUP = true;   // false para demonstrar o windup (M4 §4.2)

// Conversão ângulo <-> contas (medir no Passo 2 do Trabalho 2)
// ex.: encoder de 12 pulsos/volta x quadratura 2x x redução -> contas_por_grau
const float CONTAS_POR_GRAU = 1.0;   // AJUSTAR para a sua bancada

// ---------------- Perfil de referências (degraus, em graus) ----------------
const int N_DEGRAUS = 4;
float perfil_graus[N_DEGRAUS]   = { 0, 90, -90, 0 };
unsigned long degrau_ms[N_DEGRAUS] = { 0, 2000, 7000, 12000 };  // instantes de troca
unsigned long T_FIM_MS = 17000;

// ---------------- Estado ----------------
volatile long enc_count = 0;
float xi = 0.0;        // estado do integrador
float xf = 0.0;        // estado do filtro da derivada

void isr_enc() {
  if (digitalRead(PIN_ENC_B)) enc_count++;
  else                        enc_count--;
}

void aplica_pwm(int u) {
  u = constrain(u, -PWM_MAX, PWM_MAX);
  if (u >= 0) { digitalWrite(PIN_IN1, HIGH); digitalWrite(PIN_IN2, LOW); }
  else        { digitalWrite(PIN_IN1, LOW);  digitalWrite(PIN_IN2, HIGH); }
  analogWrite(PIN_PWM, abs(u));
}

float referencia_em(unsigned long t_ms) {
  float r_graus = perfil_graus[N_DEGRAUS - 1];
  for (int i = 0; i < N_DEGRAUS; i++) {
    if (t_ms < degrau_ms[i]) { r_graus = (i == 0) ? perfil_graus[0] : perfil_graus[i - 1]; break; }
  }
  // degrau_ms[0]=0 -> antes do primeiro instante vale perfil_graus[0]
  if (t_ms < degrau_ms[0]) r_graus = perfil_graus[0];
  for (int i = 0; i < N_DEGRAUS; i++)
    if (t_ms >= degrau_ms[i]) r_graus = perfil_graus[i];
  return r_graus * CONTAS_POR_GRAU;   // em contas
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
  Serial.println("# pid_motor — t[s],r[contas],angle[contas],pwm");

  const float Ts = Ts_ms / 1000.0;
  unsigned long t0 = millis();
  unsigned long t_am = t0;

  while (millis() - t0 < T_FIM_MS) {
    unsigned long agora = millis();
    if (agora - t_am < Ts_ms) continue;
    t_am = agora;

    noInterrupts();
    long y_counts = enc_count;
    interrupts();
    float y = (float)y_counts;                 // posição em contas
    float r = referencia_em(agora - t0);       // referência em contas
    float e = r - y;

    // ---- derivada filtrada SOBRE A MEDIÇÃO ----
    float dxf = N_FILT * (-y - xf);
    xf += dxf * Ts;
    float uD = kd * dxf;

    // ---- PID (antes do limitador) ----
    float u_unsat = kp * e + ki * xi + uD;
    float u = constrain(u_unsat, -PWM_MAX, PWM_MAX);

    // ---- anti-windup por CLAMPING (M4 §4.2) ----
    bool sat_e_mesmo_sinal =
        (u_unsat >=  PWM_MAX && e > 0) ||
        (u_unsat <= -PWM_MAX && e < 0);
    if (!(ANTI_WINDUP && sat_e_mesmo_sinal)) {
      xi += e * Ts;                            // integra (ou congela)
    }

    aplica_pwm((int)u);

    Serial.print((agora - t0) / 1000.0, 3);
    Serial.print(",");
    Serial.print(r, 1);
    Serial.print(",");
    Serial.print(y, 1);
    Serial.print(",");
    Serial.println((int)u);
  }

  aplica_pwm(0);
  Serial.println("# fim do ensaio");
}

void loop() {
  // ensaio único; resete a placa para repetir
}
