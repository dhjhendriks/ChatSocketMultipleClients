import socket,select,errno,sys,os,threading,time,argparse
from datetime import datetime
from source.settings import *
from source.language import *

def welcome(VERSION,EXIT_STRING):
    os.system('cls')
    print(f"{get_text('welcome',L)} {VERSION}")
    print(f"{get_text('type',L)} '{EXIT_STRING}' {get_text('to exit',L)}\n")

############################### Arguments

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

def server_send(sockets_list,my_socket,clients,logfile,HEADER_LENGTH,EXIT_STRING):
    while True:
        message = input()
        if message == EXIT_STRING:
            text_message(f"{logfile}",f"{get_text('You stopped the server',L)}")
            sys.exit()

def receive_message(my_socket,HEADER_LENGTH):
    try:
        message_header = my_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode(CODEC).strip())
        return {'header': message_header, 'data': my_socket.recv(message_length)}
    except:
        return False

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
                text_message(f"{logfile}",f"Accepted new connection from {client_address} - username: {user['data'].decode(CODEC)}")
            else:
                message = receive_message(notified_socket,HEADER_LENGTH)
                if message is False:
                    text_message(f"{logfile}",f"Closed connection from: {clients[notified_socket]['data'].decode(CODEC)}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                text_message(f"{logfile}",f"{user['data'].decode(CODEC)}: {message['data'].decode(CODEC)}")
                user = clients[notified_socket]
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

############################### Client

def client_send(my_username,my_socket,logfile,EXIT_STRING):
    while True:
        message = input()
        if message == EXIT_STRING:
            text_message(f"{logfile}",f"You closed the connection")
            sys.exit()
        if message:
            my_socket.send(header(encod(message)) + encod(message))
            text_message(f"{logfile}",f"{my_username}> {message}")
           
def client_recv(my_socket,HEADER_LENGTH,logfile):
    while True:
        try:
            while True:
                username_header = my_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    text_message(f"{logfile}",f"Connection closed by the server")
                    sys.exit()
                username_length = int(username_header.decode(CODEC).strip())
                username = my_socket.recv(username_length).decode(CODEC)
                message_header = my_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode(CODEC).strip())
                recv_message = my_socket.recv(message_length).decode(CODEC)
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