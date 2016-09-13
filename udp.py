from __future__ import print_function
import socket
from contextlib import closing


def read_udp():
    host = "127.0.0.1"
    port = 4001
    bufsize = 4096

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with closing(sock):
        sock.bind((host, port))
        while True:
            print(sock.recv(bufsize))
    return


def send_udp():
    host = "127.0.0.1"
    port = 4000
    send_data = "From Python"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(send_data, (host, port))

if __name__ == "__main__":
    send_udp()
    read_udp()
