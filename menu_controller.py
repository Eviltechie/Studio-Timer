import menu

class MenuController:
    def __init__(self):
        self.pages = [menu.MenuDirectionPreset(self), menu.MenuFiveSeconds(self)]
        self.active_page = self.pages[0]
        self.active_page.display()
    
    def next_page(self):
        self.pages.append(self.pages.pop(0))
        self.active_page = self.pages[0]
        self.active_page.display()
