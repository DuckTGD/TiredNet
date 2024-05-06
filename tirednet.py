import socket
import requests
import threading
import time

log_msg = False
log_new_connection = False
log_connection_ammount = False

message_callbacks = {}
client_message_listeners = {}

def formated(text, format):
    return text.encode(format)

# 100% not copied from the interwebz
CONSOLECOLOR_RESET = "\u001b[0m"
CONSOLECOLOR_BLACK = "\u001b[30m"
CONSOLECOLOR_RED = "\u001b[31m"
CONSOLECOLOR_GREEN = "\u001b[32m"
CONSOLECOLOR_YELLOW = "\u001b[33m"
CONSOLECOLOR_BLUE = "\u001b[34m"
CONSOLECOLOR_MAGENTA = "\u001b[35m"
CONSOLECOLOR_CYAN = "\u001b[36m"
CONSOLECOLOR_WHITE = "\u001b[37m"
# Testing to see if my colors do not look like complete dogshit
# print(f"{CONSOLECOLOR_YELLOW}[MSG-127.0.0.1] {CONSOLECOLOR_GREEN}message {CONSOLECOLOR_RESET}- {CONSOLECOLOR_CYAN}I LOVE FEMBOYS{CONSOLECOLOR_RESET}")
# print(f"{CONSOLECOLOR_YELLOW}[NEW CONNECTION] {CONSOLECOLOR_CYAN}127.0.0.1 {CONSOLECOLOR_GREEN}connected.")
# print(f"{CONSOLECOLOR_YELLOW}[INIT] {CONSOLECOLOR_GREEN}Initializing...{CONSOLECOLOR_RESET}")
# print(f"{CONSOLECOLOR_YELLOW}[SERVER CONFIG] {CONSOLECOLOR_GREEN}ADDR: {CONSOLECOLOR_CYAN}127.0.0.1{CONSOLECOLOR_RESET}, {CONSOLECOLOR_GREEN}FORMAT: {CONSOLECOLOR_CYAN}trashencoding{CONSOLECOLOR_RESET}, {CONSOLECOLOR_GREEN}DISCONNECT: {CONSOLECOLOR_CYAN}!disconnect{CONSOLECOLOR_RESET}")
# print(f"{CONSOLECOLOR_YELLOW}[STARTING] {CONSOLECOLOR_GREEN}Server is starting...{CONSOLECOLOR_RESET}")
# print(f"{CONSOLECOLOR_YELLOW}[ACTIVE CONNECTIONS] {CONSOLECOLOR_GREEN}69420{CONSOLECOLOR_RESET}")

def init(localhost=True, format="utf-8", disconnect="!DISCONNECT"):
    global SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE, PORT, server, msg
    print(f"{CONSOLECOLOR_YELLOW}[INIT] {CONSOLECOLOR_GREEN}Initializing...{CONSOLECOLOR_RESET}")
    PORT = 5050
    try:
        if localhost:
            SERVER = socket.gethostbyname(socket.gethostname())
        else:
            SERVER = socket.gethostbyname(requests.get('https://api.ipify.org').text)
    except Exception as e:
        print(f"{CONSOLECOLOR_RED}[ERROR IN SERVER INIT FUNCTION: FAILED TO SET SERVER] {e}{CONSOLECOLOR_RESET}")
    ADDR = (SERVER, PORT)
    FORMAT = format
    DISCONNECT_MESSAGE = disconnect
    msg = b''
    print(f"{CONSOLECOLOR_YELLOW}[SERVER CONFIG] {CONSOLECOLOR_GREEN}ADDR: {CONSOLECOLOR_CYAN}{ADDR}{CONSOLECOLOR_RESET}, {CONSOLECOLOR_GREEN}FORMAT: {CONSOLECOLOR_CYAN}{FORMAT}{CONSOLECOLOR_RESET}, {CONSOLECOLOR_GREEN}DISCONNECT: {CONSOLECOLOR_CYAN}{DISCONNECT_MESSAGE}{CONSOLECOLOR_RESET}")

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
    except Exception as e:
        print(f"{CONSOLECOLOR_RED}[ERROR IN SERVER INIT FUNCTION: FAILED TO CREATE AND BIND SERVER] {e}{CONSOLECOLOR_RESET}")

def Empty():
    try:
        pass
    except Exception as e:
        print(f"ok now how the fuck did a error happen in a empty function?!?! {e}")

