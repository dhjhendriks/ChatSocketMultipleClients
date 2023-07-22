import socket,select,errno,sys,os
from datetime import datetime
from source.settings import *

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False

def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def filewrite(text):
    with open('server.log', 'a') as logfile:
        logfile.write(text + "\n")

def clear_screen():
    os.system('cls')

def server_message(text):
    message = f"{get_time()} - {text}"
    print(f"{message}")
    filewrite(f"{message}")
