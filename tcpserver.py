# !/usr/bin/python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        TCP/IP communication
# Purpose:
#
# Author:      Kilo11
#
# Created:     29/09/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10013
# -------------------------------------------------------------------------------

# モジュールインポート
# from __future__ import print_function
import socket
import tcpclient as tcp
from contextlib import closing


class TcpSrvCom(tcp.TcpCliCom):
    """ TCP/IP通信 サーバー """
    def __init__(self):
        tcp.TcpCliCom.__init__(self)

    def read_server(self, host=None, port=None, bufsize=4096,
                    onetime=False, reply=None):
        """ サーバー側 受信 """
        if host is None:
            host = self.server_host
        if port is None:
            port = self.client_port

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with closing(sock):
                sock.bind((host, port))
                sock.listen(1)
                sock, addr = sock.accept()
                print("Connected by" + str(addr))

                while True:
                    read_data = sock.recv(bufsize)
                    print("Get data from TCP/IP: " + str(read_data))
                    print("")

                    if reply is not None:
                        sock.send(str(reply))
                        print("Send data from TCP/IP: " + str(reply))
                        print("")

                    if onetime is True and read_data is not None:
                        break
                    if read_data == "q":
                        break
            return read_data

        except socket.timeout:
            print("Time out")
            print("")

    def send_server(self, host=None, port=None, bufsize=4096,
                    send_data="From Python"):
        """ サーバー側 送信 """
        if host is None:
            host = self.server_host
        if port is None:
            port = self.client_port

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with closing(sock):
                sock.bind((host, port))
                sock.listen(1)
                sock, addr = sock.accept()
                print("Connected by" + str(addr))
                print("")

                sock.send(send_data)
                print("Send data from TCP/IP: " + str(send_data))
                print("")
            return send_data

        except socket.timeout:
            print("Time out")
            print("")


def main():
    udc = TcpSrvCom()
    udc.read_server(onetime=True, reply="OK from python")
    udc.send_server(send_data="Test method")

if __name__ == "__main__":
    main()
