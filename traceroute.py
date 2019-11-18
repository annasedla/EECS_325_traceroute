import sys
import socket
import struct
import select
import time


class Traceroute:

    def __init__(self):
        print('hi')


def main():

    # Payloud setup
    msg = 'measurement for class project.questions to student abc123 @ case.edu or professor mxr136 @ case.edu'
    payload = bytes(msg + 'a' * (1472 -len(msg)), 'ascii')
    send_sock.sendto(payload, (dest_ip, dest_port))
    print('hello')

    # Outbound socket setup
    outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ttl = 0 #TODO
    out.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    # Receiver socket setup
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    #maybe required
    recv.socket.bind('', 0)
    icmp_packet = recv_sock.recv(max_length_of_expected_packet)


    # unpack packages
    port_from_packet = struct.unpack("!H", packet[x:x + 2])[0]

if __name__ == "__main__":
    main()
