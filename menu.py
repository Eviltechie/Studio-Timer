import lcd
import led
import time

#Timer 1     100%#
#IP             ~#

class Menu:
    def __init__(self, menu_controller, timer_controller):
        self.menu_controller = menu_controller
        self.timer_controller = timer_controller
    
    def display(self):
        pass
    
    def softkey_1_press(self):
        pass
    
    def softkey_1_release(self):
        pass
    
    def softkey_2_press(self):
        pass
    
    def softkey_2_release(self):
        pass
    
    def softkey_3_press(self):
        self.menu_controller.next_page()
    
    def softkey_3_release(self):
        pass
    
    def digit(self, digit):
        pass

class MenuDirectionPreset(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(1, 0)
        if self.timer_controller.active_timer.direction == "up":
            led.sw_rgb(4, 0, 255, 0)
            lcd.write("Up    Preset   ~")
        else:
            led.sw_rgb(4, 255, 0, 0)
            lcd.write("Down  Preset   ~")
        led.sw_hsv(9, 160, 255, 50)
    
    def softkey_1_press(self):
        if self.timer_controller.active_timer.direction == "down":
            self.timer_controller.active_timer.set_direction("up")
        else:
            self.timer_controller.active_timer.set_direction("down")
        self.display()
    
    def softkey_2_press(self):
        self.menu_controller.mode = "menu_2"
        led.keypad_color(160, 255, 50)
        led.sw_hsv(9, 160, 255, 100)
    
    def softkey_2_release(self):
        self.menu_controller.mode = "normal"
        if self.timer_controller.active_timer.running:
            led.keypad_color(32, 255, 0)
        else:
            led.keypad_color(32, 255, 50)
        led.sw_hsv(9, 160, 255, 50)
    
    def digit(self, digit):
        presets = {
            0: 30,
            1: 60,
            2: 120,
            3: 180,
            4: 240,
            5: 300,
            6: 360,
            7: 420,
            8: 480,
            9: 540,
        }
        if self.menu_controller.mode == "menu_2":
            self.timer_controller.active_timer.set_time(presets[digit])

class MenuFiveSeconds(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(1, 0)
        lcd.write("-5s    +5s     ~")
        led.sw_rgb(4, 255, 255, 255)
        led.sw_rgb(9, 255, 255, 255)
    
    def softkey_1_press(self):
        new_time = self.timer_controller.active_timer.time - 5
        if new_time < 0:
            new_time = 0
        self.timer_controller.active_timer.set_time(new_time)
    
    def softkey_2_press(self):
        new_time = self.timer_controller.active_timer.time + 5
        if new_time > 359999:
            new_time = 359999
        self.timer_controller.active_timer.set_time(new_time)

class MenuOneMinute(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(1, 0)
        lcd.write("-1m    +1m     ~")
        led.sw_rgb(4, 255, 255, 255)
        led.sw_rgb(9, 255, 255, 255)
    
    def softkey_1_press(self):
        new_time = self.timer_controller.active_timer.time - 60
        if new_time < 0:
            new_time = 0
        self.timer_controller.active_timer.set_time(new_time)
    
    def softkey_2_press(self):
        new_time = self.timer_controller.active_timer.time + 60
        if new_time > 359999:
            new_time = 359999
        self.timer_controller.active_timer.set_time(new_time)
        
class MenuSpeed(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(0, 12)
        lcd.write(str(self.timer_controller.active_timer.rate))
        lcd.set_position(1, 0)
        lcd.write("-10%   +10%    ~")
        led.sw_rgb(4, 255, 255, 255)
        led.sw_rgb(9, 255, 255, 255)
    
    def softkey_1_press(self):
        new_rate = self.timer_controller.active_timer.rate - 100
        if new_rate < 500:
            new_rate = 500
        self.timer_controller.active_timer.change_rate(new_rate)
        self.display()
    
    def softkey_2_press(self):
        new_rate = self.timer_controller.active_timer.rate + 100
        if new_rate > 1500:
            new_rate = 1500
        self.timer_controller.active_timer.change_rate(new_rate)
        self.display()

class MenuTimerSelect(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(1, 0)
        lcd.write("Select         ~")
        led.sw_rgb(4, 255, 255, 255)
        led.sw_rgb(9, 0, 0, 0)
