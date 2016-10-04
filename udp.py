# !/usr/bin/python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        UDP/IP communication
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
import os
import time
import socket
from contextlib import closing


class UdpCommun:
    """ UDP/IP通信 """
    def __init__(self):
        self.host_name = socket.gethostname()
        self.local_port = 9000
        self.remote_port = 60001
        self.local_addr = (socket.gethostbyname(self.host_name),
                           self.local_port)

        if socket.gethostname() == "cad0021":
            self.local_host = "172.21.38.192"
            print("Selected Creo PC")
        elif socket.gethostname() == "PC-SA4110204580":
            self.local_host = "192.168.1.11"
            print("Selected Creo PC")

        elif os.uname()[1] == "ProSalad13.local":
            self.local_host = "10.0.1.31"
            print("Selected MacBook Pro")
        else:
            self.local_host = "192.168.1.5"
            print("Selected unknouwn PC")

        print("Host name: " + self.host_name)
        print("Local addr: " + str(self.local_addr))
        print("")

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
    # !!!: 試す
    # sended = udc.send_udp(host="192.168.1.5:9000")
    print("Send from python: " + sended)

    readed = udc.read_udp(onetime=True)
    print("Read from python: " + readed)

if __name__ == "__main__":
    main()
