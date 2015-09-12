# coding=utf-8
import socket
import threading
import time

SERVER_CLIENT_PORT=9002
SERVER_PI_PORT=9003

#心跳包线程
class PiThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.piConnected=False
		self.connectLock=threading.Lock()
	
	def isPiConnected(self):
		self.connectLock.acquire()
		ret=self.piConnected
		self.connectLock.release()
		return ret
		
	def setPiConnected(self, value):
		self.connectLock.acquire()
		self.piConnected=value
		self.connectLock.release()
		
	def run(self):
		global piUdp
		global piAddress
		lastTime=0
		while True:
			while(not self.isPiConnected()):
				data,piAddress=piUdp.recvfrom(1024)
				if(data=="imfuckingcoming"):
					piUdp.sendto("metoo", piAddress)
					print("Raspberry connected\n")
					print("IP: "+piAddress[0]+"    ")
					print("Port: "+str(piAddress[1])+"\n")	
					self.setPiConnected(True)
			piUdp.settimeout(30)
			lastTime=time.time()
			while(self.isPiConnected()):
				try:
					data, piAddress=piUdp.recvfrom(1024)
				except socket.timeout:
					print("Raspberry disconnect\n")
					self.setPiConnected(False)
					break
				if(time.time()-lastTime>30):
					print("Raspberry disconnect\n")
					self.setPiConnected(False)
					break
				if(data=="online"):
					self.lastTime=time.time()
					#piUdp.sendto("online", piAddress)
		
def setupUdp():
	global clientUdp
	global piUdp
	clientUdp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientUdp.bind(("", SERVER_CLIENT_PORT))
	print("Client UDP is listening on port: "+str(SERVER_CLIENT_PORT))
	piUdp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	piUdp.bind(("", SERVER_PI_PORT))
	print("Raspberry UDP is listening on port: "+str(SERVER_PI_PORT))
	
def handleClient(piThread):
	global piUdp
	global clientUdp
	while(True):
		data=clientUdp.recv(1024)
		if(piThread.isPiConnected()):
			piUdp.sendto(data, piAddress)
		
try:
	setupUdp()
	piThread=PiThread()
	piThread.setDaemon(True)
	piThread.start()
	handleClient(piThread)
	
except KeyboardInterrupt:
	piUdp.close()
	clientUdp.close()
		
