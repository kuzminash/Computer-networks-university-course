import socket
import ipaddress



def output_ur():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f'Your ip: {str(local_ip)}')
    network = ipaddress.IPv4Network(local_ip)
    print(f'Netmask {network.netmask}')

def all_ports():
    start = int(input('Start port number '))
    end = int(input('End port number '))
    IP = '127.0.0.1'
    for port in range(start, end + 1):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = (IP, port)
        result_of_check = a_socket.connect_ex(location)
        if result_of_check == 0:
            print(f'Port {port} is available')
        else:
            print(f'Port {port} is not open')


if __name__ == '__main__':
    all_ports()
