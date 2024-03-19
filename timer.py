import led
import lcd
import picozero
import machine
import micropython


led.lcd_rgb(255,0,0)
lcd.clear_screen()
led.colons(255,255,255,255)
led.sw_rgb(10, 255, 0, 0)

time = "      "

def time_push(digit):
    global time
    time = time[-5:] + str(digit)
    display_time()

def display_time():
    global time
    led.digit_1(time[0])
    led.digit_2(time[1])
    led.digit_3(time[2])
    led.digit_4(time[3])
    led.digit_5(time[4])
    led.digit_6(time[5])

# Button() uses GPIO number

# 7
sw1 = picozero.Button(14)

def button_digit_7():
    print("7")

sw1.when_pressed = button_digit_7

# 8
sw2 = picozero.Button(11)

def button_digit_8():
    print("8")

sw2.when_pressed = button_digit_8

# 9
sw3 = picozero.Button(10)

def button_digit_9():
    print("9")

sw3.when_pressed = button_digit_9

# softkey 1
sw4 = picozero.Button(4)

def button_softkey_1():
    print("softkey_1")

sw4.when_pressed = button_softkey_1

# 0
sw5 = picozero.Button(21)

def button_digit_0():
    print("0")

sw5.when_pressed = button_digit_0

# 4
sw6 = picozero.Button(15)

def button_digit_4():
    print("4")

sw6.when_pressed = button_digit_4

# 5
sw7 = picozero.Button(17)

def button_digit_5():
    print("5")

sw7.when_pressed = button_digit_5

# 6
sw8 = picozero.Button(16)

def button_digit_6():
    print("6")

sw8.when_pressed = button_digit_6

# softkey 2
sw9 = picozero.Button(3)

def button_softkey_2():
    print("softkey_2")

sw9.when_pressed = button_softkey_2

# start/stop
sw10 = picozero.Button(26)

def button_start_stop():
    global timer_running
    if timer_running:
        timerA_stop()
    else:
        timerA_start()

sw10.when_pressed = button_start_stop

# 1
sw11 = picozero.Button(18)

def button_digit_1():
    print("1")

sw11.when_pressed = button_digit_1

# 2
sw12 = picozero.Button(19)

def button_digit_2():
    print("2")

sw12.when_pressed = button_digit_2

# 3
sw13 = picozero.Button(20)

def button_digit_3():
    print("3")

sw13.when_pressed = button_digit_3

#softkey 3
sw14 = picozero.Button(2)

def button_softkey_3():
    print("softkey_3")

sw14.when_pressed = button_softkey_3

# reset
sw15 = picozero.Button(22)

def button_reset():
    print("reset")

sw15.when_pressed = button_reset

timer_running = False
timer_direction = "down"
hue = 0

def tick(x):
    print("tick")
    global hue
    led.sw_hsv(10, hue, 255, 255)
    hue += 1
    if hue == 255:
        hue = 0

def timerA_callback(t):
    micropython.schedule(tick, 0)

timerA = machine.Timer()

# A period of 1000 will cause us to lose milliseconds when stopped if we count based on this
def timerA_start():
    timerA.init(mode=machine.Timer.PERIODIC, period=1000, callback=timerA_callback)
    global timer_running
    timer_running = True
    led.sw_rgb(10, 0, 255, 0)

def timerA_stop():
    global timer_running
    timerA.deinit()
    timer_running = False
    led.sw_rgb(10, 255, 0, 0)