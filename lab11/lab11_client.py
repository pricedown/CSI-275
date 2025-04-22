"""TLS secured server client

Author: Joseph Isaacs
Class: CSI-275-01
Assignment: Lab 11 -- Encrypting connections with TLS
Due Date: Apr 26 2025 at 11:59pm

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
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

    # load the client's certificate and private key
    context.load_cert_chain(certfile='cli_cert.crt', keyfile="cli_key.key")
    # load the server's certificate so that it can be verified by the client
    context.load_verify_locations('srv_cert.crt')

    # Create a socket
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # wrap the socket with our default context
    sock = context.wrap_socket(raw_sock, server_hostname='localhost')
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
