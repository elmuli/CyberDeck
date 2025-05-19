from machine import Pin
import time

cols = [Pin(3, Pin.OUT),Pin(4, Pin.OUT)]
rows = [Pin(1, Pin.IN, Pin.PULL_DOWN),Pin(2, Pin.IN, Pin.PULL_DOWN)]

keys = [["K1", "K2"],
        ["K3", "K4"]]

def scan_keys():
    pressed_keys = []

    for i, col in enumerate(cols):
        #print(i," col")
        for c in cols:
            c.low()
        
        col.high()
        time.sleep_us(20)

        for j, row in enumerate(rows):
            #print(j," row"," rowState: ",row.value())
            if row.value():
                pressed_keys.append(keys[j][i])

    #print("lapi")
    
    return pressed_keys

while True:
    keys_pressed = scan_keys()
    if keys_pressed:
        print("Pressed:",",".join(keys_pressed))
    time.sleep(0.1)