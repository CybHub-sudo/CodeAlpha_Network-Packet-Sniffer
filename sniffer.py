import socket
import struct

def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('!6s6sH', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]

def get_mac_addr(bytes_addr):
    return ':'.join(format(b, '02x') for b in bytes_addr)

def main():
    # Create a raw socket and bind it to the public interface
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    print("Starting packet capture... Press Ctrl+C to stop.")
    try:
        while True:
            raw_data, addr = conn.recvfrom(65535)
            dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
            print('\nEthernet Frame:')
            print(f'Destination: {dest_mac}, Source: {src_mac}, Protocol: {eth_proto}')
    except KeyboardInterrupt:
        print("\nPacket capture stopped.")

if __name__ == '__main__':
    main()

