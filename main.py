import tirednet

tirednet.init()

tirednet.log_connection_ammount = True
tirednet.log_new_connection = True
tirednet.log_msg = True

def callback_test(addr, msg, conn):
    print(msg)

tirednet.add_message_callback("CALLBACK_TEST", callback_test)

tirednet.start()
