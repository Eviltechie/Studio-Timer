import machine
import time

lcd = machine.UART(0)
lcd.init(baudrate=9600, bits=8, parity=None, stop=1, tx=machine.Pin(12), rx=machine.Pin(13))

# Clears the screen and returns cursor to top left.
def clear_screen():
    lcd.write(b'\xFE\x51')
    time.sleep(0.005) # Sleep during display execution time
    
# Moves the cursor to the specified line and column, zero indexed.
def set_position(line, column):
    if line < 0 or line > 1:
        raise Exception("Line out of range")
    if column < 0 or column > 15:
        raise Exception("Column out of range")
    msg = bytearray(b'\xFE\x45')
    pos = (line * 0x40) + column
    msg.append(pos)
    lcd.write(msg)

# Write text to the display.
def write(text):
    lcd.write(text)
