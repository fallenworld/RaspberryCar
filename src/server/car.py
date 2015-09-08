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
        self.speed=5
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup([Car.in1, Car.in2, Car.in3, Car.in4], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup([Car.ena, Car.enb], GPIO.OUT)
        Car.enaOut=GPIO.PWM(Car.ena, 1000)
        Car.enbOut=GPIO.PWM(Car.enb, 1000)
        Car.enaOut.start(50)
        Car.enbOut.start(50)

    def forward(self):
        GPIO.output([Car.in1, Car.in2], (GPIO.HIGH, GPIO.LOW))
        GPIO.output([Car.in3, Car.in4], (GPIO.HIGH, GPIO.LOW))

    def backward(self):
        GPIO.output([Car.in1, Car.in2], (GPIO.LOW, GPIO.HIGH))
        GPIO.output([Car.in3, Car.in4], (GPIO.LOW, GPIO.HIGH))

    def stop(self):
        GPIO.output([Car.in1, Car.in2, Car.in3, Car.in4], GPIO.HIGH)

    def goStraight(self):
        Car.enaOut.changeDutyCycle(self.speed*10)
        Car.enbOut.changeDutyCycle(self.speed*10)

    def turnRight(self):
        Car.enaOut.changeDutyCycle(100)
        Car.enbOut.changeDutyCycle(self.speed*10)

    def turnLeft(self):
        Car.enaOut.changeDutyCycle(self.speed*10)
        Car.enbOut.changeDutyCycle(100)

    def onKeyChanged(self):
        if(self.forwardKeyPressed):
            if(self.backKeyPressed):
                self.stop()
            else:
                self.forward()
                if(self.rightKeyPressed):
                    if(!self.leftKeyPressed):
                        self.turnRIght()
                    else:
                        self.goStraight()
                elif(self.leftKeyPressed):
                    if(!self.rightKeyPressed):
                        self.turnLeft()
                    else:
                        self.goStraight()
                else:
                        self.goStraight()
        else:
            if(self.forwardKeyPressed):
                self.stop()
            else:
                self.backward()
                if(self.rightKeyPressed):
                    if(!self.leftKeyPressed):
                        self.turnRIght()
                    else:
                        self.goStraight()
                elif(self.leftKeyPressed):
                    if(!self.rightKeyPressed):
                        self.turnLeft()
                    else:
                        self.goStraight()
                else:d
                    Car.enaOut.changeDutyCycle(self.speed*10)
                    Car.enbOut.changeDutyCycle(self.speed*10)
        

try:
    
except KeyboardInterrupt:
    Car.enaOut.stop()
    Car.enbOut.stop()
    GPIO.cleanup()

Car.enaOut.stop()
Car.enbOut.stop()
GPIO.cleanup()