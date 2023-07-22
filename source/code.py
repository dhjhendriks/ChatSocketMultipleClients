import socket
import select
import errno
import sys
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

def print_time():
    tt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(tt)