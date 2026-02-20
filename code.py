import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Assign keyboard and consumer control
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# Order the pins
key_pins = {
    "1": board.A2,
    "2": board.A3,
    "3": board.SCK,

    "4": board.A0,
    "5": board.TX,
    "6": board.MISO,

    "7": board.A1,
    "8": board.RX,
    "9": board.MOSI,
}

# Actions for each key
actions = {
    "1": ("media", ConsumerControlCode.SCAN_PREVIOUS_TRACK),   # Back song
    "2": ("media", ConsumerControlCode.PLAY_PAUSE),            # Play/Pause
    "3": ("keycode", [Keycode.WINDOWS, Keycode.R]),            # Win + R (not working)

    "4": ("media_hold", ConsumerControlCode.VOLUME_DECREMENT), # Volume down (hold)
    "5": ("media_hold", ConsumerControlCode.VOLUME_INCREMENT), # Volume up (hold)

    "6": ("toggle", None),                                     # Toggle Snip <-> ESC
    "7": ("keycode", [Keycode.ALT, Keycode.F4]),               # Alt+F4
    "8": ("keycode", [Keycode.WINDOWS, Keycode.E]),            # File Explorer
    "9": ("media", ConsumerControlCode.SCAN_NEXT_TRACK),
}

# Setup buttons
buttons = {}
for key, pin in key_pins.items():
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons[key] = btn

# Toggle state for key 6
snip_mode = False

# Main loop
last_pressed = set()

while True:
    pressed = set()

    # Read all buttons
    for key, btn in buttons.items():
        if not btn.value:
            pressed.add(key)

    # Detect new presses
    new_keys = pressed - last_pressed

    # Handle one-shot actions
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
                    # Win + Shift + S
                    kbd.send(Keycode.WINDOWS, Keycode.SHIFT, Keycode.S)
                else:
                    # ESC
                    kbd.send(Keycode.ESCAPE)

    # Handle hold actions (volume)
    for key in pressed:
        if key in actions:
            action_type, value = actions[key]
            if action_type == "media_hold":
                cc.send(value)

    last_pressed = pressed
    time.sleep(0.05)
