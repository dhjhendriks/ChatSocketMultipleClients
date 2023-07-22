from source.helpers import *
from source.settings import *

match get_arguments():
    case "s" | "server":
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.bind((IP, PORT))
        my_socket.listen()

        sockets_list = [my_socket]
        clients = {}
                
        welcome(VERSION,EXIT_STRING)
        text_message(f"{logfile}",f"{get_text('Listening_text',L)} {IP}:{PORT}...")

        threading.Thread(target=server_send, args=[sockets_list,my_socket,clients,logfile,HEADER_LENGTH,EXIT_STRING], daemon=False).start()
        threading.Thread(target=server_recv, args=[sockets_list,my_socket,clients,logfile,HEADER_LENGTH], daemon=True).start()

    case "c" | "client":
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((IP, PORT))
        my_socket.setblocking(False)

        welcome(VERSION,EXIT_STRING)
        my_username = input(f"{get_text('Enter Username',L)}: ")
        logfile = f"client_{my_username}.log"

        username = my_username.encode(CODEC)
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode(CODEC)
        my_socket.send(username_header + username)
        text_message(f"{logfile}",f"{get_text('The server on',L)} {IP}:{PORT} {get_text('accepted the username',L)}: {my_username}")

        threading.Thread(target=client_send, args=[my_username,my_socket,HEADER_LENGTH,logfile,EXIT_STRING], daemon=False).start()
        threading.Thread(target=client_recv, args=[my_socket,HEADER_LENGTH,logfile], daemon=True).start()

    case _:
        print(get_text('Argument_text',L))
