import led
import lcd
import picozero
import machine
import micropython


led.lcd_rgb(255,0,0)
lcd.clear_screen()

# Button() uses GPIO number

# 7
sw1 = picozero.Button(14)

# 8
sw2 = picozero.Button(11)

# 9
sw3 = picozero.Button(10)

# softkey 1
sw4 = picozero.Button(4)

# 0
sw5 = picozero.Button(21)

# 4
sw6 = picozero.Button(15)

# 5
sw7 = picozero.Button(17)

# 6
sw8 = picozero.Button(16)

# softkey 2
sw9 = picozero.Button(3)

# start/stop
sw10 = picozero.Button(26)

# 1
sw11 = picozero.Button(18)

# 2
sw12 = picozero.Button(19)

# 3
sw13 = picozero.Button(20)

#softkey 3
sw14 = picozero.Button(2)

# reset
sw15 = picozero.Button(22)

timer_running = False

def tick(x):
    pass

def timerA_callback(t):
    micropython.schedule(tick, 0)

timerA = machine.Timer()

def timerA_start():
    timerA.init(mode=machine.Timer.PERIODIC, period=1000, callback=timerA_callback)
    global timer_running
    timer_running = True

def timerA_stop():
    global timer_running
    timerA.deinit()
    timer_running = False