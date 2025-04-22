"""TLS secured threaded TCP server

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
import _thread

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server


def handler(ssl_sock, address):
    """Receive messages and print them to the console."""
    try:
        while True:
            # Receive the data
            data = ssl_sock.recv(4096)
            if not data:
                break

            # Decode the data
            message = data.decode('ascii')

            # Print the message
            print(f"Message from {address}: {message}")
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    finally:
        ssl_sock.close()

if __name__ == "__main__":
    # create a default ssl context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # load the server's certificate and private key
    context.load_cert_chain(certfile="srv_cert.crt", keyfile="srv_key.key")
    # load the client's certificate to be verified by the server
    context.load_verify_locations(cafile="cli_cert.crt")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(20)

    while True:
        # For every connection we get, spin off a new thread to
        # handle the accept socket
        client_sock, addr = sock.accept()
        try:
            # wrap the socket using the ssl context
            ssl_client_sock = context.wrap_socket(client_sock, server_side=True)
            _thread.start_new_thread(handler, (ssl_client_sock, addr))
        except ssl.SSLError as e:
            print(f"Failed TLS handshake: {e}")
            client_sock.close()
