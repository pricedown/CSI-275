"""Practicing with UDP Sockets

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
The following code was adapted from code written by Joshua Auerbach (jauerbach@champlain.edu)
"""

import socket
import constants
from constants import INITIAL_TIMEOUT, MAX_TIMEOUT


class TimeOutError(Exception):
    def __init__(self, message):
        super().__init__(message)

class UDPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message_by_character(self, message):
        self.udp_socket.connect((self.host, self.port))
        result = ""
        for character in message:
            wait_time = INITIAL_TIMEOUT
            while True:
                self.udp_socket.settimeout(wait_time)
                self.udp_socket.sendto(character.encode('ascii'), (self.host, self.port))
                try:
                    data, address = self.udp_socket.recvfrom(constants.MAX_BYTES)
                    result += data.decode('ascii')
                except TimeoutError:
                    wait_time *= 2
                    if wait_time >= MAX_TIMEOUT:
                        raise TimeOutError("Server unresponsive")
                else:
                    break
        return result

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
