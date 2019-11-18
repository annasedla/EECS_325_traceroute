import sys
import socket
import struct
import select
import time


class Traceroute:

    def __init__(self):
        print('hi')


def main():

    port_number = 33434
    ttl = 30 #TODO

    targets_file = open('targets.txt', 'r')

    targets = []
    name = targets_file.readline().rstrip()

    while name != '':
        tuple = []
        tuple.append(name)
        tuple.append(socket.gethostbyname(name))
        targets.append(tuple)
        name = targets_file.readline().rstrip()

    print(targets)

    # PAYLOAD SETUP
    msg = 'measurement for class project.questions to student abc123 @ case.edu or professor mxr136 @ case.edu'
    payload = bytes(msg + 'a' * (1472 -len(msg)), 'ascii')
    send_sock.sendto(payload, (dest_ip, port_number)) #TODO change
    print('hello')

    # OUTBOUND SOCKET
    outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    outbound_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    # RECEIVER SOCKET
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    receiver_socket.bind('', 0)  # maybe required






    icmp_packet = recv_sock.recv(max_length_of_expected_packet)


    # unpack packages
    port_from_packet = struct.unpack("!H", packet[x:x + 2])[0]

if __name__ == "__main__":
    main()