class Client():
    def __init__(self, server, port):
        self.PORT = port
        self.SERVER = server
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.ADDR = (self.SERVER, self.PORT)
        self.connectedCallback = Empty

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print(f"{CONSOLECOLOR_RED}[ERROR IN CLIENT INIT FUNCTION: FAILED TO CREATE AND BIND SERVER] {e}{CONSOLECOLOR_RESET}")

    def connect(self):
        try:
            self.client.connect(self.ADDR)
            self.connectedCallback()
        except Exception as e:
            print(f"{CONSOLECOLOR_RED}[ERROR IN CLIENT CONNECT FUNCTION: FAILED TO CONNECT] {e}{CONSOLECOLOR_RESET}")
    
    def send(self, msg):
        try:
            self.client.send(bytes(msg, self.FORMAT))
            return self.client.recv(2048).decode(self.FORMAT)
        except Exception as e:
            print(f"{CONSOLECOLOR_RED}[ERROR IN CLIENT SEND FUNCTION: FAILED TO SEND] {e}{CONSOLECOLOR_RESET}")

def add_message_callback(message, callback):
    global message_callbacks
    message_callbacks[message] = callback

def handle_client(conn, addr):
    global SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE, PORT, server, message_callbacks, msg
    if log_new_connection:
        print(f"{CONSOLECOLOR_YELLOW}[NEW CONNECTION] {CONSOLECOLOR_CYAN}{addr} connected.{CONSOLECOLOR_RESET}")

    connected = True
    while connected:
        try:
            msg_ = conn.recv(2048).decode(FORMAT)
        except Exception as e:
            print(f"{CONSOLECOLOR_RED}[ERROR IN HANDLE CLIENT FUNCTION: FAILED TO RECIEVE DATA] {e}{CONSOLECOLOR_RESET}")
        msg_length = len(msg_)
        if msg_length > 0:
            msg = msg_
            try:
                msg_data = msg.split("#", 1)[1]
            except IndexError:
                msg_data = ""
            if msg == DISCONNECT_MESSAGE:
                connected = False
            if log_msg:
                print(f"{CONSOLECOLOR_YELLOW}[MSG-{addr}] {CONSOLECOLOR_GREEN}{msg.split('#')[0]} {CONSOLECOLOR_RESET}- {CONSOLECOLOR_CYAN}{msg_data}{CONSOLECOLOR_RESET}")
            
            if msg in message_callbacks:
                try:
                    server_wants_response = message_callbacks[msg](addr, msg, conn, msg_data)
                except Exception as e:
                    print(f"{CONSOLECOLOR_RED}[ERROR IN HANDLE CLIENT FUNCTION: FAILED TO HANDLE CLIENT MESSAGE CALLBACK] {e}{CONSOLECOLOR_RESET}")
                try:
                    if server_wants_response:
                        conn.send(server_wants_response)
                    else:
                        conn.send(formated("OK", FORMAT))
                except Exception as e:
                    print(f"{CONSOLECOLOR_RED}[ERROR IN HANDLE CLIENT FUNCTION: FAILED TO SEND RESPONSE DATA] {e}{CONSOLECOLOR_RESET}")
    
    conn.close()

def start():
    global SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE, PORT, server, msg
    try:
        server.listen()
    except Exception as e:
        print(f"{CONSOLECOLOR_RED}[ERROR IN START FUNCTION: FAILED TO START SERVER WITH LISTEN] {e}{CONSOLECOLOR_RESET}")
    print(f"{CONSOLECOLOR_YELLOW}[LISTENING] {CONSOLECOLOR_GREEN}Server is listening on {CONSOLECOLOR_CYAN}{ADDR}{CONSOLECOLOR_RESET}")
    while True:
        try:
            conn, addr = server.accept()
        except Exception as e:
            print(f"{CONSOLECOLOR_RED}[ERROR IN SERVER LOOP: FAILED TO ACCEPT CONNECTION] {e}{CONSOLECOLOR_RESET}")
        try:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except Exception as e:
            print(f"{CONSOLECOLOR_RED}[ERROR IN SERVER LOOP: FAILED TO START THREAD FOR NEW CONNECTION] {e}{CONSOLECOLOR_RESET}")
        if log_connection_ammount:
            print(f"{CONSOLECOLOR_YELLOW}[ACTIVE CONNECTIONS] {CONSOLECOLOR_GREEN}{threading.active_count() - 1}{CONSOLECOLOR_RESET}")

def start_server():
    global SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE, PORT, server, msg
    print(f"{CONSOLECOLOR_YELLOW}[STARTING] {CONSOLECOLOR_GREEN}Server is starting...{CONSOLECOLOR_RESET}")
    start()
