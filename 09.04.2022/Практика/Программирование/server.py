import socket
import random
import time
host = '127.0.0.1'
port = 5005
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_udp.bind((host,port))
while True:
    obj, address = socket_udp.recvfrom(1024)
    loose = (random.randint(1, 100) > 80)
    if loose:
        continue
    time.sleep(random.random())
    socket_udp.sendto(obj.decode().upper().encode(), address)

