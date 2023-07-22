import socket,select,errno,sys,os,threading,time,argparse
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

def filewrite(logfile,text):
    with open(logfile, 'a') as log:
        log.write(text + "\n")

def welcome(VERSION,EXIT_STRING):
    os.system('cls')
    print(f"Welcome to Socket! {VERSION}")
    print(f"Type '{EXIT_STRING}' to exit\n")


def text_message(logfile,text):
    message = f"{get_time()} - {text}"
    print(f"{message}")
    filewrite(f"{logfile}",f"{message}")

def client_input(my_username,client_socket,HEADER_LENGTH,logfile,EXIT_STRING):
    while True:
        message = input()
        if message == EXIT_STRING:
            text_message(f"{logfile}",f"You closed the connection")
            sys.exit()
        if message:
            send_message = message.encode('utf-8')
            message_header = f"{len(send_message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + send_message)
            text_message(f"{logfile}",f"{my_username}> {message}")
           
def client_recv(client_socket,HEADER_LENGTH,logfile):
    while True:
        try:
            while True:
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    text_message(f"{logfile}",f"Connection closed by the server")
                    sys.exit()
                username_length = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_length).decode('utf-8')
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                recv_message = client_socket.recv(message_length).decode('utf-8')
                text_message(f"{logfile}",f'{username}> {recv_message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                text_message(f"{logfile}",f"{str(e)}")
                sys.exit()
            continue
        except Exception as e:
            text_message(f"{logfile}",f"{str(e)}")
            sys.exit() 

def server_input(logfile,EXIT_STRING):
    while True:
        message = input()
        if message == EXIT_STRING:
            text_message(f"{logfile}",f"You stopped the server.")
            sys.exit()

def server_recv(sockets_list,server_socket,clients,logfile):
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                user = receive_message(client_socket)
                if user is False:
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user
                text_message(f"{logfile}",f"Accepted new connection from {client_address} - username: {user['data'].decode('utf-8')}")
            else:
                message = receive_message(notified_socket)
                if message is False:
                    text_message(f"{logfile}",f"Closed connection from: {clients[notified_socket]['data'].decode('utf-8')}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                user = clients[notified_socket]
                text_message(f"{logfile}",f"{user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]


