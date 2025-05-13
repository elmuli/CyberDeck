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

#setup pins
#columns
Button_in_1 = board.GP0
Button_in_2 = board.GP1
#rows
Button_in_3 = board.GP4
Button_out_1 = board.GP2
Button_out_2 = board.GP3

#pin initialation
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

#layout layers
Layer_1 = [["K1", "K2"],
        ["K3", "K4"],
        ["_","KF"]]

Layer_2 = [["R1", "R2"],
        ["R3", "R4"],
        ["_","KF"]]

#scan pressed keys
def scan_keys(layer):
    pressed_keys = []

    for i, col in enumerate(cols):
        for c in cols:
            c.value = False
        col.value = True
        time.sleep(0.05)
        for j, row in enumerate(rows):
            if row.value:
                pressed_keys.append(layer[j][i])
    
    return pressed_keys

#check pressd keys
def check_keys():
    pressed_keys = scan_keys(Layer_1)
    Fkey = False
    if pressed_keys:
        #check if funcKey pressed
        for fk in pressed_keys:
            if fk == "KF":
                Fkey = True
        #layert one
        if(not Fkey): 
            for key in pressed_keys: 
                if key=="K1":
                    keyboard.send(Keycode.ONE)
                    led.value = True
                    break
                elif key=="K2":
                    keyboard.send(Keycode.TWO)
                    led.value = True
                    break
                elif key=="K3":
                    keyboard.send(Keycode.THREE)
                    led.value = True
                    break
                elif key=="K4":
                    keyboard.send(Keycode.FOUR)
                    led.value = True
                    break
                if(Fkey):
                    break
        #layer two
        if(Fkey):
            pressed_keys_l2 = scan_keys(Layer_2)
            if pressed_keys_l2:
                print("Pressed:",",".join(pressed_keys_l2))
                for i, key in enumerate(pressed_keys_l2):
                    if key=="R1":
                        keyboard.send(Keycode.FIVE)
                        led.value = True
                        break
                    elif key=="R2":
                        keyboard.send(Keycode.SIX)
                        led.value = True
                        break
                    elif key=="R3":
                        keyboard.send(Keycode.SEVEN)
                        led.value = True
                        break
                    elif key=="R4":
                        keyboard.send(Keycode.EIGHT)
                        led.value = True
                        break

#main loop
while True:
    
    led.value = False
    check_keys()

    time.sleep(0.01)
