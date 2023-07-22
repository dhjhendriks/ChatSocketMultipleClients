from source.helpers import *
from source.settings import *

parser = argparse.ArgumentParser()
parser.add_argument("type")
args = parser.parse_args()
arg1 = args.type.lower()

match arg1:
    case "s" | "server":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP, PORT))
        server_socket.listen()

        sockets_list = [server_socket]
        clients = {}
        logfile = "server.log"
        
        welcome(VERSION,EXIT_STRING)
        text_message(f"{logfile}",f"Listening for connections on {IP}:{PORT}...")

        threading.Thread(target=server_send, args=[logfile,EXIT_STRING], daemon=False).start()
        threading.Thread(target=server_recv, args=[sockets_list,server_socket,clients,logfile,HEADER_LENGTH], daemon=True).start()

    case "c" | "client":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        client_socket.setblocking(False)

        welcome(VERSION,EXIT_STRING)
        my_username = input("Enter Username: ")
        logfile = f"client_{my_username}.log"

        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)
        text_message(f"{logfile}",f"The server on {IP}:{PORT} accepted the username: {my_username}")

        threading.Thread(target=client_send, args=[my_username,client_socket,HEADER_LENGTH,logfile,EXIT_STRING], daemon=False).start()
        threading.Thread(target=client_recv, args=[client_socket,HEADER_LENGTH,logfile], daemon=True).start()

    case _:
        print("Argument 'type' has to be (s)erver or (c)lient")