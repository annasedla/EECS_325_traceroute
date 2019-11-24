import sys
import socket
import struct
import select
import time


def main():

    port_number = 33434
    ttl = 30  #TODO maybe change that

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

    for target in targets:
        ttl_x = 1
        num_hops = 0

        destination_address = socket.gethostbyaddr(target[1])

        # OUTBOUND SOCKET
        outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        outbound_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

        # RECEIVER SOCKET
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        receiver_socket.bind('', 0)  # maybe required

        # PAYLOAD SETUP
        msg = 'Measurement for Networks class project. ' \
              'Questions to student axs1202@case.edu or professor mxr136@case.edu'
        payload = bytes(msg + 'a' * (1472 -len(msg)), 'ascii')
        outbound_socket.sendto(payload, (target[1], port_number))

        # Begin measuring time to send packets
        start = time.time()

        

        # Close both sockets
        outbound_socket.close()
        receiver_socket.close()

        icmp_packet = recv_sock.recv(max_length_of_expected_packet)


        # unpack packages
        port_from_packet = struct.unpack("!H", packet[x:x + 2])[0]

if __name__ == "__main__":
    main()
