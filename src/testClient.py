import socket
import time
address=("localhost", 9001)

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto("w", address)
s.sendto("d", address)
time.sleep(1)
s.sendto("x", address)