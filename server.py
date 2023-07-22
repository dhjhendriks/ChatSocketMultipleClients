from source.helpers import *
from source.settings import *

logfile = "server.log"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}

clear_screen()
text_message(f"{logfile}",f"Listening for connections on {IP}:{PORT}...")

while True:
    server(sockets_list,server_socket,clients,logfile)
