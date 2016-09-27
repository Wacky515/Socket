# !/usr/bin/python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        UDP/IP
# Purpose:
#
# Author:      Kilo11
#
# Created:     13/09/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10012
# -------------------------------------------------------------------------------

# モジュールインポート
# from __future__ import print_function
import time
import socket
from contextlib import closing


class UdpCommun:
    """ UDP/IP通信 """
    # def __init__(self):
    #     self.host = socket.gethostname()
    #     self.port = 4000
    #     self.addr = (socket.gethostbyname(self.host), self.port)

    def read_udp(self, host="0.0.0.0", port=4000, bufsize=4096, onetime=False):
        """ 受信 """
        read_data = ""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with closing(sock):
            sock.bind((host, port))
            sock.connect(("172.21.38.192", 60001))
            while True:
                read_data = sock.recv(bufsize).strip()
                print("Get data from UDP/IP: " + str(read_data))
                if onetime is True and read_data != "":
                    break
        return read_data

    def send_udp(self, host="127.0.0.1", port=4001,
                 onetime=False, send_data="From Python"):
        """ 送信 """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.sendto(send_data, (host, port))  with closing(sock):
        with closing(sock):
            sock.connect(("172.21.38.192", 60001))
            while True:
                sock.sendto(send_data, (host, port))
                print("Send data from UDP/IP: " + str(send_data))
                if onetime is True:
                    break
                time.sleep(1.0)
        return

    def multi_cast_send_udp(self,
                            host="127.0.0.1",
                            multicast_group="172.21.38.192",
                            port=4001,
                            onetime=False, send_data="From Python"):
        """ マルチキャスト 送信 """
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.setsockopt(socket.IPPROTO_IP,
                            socket.IP_MULTICAST_IF,
                            socket.inet_aton(host))
            while True:
                sock.sendto(send_data, (multicast_group, port))
                print("Send data from UDP/IP: " + str(send_data))
                if onetime is True:
                    break
                time.sleep(1.0)
        return


def main():
    host = socket.gethostname()
    print("Host name: " + str(host))
    print("Host addr: " + str(socket.gethostbyname(host)))
    print("")

    # udc = UdpCommun()
    # udc.read_udp(port=9000, onetime=True)
    # udc.read_udp(port=9000, onetime=False)
    # udc.read_udp(port=9000, onetime=False)
    # udc.read_udp(host="192.168.1.5", port=9000, onetime=True)

    # udc.send_udp(host="192.168.1.5", port=60001, onetime=True, send_data="OK")
    # udc.send_udp(host="172.21.38.192",
    # udc.send_udp(host="192.168.1.5",
    #              port=60001, onetime=True, send_data="Send OK")
    # udc.multi_cast_send_udp(host="172.21.38.192",
    # udc.multi_cast_send_udp(host="192.168.1.11",
    #                         port=60001, onetime=False,
    #                         send_data="Multicasting OK")

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.sendto("OKb", ("127.0.0.1", 60001))

    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # DESTINATION_ADDR = "172.21.38.192"
    # SOURCE_PORT, DESTINATION_PORT = 31415, 80
    # sock.bind(("172.21.38.192", SOURCE_PORT))
    # sock.connect((DESTINATION_ADDR, DESTINATION_PORT))

    UDP_IP = "172.21.38.192"
    # UDP_IP = "192.168.1.5"
    UDP_PORT = 60001
    MESSAGE = "OK test"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.connect(("192.168.1.11", 9000))
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    main()
