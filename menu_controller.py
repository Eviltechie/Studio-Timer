import menu

class MenuController:
    def __init__(self, timer_controller):
        self.pages = [
            menu.MenuDirectionPreset(self, timer_controller),
            menu.MenuFiveSeconds(self, timer_controller),
            menu.MenuOneMinute(self, timer_controller),
            menu.MenuSpeed(self, timer_controller),
            menu.MenuTimerSelect(self, timer_controller),
            ]
        self.active_page = self.pages[0]
        self.display()
        self.mode = "normal"
        self.ref_1_release = None
        self.ref_2_release = None
        self.ref_3_release = None
    
    def next_page(self):
        self.softkey_1_release() # Force release pressed keys
        self.softkey_2_release()
        self.softkey_3_release()
        self.pages.append(self.pages.pop(0))
        self.active_page = self.pages[0]
        self.active_page.display()

    def display(self):
        self.active_page.display()
    
    def softkey_1_press(self):
        self.active_page.softkey_1_press()
        self.ref_1_release = self.active_page.softkey_1_release
    
    def softkey_1_release(self):
        if self.ref_1_release is not None:
            self.ref_1_release()
            self.ref_1_release = None
    
    def softkey_2_press(self):
        self.active_page.softkey_2_press()
        self.ref_2_release = self.active_page.softkey_2_release
    
    def softkey_2_release(self):
        if self.ref_2_release is not None:
            self.ref_2_release()
            self.ref_2_release = None
    
    def softkey_3_press(self):
        self.active_page.softkey_3_press()
        self.ref_3_release = self.active_page.softkey_3_release
    
    def softkey_3_release(self):
        if self.ref_3_release is not None:
            self.ref_3_release()
            self.ref_3_release = None
    
    def digit(self, digit):
        self.active_page.digit(digit)
