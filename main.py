import led
import lcd
import button
import select
import sys
import re

poll_object = select.poll()
poll_object.register(sys.stdin, select.POLLIN)

# Button() uses GPIO number
sw1 = button.PrintButton(14, "digit_7")
sw2 = button.PrintButton(11, "digit_8")
sw3 = button.PrintButton(10, "digit_9")
sw4 = button.PrintButton(4, "softkey_1")
sw5 = button.PrintButton(21, "digit_0")
sw6 = button.PrintButton(15, "digit_4")
sw7 = button.PrintButton(17, "digit_5")
sw8 = button.PrintButton(16, "digit_6")
sw9 = button.PrintButton(3, "softkey_2")
sw10 = button.PrintButton(26, "start_stop")
sw11 = button.PrintButton(18, "digit_1")
sw12 = button.PrintButton(19, "digit_2")
sw13 = button.PrintButton(20, "digit_3")
sw14 = button.PrintButton(2, "softkey_3")
sw15 = button.PrintButton(22, "reset")

buffer = []

lcd.clear_screen()
led.lcd_rgb(0, 0, 0)
led.keypad_color(0, 0, 0)
led.sw_rgb(4, 0, 0, 0)
led.sw_rgb(9, 0, 0, 0)
led.sw_rgb(14, 0, 0, 0)
led.sw_rgb(10, 0, 0, 0)
led.sw_rgb(15, 0, 0, 0)

while True:
    if poll_object.poll(0):
        ch = sys.stdin.read(1)
        if ch == "\n":
            pass
        elif ch == "~":
            exec("".join(buffer))
            #parse_buffer("".join(buffer))
            buffer = []
        else:
            buffer.append(ch)
            #print(ord(ch))
            #print(buffer)