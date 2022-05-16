import random
import socket
import datetime

import PySimpleGUI as pys


now = 'udp'
font = ("Didot", 15)
layout = [
    [pys.Text('IP', size=(20, 1), text_color='#990040',background_color='#9dc0fc'), pys.InputText('127.0.0.1')],
    [pys.Text('Port', size=(20, 1), text_color='#990040',background_color='#9dc0fc'), pys.InputText('12321')],
    [pys.Text('Number of packages', size=(20, 1), text_color='#990040',background_color='#9dc0fc'), pys.Text(key = 'packages')],
    [pys.Text('Speed', size=(20, 1), text_color='#990040',background_color='#9dc0fc'), pys.Text(key = 'speed')],
    [pys.Button('Change host and port')],
    [pys.Button('Start')],
]

text = 'UDP Receiver' if now == 'udp' else 'TCP Receiver'
window = pys.Window(text, layout, background_color='#FFD1C1', font = font)


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('127.0.0.1', 12321))
tcp_socket.listen(1)
if now == 'udp':
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.settimeout(1)
    udp_socket.bind(('127.0.0.1', 12321))

maxx = 1500



while True:
    event, values = window.read()
    if event == "Exit" or event == pys.WIN_CLOSED:
        break

    if event == 'Change host and port':
        tcp_socket.close()
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((values[0], int(values[1])))
        tcp_socket.listen()
        if now == 'udp':
            udp_socket.close()
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp_socket.settimeout(1)
            udp_socket.bind((values[0], int(values[1])))

    if event == "Start":
        count = 0
        start_time = 0
        receive, _ = tcp_socket.accept()
        should = int(receive.recv(maxx).decode().split()[0])
        for i in range(should):
            if now == 'tcp':
                message_time = receive.recv(maxx).decode().split()[0]
            if now == 'udp':
                message_time = (udp_socket.recvfrom(maxx)[0]).decode().split()[0]
            count += 1
            if start_time == 0: start_time = int(message_time)
        duration = int(datetime.datetime.now().timestamp() * 1000)

        window['speed'].Update(f'{maxx * count / (duration - start_time)} KB/s')
        window['packages'].Update(f'{count} out of {should}')

        receive.close()

window.close()