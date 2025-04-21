"""TLS threaded TCP server.
"""

import socket
import ssl
import _thread

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server


def handler(ssl_client_sock, addr):
    """Receive messages and print them to the console."""
    try:
        while True:
            # Receive the data
            data = ssl_client_sock.recv(4096)
            if not data:
                break

            # Decode the data
            message = data.decode('ascii')

            # Print the message
            print(message)
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    finally:
        ssl_client_sock.close()

if __name__ == "__main__":
    # Create our listening socket
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="srv_cert.crt", keyfile="srv_key.key")

    context.load_verify_locations(cafile="cli_cert.crt")
    context.verify_mode = ssl.CERT_REQUIRED

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(20)

    while True:
        # For every connection we get, spin off a new thread to
        # handle the accept socket
        client_sock, addr = sock.accept()
        try:
            ssl_client_sock = context.wrap_socket(client_sock, server_side=True)
            _thread.start_new_thread(handler, (ssl_client_sock, addr))
        except ssl.SSLError as e:
            print(f"Failed TLS handshake: {e}")
            client_sock.close()