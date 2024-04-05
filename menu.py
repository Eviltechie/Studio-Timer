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
            led.keypad_color(0, 0, 0)
        else:
            self.timer_controller.display_keypad()
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
        self.timer_controller.time_string_to_seconds()
        new_time = self.timer_controller.active_timer.time - 5
        if new_time < 0:
            new_time = 0
        self.timer_controller.active_timer.set_time(new_time)
    
    def softkey_2_press(self):
        self.timer_controller.time_string_to_seconds()
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
        self.timer_controller.time_string_to_seconds()
        new_time = self.timer_controller.active_timer.time - 60
        if new_time < 0:
            new_time = 0
        self.timer_controller.active_timer.set_time(new_time)
    
    def softkey_2_press(self):
        self.timer_controller.time_string_to_seconds()
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
    
    def softkey_1_press(self):
        self.menu_controller.mode = "menu_1"
        led.sw_hsv(1, self.timer_controller.timers[6].h, self.timer_controller.timers[6].s, self.timer_controller.timers[6].v)
        led.sw_hsv(2, self.timer_controller.timers[7].h, self.timer_controller.timers[7].s, self.timer_controller.timers[7].v)
        led.sw_hsv(3, self.timer_controller.timers[8].h, self.timer_controller.timers[8].s, self.timer_controller.timers[8].v)
        led.sw_hsv(5, 0, 0, 0)
        led.sw_hsv(6, self.timer_controller.timers[3].h, self.timer_controller.timers[3].s, self.timer_controller.timers[3].v)
        led.sw_hsv(7, self.timer_controller.timers[4].h, self.timer_controller.timers[4].s, self.timer_controller.timers[4].v)
        led.sw_hsv(8, self.timer_controller.timers[5].h, self.timer_controller.timers[5].s, self.timer_controller.timers[5].v)
        led.sw_hsv(11, self.timer_controller.timers[0].h, self.timer_controller.timers[0].s, self.timer_controller.timers[0].v)
        led.sw_hsv(12, self.timer_controller.timers[1].h, self.timer_controller.timers[1].s, self.timer_controller.timers[1].v)
        led.sw_hsv(13, self.timer_controller.timers[2].h, self.timer_controller.timers[2].s, self.timer_controller.timers[2].v)
    
    def softkey_1_release(self):
        self.menu_controller.mode = "normal"
        self.timer_controller.display_keypad()
    
    def digit(self, digit):
        if digit == 0:
            return
        self.timer_controller.set_active(digit - 1) # -1 because people aren't zero indexed
