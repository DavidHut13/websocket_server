import socket

HEADER = 8
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "quit"
# the address of the server
SERVER = '192.168.1.72'
# Create a tuple with the ip and port #
ADDR = (SERVER, PORT)
#create the client socket SOCK_STREAM means that the data is sent
# in seqential order and not randomly and is what TCP most commonly uses.
# AF_NET  specifies what addresses the socket can communicate with (IPv4)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



def sendData(msg):
    # Accepting message, retrieving size of message, 
    # encoding both, then setting up message with header then sending.
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    send_message = (send_length + message)
    # Must send a Byte Object
    client.send(send_message)
    

    

def recieveData():
        # Recieve the header
    while True:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # Recieve the message after the header.
            msg = client.recv(msg_length).decode(FORMAT)
        print(f"[{SERVER}] {msg}")
        



while True:
    message = input('Type Message...')
    sendData(message)
    
    






