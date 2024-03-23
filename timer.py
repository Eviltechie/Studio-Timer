import led
import lcd
import picozero
import machine
import micropython
import random
import time

time_string = "000000"
time_seconds = 0

def time_push(digit):
    global time_string
    time_string = time_string[-5:] + str(digit)
    display_time()

def display_time():
    global time_string
    led.digit_1(time_string[0])
    led.digit_2(time_string[1])
    led.digit_3(time_string[2])
    led.digit_4(time_string[3])
    led.digit_5(time_string[4])
    led.digit_6(time_string[5])

def time_seconds_to_string():
    global time_seconds
    global time_string
    
    hours = time_seconds // 3600
    remainder = time_seconds % 3600
    
    minutes = remainder // 60
    seconds = remainder % 60
    
    time_string = "{:02d}{:02d}{:02d}".format(hours, minutes, seconds)

def time_string_to_seconds():
    global time_string
    global time_seconds
    
    try:
        hours = int(time_string[0:2])
    except ValueError:
        hours = 0
    
    try:
        minutes = int(time_string[2:4])
    except ValueError:
        minutes = 0
    
    try:
        seconds = int(time_string[4:6])
    except ValueError:
        seconds = 0
    
    if seconds > 59:
        minutes = minutes + (seconds // 60)
        seconds = seconds % 60
    
    if minutes > 59:
        hours = hours + (minutes // 60)
        minutes = minutes % 60
    
    if hours > 99:
        hours = 99
    
    time_seconds = (hours * 60 * 60) + (minutes * 60) + seconds

class Keypad_Button:    
    def __init__(self, digit, preset_seconds):
        self.digit = digit
        self.preset_seconds = preset_seconds
    
    def button(self):
        global timer_running
        global mode
        if not timer_running and mode == "normal":
            time_push(str(self.digit))
        if mode == "preset":
            global time_seconds
            time_seconds = self.preset_seconds
            time_seconds_to_string()
            display_time()
        print("Button_" + str(self.digit))

# Button() uses GPIO number

# 7
sw1 = picozero.Button(14)
sw1.when_pressed = Keypad_Button(7, 420).button

# 8
sw2 = picozero.Button(11)
sw2.when_pressed = Keypad_Button(8, 480).button

# 9
sw3 = picozero.Button(10)
sw3.when_pressed = Keypad_Button(9, 540).button

# softkey 1
sw4 = picozero.Button(4)

def button_softkey_1():
    global timer_direction
    if timer_direction == "down":
        timer_direction = "up"
        led.sw_rgb(4, 0, 255, 0)
    else:
        timer_direction = "down"
        led.sw_rgb(4, 255, 0, 0)
    print("Button_softkey_1")

sw4.when_pressed = button_softkey_1

# 0
sw5 = picozero.Button(21)
sw5.when_pressed = Keypad_Button(0, 30).button

# 4
sw6 = picozero.Button(15)
sw6.when_pressed = Keypad_Button(4, 240).button

# 5
sw7 = picozero.Button(17)
sw7.when_pressed = Keypad_Button(5, 300).button

# 6
sw8 = picozero.Button(16)
sw8.when_pressed = Keypad_Button(6, 360).button

# softkey 2
sw9 = picozero.Button(3)

def button_softkey_2_press():
    global mode
    mode = "preset"
    keypad_color(160, 255, 50)
    led.sw_hsv(9, 160, 255, 100)
    print("Button_softkey_2_press")

def button_softkey_2_release():
    global mode
    mode = "normal"
    global timer_running
    if timer_running:
        keypad_color(32, 255, 0)
    else:
        keypad_color(32, 255, 50)
    led.sw_hsv(9, 160, 255, 50)
    print("Button_softkey_2_release")

sw9.when_pressed = button_softkey_2_press
sw9.when_released= button_softkey_2_release

# start/stop
sw10 = picozero.Button(26)

def button_start_stop():
    global timer_running
    global timer_direction
    if timer_running:
        timerA_stop()
    else:
        timerA_start()
    print("Button_start_stop")

sw10.when_pressed = button_start_stop

# 1
sw11 = picozero.Button(18)
sw11.when_pressed = Keypad_Button(1, 60).button

# 2
sw12 = picozero.Button(19)
sw12.when_pressed = Keypad_Button(2, 120).button

# 3
sw13 = picozero.Button(20)
sw13.when_pressed = Keypad_Button(3, 180).button

#softkey 3
sw14 = picozero.Button(2)

def button_softkey_3():
    print("Button_softkey_3")

sw14.when_pressed = button_softkey_3

# reset
sw15 = picozero.Button(22)

def button_reset():
    global time_string
    global time_seconds
    time_string = "000000"
    time_seconds = 0
    display_time()
    print("Button_reset")

sw15.when_pressed = button_reset

timer_running = False
timer_direction = "down"
mode = "normal"
hue = 0

def tick(x):
    global time_seconds
    global timer_direction
    if timer_direction == "down":
        if time_seconds <= 0:
            timerA_stop()
        else:
            time_seconds -= 1
            time_seconds_to_string()
        if time_seconds <= 0:
            timerA_stop()
    else: # up
        if time_seconds >= 359999:
            timerA_stop()
        else:
            time_seconds += 1
            time_seconds_to_string()
        if time_seconds >= 359999:
            timerA_stop()
    display_time()
    print("tick")

def timerA_callback(t):
    micropython.schedule(tick, 0)

timerA = machine.Timer()

# A period of 1000 will cause us to lose milliseconds when stopped if we count based on this
def timerA_start():
    time_string_to_seconds()
    global time_seconds
    global timer_direction
    if timer_direction == "down" and time_seconds <= 0:
        return
    if timer_direction == "up" and time_seconds >= 359999:
        return
    timerA.init(mode=machine.Timer.PERIODIC, period=1000, callback=timerA_callback)
    global timer_running
    timer_running = True
    keypad_color(32, 255, 0)
    led.sw_rgb(10, 0, 255, 0)
    display_time()

def timerA_stop():
    global timer_running
    timerA.deinit()
    timer_running = False
    led.sw_rgb(10, 255, 0, 0)
    keypad_color(32, 255, 50)

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
display_time()
