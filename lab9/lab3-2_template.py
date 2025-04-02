"""A client to the JSON sorting server
"""
import json
import socket


def build_list():
    """Collect input from the user and return it as a list.

    Only numeric input will be included; strings are rejected.
    """
    #Create a list to store our numbers
    unsorted_list = []

    # Create a variable for input
    user_input = ""

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a number, or 'done' to stop.")

        # Validate our input, and add it to out list
        # if it's a number
        try:
            # Were we given an integer?
            unsorted_list.append(int(user_input))
        except ValueError:
            try:
                # Were we given a floating-point number?
                unsorted_list.append(float(user_input))
            except ValueError:
                # Non-numeric input - if it's not "done",
                # reject it and move on
                if (user_input != "done"):
                    print ("ERROR: Non-numeric input provided.")
                continue

    # Once we get here, we're done - return the list
    return unsorted_list

def sort_list(unsorted_list):
    """Sort list and send it back to the server

    :param unsorted_list: The unsorted list
    :return:
    """

    # Transform list into JSON object
    json_list = json.dumps(unsorted_list)

    # Create a socket and connect to port 7778 on localhost
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('localhost', 7778)
    sock.connect(addr)
    sock.sendall(json_list.encode('utf-8'))
    received = sock.recv(4096)

    # Reconstructed list from JSON
    received_list = json.loads(received.decode('utf-8'))
    print(received_list)
    sock.close()

def main():
    """Call the build_list and sort_list functions, and print the result."""
    number_list = build_list()
    sort_list(number_list)

if __name__ == "__main__":
    main()

