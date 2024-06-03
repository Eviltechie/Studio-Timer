import led
import lcd
import button
import select
import sys
import re

poll_object = select.poll()
poll_object.register(sys.stdin, select.POLLIN)

# Button() uses GPIO number
sw1 = button.PrintButton(14, "7")
sw2 = button.PrintButton(11, "8")
sw3 = button.PrintButton(10, "9")
sw4 = button.PrintButton(4, "softkey_1")
sw5 = button.PrintButton(21, "0")
sw6 = button.PrintButton(15, "4")
sw7 = button.PrintButton(17, "5")
sw8 = button.PrintButton(16, "6")
sw9 = button.PrintButton(3, "softkey_2")
sw10 = button.PrintButton(26, "start_stop")
sw11 = button.PrintButton(18, "1")
sw12 = button.PrintButton(19, "2")
sw13 = button.PrintButton(20, "3")
sw14 = button.PrintButton(2, "softkey_3")
sw15 = button.PrintButton(22, "reset")

buffer = []

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