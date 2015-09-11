import RPi.GPIO as GPIO
import time
import socket

UdpPort=9001
SERVER_PI_PORT
SERVER_IP="121.42.147.185"

class Car:
    #Define the GPIO interfaces
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
        self.forwardKeyPressed=False
        self.backwardKeyPressed=False
        self.leftKeyPressed=False
        self.rightKeyPressed=False
        self.rushKeyPressed=False

    def forward(self):
        GPIO.output([Car.in1, Car.in2], (GPIO.HIGH, GPIO.LOW))
        GPIO.output([Car.in3, Car.in4], (GPIO.HIGH, GPIO.LOW))

    def backward(self):
        GPIO.output([Car.in1, Car.in2], (GPIO.LOW, GPIO.HIGH))
        GPIO.output([Car.in3, Car.in4], (GPIO.LOW, GPIO.HIGH))

    def stop(self):
        GPIO.output([Car.in1, Car.in2, Car.in3, Car.in4], GPIO.HIGH)

    def goStraight(self):
        Car.enaOut.ChangeDutyCycle(self.speed*10)
        Car.enbOut.ChangeDutyCycle(self.speed*10)

    def turnRight(self):
        Car.enaOut.ChangeDutyCycle(100)
        Car.enbOut.ChangeDutyCycle(self.speed*5)

    def turnLeft(self):
        Car.enaOut.ChangeDutyCycle(self.speed*5)
        Car.enbOut.ChangeDutyCycle(100)

    def rush(self):
        GPIO.output([Car.in1, Car.in2], (GPIO.HIGH, GPIO.LOW))
        GPIO.output([Car.in3, Car.in4], (GPIO.HIGH, GPIO.LOW))
        Car.enaOut.ChangeDutyCycle(100)
        Car.enbOut.ChangeDutyCycle(100)

    def changeKey(self, data):
        if(data=="w"):
            self.forwardKeyPressed=True
        elif(data=="x"):
            self.forwardKeyPressed=False
        elif(data=="s"):
            self.backwardKeyPressed=True
        elif(data=="t"):
            self.backwardKeyPressed=False
        elif(data=="a"):
            self.leftKeyPressed=True
        elif(data=="b"):
            self.leftKeyPressed=False
        elif(data=="d"):
            self.rightKeyPressed=True
        elif(data=="e"):
            self.rightKeyPressed=False
        elif(data=="^"):
            self.rushKeyPressed=True
        elif(data=="."):
            self.rushKeyPressed=False
        else:
            print("Unkown message: "+data+"\n")
        self.onKeyChanged()


    def onKeyChanged(self):
        if(self.rushKeyPressed):
            self.rush()
        elif(self.forwardKeyPressed):
            if(self.backwardKeyPressed):
                self.stop()
            else:
                self.forward()
                if(self.rightKeyPressed):
                    if(not self.leftKeyPressed):
                        self.turnRight()
                    else:
                        self.goStraight()
                elif(self.leftKeyPressed):
                    if(not self.rightKeyPressed):
                        self.turnLeft()
                    else:
                        self.goStraight()
                else:
                        self.goStraight()
        elif(self.backwardKeyPressed):
            if(self.forwardKeyPressed):
                self.stop()
            else:
                self.backward()
                if(self.rightKeyPressed):
                    if(not self.leftKeyPressed):
                        self.turnRight()
                    else:
                        self.goStraight()
                elif(self.leftKeyPressed):
                    if(not self.rightKeyPressed):
                        self.turnLeft()
                    else:
                        self.goStraight()
                else:
                    self.goStraight()
        else:
            self.stop()
        
def startSocket(_car_):
	global s
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UdpPort));
    print("UPD socket created, listening on: "+str(UdpPort)+"\n")
	print("Connecting to server...\n")
	s.sendto("imfuckingcoming", (SERVER_IP, SERVER_PI_PORT))
	s.settimeout(8)
	data=s.recv()
	if(data=="metoo"):
		print("Server connected successfully!\n")
	s.settimeout(None)
    while True:
        data=s.recv(1024)
        _car_.changeKey(data)
        #print(data+"\n")

try:
    car=Car()
    startSocket(car)
except KeyboardInterrupt:
    s.close()
    Car.enaOut.stop()
    Car.enbOut.stop()
    GPIO.cleanup()

s.close()
Car.enaOut.stop()
Car.enbOut.stop()
GPIO.cleanup()