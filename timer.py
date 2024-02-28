import led
import lcd


led.lcd_rgb(255,0,0)

lcd.clear_screen()
lcd.set_position(0, 0)
lcd.write('Hello, world!')
