import socket,select,errno,sys,os,threading,time,argparse
from datetime import datetime
from configparser import ConfigParser

def welcome(VERSION,EXIT_STRING):
    os.system('cls')
    print(f"{get_text('welcome')} {VERSION}")
    print(f"{get_text('type')} '{EXIT_STRING}' {get_text('to exit')}\n")

############################### Variables

def settings_read(menu,setting):
    config = ConfigParser()
    config.read('config.ini')
    return config.get(menu, setting)

def settings_write():
    config = ConfigParser()
    config.read('config.ini')
    config.set('main', 'PORT', '80')

    with open('config.ini', 'w') as f:
        config.write(f)

def get_text(text):
    global LANGUAGE
    language = ConfigParser()
    language.read('language.ini')
    return language.get(text, LANGUAGE)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    args = parser.parse_args()
    return args.type.lower()

############################### Logging

def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def filewrite(logfile,text):
    with open(logfile, 'a') as log:
        log.write(text + "\n")

def text_message(logfile,text):
    message = f"{get_time()} - {text}"
    print(f"{message}")
    filewrite(f"{logfile}",f"{message}")

############################### Server

def receive_message(my_socket,HEADER_LENGTH):
    try:
        message_header = my_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        return {'header': message_header, 'data': my_socket.recv(length(message_header))}
    except:
        return False

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

def client_send(my_socket,logfile,EXIT_STRING):
    while True:
        message = input()
        if message == EXIT_STRING:
            text_message(f"{logfile}",f"{get_text('you closed the connection')}")
            sys.exit()
        if message:
            my_socket.send(header(encod(message)) + encod(message))
           
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

def encod(text):
    global CODEC
    return text.encode(CODEC)

def decod(text):
    global CODEC
    return text.decode(CODEC)

def header(text):
    global HEADER_LENGTH
    return encod(f"{len(text):<{HEADER_LENGTH}}")

def length(text):
    global CODEC
    return int(text.decode(CODEC).strip())

############################### Variables

VERSION = settings_read('main','version')
IP = settings_read('main','ip')
PORT = int(settings_read('main','port'))
HEADER_LENGTH = int(settings_read('main','header_length'))
EXIT_STRING = settings_read('main','exit_string')
CODEC = settings_read('main','codec')
LANGUAGE =  settings_read('main','language')
logfile = settings_read('main','logfile')
my_username = settings_read('main','username_server')

############################### MAIN

welcome(VERSION,EXIT_STRING)

temp = input (f"IP {IP}: ")
if temp != "": IP = temp
temp = input (f"Port {PORT}: ")
if temp != "": PORT = temp


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
            print(get_text('server not awnsering'))
            sys.exit()
        my_socket.setblocking(False)

        my_username = input(f"{get_text('Enter Username')}: ")
        logfile = f"client_{my_username}.log"

        username = my_username.encode(CODEC)
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode(CODEC)
        my_socket.send(username_header + username)
        text_message(f"{logfile}",f"{get_text('The server on')} {IP}:{PORT} {get_text('accepted the username')}: {my_username}")

        threading.Thread(target=client_send, args=[my_socket,logfile,EXIT_STRING], daemon=False).start()
        threading.Thread(target=client_recv, args=[my_socket,HEADER_LENGTH,logfile], daemon=True).start()

    case _:
        print(get_text('argument text'))
