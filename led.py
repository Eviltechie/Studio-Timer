import machine
import colors

#Init i2c
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

switch_address = {
    1: 0x36,
    2: 0x39,
    3: 0x3C,
    4: 0x3F,
    5: 0x42,
    6: 0x48,
    7: 0x4B,
    8: 0x4E,
    9: 0x51,
    10: 0x54,
    11: 0x5A,
    12: 0x5D,
    13: 0x60,
    14: 0x63,
    15: 0x66,
}

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

def write_dev_config_3(i2c, down_deghost, up_deghost, maximum_current, up_deghost_enable):
    data = (down_deghost << 6) + (up_deghost << 4) + (maximum_current << 1) + up_deghost_enable
    reg_write(i2c, 0x40, 0x04, data)

# Sets the overall max current for R/B/G channels. Default is 50%.
def rgb_current_set(r, g, b):
    if r < 0 or g < 0 or b < 0 or r > 127 or g > 127 or b > 127:
        raise Exception("Current out of range")
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x40, 0x09, msg)

# CS15, SW3, SW4, SW5
def lcd_rgb(r, g, b):
    if r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255:
        raise Exception("Brightness out of range")
    msg = bytearray()
    msg.append(r)
    i2c.writeto_mem(0x42, 0x45, msg)
    
    msg = bytearray()
    msg.append(g)
    i2c.writeto_mem(0x42, 0x57, msg)
    
    msg = bytearray()
    msg.append(b)
    i2c.writeto_mem(0x42, 0x69, msg)

def lcd_current(r, g, b):
    if r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255:
        raise Exception("Brightness out of range")
    msg = bytearray()
    msg.append(r)
    i2c.writeto_mem(0x41, 0x45, msg)
    
    msg = bytearray()
    msg.append(g)
    i2c.writeto_mem(0x41, 0x57, msg)
    
    msg = bytearray()
    msg.append(b)
    i2c.writeto_mem(0x41, 0x69, msg)

def sw_rgb(sw, r, g, b):
    if sw < 1 or sw > 15:
        raise Exception("Switch out of range")
    if r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255:
        raise Exception("Brightness out of range")
    msg = bytearray()
    msg.append(r)
    msg.append(g)
    msg.append(b)
    i2c.writeto_mem(0x42, switch_address[sw], msg)

def sw_hsv(sw, h, s, v):
    if sw < 1 or sw > 15:
        raise Exception("Switch out of range")
    if h < 0 or s < 0 or v < 0 or h > 255 or s > 255 or v > 255:
        raise Exception("HSV out of range")
    rgb = colors.rainbow(h, s, v)
    msg = bytearray()
    msg.append(rgb[0])
    msg.append(rgb[1])
    msg.append(rgb[2])
    i2c.writeto_mem(0x42, switch_address[sw], msg)

def keypad_color(h, s, v):
    sw_hsv(1, h, s, v)
    sw_hsv(2, h, s, v)
    sw_hsv(3, h, s, v)
    sw_hsv(6, h, s, v)
    sw_hsv(7, h, s, v)
    sw_hsv(8, h, s, v)
    sw_hsv(11, h, s, v)
    sw_hsv(12, h, s, v)
    sw_hsv(13, h, s, v)
    sw_hsv(5, h, s, v)

def colons(a, b, c, d):
    if a < 0 or b < 0 or c < 0 or d < 0 or a > 255 or b > 255 or c > 255 or d > 255:
        raise Exception("Brightness out of range")
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

def digit_1(value):
    segments = {
        " ": b'\x00\x00\x00\x00\x00\x00\x00\x00',
        "0": b'\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00',
        "1": b'\x00\xFF\xFF\x00\x00\x00\x00\x00',
        "2": b'\xFF\xFF\x00\xFF\xFF\x00\xFF\x00',
        "3": b'\xFF\xFF\xFF\xFF\x00\x00\xFF\x00',
        "4": b'\x00\xFF\xFF\x00\x00\xFF\xFF\x00',
        "5": b'\xFF\x00\xFF\xFF\x00\xFF\xFF\x00',
        "6": b'\xFF\x00\xFF\xFF\xFF\xFF\xFF\x00',
        "7": b'\xFF\xFF\xFF\x00\x00\x00\x00\x00',
        "8": b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00',
        "9": b'\xFF\xFF\xFF\xFF\x00\xFF\xFF\x00',
        ".": b'\x00\x00\x00\x00\x00\x00\x00\xFF',
    }
    i2c.writeto_mem(0x42, 0x00, segments[value])

# FGDC.ABE
def digit_2(value):
    segments = {
        " ": b'\x00\x00\x00\x00\x00\x00\x00\x00',
        "0": b'\xFF\x00\xFF\xFF\x00\xFF\xFF\xFF',
        "1": b'\x00\x00\x00\xFF\x00\x00\xFF\x00',
        "2": b'\x00\xFF\xFF\x00\x00\xFF\xFF\xFF',
        "3": b'\x00\xFF\xFF\xFF\x00\xFF\xFF\x00',
        "4": b'\xFF\xFF\x00\xFF\x00\x00\xFF\x00',
        "5": b'\xFF\xFF\xFF\xFF\x00\xFF\x00\x00',
        "6": b'\xFF\xFF\xFF\xFF\x00\xFF\x00\xFF',
        "7": b'\x00\x00\x00\xFF\x00\xFF\xFF\x00',
        "8": b'\xFF\xFF\xFF\xFF\x00\xFF\xFF\xFF',
        "9": b'\xFF\xFF\xFF\xFF\x00\xFF\xFF\x00',
        ".": b'\x00\x00\x00\x00\xFF\x00\x00\x00',
    }
    i2c.writeto_mem(0x42, 0x12, segments[value])

