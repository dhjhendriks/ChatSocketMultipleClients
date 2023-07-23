#!/usr/bin/env python
""" See README.md
Longer description of this module.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__    = "Daniël Hendriks"
__contact__   = "daan@hze.nl"
__copyright__ = "Copyright 2023, HZE"
__date__      = "2023-07-23"
__license__   = "GPLv3"
__status__    = "Development"
__version__   = "V0.1.2"

# Import library
import socket,select,errno,sys,os,threading,time,argparse,ipaddress,string
from datetime import datetime
from configparser import ConfigParser

# Clear screen and print welcme message
def welcome(VERSION,EXIT_STRING):
    os.system('cls')
    print(f"{get_text('welcome')} {__version__}")
    print(f"{get_text('type')} '{EXIT_STRING}' {get_text('to exit')}\n")

############################### Variables

# Read a setting from the config file
def settings_read(section,key):
    config = ConfigParser()
    config.read('config.ini')
    return config.get(section, key)

# Write a setting to the config file
def settings_write(section,key,value):
    config = ConfigParser()
    config.read('config.ini')
    config.set(section, key, value)
    with open('config.ini', 'w') as f:
        config.write(f)

# Get a valid IP
def get_IP(IP):
    temp = input (f"IP {IP}: ")
    if temp:
        if not validate_ip_address(temp):
            print(get_text('not valid'))
            sys.exit()
        IP = temp
        settings_write('main','ip',temp)
    return IP

# Validate the IP address
def validate_ip_address(IP):
   try:
       ip_object = ipaddress.ip_address(IP)
       return True
   except ValueError:
       return False

# Get a valid port
def get_PORT(PORT):
    temp = input (f"Port {PORT}: ")
    if temp:
        if not validate_port(temp):
            print(get_text('not valid'))
            sys.exit()
        PORT = temp
        settings_write('main','port',temp)
    return PORT

# Validate the port
def validate_port(PORT):
   try:
       if 1 <= int(PORT) <= 65535:
        return True
   except ValueError:
       return False

# Get a valid username
def get_username():
    temp = input (f"{get_text('Enter Username')}: ")
    if temp:
        if not validate_username(temp):
            print(get_text('not valid'))
            sys.exit()
    return temp

# Validate username
def validate_username(username):
    match=string.ascii_letters + string.digits + '_'
    if not all([x in match for x in username]):
        return False
    if not (len(username) >=4 and len(username) <=25):
        return False
    if not username[0].isalpha():
        return False
    if username[-1:] == '_':
        return False
    return True

# Get text from language.ini
def get_text(text):
    global LANGUAGE
    language = ConfigParser()
    language.read('language.ini')
    return language.get(text, LANGUAGE)

# Get the python arguments
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    args = parser.parse_args()
    return args.type.lower()

############################### Logging

# Get text of date and time
def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Write text in file
def filewrite(logfile,text):
    with open(logfile, 'a') as log:
        log.write(text + "\n")

# Write text on screen and in file
def text_message(logfile,text):
    message = f"{get_time()} - {text}"
    print(f"{message}")
    filewrite(f"{logfile}",f"{message}")

############################### Server

# Server receive message
def receive_message(my_socket,HEADER_LENGTH):
    try:
        message_header = my_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        return {'header': message_header, 'data': my_socket.recv(length(message_header))}
    except:
        return False

# Server send loop
def server_send(clients,logfile,EXIT_STRING):
    global server_message,my_username
    while True:
        server_message = input()
        if server_message == EXIT_STRING:
            text_message(f"{logfile}",f"{get_text('You stopped the server')}")
            sys.exit()
        if len(server_message) :
            for client_socket in clients:
                client_socket.send(header(encod(my_username)) + encod(my_username)+header(encod(server_message)) + encod(server_message))
            server_message=""

# Server receive loop
def server_recv(sockets_list,my_socket,clients,logfile,HEADER_LENGTH):
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == my_socket:
                client_socket, client_address = my_socket.accept()
                user = receive_message(client_socket,HEADER_LENGTH)
                if user is False:
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user
                text_message(f"{logfile}",f"{get_text('Accepted new connection from')} {client_address} - {get_text('username')}: {user['data'].decode(CODEC)}")
            else:
                message = receive_message(notified_socket,HEADER_LENGTH)
                if message is False:
                    text_message(f"{logfile}",f"{get_text('closed connection from')}: {clients[notified_socket]['data'].decode(CODEC)}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                text_message(f"{logfile}",f"{user['data'].decode(CODEC)}: {message['data'].decode(CODEC)}")
                user = clients[notified_socket]
                for client_socket in clients:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

############################### Client

# Client send loop
def client_send(my_socket,logfile,EXIT_STRING):
    while True:
        message = input()
        if message == EXIT_STRING:
            text_message(f"{logfile}",f"{get_text('you closed the connection')}")
            sys.exit()
        if message:
            my_socket.send(header(encod(message)) + encod(message))

# Client receive loop           
def client_recv(my_socket,HEADER_LENGTH,logfile):
    while True:
        try:
            while True:
                username_header = my_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    text_message(f"{logfile}",f"{get_text('connection closed by the server')}")
                    sys.exit()
                username_length = length(username_header)
                username = decod(my_socket.recv(username_length))
                message_header = my_socket.recv(HEADER_LENGTH)
                message_length = length(message_header)
                recv_message = decod(my_socket.recv(message_length))
                text_message(f"{logfile}",f'{username}> {recv_message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                text_message(f"{logfile}",f"{str(e)}")
                sys.exit()
            continue
        except Exception as e:
            text_message(f"{logfile}",f"{str(e)}")
            sys.exit() 

############################### Encode/Decode

# Encode text
def encod(text):
    global CODEC
    return text.encode(CODEC)

# Decode text
def decod(text):
    global CODEC
    return text.decode(CODEC)

# Get header
def header(text):
    global HEADER_LENGTH
    return encod(f"{len(text):<{HEADER_LENGTH}}")

 # Get length
def length(text):
    global CODEC
    return int(text.decode(CODEC).strip())

############################### Variables

IP = settings_read('main','ip')
PORT = int(settings_read('main','port'))
HEADER_LENGTH = int(settings_read('main','header_length'))
EXIT_STRING = settings_read('main','exit_string')
CODEC = settings_read('main','codec')
LANGUAGE =  settings_read('main','language')
logfile = settings_read('main','logfile')
my_username = settings_read('main','username_server')

############################### MAIN

welcome(__version__,EXIT_STRING)

IP = get_IP(IP)
PORT = get_PORT(PORT)

# Execute server or client code
match get_arguments():
    case "s" | "server":
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.bind((IP, PORT))
        my_socket.listen()

        sockets_list = [my_socket]
        clients = {}
                
        text_message(f"{logfile}",f"{get_text('listening text')} {IP}:{PORT}...")

        threading.Thread(target=server_send, args=[clients,logfile,EXIT_STRING], daemon=False).start()
        threading.Thread(target=server_recv, args=[sockets_list,my_socket,clients,logfile,HEADER_LENGTH], daemon=True).start()

    case "c" | "client":
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            my_socket.connect((IP, PORT))
        except:
            print(f"{get_text('server not awnsering')} {IP}:{PORT}")
            sys.exit()
        my_socket.setblocking(False)

        my_username = get_username()
        logfile = f"client_{my_username}.log"

        username = my_username.encode(CODEC)
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode(CODEC)
        my_socket.send(username_header + username)
        text_message(f"{logfile}",f"{get_text('The server on')} {IP}:{PORT} {get_text('accepted the username')}: {my_username}")

        threading.Thread(target=client_send, args=[my_socket,logfile,EXIT_STRING], daemon=False).start()
        threading.Thread(target=client_recv, args=[my_socket,HEADER_LENGTH,logfile], daemon=True).start()

    case _:
        print(get_text('argument text'))
