# A threaded client for a chat program operating over TCP sockets.

import socket
import threading
import json

HOST = 'localhost'
PORT_RECV = 5001
PORT_SEND = 5000

def recvall(sock, length):
    """Receives all data until length matched or received empty."""

    data = b""
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            return data
        data += more
    return data

def send_json(sock, data):
    """Sends length-prefixed data as a json object encoded in utf-8."""

    encoded = json.dumps(data).encode('utf-8')
    length = len(encoded).to_bytes(4, 'big')
    sock.sendall(length + encoded)

def recv_json(sock):
    """Returns received length-prefixed json object encoded with utf-8."""

    raw_len = recvall(sock, 4)
    if not raw_len:
        return None

    msg_len = int.from_bytes(raw_len, 'big')
    msg_data = recvall(sock, msg_len)
    msg = json.loads(msg_data.decode('utf-8'))
    return msg


def recv_forever(sock):
    """Receives json messages in a loop."""
    while True:
        msg = recv_json(sock)
        if not msg:
            break

        if msg[0] == "BROADCAST":
            print(f"{msg[1]}: {msg[2]}")
        elif msg[0] == "PRIVATE":
            print(f"{msg[1]} (private): {msg[2]}")
        elif msg[0] == "SERVER":
            print(f"[Server]: {msg[1]}")

def send_forever(sock, username):
    """Sends json messages in a loop."""

    while True:
        msg = input()
        if msg == "!exit":
            send_json(sock, ["EXIT", username])
            break
        if msg.startswith("@"):
            # TODO: maybe try and catch invalid format
            parts = msg.split(' ', 1)
            recipient = parts[0][1:]
            message = parts[1]
            send_json(sock, ["PRIVATE", username, message, recipient])
        else:
            send_json(sock, ["BROADCAST", username, msg])

def pick_username():
    """Prompts user to select their name."""

    while True:
        name = input("Enter a username (no spaces): ")
        if ' ' in name:
            print("No spaces allowed.")
        else:
            return name

if __name__ == "__main__":
    username = pick_username()

    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_sock.connect((HOST, PORT_RECV))
    send_json(recv_sock, ["START", username])

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.connect((HOST, PORT_SEND))

    threading.Thread(target=recv_forever, args=(recv_sock,), daemon=False).start()
    send_forever(send_sock, username)
