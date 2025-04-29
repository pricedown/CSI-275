import socket
import threading
import json

HOST = 'localhost'
PORT_RECV = 5000
PORT_SEND = 5001

clients = {}  # dictionary of usernames to sockets

def recvall(conn, length):
    """Receives all data until length matched or received empty."""

    data = b''
    while len(data) < length:
        more = conn.recv(length - len(data))
        if not more:
            return data
        data += more
    return data

def send_json(sock, data):
    """Sends length-prefixed data as a json object encoded in utf-8."""

    encoded = json.dumps(data).encode('utf-8')
    length = len(encoded).to_bytes(4, 'big')
    sock.sendall(length + encoded)

def serve_chatter(conn):
    """Receives messages from a chat client and relays them to other clients."""

    while True:
        raw_len = recvall(conn, 4)
        if not raw_len:
            break

        msg_len = int.from_bytes(raw_len, 'big')
        msg_data = recvall(conn, msg_len)
        msg = json.loads(msg_data.decode('utf-8'))

        if not msg:
            continue

        msg_type = msg[0]

        if msg_type == "BROADCAST":
            sender, text = msg[1], msg[2]
            print(f"[BROADCAST] {sender}: {text}")
            for user, sock in clients.items():
                send_json(sock, ["BROADCAST", sender, text])

        elif msg_type == "PRIVATE":
            sender, text, recipient = msg[1], msg[2], msg[3]
            print(f"[PRIVATE] {sender} -> {recipient}: {text}")
            if recipient in clients:
                send_json(clients[recipient], ["PRIVATE", sender, text])
            else:
                if sender in clients:
                    send_json(clients[sender], ["SERVER", f"User '{recipient}' not found."])

        elif msg_type == "EXIT":
            sender = msg[1]
            if sender in clients:
                clients[sender].close()
                del clients[sender]
                print(f"{sender} has disconnected.")
            break
    conn.close()

def register_listener(conn):
    """Accepts to chat clients and adds them to the dictionary."""

    raw_len = recvall(conn, 4)
    msg_len = int.from_bytes(raw_len, 'big')
    msg_data = recvall(conn, msg_len)
    msg = json.loads(msg_data.decode('utf-8'))

    if msg[0] == "START":
        username = msg[1]
        clients[username] = conn
        print(f"{username} connected.")

def accept_sending_clients():
    """Continuously spawns threads to serve new sending clients."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT_RECV))
    sock.listen()
    print(f"Listening for sender clients on port {PORT_RECV}")
    while True:
        conn, _ = sock.accept()
        threading.Thread(target=serve_chatter, args=(conn,), daemon=False).start()

def accept_receiving_clients():
    """Continuously spawns threads to register new receiving clients."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT_SEND))
    sock.listen()
    print(f"Listening for receiving clients on port {PORT_SEND}")
    while True:
        conn, _ = sock.accept()
        threading.Thread(target=register_listener, args=(conn,), daemon=False).start()

if __name__ == "__main__":
    threading.Thread(target=accept_sending_clients, daemon=False).start()
    accept_receiving_clients()
