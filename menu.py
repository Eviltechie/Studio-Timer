import lcd
import led

#1234567812345678#
#Timer 1     100%#
#Down Preset    ~#

#Timer 1     100%#
#-5s   +5s      ~#

#Timer 1     100%#
#-1m   +1m      ~#

#Timer 1     100%#
#-10%  +10%     ~#

#Timer 1     100%#
#Select         ~#

#Timer 1     100%#
#IP             ~#

class Menu:
    def __init__(self, menu_controller):
        self.menu_controller = menu_controller
    
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
        pass
    
    def softkey_3_release(self):
        pass
    
    def digit(self, digit):
        pass

class MenuDirectionPreset(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write("Timer 1")
        lcd.set_position(1, 0)
        lcd.write("Down Preset    ~")
    
    def softkey_3_press(self):
        self.menu_controller.next_page()

class MenuFiveSeconds(Menu):
    def display(self):
        lcd.clear_screen()
        lcd.write("Timer 1")
        lcd.set_position(1, 0)
        lcd.write("-5s    +5s     ~")
    
    def softkey_3_press(self):
        self.menu_controller.next_page()
