import select
import sys
import button

poll_object = select.poll()
poll_object.register(sys.stdin, select.POLLIN)

buffer = []

def parse_buffer(buf):
    print(buf)
    pass

# start/stop
sw10 = button.PrintButton(26, "start_stop")

while True:
    if poll_object.poll(0):
        ch = sys.stdin.read(1)
        if ch == "\n":
            pass
        elif ch == "~":
                parse_buffer("".join(buffer))
                buffer = []
        else:
            buffer.append(ch)
            #print(ord(ch))
            print(buffer)
