import tirednet
import socket
import time

client = tirednet.Client(socket.gethostbyname(socket.gethostname()), 5050)
client.connect()
time.sleep(1)

# def other_callback_test(msg):
#     print("a-------" + msg)

# client.add_message_listener("&MSG-RECIEVED", other_callback_test, client)

response = client.send("CALLBACK_TEST#TEST_DATA")
print(response)
client.send(client.DISCONNECT_MESSAGE)
