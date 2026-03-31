"""
Forza Horizon 4 — Arduino Motion Controller
Button 1 (D4) = W | Button 2 (D5) = S | Button 3 (D7) = R
Joystick click      = toggle steering / camera mode
Joystick down       = Enter (steering mode) / ↓ (camera mode)

pip install pyserial pynput
"""

import serial
import time
from pynput.keyboard import Controller, Key

SERIAL_PORT  = "COM3"    # ← change to your port
BAUD_RATE    = 115200
RECONNECT_S  = 3

JOY_X_INVERT = False
JOY_Y_INVERT = False

KEY_LEFT      = 'a'
KEY_RIGHT     = 'd'
KEY_ACCEL     = 'w'
KEY_BRAKE     = 's'
KEY_R         = 'r'
KEY_ENTER     = Key.enter
KEY_CAM_UP    = Key.up
KEY_CAM_DOWN  = Key.down
KEY_CAM_LEFT  = Key.left
KEY_CAM_RIGHT = Key.right

kb    = Controller()
_held = set()

def press(key):
    if key not in _held:
        kb.press(key)
        _held.add(key)

def release(key):
    if key in _held:
        kb.release(key)
        _held.discard(key)

def release_all():
    for key in list(_held):
        try:
            kb.release(key)
        except Exception:
            pass
    _held.clear()

def release_all_joystick_keys():
    release(KEY_LEFT)
    release(KEY_RIGHT)
    release(KEY_CAM_LEFT)
    release(KEY_CAM_RIGHT)
    release(KEY_CAM_UP)
    release(KEY_CAM_DOWN)
    release(KEY_ENTER)

def parse_packet(line: str):
    if line.startswith("STATUS:"):
        print(f"[Arduino] {line}")
        return None
    try:
        parts = {}
        for token in line.strip().split():
            k, v = token.split(":")
            parts[k] = int(v)
        assert all(k in parts for k in ("B1", "B2", "B3", "JX", "JY", "JM"))
        return parts
    except Exception:
        return None

def handle_btn1(pressed):
    if pressed: press(KEY_ACCEL)
    else:       release(KEY_ACCEL)

def handle_btn2(pressed):
    if pressed: press(KEY_BRAKE)
    else:       release(KEY_BRAKE)

def handle_btn3(pressed):
    if pressed: press(KEY_R)
    else:       release(KEY_R)

def handle_steering(jx, jy):
    # Left / Right → A / D
    if jx == -1:
        press(KEY_LEFT);  release(KEY_RIGHT)
    elif jx == 1:
        press(KEY_RIGHT); release(KEY_LEFT)
    else:
        release(KEY_LEFT); release(KEY_RIGHT)

    # Down → Enter (confirm rewind), Up → nothing in steering mode
    if jy == -1:
        press(KEY_ENTER)
    else:
        release(KEY_ENTER)

def handle_camera(jx, jy):
    # Left / Right
    if jx == -1:
        press(KEY_CAM_LEFT);  release(KEY_CAM_RIGHT)
    elif jx == 1:
        press(KEY_CAM_RIGHT); release(KEY_CAM_LEFT)
    else:
        release(KEY_CAM_LEFT); release(KEY_CAM_RIGHT)

    # Up / Down
    if jy == 1:
        press(KEY_CAM_UP);   release(KEY_CAM_DOWN)
    elif jy == -1:
        press(KEY_CAM_DOWN); release(KEY_CAM_UP)
    else:
        release(KEY_CAM_UP); release(KEY_CAM_DOWN)

def run():
    prev_mode = 0
    while True:
        try:
            print(f"[Info] Connecting to {SERIAL_PORT}...")
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print("[Info] Connected! Focus Forza now.")
            print("[Info] Mode: STEERING")
            time.sleep(2)

            while True:
                try:
                    raw = ser.readline().decode("utf-8", errors="ignore").strip()
                except UnicodeDecodeError:
                    continue

                if not raw:
                    continue

                pkt = parse_packet(raw)
                if pkt is None:
                    continue

                jx   = -pkt["JX"] if JOY_X_INVERT else pkt["JX"]
                jy   = -pkt["JY"] if JOY_Y_INVERT else pkt["JY"]
                mode = pkt["JM"]

                if mode != prev_mode:
                    release_all_joystick_keys()
                    print(f"[Info] Mode: {'CAMERA' if mode else 'STEERING'}")
                    prev_mode = mode

                handle_btn1(bool(pkt["B1"]))
                handle_btn2(bool(pkt["B2"]))
                handle_btn3(bool(pkt["B3"]))

                if mode == 0:
                    handle_steering(jx, jy)
                else:
                    handle_camera(jx, jy)

        except serial.SerialException as e:
            print(f"[Error] {e}")
            release_all()
            time.sleep(RECONNECT_S)
        except KeyboardInterrupt:
            print("\n[Info] Exiting...")
            release_all()
            break

if __name__ == "__main__":
    run()