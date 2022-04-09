import select
import socket
import datetime
import threading

host = '127.0.0.1'
port = 5005
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

received = []
times = []
def end():
    print(f'Статистика для Ping для {host}')
    print(f'Пакетов отправлено - {sum(received)}, получено - {len(received)}, потеряно - {len(received) - sum(received)}({len(received) - sum(received)}0%)')

    print('Приблизительное время приема-передачи в мс:')
    print(f'Минимальное - {min(times)}, Максимальное - {max(times)}, Среднее - {sum(times) / len(times)}')

for i in range(10):
    try:
        time_send = datetime.datetime.now()
        socket_udp.settimeout(10)
        socket_udp.sendto((f'{i + 1} {time_send}').encode(), (host, port))
        obj, _ = socket_udp.recvfrom(1024)
        time_receive = datetime.datetime.now()
        circle = (time_receive - time_send).microseconds / 1000
        print(f'Ответ от {host}: число байт={len(obj)} время={circle}')
        received.append(1)
        times.append(circle)
    except:
        print('Request timed out')
        received.append(0)
end()