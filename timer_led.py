import machine

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

# Sets the max current for R/B/G channels. Default is 50%.
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
