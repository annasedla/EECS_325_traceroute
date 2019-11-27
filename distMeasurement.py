import socket
import struct
import select
import time


def main():

    port_number = 33434
    max_packet_lenght = 1528
    TTL = 60

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
        probe_response_matching = []

        # OUTBOUND SOCKET
        outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        outbound_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, TTL)  # as the instructions suggested

        # RECEIVER SOCKET
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        # PAYLOAD SETUP
        msg = 'Measurement for Networks class project. ' \
              'Questions to student axs1202@case.edu or professor mxr136@case.edu'
        payload = bytes(msg + 'a' * (1472 - len(msg)), 'ascii')
        outbound_socket.sendto(payload, (target[1], port_number))

        # Begin measuring time to send packets
        started_select = time.time()

        # With the policy of the project the following
        # portions of the code are adapted from https://gist.github.com/pklaus/856268
        while True:
            # rec_packet = []
            # addr = []

            srcIp = 0
            port_from_packet = 0
            imcp_packet = 0

            # Decided to use select on the socket so we are not probing forever
            ready = select.select([receiver_socket], [], [], 3)  # inputs, outputs, inputs, timeout

            rtt = time.time() - started_select
            if ready[0] == []:  # Timeout set to 3 seconds, TODO maybe try few more times
                break
            try:
                imcp_packet = receiver_socket.recv(max_packet_lenght)
                srcIp = str(imcp_packet[40]) + "." + str(imcp_packet[41]) + "." +\
                        str(imcp_packet[42]) + "." + str(imcp_packet[43])

                port_from_packet = struct.unpack("!H", imcp_packet[50:52])[0]  # as per instructions

                print('ip, try two: ', srcIp)
                print('port, try two', port_from_packet)

            except socket.error:
                pass

            num_hops = TTL - imcp_packet[36]

            # METHOD 1
            if srcIp == target[1]:
                probe_response_matching.append('IP addresses match')

            # METHODS 3
            if port_from_packet == port_number:
                probe_response_matching.append('Port numbers match')

            if len(probe_response_matching) > 0:
                break

                # rec_packet, addr = receiver_socket.recvfrom(4096)  # Receive from this port
                #
                # icmp_header = rec_packet[20:28]
                # ip = rec_packet[0:20]
                #
                # print('NEW MEASUREMENT:')
                # print('size of received packet: ', len(rec_packet))
                # print('maybe the ip: ', ip)
                #
                # #first 20 IP, 8 byters imcp, 20 bytes next our own IP coming back, 8 bytes of UDP header bouncing back
                # type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)
                #
                # print('address: ', addr)
                # print('p id: ', p_id)
                # print('type: ', type)
                # print('code: ', code)
                # print('sequence: ', sequence)
                # print('checksum: ', checksum)
                #
                # addr = addr[0]

            #
            # if addr == target[1]:
            #     break
            # # exit if ttl of the outbound socket exceeds the TTL constant TODO i believe this is wrong
            # if ttl_x > TTL:
            #     break

        # Close both sockets
        outbound_socket.close()
        receiver_socket.close()

        # OUTPUT
        print('Traceroute finished for site: ', target[0])
        print('Total number of router hops: ', num_hops)  # Number of router hops
        print('RTT between us and site: ', rtt)  # RTT between us and the destination
        print('Number of probe response mathcing criteria: ,', probe_response_matching)
        print('Packet size: ', len(imcp_packet) - 28)  # need to subtract the header
        print()


if __name__ == "__main__":
    main()
