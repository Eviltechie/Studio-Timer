import timer_led
import timer_lcd
    
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

clear_screen()
set_position(0, 0)
lcd.write('Hello, world!')
