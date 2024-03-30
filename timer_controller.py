import timer

class TimerController:
    
    def __init__(self):
        self.time_string = "000000"
        self.timers = [timer.Timer(self), timer.Timer(self), timer.Timer(self)]
        self.active_timer = self.timers[0]
    
    def notify(self, timer):
        if timer == self.active_timer:
            print("notify active")
        else:
            print("notify")

x = TimerController()
x.timers[0].set_time(300)
x.timers[1].set_time(300)
x.timers[2].set_time(300)
