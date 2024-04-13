import socket
import requests
import threading
import time

log_msg = False
log_new_connection = False
log_connection_ammount = False

message_callbacks = {}

def init(localhost=True):
    global SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE, PORT, server, msg
    print("[INIT] Initializing...")
    PORT = 5050
    if localhost:
        SERVER = socket.gethostbyname(socket.gethostname())
    else:
        SERVER = socket.gethostbyname(requests.get('https://api.ipify.org').text)
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    msg = b''
    print(f"[CONFIG] SERVER: ADDR: {ADDR}, FORMAT: {FORMAT}, DISCONNECT: {DISCONNECT_MESSAGE}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

class Client():
    def __init__(self, server_, port_):
        self.PORT = port_
        self.SERVER = server_
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.ADDR = (self.SERVER, self.PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect(self.ADDR)
    
    def send(self, msg):
        # msg_bytes = msg.encode(self.FORMAT)
        self.client.send(bytes(msg, self.FORMAT))
        return self.client.recv(2048).decode(self.FORMAT)

def add_message_callback(message, callback):
    global message_callbacks
    message_callbacks[message] = callback

def handle_client(conn, addr):
    global SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE, PORT, server, message_callbacks, msg
    if log_new_connection:
        print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_ = conn.recv(2048).decode(FORMAT)
        msg_length = len(msg_)
        if msg_length > 0:
            msg = msg_
            if msg == DISCONNECT_MESSAGE:
                connected = False
            if log_msg:
                print(f"[MSG-{addr}] {msg}")
            
            if msg in message_callbacks:
                message_callbacks[msg](addr, msg, conn)

            conn.send("&MSG-RECIEVED".encode(FORMAT))
    
    conn.close()

def start():
    global SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE, PORT, server, msg
    server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        if log_connection_ammount:
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def start_server():
    global SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE, PORT, server, msg
    print("[STARTING] Server is starting...")
    start()
