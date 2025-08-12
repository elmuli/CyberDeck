import math
import sys
import time
import board
import busio
from adafruit_hid.mouse import Mouse
import usb_hid
from digitalio import DigitalInOut
from circuitpython_cirque_pinnacle import (
    PinnacleTouchSPI,
    PinnacleTouchI2C,  # noqa: imported-but-unused
    PINNACLE_ABSOLUTE,
    AbsoluteReport,
)
import asyncio

IS_ON_LINUX = sys.platform.lower() == "linux"

print("Cirque Pinnacle absolute mode\n")

# the pin connected to the trackpad's DR pin.
dr_pin = DigitalInOut(board.GP6 if not IS_ON_LINUX else board.GP6)

print("-- Using SPI interface.")
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP0)
ss_pin = DigitalInOut(board.GP5 if not IS_ON_LINUX else board.GP5)
trackpad = PinnacleTouchSPI(spi, ss_pin, dr_pin)

trackpad.data_mode = PINNACLE_ABSOLUTE  # ensure Absolute mode is enabled
trackpad.absolute_mode_config(z_idle_count=1)  # limit idle packet count to 1

# an object to hold the data reported by the Pinnacle
data = AbsoluteReport()
Data = None

mouse = Mouse(usb_hid.devices)

last_x = None
last_y = None

TRACKPAD_MAX = 1999
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
was_touching = False
touch_start_time = None
isRight = False
TAP_MAX_DURATION = 0.2 
X_RES = 1999
Y_RES = 1999
Y_THRESHOLD = Y_RES // 2
SCROLL_ZONE_WIDTH = 600
SCROLL_SCALE = 0.3

def map_position(val, max_val, screen_size):
    return int((val / max_val) * screen_size)

def print_data():
    global last_x
    global last_y
    global was_touching
    global touch_start_time
    global isRight
    """Print available data reports from the Pinnacle touch controller
    until there's no input for a period of ``timeout`` seconds."""
    while trackpad.available():  # is there new data?
        trackpad.read(data)
        # specification sheet recommends clamping absolute position data of
        # X & Y axis for reliability
        if data.z:  # only clamp values if Z axis is not idle.
            data.x = max(128, min(1920, data.x))  # X-axis
            data.y = max(64, min(1472, data.y))  # Y-axis
        if data.z:
            if not was_touching:
                touch_start_time = time.monotonic()
                was_touching = True
            x = map_position(-data.y, TRACKPAD_MAX, SCREEN_WIDTH)
            y = map_position(data.x, TRACKPAD_MAX, SCREEN_HEIGHT)
            if last_x is not None and last_y is not None:
                dx = x - last_x
                dy = y - last_y
                #print(data.x, data.y, data.z)
                if data.y < SCROLL_ZONE_WIDTH or data.y > (X_RES - SCROLL_ZONE_WIDTH):
                    mouse.move(wheel=int(-dy*SCROLL_SCALE))
                else:
                    mouse.move(x=dx, y=dy)
                    
            if data.y < 300 and data.x < 550:
                isRight = True
            
            last_x = x
            last_y = y
        else:
            last_x = None
            last_y = None
            if was_touching and touch_start_time:
                duration = time.monotonic() - touch_start_time
            if duration < TAP_MAX_DURATION:
                if isRight:
                    mouse.press(Mouse.RIGHT_BUTTON)
                else:
                    mouse.press(Mouse.LEFT_BUTTON)
            touch_start_time = None
            was_touching = False
            isRight = False
            mouse.release(Mouse.LEFT_BUTTON)
            mouse.release(Mouse.RIGHT_BUTTON)

#while True:
def Main():
    while True:
        print_data()
        await asyncio.sleep(0)

