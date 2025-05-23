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

RowInPins=[board.GP0,board.GP1,board.GP2,board.GP3,board.GP4]
ColumnOutPins=[board.GP5,board.GP6]

rows=[]
for b, button in enumerate(RowInPins):
    rows.append(DigitalInOut(button))
    rows[b].direction = Direction.INPUT
    rows[b].pull = Pull.DOWN

cols=[]
for col_, column in enumerate(ColumnOutPins):
    cols.append(DigitalInOut(column))
    cols[col_].direction = Direction.OUTPUT

Layer_1=[["K1", "K2"],
        ["K3", "K4"],
        ["K5","K6"],
        ["K7","K8"],
        ["KF_1","KF_2"]]

Layer_2=[["R1", "R2"],
        ["R3", "R4"],
        ["R5","R6"],
        ["R7","R8"],
        ["KF_1","KF_2"]]

key_map_1={
    "K1": Keycode.Q,
    "K2": Keycode.W,
    "K3": Keycode.E,
    "K4": Keycode.R,
    "K5": Keycode.T,
    "K6": Keycode.Y,
    "K7": Keycode.SPACE,
    "K8": Keycode.ENTER
}

key_map_2={
    "R1": Keycode.U,
    "R2": Keycode.I,
    "R3": Keycode.O,
    "R4": Keycode.P,
    "R5": Keycode.A,
    "R6": Keycode.S,
    "R7": Keycode.D,
    "R8": Keycode.F
}

key_map_3={
    "K1": Keycode.G,
    "K2": Keycode.H,
    "K3": Keycode.J,
    "K4": Keycode.K,
    "K5": Keycode.L,
    "K6": Keycode.Z,
    "K7": Keycode.X,
    "K8": Keycode.C
}

key_map_4={
    "K1": Keycode.V,
    "K2": Keycode.B,
    "K3": Keycode.N,
    "K4": Keycode.M,
    "K5": Keycode.COMMA,
    "K6": Keycode.KEYPAD_PERIOD,
    "K7": Keycode.SLASH,
    "K8": Keycode.BACKSPACE
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
    led.value = True
    return Pressed_keys

Last_keys = []
def check_keys():
    global Last_keys
    pressed_keys_l1 = scan_keys(Layer_1)
    pressed_keys_l2 = []
    Fkey1 = False
    Fkey2 = False
    if pressed_keys_l1:
        for fk in pressed_keys_l1:
            if fk == "KF_1":
                Fkey1 = True
            elif fk == "KF_2":
                Fkey2 = True
        if(not Fkey1 and not Fkey2): 
            for key in pressed_keys_l1:
                if key in key_map_1:
                    keyboard.press(key_map_1[key])
        if(Fkey1 and not Fkey2):
            pressed_keys_l2 = scan_keys(Layer_2)
            if pressed_keys_l2:
                for key in (pressed_keys_l2):
                    if key in key_map_2:
                        keyboard.press(key_map_2[key])
        if(Fkey2 and not Fkey1): 
            for key in pressed_keys_l1:
                if key in key_map_3:
                    keyboard.press(key_map_3[key])
        if(Fkey2 and Fkey1):
            for key in pressed_keys_l1:
                if key in key_map_3:
                    keyboard.press(key_map_4[key])
    for k in Last_keys:
        if k not in pressed_keys_l1:
            if k in key_map_1:
                keyboard.release(key_map_1[k])
            if k in key_map_3:
                keyboard.release(key_map_3[k])
            if k in key_map_4:
                keyboard.release(key_map_4[k])
        if k not in pressed_keys_l2:
            if k in key_map_2:
                keyboard.release(key_map_2[k])
    #print(Fkey1," ",Fkey2)
    Last_keys = pressed_keys_l1+pressed_keys_l2
    
while True:
    led.value = False
    check_keys()
    time.sleep(0.01)
