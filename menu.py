import lcd
import led

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
    
    def softkey_1_press(self):
        if self.timer_controller.active_timer.direction == "down":
            self.timer_controller.active_timer.set_direction("up")
        else:
            self.timer_controller.active_timer.set_direction("down")
        self.display()

class MenuFiveSeconds(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(1, 0)
        lcd.write("-5s    +5s     ~")

class MenuOneMinute(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(1, 0)
        lcd.write("-1m    +1m     ~")
        
class MenuSpeed(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(1, 0)
        lcd.write("-10%   +10%    ~")

class MenuTimerSelect(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write(self.timer_controller.active_timer.timer_name)
        lcd.set_position(1, 0)
        lcd.write("Select         ~")
