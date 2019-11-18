import sys
import socket
import struct
import select
import time


class Traceroute:

    def __init__(self):
        print('hi')


def main():
    msg = 'measurement for class project.questions to student abc123 @ case.edu or professor mxr136 @ case.edu'
    payload = bytes(msg + 'a' * (1472 -len(msg)), 'ascii')
    send_sock.sendto(payload, (dest_ip, dest_port))
    print('hello')


if __name__ == "__main__":
    main()
