import led
import lcd
import button
import machine
import micropython
import random
import time
import timer_controller
import menu_controller
import menu

t_controller = timer_controller.TimerController()
m_controller = menu_controller.MenuController(t_controller)

class Keypad_Button:    
    def __init__(self, digit):
        self.digit = digit
    
    def button(self):
        global t_controller
        global m_controller
        if not t_controller.active_timer.running and m_controller.mode == "normal":
            t_controller.push_digit(str(self.digit))
        if m_controller.mode == "menu_1":
            m_controller.digit(self.digit)
        if m_controller.mode == "menu_2":
            m_controller.digit(self.digit)
        if m_controller.mode == "menu_3":
            m_controller.digit(self.digit)
        print("Button_" + str(self.digit))

# Button() uses GPIO number

# 7
sw1 = button.Button(14, Keypad_Button(7).button)

# 8
sw2 = button.Button(11, Keypad_Button(8).button)

# 9
sw3 = button.Button(10, Keypad_Button(9).button)

# softkey 1
sw4 = button.Button(4)

def button_softkey_1_press():
    m_controller.softkey_1_press()
    print("Button_softkey_1_press")

def button_softkey_1_release():
    m_controller.softkey_1_release()
    print("Button_softkey_1_release")

sw4.on_press = button_softkey_1_press
sw4.on_release = button_softkey_1_release

# 0
sw5 = button.Button(21, Keypad_Button(0).button)

# 4
sw6 = button.Button(15, Keypad_Button(4).button)

# 5
sw7 = button.Button(17, Keypad_Button(5).button)

# 6
sw8 = button.Button(16, Keypad_Button(6).button)

# softkey 2
sw9 = button.Button(3)

def button_softkey_2_press():
    m_controller.softkey_2_press()
    print("Button_softkey_2_press")

def button_softkey_2_release():
    m_controller.softkey_2_release()
    print("Button_softkey_2_release")

sw9.on_press = button_softkey_2_press
sw9.on_release = button_softkey_2_release

# start/stop
sw10 = button.Button(26)

def button_start_stop():
    global t_controller
    if t_controller.active_timer.running:
        if t_controller.active_timer.stop():
            led.sw_rgb(10, 255, 0, 0)
            led.keypad_color(32, 255, 50)
    else:
        t_controller.time_string_to_seconds()
        if t_controller.active_timer.start():
            led.keypad_color(32, 255, 0)
            led.sw_rgb(10, 0, 255, 0)
    print("Button_start_stop")

sw10.on_press = button_start_stop

# 1
sw11 = button.Button(18, Keypad_Button(1).button)

# 2
sw12 = button.Button(19, Keypad_Button(2).button)

# 3
sw13 = button.Button(20, Keypad_Button(3).button)

#softkey 3
sw14 = button.Button(2)

def button_softkey_3_press():
    m_controller.softkey_3_press()
    print("Button_softkey_3_press")

def button_softkey_3_release():
    m_controller.softkey_3_release()
    print("Button_softkey_3_release")

sw14.on_press = button_softkey_3_press
sw14.on_release = button_softkey_3_release

# reset
sw15 = button.Button(22)

def button_reset():
    global t_controller
    global m_controller
    t_controller.active_timer.set_time(0)
    t_controller.active_timer.change_rate(1000)
    if isinstance(m_controller.active_page, menu.MenuSpeed):
        m_controller.display()
    print("Button_reset")

sw15.on_press = button_reset

hue = 0

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
led.keypad_color(32, 255, 50)
led.sw_hsv(15, 32, 255, 50)
led.lcd_rgb(255, 0, 0)
led.sw_rgb(14, 50, 50, 50) # soft 3
t_controller.display_time()
m_controller.display() # not sure why we have to do this separate
