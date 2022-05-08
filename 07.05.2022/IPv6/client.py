import socket


while True:
	message = input()
	sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
	sock.sendto(message.encode(), ('0:0:0:0:0:0:0:1', 8000))