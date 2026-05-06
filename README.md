# 🎮 Forza Horizon 4 — Arduino Motion Controller

A DIY motion controller for Forza Horizon 4 built with Arduino Uno, a joystick module, and push buttons. Controls steering, acceleration, braking, and camera using physical hardware instead of a keyboard.

---

## 🔧 Hardware Required

- Arduino Uno
- Joystick module (KY-023 or similar)
- 3 push buttons
- Breadboard + jumper wires
- USB cable (Type-B)

---

## 🔌 Wiring

| Component | Pin | Arduino |
|---|---|---|
| Button 1 (W) | One leg | D4 |
| Button 1 (W) | Other leg | GND |
| Button 2 (S) | One leg | D5 |
| Button 2 (S) | Other leg | GND |
| Button 3 (R) | One leg | D7 |
| Button 3 (R) | Other leg | GND |
| Joystick VCC | VCC | 5V |
| Joystick GND | GND | GND |
| Joystick VRX | Horizontal | A0 |
| Joystick VRY | Vertical | A1 |
| Joystick SW | Click button | D6 |

---

## 🕹️ Controls

| Input | Steering Mode | Camera Mode |
|---|---|---|
| Joystick left/right | A / D (steer) | ← / → (camera) |
| Joystick up | — | ↑ (look up) |
| Joystick down | Enter (confirm rewind) | ↓ (look down) |
| Joystick click | Switch to camera mode | Switch to steering mode |
| Button 1 (D4) | W (accelerate) | W (accelerate) |
| Button 2 (D5) | S (brake) | S (brake) |
| Button 3 (D7) | R (rewind) | R (rewind) |

---

## 🚀 Setup

### Arduino

1. Open `forza_controller.ino` in Arduino IDE
2. Upload to your Arduino Uno
3. Open Serial Monitor at **115200 baud** and confirm you see `STATUS:READY`

### Python

1. Install dependencies:
```bash
pip install pyserial pynput
```

2. Open `forza_controller.py` and change the port:
```python
SERIAL_PORT = "COM3"  # check Device Manager for your port
```

3. Run the script:
```bash
python forza_controller.py
```

4. Focus the **Forza Horizon 4** window and start driving!

---

## 🔄 How Mode Switching Works

The joystick has a built in click button (SW pin). A single click toggles between two modes. The terminal prints the current mode so you always know which one is active.

```
[Info] Mode: STEERING   ← joystick controls A/D
[Info] Mode: CAMERA     ← joystick controls arrow keys
```

---

## 🛠️ Troubleshooting

**Buttons not working**
Make sure each button has one leg on the signal pin and the other on GND. They straddle the center gap of the breadboard diagonally (top-right to bottom-left or vice versa).

**Mode not switching**
Check that the joystick SW pin is connected to D6 and the other side goes to GND.

**Wrong COM port**
Open Device Manager on Windows, expand Ports, and find the port labeled Arduino Uno.

**Joystick axes reversed**
Set `JOY_X_INVERT = True` or `JOY_Y_INVERT = True` in the Python script.

**Keys getting stuck**
Close the Python script with `Ctrl+C` — it will release all keys automatically on exit.

---

## 📁 Project Structure

```
forza-motion-controller/
├── forza_controller.ino   # Arduino code
├── forza_controller.py    # Python code
└── README.md
```

---

## 🛠️ Built With

- [Arduino Uno](https://www.arduino.cc/)
- [Python 3](https://www.python.org/)
- [pyserial](https://pypi.org/project/pyserial/)
- [pynput](https://pypi.org/project/pynput/)

---

*Recommended soundtrack — Run by Avicii* 🎵
