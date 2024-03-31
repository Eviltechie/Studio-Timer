import led
import lcd
import button
import machine
import micropython
import random
import time
import timer_controller

controller = timer_controller.TimerController()

class Keypad_Button:    
    def __init__(self, digit, preset_seconds):
        self.digit = digit
        self.preset_seconds = preset_seconds
    
    def button(self):
        global controller
        global mode
        if not controller.active_timer.running and mode == "normal":
            controller.push_digit(str(self.digit))
        if mode == "preset":
            controller.active_timer.set_time(self.preset_seconds)
        print("Button_" + str(self.digit))

# Button() uses GPIO number

# 7
sw1 = button.Button(14, Keypad_Button(7, 420).button)

# 8
sw2 = button.Button(11, Keypad_Button(8, 480).button)

# 9
sw3 = button.Button(10, Keypad_Button(9, 540).button)

# softkey 1
sw4 = button.Button(4)

def button_softkey_1():
    global controller
    if controller.active_timer.direction == "down":
        controller.active_timer.set_direction("up")
        led.sw_rgb(4, 0, 255, 0)
    else:
        controller.active_timer.set_direction("down")
        led.sw_rgb(4, 255, 0, 0)
    print("Button_softkey_1")

sw4.on_press = button_softkey_1

# 0
sw5 = button.Button(21, Keypad_Button(0, 30).button)

# 4
sw6 = button.Button(15, Keypad_Button(4, 240).button)

# 5
sw7 = button.Button(17, Keypad_Button(5, 300).button)

# 6
sw8 = button.Button(16, Keypad_Button(6, 360).button)

# softkey 2
sw9 = button.Button(3)

def button_softkey_2_press():
    global mode
    mode = "preset"
    keypad_color(160, 255, 50)
    led.sw_hsv(9, 160, 255, 100)
    print("Button_softkey_2_press")

def button_softkey_2_release():
    global mode
    mode = "normal"
    global controller
    if controller.active_timer.running:
        keypad_color(32, 255, 0)
    else:
        keypad_color(32, 255, 50)
    led.sw_hsv(9, 160, 255, 50)
    print("Button_softkey_2_release")

sw9.on_press = button_softkey_2_press
sw9.on_release = button_softkey_2_release

# start/stop
sw10 = button.Button(26)

def button_start_stop():
    global controller
    if controller.active_timer.running:
        if controller.active_timer.stop():
            led.sw_rgb(10, 255, 0, 0)
            keypad_color(32, 255, 50)
    else:
        controller.time_string_to_seconds()
        if controller.active_timer.start():
            keypad_color(32, 255, 0)
            led.sw_rgb(10, 0, 255, 0)
    print("Button_start_stop")

sw10.on_press = button_start_stop

# 1
sw11 = button.Button(18, Keypad_Button(1, 60).button)

# 2
sw12 = button.Button(19, Keypad_Button(2, 120).button)

# 3
sw13 = button.Button(20, Keypad_Button(3, 180).button)

#softkey 3
sw14 = button.Button(2)

def button_softkey_3():
    print("Button_softkey_3")

sw14.on_press = button_softkey_3

# reset
sw15 = button.Button(22)

def button_reset():
    global controller
    controller.active_timer.set_time(0)
    controller.active_timer.change_rate(1000)
    print("Button_reset")

sw15.on_press = button_reset

mode = "normal"
hue = 0

def keypad_color(h, s, v):
    led.sw_hsv(1, h, s, v)
    led.sw_hsv(2, h, s, v)
    led.sw_hsv(3, h, s, v)
    led.sw_hsv(6, h, s, v)
    led.sw_hsv(7, h, s, v)
    led.sw_hsv(8, h, s, v)
    led.sw_hsv(11, h, s, v)
    led.sw_hsv(12, h, s, v)
    led.sw_hsv(13, h, s, v)
    led.sw_hsv(5, h, s, v)

def carbonite_screensaver():
    while True:
        button = random.choice(range(1, 16))
        hue = random.randrange(255)
        for value in range(255,-1,-1):
            led.sw_hsv(button, hue, 255, value)
            time.sleep(0.01)

led.lcd_rgb(0,0,0)
lcd.clear_screen()
led.colons(255,255,255,255)
led.sw_rgb(10, 255, 0, 0)
led.sw_rgb(4, 255, 0, 0)
keypad_color(32, 255, 50)
led.sw_hsv(15, 32, 255, 50)
led.sw_hsv(9, 160, 255, 50)
controller.display_time()
