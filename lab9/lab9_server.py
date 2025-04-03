"""Server code for Lab 9.

Author: Duane Dunston (original author)
Author: Jason Reeves (modified code for CSI-275)
Author: Joseph Isaacs (modified code again for CSI-275)
Class: CSI-275-01/02
Assignment: Lab/HW 9 - JSON Client/Server

"""

import socket
import _thread
import zlib
import time
import datetime
import json

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server

def handler(client_socket, addr):
    """Handler function for socket connections.

    Data submitted must be in the form "[num1 num2 ... numN]",
    where num1 through numN must be integers or floating-point numbers.

    """
    while True:
        # Receive the data
        data = client_socket.recv(4096)
        if not data:
            break

        # Decode the data into a list
        data_list = json.loads(zlib.decompress(data).decode('utf-8'))

        # Get time of connection
        now = datetime.datetime.now().timestamp()
        now_readable = time.ctime(now)

        # Print data and time of reception
        print(f"{now_readable}: Got {data} from {addr}")

        # Validate data
        is_error = False

        if len(data_list) == 0:
            print("Data list is empty")
            is_error = True
        else:
            sort_mode = data_list[0]
            if sort_mode not in [ 'a', 'd', 's' ]:
                is_error = True

        data_list = data_list[1:]
        for element in data_list:
            try:
                # This will allow numeric data through
                float(element)
            except ValueError:  # Data is non-numeric
                print("Value Error")
                is_error = True

        return_data = ""
        if not is_error:
            # Sort data
            if sort_mode == 'a':
                data_list.sort()
            elif sort_mode == 'd':
                data_list.sort(reverse=True)
            elif sort_mode == 's':
                data_list.sort(key=str)

            # Return the data to the client
            return_data = json.dumps(data_list)
        else:  # Error
            return_data = json.dumps(["ERROR"])

        # Send our response, whatever it may be
        print(f"Returning {return_data} to the client")
        client_socket.sendall(zlib.compress(return_data.encode('utf-8'),6))


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(20)

    while 1:
        client_sock, address = sock.accept()
        _thread.start_new_thread(handler, (client_sock, address))
