import socket
import struct
import select
import time


def main():

    port_number = 33434
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

        # destination_address = socket.gethostbyaddr(target[1])

        # OUTBOUND SOCKET
        outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        outbound_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, TTL)  # as the instructions suggested

        # RECEIVER SOCKET
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        # receiver_socket.bind('', 0)  # maybe required

        # PAYLOAD SETUP
        msg = 'Measurement for Networks class project. ' \
              'Questions to student axs1202@case.edu or professor mxr136@case.edu'
        payload = bytes(msg + 'a' * (1472 - len(msg)), 'ascii')
        outbound_socket.sendto(payload, (target[1], port_number))

        # Begin measuring time to send packets
        started_select = time.time()

        # With the policy of the project the following code is adapted from https://gist.github.com/pklaus/856268
        while True:
            rec_packet = []
            addr = []

            # Decided to use select on the socket so we are not probing forever
            ready = select.select([receiver_socket], [], [], 3)

            rtt = time.time() - started_select
            if ready[0] == []:  # Timeout
                break
            try:
                rec_packet, addr = receiver_socket.recvfrom(4096)

                print('rec_packet: ', rec_packet)
                print('addr: ', addr)
                # icmp_packet = receiver_socket.recv(max_length_of_expected_packet)

                icmp_header = rec_packet[20:28]
                #TODO first 20 IP, 8 byters imcp, 20 bytes next our own IP coming back, 8 bytes of UDP header bouncing back
                type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)
                # port_from_packet = struct.unpack("!H", packet[x:x + 2])[0]

                print('address: ', addr)
                print('p id: ', p_id)
                print('targe: ', target[1])

                addr = addr[0]
            except socket.error:
                pass

            num_hops = TTL - rec_packet[36]

            # METHOD 1 maybe?
            if addr == target[1]:
                break

            # METHODS 3

            if ttl_x > TTL:
                break

            # if p_id == packet_id:
            #     return time_received - time_sent
            # time_left -= time_received - time_sent
            # if time_left <= 0:
            #     break

        # Close both sockets
        outbound_socket.close()
        receiver_socket.close()

        try:
            addr
        except NameError:
            print('Error on site: ', target[0])

        else:
            # OUTPUT
            print('Traceroute finished for site: ', target[0])
            print('Total number of router hops: ', num_hops)  # Number of router hops
            print('RTT between us and site: ', rtt)  # RTT between us and the destination
            # TODO Number of probe response matching criteria
            print('Packet', len(rec_packet) - 28)
            print()


if __name__ == "__main__":
    main()
