import machine
from machine import UART, Pin

# Setup I2C
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

# Scan for I2C devices
devices = i2c.scan()

# Print devices found.
if devices:
    for d in devices:
        print(hex(d))
        print(bin(d))
# We should expect the following:
#  Broadcast addresses for the LP5866, we don't use these.
#   0x54/1010100
#   0x55/1010101
#   0x56/1010110
#   0x57/1010111
#  Independent addresses for the L5866, which we use.
#   0x40/1000000
#   0x41/1000001
#   0x42/1000010
#   0x43/1000011
# (Since the LP5866 has so many registers it actually responds to 4 "normal" addresses.)
# 0x40 0x0XX
# 0x41 0x1XX
# 0x42 0x2XX
# 0x43 0x3XX

def reg_write(i2c, addr, reg, data):
    msg = bytearray()
    msg.append(data)
    i2c.writeto_mem(addr, reg, msg)
    
def reg_read(i2c, addr, reg, nbytes=1):
    if nbytes < 1:
        return bytearray()
    data = i2c.readfrom_mem(addr, reg, nbytes)
    return data

def dev_initial(max_line_num, data_ref_mode, pwm_fre):
    return (max_line_num << 3) + (data_ref_mode << 1) + pwm_fre

#def read_dev_config_3():
    

def write_dev_config_3(i2c, down_deghost, up_deghost, maximum_current, up_deghost_enable):
    data = (down_deghost << 6) + (up_deghost << 4) + (maximum_current << 1) + up_deghost_enable
    reg_write(i2c, 0x40, 0x04, data)
    
#max 127
def rgb_current_set(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x40, 0x09, msg)

# CS15, SW3, SW4, SW5
def lcd_rgb(r, g, b):
    msg = bytearray()
    msg.append(r)
    i2c.writeto_mem(0x42, 0x45, msg)
    
    msg = bytearray()
    msg.append(g)
    i2c.writeto_mem(0x42, 0x57, msg)
    
    msg = bytearray()
    msg.append(b)
    i2c.writeto_mem(0x42, 0x69, msg)
    
#max 255
def lcd_current(r, g, b):
    msg = bytearray()
    msg.append(r)
    i2c.writeto_mem(0x41, 0x45, msg)
    
    msg = bytearray()
    msg.append(g)
    i2c.writeto_mem(0x41, 0x57, msg)
    
    msg = bytearray()
    msg.append(b)
    i2c.writeto_mem(0x41, 0x69, msg)
    
# CS0, CS1, CS3, SW3

def sw_1(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x36, msg)
    
def sw_2(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x39, msg)
    
def sw_3(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x3C, msg)
    
def sw_4(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x3F, msg)
    
def sw_5(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x42, msg)
    
def sw_6(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x48, msg)
    
def sw_7(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x4B, msg)
    
def sw_8(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x4E, msg)
    
def sw_9(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x51, msg)
    
def sw_10(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x54, msg)
    
def sw_11(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x5A, msg)
    
def sw_12(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x5D, msg)
    
def sw_13(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x60, msg)
    
def sw_14(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x63, msg)
    
def sw_15(r, g, b):
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, 0x66, msg)
    
def dig_1(a, b, c, d, e, f, g, dp):
    msg = bytearray()
    msg.append(a)
    msg.append(b)
    msg.append(c)
    msg.append(d)
    msg.append(e)
    msg.append(f)
    msg.append(g)
    msg.append(dp)
    i2c.writeto_mem(0x42, 0x00, msg)
    
def dig_2(a, b, c, d, e, f, g, dp):
    msg = bytearray()
    msg.append(f)
    msg.append(g)
    msg.append(d)
    msg.append(c)
    msg.append(dp)
    msg.append(a)
    msg.append(b)
    msg.append(e)
    i2c.writeto_mem(0x42, 0x12, msg)
    
def dig_3(a, b, c, d, e, f, g, dp):
    msg = bytearray()
    msg.append(a)
    msg.append(b)
    msg.append(c)
    msg.append(d)
    msg.append(e)
    msg.append(f)
    msg.append(g)
    msg.append(dp)
    i2c.writeto_mem(0x42, 0x24, msg)
    
def dig_4(a, b, c, d, e, f, g, dp):
    msg = bytearray()
    msg.append(a)
    msg.append(b)
    msg.append(c)
    msg.append(d)
    msg.append(e)
    msg.append(f)
    msg.append(g)
    msg.append(dp)
    i2c.writeto_mem(0x42, 0x08, msg)
    
def dig_5(a, b, c, d, e, f, g, dp):
    msg = bytearray()
    msg.append(f)
    msg.append(g)
    msg.append(d)
    msg.append(c)
    msg.append(dp)
    msg.append(a)
    msg.append(b)
    msg.append(e)
    i2c.writeto_mem(0x42, 0x1A, msg)
    
def dig_6(a, b, c, d, e, f, g, dp):
    msg = bytearray()
    msg.append(a)
    msg.append(b)
    msg.append(c)
    msg.append(d)
    msg.append(e)
    msg.append(f)
    msg.append(g)
    msg.append(dp)
    i2c.writeto_mem(0x42, 0x2C, msg)
    
def colons(a, b, c, d):
    msg = bytearray()
    msg.append(a)
    i2c.writeto_mem(0x42, 0x10, msg)
    
    msg = bytearray()
    msg.append(b)
    i2c.writeto_mem(0x42, 0x22, msg)
    
    msg = bytearray()
    msg.append(c)
    i2c.writeto_mem(0x42, 0x34, msg)
    
    msg = bytearray()
    msg.append(d)
    i2c.writeto_mem(0x42, 0x46, msg)


# 0x40 0x0XX
# 0x41 0x1XX
# 0x42 0x2XX
# 0x43 0x3XX

reg_write(i2c, 0x40, 0x00, 1) #enable
reg_write(i2c, 0x40, 0x01, dev_initial(0x6, 0x0, 0x0))
reg_write(i2c, 0x40, 0x00, 0)
reg_write(i2c, 0x40, 0x00, 1)

rgb_current_set(127,127,127)
lcd_current(255,255,255)

lcd_rgb(255,0,0)

uart0 = UART(0)
uart0.init(baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(12), rx=Pin(13))
#uart0.write(b'\xFE')
#uart0.write(b'\x51')
#uart0.write('hello')

# Clears the screen and returns cursor to top left.
def clear_screen():
    uart0.write(b'\xFE\x51')
    
# Moves the cursor to the specified line and column, zero indexed.
def set_position(line, column):
    if line < 0 or line > 1:
        raise Exception("Line out of range")
    if column < 0 or column > 15:
        raise Exception("Column out of range")
    msg = bytearray(b'\xFE\x45')
    pos = (line * 0x40) + column
    msg.append(pos)
    uart0.write(msg)
    
clear_screen()
set_position(0, 0)
uart0.write('Hello, world!')