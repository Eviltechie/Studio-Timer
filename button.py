import micropython
import time
import machine

class Button:    
    def __init__(self, pin_number, on_press=None, on_release=None):
        # GPIO number used to construct a Pin
        self.pin_number = pin_number
        # Method to run on press, or None
        self.on_press = on_press
        # Method to run on release, or None
        self.on_release = on_release
        
        self.pin = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pin.irq(handler=self.handle_irq, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, hard=True)
        self.callback_ref = self.callback
        self.pressed = False
    
    # Handle the hard interupt
    def handle_irq(self, pin):
        self.pin.irq(handler=None)
        micropython.schedule(self.callback_ref, None)
    
    # Re-enable the hard interupt
    def reset_irq(self):
        self.pin.irq(handler=self.handle_irq, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, hard=True)
    
    # The interrupt handler schedules this to run so we can allocate memory and such
    def callback(self, x):
        self.pressed = not self.pressed
        if self.pressed and self.on_press is not None:
            self.on_press()
        elif self.on_release is not None:
            self.on_release()
        # Blocking isn't great, alternative can be to build a timer that
        # runs every 20ms and then push onto a queue to re-enable.
        time.sleep(0.02)
        self.reset_irq()

class PrintButton(Button):
    def __init__(self, pin_number, name):
        self.name = name
        super().__init__(pin_number, self.press, self.release)
    
    def press(self):
        print("Button_" + self.name + "_press")
    
    def release(self):
        print("Button_" + self.name + "_release")
