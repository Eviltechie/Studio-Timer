import timer

class TimerController:
    
    def __init__(self):
        self.time_string = "000000"
        self.timers = [timer.Timer(self), timer.Timer(self), timer.Timer(self)]
        self.active_timer = self.timers[0]
    
    def time_seconds_to_string(self):
        time_seconds = self.active_timer.time
        
        hours = time_seconds // 3600
        remainder = time_seconds % 3600
        
        minutes = remainder // 60
        seconds = remainder % 60
        
        self.time_string = "{:02d}{:02d}{:02d}".format(hours, minutes, seconds)
    
    def notify(self, timer):
        if timer == self.active_timer:
            self.time_seconds_to_string();
            print(self.time_string)

x = TimerController()
x.timers[0].set_time(300)
x.timers[1].set_time(300)
x.timers[2].set_time(300)
