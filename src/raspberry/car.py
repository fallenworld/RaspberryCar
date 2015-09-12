import RPi.GPIO as GPIO
import time
import socket
import threading
import os

UdpPort=9001
SERVER_PI_PORT=9003
SERVER_IP="121.42.147.185"
serverAddress=(SERVER_IP, SERVER_PI_PORT)

class ConnectThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.online=False
		self.onlineLock=threading.Lock()

	def isOnline(self):
		self.onlineLock.acquire()
		ret=self.online
		self.onlineLock.release()
		return ret
		
	def setOnline(self, value):
		self.onlineLock.acquire()
		self.online=value
		self.onlineLock.release()
		
	def run(self):
		global udp
		lastTime=0
		while(True):
			print("Connecting to server...\n")
			udp.sendto("imfuckingcoming", serverAddress)
			udp.settimeout(5)
			try:
				data=udp.recv(1024)
			except:
				print("Connect time out\n")
				os._exit(1)
			if(data=="metoo"):
				print("Server connected successfully!\n")
				self.setOnline(True);
				udp.settimeout(None)
			else:
				print("Wrong message received from server: "+data+"\n")
				os._exit(1)
			lastTime=time.time()
			while self.isOnline():
				udp.sendto("online", serverAddress)
				time.sleep(10)
				
					
class Car:
    #Define the GPIO interfaces
    in1=16
    in2=18
    in3=13
    in4=15
    ena=11
    enb=12

    def __init__(self, connectThread):
	self.connectThread=connectThread
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
			
    def waitMessage(self):
        global udp
        lastTime=time.time()
        while True:
            if(connectThread.isOnline()):
                data=udp.recv(1024)
                self.changeKey(data)
            else:
                time.sleep(1)
		'''
		udp.settimeout(30)
		while True:
			try:
				data=udp.recv(1024)
			except socket.timeout
				if(self.connectThread.isOnline())
					print("Server disconnect\n")
					self.connectThread.setOnline(False)
			if(time.time()-lastTime>30):
				print("Server disconnect\n")
				self.setPiConnected(False)
			if(data=="online"):
				self.lastTime=time.time()
			else:
				if()
		'''		
				

def startSocket():
    global udp
    udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("", UdpPort));
    print("UPD socket created, listening on: "+str(UdpPort)+"\n")
	
def clean():
    udp.close()
    Car.enaOut.stop()
    Car.enbOut.stop()
    GPIO.cleanup()

try:
    startSocket()
    connectThread=ConnectThread()
    connectThread.setDaemon(True)
    car=Car(connectThread)
    connectThread.start()
    car.waitMessage()
    clean()
	

except KeyboardInterrupt:
    clean()
