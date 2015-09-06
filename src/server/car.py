import RPi.GPIO as GPIO
import time

class Car:
    in1=16
    in2=18
    in3=13
    in4=15
    ena=11
    enb=12

    def __init__(self):
        self.speed=3
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup([Car.in1, Car.in2, Car.in3, Car.in4], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup([Car.ena, Car.enb], GPIO.OUT)
    
    def move(self):
        GPIO.output([Car.in1, Car.in2], (GPIO.HIGH, GPIO.LOW))
        GPIO.output([Car.in3, Car.in4], (GPIO.HIGH, GPIO.LOW))
        GPIO.output([Car.ena, Car.enb], GPIO.HIGH)
        #Car.enaOut=GPIO.PWM(Car.ena, 14000)
        #Car.enbOut=GPIO.PWM(Car.enb, 14000)
        #Car.enaOut.start(100)
        #Car.enbOut.start(100)
        time.sleep(2)
        GPIO.output([Car.in1, Car.in2, Car.in3, Car.in4], GPIO.LOW)
        #Car.enaOut.stop()
        #Car.enbOut.stop()

try:
    car=Car()
    car.move()
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()