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
    lst = []
    while True:
        number = input("Append number: ")
        
        if number.lower() == "done":
            return lst
        
        try: 
            lst.append(float(number))
        except ValueError:
            print("Please only input a number")

def sort_list(unsortedList):
    msg = "LIST "
    for n in unsortedList:
        msg += str(n) + " "
    data = msg.encode("ascii")

    print(f"Input: {msg}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("159.203.166.188", 7778)
    sock.connect(address)
    sock.send(data)

    data = sock.recv(1024)
    print("Received from server:", data.decode())

    sock.close()
            
if __name__ == '__main__':
    print("Add numbers to a list to sort (type 'done' to quit)")
    list = build_list()
    sort_list(list)
    print(f"Sorted numbers: {list}")
