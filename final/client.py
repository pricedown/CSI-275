# A threaded client for a chat program operating over TCP sockets.

import socket
import threading
import json

HOST = 'localhost'
PORT_RECV = 5001
PORT_SEND = 5000

def recvall(sock, length):
    data = b""
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            return data
        data += more
    return data

def send_json(sock, data):
    encoded = json.dumps(data).encode('utf-8')
    length = len(encoded).to_bytes(4, 'big')
    sock.sendall(length + encoded)

def recv_forever(sock):
    while True:
        raw_len = recvall(sock, 4)
        if not raw_len:
            break
        msg_len = int.from_bytes(raw_len, 'big')
        msg_data = recvall(sock, msg_len)
        msg = json.loads(msg_data.decode('utf-8'))

        # TODO: receive messages
        if msg[0] == "BROADCAST":
            print(f"{msg[1]}: {msg[2]}")

def send_forever(sock, username):
    while True:
        msg = input()
        if msg == "!exit":
            send_json(sock, ["EXIT", username])
            break
        # TODO: send messages

def pick_username():
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

    threading.Thread(target=recv_forever, args=(recv_sock,), daemon=True).start()
    send_forever(send_sock, username)
