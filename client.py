from source.helpers import *
from source.settings import *

logfile = "client.log"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

clear_screen()
my_username = input("Enter Username: ")
print(f"Type '{EXIT_STRING}' to exit\n")

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
text_message(f"{logfile}",f"The server on {IP}:{PORT} accepted the username: {my_username}")

threading.Thread(target=client_input, args=[my_username,client_socket,HEADER_LENGTH,logfile,EXIT_STRING], daemon=True).start()
threading.Thread(target=client_recv, args=[my_username,client_socket,HEADER_LENGTH,logfile,EXIT_STRING], daemon=True).start()

while True:
    time.sleep(1)
