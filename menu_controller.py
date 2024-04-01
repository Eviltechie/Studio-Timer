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
        self.active_page.display()
    
    def next_page(self):
        self.pages.append(self.pages.pop(0))
        self.active_page = self.pages[0]
        self.active_page.display()
