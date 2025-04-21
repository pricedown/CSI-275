import socket, ssl


def test_no_ssl():
    # Create and send data as usual
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.bind(("localhost", 10000))
    raw_sock.listen(20)

    while True:
        cli_sock, addr = raw_sock.accept()
        message = cli_sock.recv(4096).decode('ascii')
        print(message)
        cli_sock.close()

def test_ssl_server():
    # Create our SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("srv_cert.crt", "srv_key.key")
    context.load_verify_locations("cli_cert.crt")

    # Create and wrap our socket
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.bind(("localhost", 10000))
    raw_sock.listen(20)

    # Receive our data
    while True:
        cli_sock, addr = raw_sock.accept()
        ssl_sock = context.wrap_socket(cli_sock, server_side=True)
        message = ssl_sock.recv(4096).decode('ascii')
        print(message)
        ssl_sock.close()


if __name__ == "__main__":
    test_no_ssl()
    # test_ssl_server()