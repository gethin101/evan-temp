import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

#kbd
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

#pins
key_pins = {
    "1": board.MISO,
    "2": board.A3,
    "3": board.A0,

    "4": board.SCK,
    "5": board.TX,
    "6": board.A1,

    "7": board.RX,
    "8": board.MOSI,
    "9": board.A2,
}


actions = {
    "1": ("keycode", [Keycode.A]),                 
    "2": ("keycode", [Keycode.UP_ARROW]),        
    "3": ("keycode", [Keycode.B]),                 

    "4": ("keycode", [Keycode.LEFT_ARROW]),      
    "5": ("media_hold", ConsumerControlCode.VOLUME_INCREMENT), 

    "6": ("keycode", [Keycode.RIGHT_ARROW]),       
    "7": ("keycode", [Keycode.C]),               
    "8": ("keycode", [Keycode.DOWN_ARROW]),        
    "9": ("keycode", [Keycode.D]),                 
}


buttons = {}
for key, pin in key_pins.items():
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons[key] = btn


snip_mode = False

# Main loop
last_pressed = set()

while True:
    pressed = set()


    for key, btn in buttons.items():
        if not btn.value:
            pressed.add(key)


    new_keys = pressed - last_pressed


    for key in new_keys:
        if key in actions:
            action_type, value = actions[key]

            if action_type == "keycode":
                kbd.send(*value)

            elif action_type == "media":
                cc.send(value)

            elif action_type == "toggle":
                snip_mode = not snip_mode

                if snip_mode:
                    kbd.send(Keycode.WINDOWS, Keycode.SHIFT, Keycode.S)
                else:
                    kbd.send(Keycode.ESCAPE)


    for key in pressed:
        if key in actions:
            action_type, value = actions[key]
            if action_type == "media_hold":
                cc.send(value)

    last_pressed = pressed
    time.sleep(0.05)

    #by gethin
