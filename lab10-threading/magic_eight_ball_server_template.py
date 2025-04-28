"""A TCP server that responds to clients with eight-ball answers"""

import threading
import socket
import random

from magic_eight_ball_client import recv_until_delimiter

# Global list of 8-Ball answers
ANSWER_LIST = ["It is certain.",
               "It is decidedly so.",
               "Without a doubt.",
               "Yes - definitely.",
               "You may rely on it.",
               "As I see it, yes.",
               "Most likely.",
               "Outlook good.",
               "Yes.",
               "Signs point to yes.",
               "Reply hazy, ask again.",
               "Ask again later.",
               "Better not tell you now.",
               "Cannot predict now.",
               "Concentrate and ask again.",
               "Don't count on it.",
               "My reply is no.",
               "My sources say no.",
               "Outlook not so good.",
               "Very doubtful."]

# Server host/port information
HOST = "localhost"
SERVER_PORT = 7000

# Maximum amount of data to read in one function call
MAX_BYTES = 1024


class EightBallServer:
    """A TCP server that sends eight-ball answers back to a client."""

    def __init__(self, host, port):
        """Create the initial listening socket and start our threads."""
        self.srv_sock = self.create_server_socket(host, port)

        self.start_threads(self.srv_sock)

    def create_server_socket(self, host, port):
        """Set up the 8-Ball server socket.

        Should go through the create/bind/listen steps and return
        the created listening socket.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()

        return sock

    def accept_8ball_connections(self, listener):
        """Answer questions with Magic 8-Ball responses.

        This function should:
            - accept a connection from the listener socket
              (within our usual infinite while loop)
            - Use recv_until_delimiter() to grab questions from the client
              until it closes the socket ('?' will be the delimiter)
            - Provide a random response drawn from our 8-Ball answer set
              (see answer_list above) for each question
            - Send all the answers as a single string back to the client,
            - and close the socket.
        """

        while True:
            conn, addr = listener.accept()
            print(f"Connection from {addr}")
            answers = []

            buffer = b""
            while True:
                question, buffer = recv_until_delimiter(conn, b"?", buffer)
                if not question:
                    break  # Client disconnected
                answer = random.choice(ANSWER_LIST)
                answers.append(answer)

            if answers:
                response = "\n".join(answers) + "\n"
                conn.sendall(response.encode("utf-8"))
            conn.close()

    def accept_connections_forever(self, sock):
        """Converse with a client over `sock` until they are done talking."""
        try:
            self.accept_8ball_connections(sock)
        except EOFError:
            print('Client socket has closed')
        except ConnectionResetError:
            print('Connection reset')
        finally:
            sock.close()

    def start_threads(self, listener, workers=4):
        """Kick off the threads needed to serve 8-ball requests.

        Each thread should call accept_connections_forever() as its
        starting function.
        """

        for _ in range(workers):
            thread = threading.Thread(target=self.accept_connections_forever, args=(listener,))
            thread.start()

if __name__ == "__main__":
    eight_ball = EightBallServer(HOST, SERVER_PORT)