def digit_3(value):
    segments = {
        " ": b'\x00\x00\x00\x00\x00\x00\x00\x00',
        "0": b'\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00',
        "1": b'\x00\xFF\xFF\x00\x00\x00\x00\x00',
        "2": b'\xFF\xFF\x00\xFF\xFF\x00\xFF\x00',
        "3": b'\xFF\xFF\xFF\xFF\x00\x00\xFF\x00',
        "4": b'\x00\xFF\xFF\x00\x00\xFF\xFF\x00',
        "5": b'\xFF\x00\xFF\xFF\x00\xFF\xFF\x00',
        "6": b'\xFF\x00\xFF\xFF\xFF\xFF\xFF\x00',
        "7": b'\xFF\xFF\xFF\x00\x00\x00\x00\x00',
        "8": b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00',
        "9": b'\xFF\xFF\xFF\xFF\x00\xFF\xFF\x00',
        ".": b'\x00\x00\x00\x00\x00\x00\x00\xFF',
    }
    i2c.writeto_mem(0x42, 0x24, segments[value])

def digit_4(value):
    segments = {
        " ": b'\x00\x00\x00\x00\x00\x00\x00\x00',
        "0": b'\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00',
        "1": b'\x00\xFF\xFF\x00\x00\x00\x00\x00',
        "2": b'\xFF\xFF\x00\xFF\xFF\x00\xFF\x00',
        "3": b'\xFF\xFF\xFF\xFF\x00\x00\xFF\x00',
        "4": b'\x00\xFF\xFF\x00\x00\xFF\xFF\x00',
        "5": b'\xFF\x00\xFF\xFF\x00\xFF\xFF\x00',
        "6": b'\xFF\x00\xFF\xFF\xFF\xFF\xFF\x00',
        "7": b'\xFF\xFF\xFF\x00\x00\x00\x00\x00',
        "8": b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00',
        "9": b'\xFF\xFF\xFF\xFF\x00\xFF\xFF\x00',
        ".": b'\x00\x00\x00\x00\x00\x00\x00\xFF',
    }
    i2c.writeto_mem(0x42, 0x08, segments[value])

# FGDC.ABE
def digit_5(value):
    segments = {
        " ": b'\x00\x00\x00\x00\x00\x00\x00\x00',
        "0": b'\xFF\x00\xFF\xFF\x00\xFF\xFF\xFF',
        "1": b'\x00\x00\x00\xFF\x00\x00\xFF\x00',
        "2": b'\x00\xFF\xFF\x00\x00\xFF\xFF\xFF',
        "3": b'\x00\xFF\xFF\xFF\x00\xFF\xFF\x00',
        "4": b'\xFF\xFF\x00\xFF\x00\x00\xFF\x00',
        "5": b'\xFF\xFF\xFF\xFF\x00\xFF\x00\x00',
        "6": b'\xFF\xFF\xFF\xFF\x00\xFF\x00\xFF',
        "7": b'\x00\x00\x00\xFF\x00\xFF\xFF\x00',
        "8": b'\xFF\xFF\xFF\xFF\x00\xFF\xFF\xFF',
        "9": b'\xFF\xFF\xFF\xFF\x00\xFF\xFF\x00',
        ".": b'\x00\x00\x00\x00\xFF\x00\x00\x00',
    }
    i2c.writeto_mem(0x42, 0x1A, segments[value])

def digit_6(value):
    segments = {
        " ": b'\x00\x00\x00\x00\x00\x00\x00\x00',
        "0": b'\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00',
        "1": b'\x00\xFF\xFF\x00\x00\x00\x00\x00',
        "2": b'\xFF\xFF\x00\xFF\xFF\x00\xFF\x00',
        "3": b'\xFF\xFF\xFF\xFF\x00\x00\xFF\x00',
        "4": b'\x00\xFF\xFF\x00\x00\xFF\xFF\x00',
        "5": b'\xFF\x00\xFF\xFF\x00\xFF\xFF\x00',
        "6": b'\xFF\x00\xFF\xFF\xFF\xFF\xFF\x00',
        "7": b'\xFF\xFF\xFF\x00\x00\x00\x00\x00',
        "8": b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00',
        "9": b'\xFF\xFF\xFF\xFF\x00\xFF\xFF\x00',
        ".": b'\x00\x00\x00\x00\x00\x00\x00\xFF',
    }
    i2c.writeto_mem(0x42, 0x2C, segments[value])

def digit_1_raw(a, b, c, d, e, f, g, dp):
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
    
def dig_2_raw(a, b, c, d, e, f, g, dp):
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
    
def dig_3_raw(a, b, c, d, e, f, g, dp):
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
    
def dig_4_raw(a, b, c, d, e, f, g, dp):
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
    
def dig_5_raw(a, b, c, d, e, f, g, dp):
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
    
def dig_6_raw(a, b, c, d, e, f, g, dp):
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

reg_write(i2c, 0x40, 0x00, 1) #enable
reg_write(i2c, 0x40, 0x01, dev_initial(0x6, 0x0, 0x0))
reg_write(i2c, 0x40, 0x00, 0)
reg_write(i2c, 0x40, 0x00, 1)

rgb_current_set(127,127,127)
lcd_current(255,255,255)

# Set current of colons.
i2c.writeto_mem(0x41, 0x10, b'\x08')
i2c.writeto_mem(0x41, 0x22, b'\x08')
i2c.writeto_mem(0x41, 0x34, b'\x08')
i2c.writeto_mem(0x41, 0x46, b'\x08')

# Set current of seven segments.
i2c.writeto_mem(0x41, 0x00, b'\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F')
i2c.writeto_mem(0x41, 0x12, b'\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F')
i2c.writeto_mem(0x41, 0x24, b'\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F\x5F')
