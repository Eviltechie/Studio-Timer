class Timer

# Pass a manager that we can send updates back to so it knows when to update the display?
# Pass a color to represent the timer?
# Pass an ID for the actual machine timer?
# Not for this class, but need to store button/color state so we can implement screensaver and press feedback.
def __init__(self):
    self.direction = "down"
    self.running = False
    self.value = 0
    pass

# Start the timer.
def start(self):
    pass

# Stop the timer.
def stop(self):
    pass

# Change the rate (speed) of the timer.
# Normal tick is every 100ms.
def change_rate(self, delta):
    pass

# Change the timer direction. "up" or "down"
def set_direction(self, direction):
    pass

# Callback which is run once per tick.
def callback(self):
    pass
