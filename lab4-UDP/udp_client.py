"""Practicing with UDP Sockets by sending character strings back and forth.

Author: Joseph Isaacs
Class: CSI-275-01
Assignment: Lab 4 -- UDP Sockets

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)

Champlain College CSI-235, Spring 2019
The following code was adapted from Joshua Auerbach (jauerbach@champlain.edu)
"""
import random
import socket
import constants
from constants import INITIAL_TIMEOUT, MAX_TIMEOUT


class TimeOutError(Exception):
    """Exception raised when too many timeouts occur with the server."""


class UDPClient:
    """A UDP client for sending and receiving characters one at a time."""

    def __init__(self, host, port, use_request_ids=False):
        """Initialize the client.

        :param host: IP address of the host
        :param port: port to connect to
        :param use_request_ids: whether or not to use request ids
        """
        self.host = host
        self.port = port
        self.use_request_ids = use_request_ids
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message_by_character(self, message):
        """Send a message to the server character by character.

        :param message: The message to be sent
        :return: The server's response echo of the characters
        """
        self.udp_socket.connect((self.host, self.port))
        result = ""
        for character in message:
            wait_time = INITIAL_TIMEOUT

            # Send character
            while True:
                self.udp_socket.settimeout(wait_time)

                # Build encoded message
                request = ""
                request_id = ""
                if self.use_request_ids:
                    request_id = str(random.randint(0, constants.MAX_ID))
                    request += request_id+"|"
                request += character

                # Send, receive and catch
                msg = request.encode('ascii')
                self.udp_socket.sendto(msg, (self.host, self.port))
                try:
                    data, __ = self.udp_socket.recvfrom(constants.MAX_BYTES)
                    response = data.decode('ascii')
                except TimeoutError as exc:
                    wait_time *= 2
                    if wait_time >= MAX_TIMEOUT:
                        raise TimeOutError("Server unresponsive") from exc
                else:
                    if self.use_request_ids:
                        split_response = response.split("|")
                        if split_response[0] == request_id:
                            result += split_response[1]
                            break
                    else:
                        result += response
                        break
        return result

    def close_socket(self):
        """Close socket made when creating."""
        self.udp_socket.close()


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    client = UDPClient(constants.HOST, constants.ECHO_PORT)
    print(client.send_message_by_character("hello world"))

    client = UDPClient(constants.HOST, constants.REQUEST_ID_PORT, True)
    print(client.send_message_by_character("hello world"))


if __name__ == "__main__":
    main()
