import random
import socket
import datetime

import PySimpleGUI as pys

now = 'udp'


def create_message(ch):
    message = ""
    for _ in range(ch):
        message += chr(random.randint(34, 126))
    return message


font = ("Didot", 15)

layout = [
    [pys.Text('IP', size=(20, 1), text_color='#990040', background_color='#9dc0fc'),
     pys.InputText('127.0.0.1', key='host')],
    [pys.Text('Port', size=(20, 1), text_color='#990040', background_color='#9dc0fc'),
     pys.InputText('12321', key='port')],
    [pys.Text('Number of packages', size=(20, 1), text_color='#990040', background_color='#9dc0fc'),
     pys.InputText('5', key='packages')],
    [pys.Button('Send')],
]

text = 'Send UDP ' if now == 'udp' else 'Send TCP'
window = pys.Window(text, layout, background_color='#FFD1C1', font=font)
maxx = 1500

if now == 'udp':
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.settimeout(1)

while True:
    event, values = window.read()
    if event == "Exit" or event == pys.WIN_CLOSED:
        break

    if event == "Send":
        addr, port, packages = values['host'], int(values['port']), int(values['packages'])
        send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send.connect((addr, port))
        end = '*'
        send.sendall(f'{str(packages)} {end * (maxx - len(str(packages)) - 1)}'.encode())
        for i in range(packages):
            time = f'{int(datetime.datetime.now().timestamp() * 1000)} '
            new_message = time + create_message(maxx - len(time))
            if now == 'udp':
                udp_socket.sendto(new_message.encode(), (addr, port))
            if now == 'tcp':
                send.sendall(new_message.encode())
        send.close()

window.close()