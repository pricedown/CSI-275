"""Demonstrate a TCP server for sorting lists."""

import socket

HOST = "localhost"
PORT = 20000

class InvalidSortingRequest(Exception):
    """Invalid sorting request received by server"""
    def __init__(self, msg="Invalid sorting request"):
        self.msg = msg
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
        :return: List of unsorted numbers (floats), and the code of sort type
        """
        result = []

        message_and_code = request.split("|")
        code = 'a'
        if len(message_and_code) > 1:
            code = message_and_code[1]
        if code != 'a' and code != 'd' and code != 's':
            raise InvalidSortingRequest(f"Code is invalid: {code}")

        split_message = message_and_code[0].split(" ")
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

        return result, code


    def construct_sorted_response(self, sorted_list, code):
        """Construct outgoing message string from sorted list.

        :param sorted_list: List
        :return: String of sorted list
        """
        result = "SORTED"
        for num in sorted_list:
            try:
                result += f" {float(num):g}"
            except ValueError:
                result += f" {num}"
        return result


    def sorted_list(self, unsorted_list, code):
        if code == 'a':
            return sorted(unsorted_list)
        elif code == 'd':
            return sorted(unsorted_list, reverse=True)
        elif code == 's':
            string_list = [str(number) for number in unsorted_list]
            return sorted(string_list)
        else:
            raise InvalidSortingRequest(f"Code is invalid: {code}")


    def run_server(self):
        """Accept client connections to sort the lists they send

        :return:
        """

        self.tcp_socket.listen(20) # Backlog of 20 connections

        while True:
            connection, addr = self.tcp_socket.accept()
            while True:
                try:
                    msg = connection.recv(4096).decode('ascii')
                except ConnectionAbortedError:
                    print("Connection aborted")
                    break

                try:
                    unsorted_list, code = self.parse_unsorted_request(msg)
                except InvalidSortingRequest as e:
                    response = "ERROR"
                    print(e.msg)
                else:
                    sorted_list = self.sorted_list(unsorted_list, code)
                    response = self.construct_sorted_response(sorted_list, code)
                connection.send(response.encode('ascii'))


if __name__ == "__main__":
    server = SortServer(HOST, PORT)
    server.run_server()