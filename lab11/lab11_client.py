"""Don't forget your docstrings!
"""
import socket
import ssl

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server


def send_messages():
    """Collect text from the user and send it to our server."""
    # Create a variable for input
    user_input = ""

    context = ssl.create_default_context()

    context.load_cert_chain(certfile='cli_cert.crt', keyfile="cli_key.key")
    context.load_verify_locations('srv_cert.crt')
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED

    # Create a socket
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = context.wrap_socket(raw_sock, server_hostname=HOST)
    sock.connect((HOST, PORT))

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a message, or 'done' to exit.")

        # Encode the message
        encoded_message = user_input.encode('ascii')

        # Send the message
        sock.sendall(encoded_message)

    # Close the socket if the while loop exits
    sock.close()


def main():
    """Call send_messages to start our message loop."""
    send_messages()


if __name__ == "__main__":
    main()

