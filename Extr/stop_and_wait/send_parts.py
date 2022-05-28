
from random import randint
import socket

#в этой функции считаем контрольную сумму
def const_pocket(call, data = None):
    if data is None:
        new_data = 'ack'.encode('utf-8')
    else:
        new_data = data
    checksum = 0
    for i in new_data: checksum += i
    checksum = 0xff - checksum & 0xff
    encoded = checksum.to_bytes(1, byteorder='big') + call.to_bytes(1, byteorder='big') + new_data
    return encoded



def receive_and_construct(my_socket, size_of_the_file, size):
    need = 0
    data = []

    while size_of_the_file > 0: #работаем пока нам не придет весь файл
        try:
            pocket, address = my_socket.recvfrom(size + 2)
            if randint(1, 10) > 7: raise socket.timeout()
            if pocket[1] == need: #проверяем номер ack
                constructed = 0
                for i in pocket[2:]: constructed += i
                if (constructed & 0xff) + pocket[0] != 0xff: #проверяем checksum
                    print('Checksum is incorrect, something is missing')
                    continue #в этот момент продолжаем
                data.append(pocket[2:])
                size_of_the_file -= len(data[-1])
                print(f'Received index {pocket[1]}')
                need = (pocket[1] + 1) % 2


            my_socket.sendto(const_pocket(pocket[1]), address)
            print(f'Sent {pocket[1]} ACK.')

        except socket.timeout:
            print('Timeout exception')
            continue #продолжаем дальше работать

    total = bytes()
    for i in range(len(data)):
        total += data[i] #cобираем вместе
    print(f'Totally received {len(total)} bytes')
    return total.decode()



def send(my_socket, data, size):
    data = data.encode('utf-8')
    split = []
    i = 0
    while True:
        split.append(data[i: i + size])
        i += size
        if i >= len(data): break
    call = 1

    for i, pocket in enumerate(split):

        call += 1
        call %= 2

        new_pocket = const_pocket(call, pocket)
        while True:
            my_socket.send(new_pocket)
            print(f'Sent {i} pocket. Index {call}')
            try:
                ack, h = my_socket.recvfrom(5)
                if randint(1, 10) > 7: raise socket.timeout()
                if ack == const_pocket(call):
                    print(f'Received {call} ACK.')
                    break
            except socket.timeout:
                print('Timeout exception')
                continue #продолжаем если вышло время