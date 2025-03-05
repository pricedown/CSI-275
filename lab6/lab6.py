"""TCP server that parses a simple text protocol that uses framing technique #5 from class """

import socket

HOST = "localhost"
PORT = 45000

class LengthServer:
    """Create a server that return the length of received strings."""

    def __init__(self, host, port):
        """Creates and binds the TCP socket to use"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))

    def recvall(self, conn, length):
        """Receives exactly the amount of data stated in the length field

        :param conn: connection to receive from
        :param length:  length of data to collect
        :return: the data collected
        """
        data = b""
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                return data
            data += packet
        return data

    def calc_length(self):
        """Receives a length-prefixed message and responds verifying its length"""
        self.sock.listen()

        while True:
            connection, _ = self.sock.accept()

            length_data = self.recvall(connection, 4)
            advertised_length = int.from_bytes(length_data, byteorder='big')

            print(f"Collecting advertised {advertised_length}-byte message")
            message_data = self.recvall(connection, advertised_length)
            message_length = len(message_data)
            if message_length >= advertised_length:
                response = f"I received {message_length} bytes."
            else:
                response = "Length Error"

            print(response)
            response_data = response.encode('ascii')
            response_length = len(response_data).to_bytes(4, byteorder='big')
            connection.sendall(response_length+response_data)
            connection.close()

if __name__ == "__main__":
    server = LengthServer(HOST, PORT)
    server.calc_length()
