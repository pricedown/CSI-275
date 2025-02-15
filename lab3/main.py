"""Collecting and sorting numeric inputs from a user

Author: Joseph Isaacs
Class: CSI-275-01
Assignment: Lab 3 -- Socket Sort

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""
import socket


def build_list():
    """Prompts the user to build a list of numbers

    Returns:
        The list built by the user
    """
    lst = []
    while True:
        number = input("Append number: ")

        if number.lower() == "done":
            return lst

        try:
            lst.append(float(number))
        except ValueError:
            print("Please only input a number")


def create_sorting_request(lst):
    """Creates the string for a request to the sorting server

    Returns:
        The string that gets sent to the server
    """
    sent_message = "LIST"
    for element in lst:
        sent_message += " " + str(element)
    return sent_message


def exchange_sort_server(request):
    """Uses TCP to send the request to the server and gets a response

    Returns:
        The received string from the server
    """

    # Initialize connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("159.203.166.188", 7778)
    sock.connect(address)

    # Send & Receive list
    sock.send(request.encode("ascii"))
    received_message = sock.recv(4096).decode()

    sock.close()
    return received_message


class SortingServerError(Exception):
    pass


def parse_sorted_list(response):
    """Constructs a list from the sorting server's response message

    Returns:
        The sorted list given by the server
    """

    result = []
    split_message = response.split(" ")
    for word in split_message:
        if word == "ERROR:":
            raise SortingServerError(response)
        if word == "SORTED":
            continue
        result.append(float(word))

    return result


def sort_list(unsorted_list):
    """Sorts a list by using the sorting server

    Returns:
        The sorted list
    """
    sort_request = create_sorting_request(unsorted_list)
    print("Sending to server:", sort_request)

    sorted_response = exchange_sort_server(sort_request)
    print("Received from server:", sorted_response)

    return parse_sorted_list(sorted_response)


if __name__ == '__main__':
    print("Add numbers to a list to sort (type 'done' to quit)")
    built_list = build_list()
    sorted_list = sort_list(built_list)
    print("Sorted numbers:", sorted_list)
