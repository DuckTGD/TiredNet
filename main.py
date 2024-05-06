import tirednet

# Initialize the libary.
tirednet.init()

# Set what we want to log.
tirednet.log_connection_ammount = True
tirednet.log_new_connection = True
tirednet.log_msg = True

# Define a test message callback function.
def callback_test(addr, msg, conn, data):
    print(msg + " - " + data)

    # Return a test response.
    return tirednet.formated("&TEST-RESPONSE", tirednet.FORMAT)

# Add the test message callback.
tirednet.add_message_callback("CALLBACK_TEST", callback_test)

# Start the server
tirednet.start()
