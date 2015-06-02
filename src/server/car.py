import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
out=8
GPIO.setup(out, GPIO.OUT)

state=1

try:
    while True:
        if state==1:
            GPIO.output(out, 0)
            state=0
        else:
            GPIO.output(out, 1)
            state=1
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()