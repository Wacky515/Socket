# !/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        udp.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     13/09/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10011
# -----------------------------------------------------------------------------

# モジュールインポート
# from __future__ import print_function
import time
import socket
import tcpclient as tcp
from contextlib import closing


class UdpCommun(tcp.TcpCliCom):
    """ UDP/IP通信 """
    def __init__(self):
        tcp.TcpCliCom.__init__(self)

        self.local_port = self.client_port
        self.remote_port = self.server_port

    def read_udp(self, host=None, port=None, bufsize=4096,
                 onetime=False):  # {{{
        """ 受信 """
        if host is None:
            host = "0.0.0.0"
        if port is None:
            port = self.local_port
        read_data = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            with closing(sock):
                sock.bind((host, port))

                while True:
                    read_data = sock.recv(bufsize).strip()
                    print("Get data from UDP/IP: " + str(read_data))
                    print("")

                    if onetime is True and read_data is not None:
                        break
                return read_data

        except socket.timeout:
            print("Time out")
            print("")
# }}}

    def send_udp(self, host=None, port=None,
                 onetime=True, send_data="From Python"):  # {{{
        """ 送信 """
        if host is None:
            host = self.local_host
        if port is None:
            port = self.remote_port

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            with closing(sock):
                while True:
                    sock.sendto(send_data, (host, port))
                    print("Send data from UDP/IP: " + str(send_data))
                    print("")

                    if onetime is True:
                        break
                    time.sleep(1.0)
            return send_data

        except socket.timeout:
            print("Time out")
            print("")
# }}}

    def multicast_send_udp(self,
                           host="", multicast_group=None,
                           port=None,
                           onetime=False,
                           send_data="From Python multicasting"):  # {{{
        """ マルチキャスト 送信 """
        if host is None:
            host = self.local_host
        if port is None:
            port = self.remote_port

        if multicast_group is None:
            multicast_group = self.local_host

        try:
            with closing(socket.socket(socket.AF_INET,
                                       socket.SOCK_DGRAM)) as sock:
                sock.setsockopt(socket.IPPROTO_IP,
                                socket.IP_MULTICAST_IF,
                                socket.inet_aton(host))
                while True:
                    sock.sendto(send_data, (multicast_group, port))
                    print("Send data from UDP/IP: " + str(send_data))
                    print("")

                    if onetime is True:
                        break
                    time.sleep(1.0)
            return send_data

        except socket.timeout:
            print("Time out")
            print("")
# }}}


def main():
    udc = UdpCommun()
    sended = udc.send_udp(host="", port=9000, send_data="OK")
    print("Send from python: " + sended)

    readed = udc.read_udp(onetime=True)
    print("Read from python: " + readed)

if __name__ == "__main__":
    main()
