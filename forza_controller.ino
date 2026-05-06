// ============================================================
//  Forza Horizon 4 - Arduino Motion Controller
//  Button 1 (D4) = W | Button 2 (D5) = S | Button 3 (D7) = R
//  Joystick click (D6) = toggle steering / camera mode
//  Joystick down in steering mode = Enter
// ============================================================

#define BTN_ACCEL   4
#define BTN_BRAKE   5
#define BTN_R       7
#define JOY_X       A0
#define JOY_Y       A1
#define JOY_BTN     6

#define JOY_DEADZONE  150
#define JOY_CENTER    512

bool joyMode    = false;
bool joyBtnLast = false;

void setup() {
  Serial.begin(115200);
  pinMode(BTN_ACCEL, INPUT_PULLUP);
  pinMode(BTN_BRAKE, INPUT_PULLUP);
  pinMode(BTN_R,     INPUT_PULLUP);
  pinMode(JOY_BTN,   INPUT_PULLUP);
  Serial.println("STATUS:READY");
}

int joyAxis(int raw) {
  int delta = raw - JOY_CENTER;
  if (delta >  JOY_DEADZONE) return  1;
  if (delta < -JOY_DEADZONE) return -1;
  return 0;
}

void loop() {
  // Joystick button toggle
  bool joyBtnNow = !digitalRead(JOY_BTN);
  if (joyBtnNow && !joyBtnLast) {
    joyMode = !joyMode;
    Serial.print("STATUS:MODE:");
    Serial.println(joyMode ? "CAMERA" : "STEERING");
  }
  joyBtnLast = joyBtnNow;

  bool btn1 = !digitalRead(BTN_ACCEL);
  bool btn2 = !digitalRead(BTN_BRAKE);
  bool btn3 = !digitalRead(BTN_R);

  int jx = joyAxis(analogRead(JOY_X));
  int jy = joyAxis(analogRead(JOY_Y));

  Serial.print("B1:"); Serial.print(btn1 ? 1 : 0);
  Serial.print(" B2:"); Serial.print(btn2 ? 1 : 0);
  Serial.print(" B3:"); Serial.print(btn3 ? 1 : 0);
  Serial.print(" JX:"); Serial.print(jx);
  Serial.print(" JY:"); Serial.print(jy);
  Serial.print(" JM:"); Serial.println(joyMode ? 1 : 0);

  delay(20);
}