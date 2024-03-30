import machine

class Timer:

    # Pass a manager that we can send updates back to so it knows when to update the display?
    # Pass a color to represent the timer?
    # Pass an ID for the actual machine timer?
    # Not for this class, but need to store button/color state so we can implement screensaver and press feedback.
    def __init__(self, timer_controller):
        self.timer_controller = timer_controller
        self.direction = "down"
        self.running = False
        self.time = 0
        self.rate = 1000
        self.timer = machine.Timer()
        pass

    # Start the timer.
    def start(self):
        if self.direction == "down" and self.time <= 0: # Can't run negative
            return False
        if self.direction == "up" and self.time >= 359999: # Max 99h 59m 59s
            return False
        self.timer.init(mode=machine.Timer.PERIODIC, period=self.rate, callback=self.callback)
        self.timer_running = True
        self.timer_controller.notify(self)
        return True

    # Stop the timer.
    def stop(self):
        self.timer.deinit()
        self.timer_running = False
        self.timer_controller.notify(self)
        return True

    # Change the rate (speed) of the timer.
    # Normal tick is every 1000ms.
    def change_rate(self, rate):
        self.rate = rate
        if self.timer_running:
            self.stop()
            self.start()
        self.timer_controller.notify(self)

    # Change the timer direction. "up" or "down"
    def set_direction(self, direction):
        self.direction = direction
        self.timer_controller.notify(self)

    # Set the time, units is ???
    def set_time(self, time):
        self.time = time
        self.timer_controller.notify(self)

    # Callback which is run once per tick.
    def callback(self, x):
        if self.direction == "down":
            if self.time <= 0:
                self.stop()
            else:
                self.time -= 1
            if self.time <= 0:
                self.stop()
        else: # up
            if self.time >= 359999: # Max 99h 59m 59s
                self.stop()
            else:
                self.time += 1
            if self.time >= 359999:
                self.stop()
        self.timer_controller.notify(self)
        print(self.time)
