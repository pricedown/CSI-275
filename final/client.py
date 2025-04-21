# A client for a chat program that operates over TCP sockets.

def recv_all(self, conn, length):
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


class ChatClient:
    def __init__(self, username):
        self.name = username

    def receiving_thread(self):
        length_data = recv_all(connection, 4)
        advertised_length = int.from_bytes(length_data, byteorder='big')

if __name__ == '__main__':
    print("Client started")

