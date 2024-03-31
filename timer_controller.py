import timer
import led

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
    
    def time_string_to_seconds(self):
        try:
            hours = int(self.time_string[0:2])
        except ValueError:
            hours = 0
        
        try:
            minutes = int(self.time_string[2:4])
        except ValueError:
            minutes = 0
        
        try:
            seconds = int(self.time_string[4:6])
        except ValueError:
            seconds = 0
        
        if seconds > 59:
            minutes = minutes + (seconds // 60)
            seconds = seconds % 60
        
        if minutes > 59:
            hours = hours + (minutes // 60)
            minutes = minutes % 60
        
        if hours > 99:
            hours = 99
        
        self.active_timer.set_time((hours * 60 * 60) + (minutes * 60) + seconds)
    
    def push_digit(self, digit):
        self.time_string = self.time_string[-5:] + str(digit)
        self.display_time()
    
    def display_time(self):
        led.digit_1(self.time_string[0])
        led.digit_2(self.time_string[1])
        led.digit_3(self.time_string[2])
        led.digit_4(self.time_string[3])
        led.digit_5(self.time_string[4])
        led.digit_6(self.time_string[5])
    
    def notify(self, timer, event):
        if timer == self.active_timer:
            self.time_seconds_to_string();
            self.display_time()
        if event == "stop":
            led.sw_rgb(10, 255, 0, 0)
            led.keypad_color(32, 255, 50)
