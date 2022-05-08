import socket


sock = socket.socket(socket.AF_INET6,  socket.SOCK_DGRAM)
sock.bind(('0:0:0:0:0:0:0:1', 8000))

while True:
    c, addr = sock.recvfrom(1024)
    print(c.decode().upper())