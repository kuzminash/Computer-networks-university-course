import socket
import send_parts

HOST = 'localhost'
PORT = 12321
TIMEOUT = 1
SIZE = 1024
NOW = 'send' #поддерживаем и принятие и отправку со стороны клиента

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.settimeout(TIMEOUT)

if __name__ == '__main__':
   with open('text.txt', 'r') as f:
      contents = f.read()
   if NOW == 'send':
      server_socket.connect((HOST, PORT))
      send_parts.send(server_socket, contents, 1024)

   if NOW == 'receive':
      server_socket.bind((HOST, PORT))
      received_server_data = send_parts.receive_and_construct(server_socket, len(contents.encode('utf-8')), 1024)
      with open('server.txt', 'w') as f: f.write(received_server_data)
