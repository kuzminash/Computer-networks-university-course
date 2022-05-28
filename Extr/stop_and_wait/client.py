import socket
import send_parts

HOST = 'localhost'
PORT = 12321
TIMEOUT = 1
SIZE = 1024
NOW = 'receive' #поддерживаем и принятие и отправку со стороны клиента

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.settimeout(TIMEOUT)

if __name__ == '__main__':
   with open('text.txt', 'r') as f:
      contents = f.read()
   if NOW == 'send':
      client_socket.connect((HOST, PORT))
      send_parts.send(client_socket, contents, 1024)

   if NOW == 'receive':
      client_socket.bind((HOST, PORT))
      received_server_data = send_parts.receive_and_construct(client_socket, len(contents.encode('utf-8')), 1024)
      with open('client.txt', 'w') as f: f.write(received_server_data)