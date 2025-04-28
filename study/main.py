# 7 - Application
# 6 - Presentation
# 5 - Session
# 4 - Transport
# 3 - Network
## IP Address (Unique within net) used to route between networks
# 2 - Data link
## MAC Address (managed by switch & bridge) used to route within networks
# 1 - Physical
## eth

import socket


def udp_client(message, server_address):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.sendto(message.encode('utf-8'), server_address)
    response, response_address = udp.recvfrom(4096)
    print(f"{response_address}: {response}")
    udp.close()


def udp_server(server_address):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(server_address)
    data, client_address = udp.recvfrom(4096)
    udp.sendto(data, client_address)
    udp.close()


def tcp_client(message, server_address):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp.bind(('localhost', local_port))
    tcp.connect(server_address)
    tcp.sendall(message.encode('utf-8'))
    response = tcp.recv(4096)
    print(f"{server_address}: {response}")
    tcp.close()


def tcp_server(server_address):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(server_address)
    tcp.listen(1)
    while True:
        conn, addr = tcp.accept()
        data = conn.recv(4096)
        conn.sendall(data)
        conn.close()


def parse_getaddrinfo_output(address):
    #results = socket.getaddrinfo(address[0], address[1])
    results = socket.getaddrinfo(address[0], address[1], 0, 0, 0, socket.AI_CANONNAME)
    index = 0
    for result in results:
        family, socktype, proto, canonname, sockaddr = result
        print(f"Result {index}:")
        print(f"  Family   : {family}")
        print(f"  Socktype : {socktype}")
        print(f"  Protocol : {proto}")
        print(f"  Canonical Name: {canonname}")
        print(f"  Socket Address : {sockaddr}")
        index += 1

if __name__ == "__main__":
    parse_getaddrinfo_output(('google.com', 80))

