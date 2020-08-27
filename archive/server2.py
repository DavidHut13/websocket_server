import socket
import threading
import pickle
import select

HEADER = 8
PORT = 5050
# Get the machine local IP address. ipv4
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "quit"
CONNECTED = True
#create the client socket SOCK_STREAM means that the data is sent
#  in seqential order and not randomly and is what TCP most commonly uses.
# AF_NET  specifies what addresses the socket can communicate with (IPv4)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
sockets_list = [server]
 # Listen for a client to connect Can specify waiting Queue inside listen method
server.listen()
clients = {}


def start():
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server:
                client_socket, client_address = server.accept()
                user = recieve_message(client_socket)
                if user is False:
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user
                print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
            else:
                message = recieve_message(notified_socket)
                if message is False:
                    print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                user = clients[notified_socket]
                print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER)
        if not len(message_header):
            return False
        message_length = int(message_header.decode(FORMAT))
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False

def storeData():
    pass

print("[STARTING] server is starting...")
start()