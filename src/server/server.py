import socket

SERVER_CLIENT_PORT=9002
SERVER_PI_PORT=9003
piConnected=False

def setupUdp():
	global clientUdp
	global piUdp
	clientUdp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	clientUdp.bind(("", SERVER_CLIENT_PORT))
	print("Client UDP is listening on port: "+str(SERVER_CLIENT_PORT))
	piUdp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	piUdp.bind(("", SERVER_PI_PORT))
	print("Raspberry UDP is listening on port: "+str(SERVER_PI_PORT))
	
	
def waitPi():
	global piUdp
	global piConnected
	global piAddress
	while(not piConnected):
		data,piAddress=piUdp.recvfrom(1024)
		if(data=="imfuckingcoming"):
			piConnected=True
			piUdp.sendto("metoo", piAddress)
			print("Raspberry connected\n")
			print("IP: "+piAddress[0]+"    ")
			print("Port: "+str(piAddress[1])+"\n")
			
def handleClient():
	global piUdp
	global clientUdp
	global piConnected
	while(piConnected):
		data=recv(1024)
		piUdp.send(data)
		
while(True):
	setupUdp()
	waitPi()
	handleClient()