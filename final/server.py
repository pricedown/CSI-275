# A threaded server for a chat program operating over TCP sockets.

import socket
import threading
import json

HOST = 'localhost'
PORT_RECV = 5000
PORT_SEND = 5001

clients = {} # dictionary of usernames to sockets
lock = threading.Lock()

def recvall(conn, length):
    data = b''
    while len(data) < length:
        more = conn.recv(length - len(data))
        if not more:
            return data
        data += more
    return data

def send_json(sock, data):
    encoded = json.dumps(data).encode('utf-8')
    length = len(encoded).to_bytes(4, 'big')
    sock.sendall(length + encoded)

def handle_send_client(conn):
    while True:
        pass
        # TODO: load message w/ length prefix

        # TODO: handle message types

    conn.close()

def handle_recv_client(conn):
    raw_len = recvall(conn, 4)
    msg_len = int.from_bytes(raw_len, 'big')
    msg_data = recvall(conn, msg_len)
    msg = json.loads(msg_data.decode('utf-8'))

    if msg[0] == "START":
        username = msg[1]
        with lock:
            clients[username] = conn
            print(f"{username} connected.")

def recv_socket_thread():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT_RECV))
    sock.listen()
    while True:
        conn, _ = sock.accept()
        threading.Thread(target=handle_send_client, args=(conn,), daemon=True).start()

def send_socket_thread():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT_SEND))
    sock.listen()
    while True:
        conn, _ = sock.accept()
        threading.Thread(target=handle_recv_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    threading.Thread(target=recv_socket_thread, daemon=True).start()
    send_socket_thread()
