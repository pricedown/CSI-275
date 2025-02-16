"""Demonstrate a TCP server for sorting lists."""

import socket

HOST = "localhost"
PORT = 20000

class InvalidSortingRequest(Exception):
    """Invalid sorting request received by server"""
    def __init__(self, msg="Invalid sorting request"):
        super().__init__(msg)

class SortServer:
    """A tcp server for sorting lists."""


    def __init__(self, host, port):
        """Create a TCP server socket for the server to use.

        :param host: The host for the server socket to bind to
        :param port: The port for the server socket to bind to
        """

        self.addr = (host, port)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind(self.addr)


    def parse_unsorted_request(self, request):
        """Parse incoming unsorted message into a list.

        :param request: String message received from server
        :return: List of unsorted numbers (floats)
        """
        result = []
        split_message = request.split(" ")
        if len(split_message) < 2:
            raise InvalidSortingRequest(f"'{request}' is not a list of items separated by spaces")
        if split_message[0] != "LIST":
            raise InvalidSortingRequest(f"'{request}' does not start with LIST")

        for str_num in split_message[1::]:
            try:
                num = float(str_num)
            except ValueError:
                raise InvalidSortingRequest(f"Could not parse {str_num} into a number")
            else:
                result.append(num)

        return result

    def construct_sorted_response(self, sorted_list):
        """Construct outgoing message string from sorted list.

        :param sorted_list: List
        :return: String of sorted list
        """
        result = "SORTED"
        for num in sorted_list:
            result += f" {num:g}"
        return result



    def run_server(self):
        """Accept client connections to sort the lists they send

        :return:
        """

        self.tcp_socket.listen(20) # Backlog of 20 connections

        while True:
            connection, addr = self.tcp_socket.accept()
            msg = connection.recv(4096).decode('ascii')

            try:
                unsorted_list = self.parse_unsorted_request(msg)
            except InvalidSortingRequest:
                response = "ERROR"
            else:
                sorted_list = sorted(unsorted_list)
                response = self.construct_sorted_response(sorted_list)

            connection.sendall(response.encode('ascii'))




if __name__ == "__main__":
    server = SortServer(HOST, PORT)
    server.run_server()