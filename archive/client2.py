import socket
import select
import errno
import sys

HEADER = 8
PORT = 5050
SERVER = '192.168.1.72'
ADDR = (SERVER, PORT)
userName = input("Username: ")
#create the client socket SOCK_STREAM means that the data is sent
# in seqential order and not randomly and is what TCP most commonly uses.
# AF_NET  specifies what addresses the socket can communicate with (IPv4)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.setblocking(False)

username = userName.encode('utf-8')
username_header = f"{len(username):<{HEADER}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f"{userName} > ")
    
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):< {HEADER}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER)
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode("utf-8")
            message_header = client_socket.recv(HEADER)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')
            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General Error', str(e))
        sys.exit()