import tirednet
import socket
import time

# Define the client class. pass "socket.gethostbyname(socket.gethostname()), 5050" for localhost and port 5050
client = tirednet.Client(socket.gethostbyname(socket.gethostname()), 5050)

# Define the on_connected callback. Is called by the libary when the client has connected.
def on_connected():
    print("Connected!")
client.connectedCallback = on_connected

# Connect to the server and delay for 1 second. delay is for things to settle down. Probally not needed.
client.connect()
time.sleep(1)

# Send a message and get a response.
response = client.send("CALLBACK_TEST#TEST_DATA")
print(response)

# Send disconnect ebent to tell the server to wipe us off the face of the earth.
client.send(client.DISCONNECT_MESSAGE)
