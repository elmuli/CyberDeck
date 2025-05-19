import board
from digitalio import DigitalInOut, Direction, Pull
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT


Button_in_1 = board.GP0
Button_in_2 = board.GP1
Button_in_3 = board.GP2
Button_out_1 = board.GP3
Button_out_2 = board.GP4


R_in_1 = DigitalInOut(Button_in_1)
R_in_1.direction = Direction.INPUT
R_in_1.pull = Pull.DOWN
R_in_2 = DigitalInOut(Button_in_2)
R_in_2.direction = Direction.INPUT
R_in_2.pull = Pull.DOWN
R_in_3 = DigitalInOut(Button_in_3)
R_in_3.direction = Direction.INPUT
R_in_3.pull = Pull.DOWN

C_out_1 = DigitalInOut(Button_out_1)
C_out_1.direction = Direction.OUTPUT
C_out_2 = DigitalInOut(Button_out_2)
C_out_2.direction = Direction.OUTPUT

rows=[R_in_1,R_in_2,R_in_3]
cols=[C_out_1,C_out_2]

Layer_1 = [["K1", "K2"],
        ["K3", "K4"],
        ["_","KF"]]

Layer_2 = [["R1", "R2"],
        ["R3", "R4"],
        ["_","KF"]]

key_map_1={
    "K1": Keycode.ONE,
    "K2": Keycode.TWO,
    "K3": Keycode.THREE,
    "K4": Keycode.FOUR
}

key_map_2={
    "R1": Keycode.FIVE,
    "R2": Keycode.SIX,
    "R3": Keycode.SEVEN,
    "R4": Keycode.EIGHT
}

Pressed_keys = []

def scan_keys(layer):
    for i, col in enumerate(cols):
        for c in cols:
            c.value = False
        col.value = True
        time.sleep(0.01)
        for j, row in enumerate(rows):
            key = layer[j][i]
            if row.value:
                if key not in Pressed_keys:
                    Pressed_keys.append(layer[j][i])
            else:
                if layer[j][i] in Pressed_keys:
                    Pressed_keys.remove(layer[j][i])
    return Pressed_keys

Last_keys = []
def check_keys():
    global Last_keys
    pressed_keys_l1 = scan_keys(Layer_1)
    pressed_keys_l2 = []
    Fkey = False
    if pressed_keys_l1:
        for fk in pressed_keys_l1:
            if fk == "KF":
                Fkey = True
        if(not Fkey): 
            for key in pressed_keys_l1:
                if key in key_map_1:
                    keyboard.press(key_map_1[key])
        if(Fkey):
            pressed_keys_l2 = scan_keys(Layer_2)
            if pressed_keys_l2:
                for key in (pressed_keys_l2):
                    if key in key_map_2:
                        keyboard.press(key_map_2[key])
    for k in Last_keys:
        if k not in pressed_keys_l1:
            if k in key_map_1:
                keyboard.release(key_map_1[k])
        if k not in pressed_keys_l2:
            if k in key_map_2:
                keyboard.release(key_map_2[k])
    Last_keys = pressed_keys_l1+pressed_keys_l2
while True:
    
    led.value = False
    check_keys()

    time.sleep(0.01)