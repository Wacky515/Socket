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
import os
import socket
from contextlib import closing


class TcpSrvCom:
    """ TCP/IP通信 """
    def __init__(self):
        self.server_name = socket.gethostname()
        self.client_port = 9000
        self.server_port = 60001
        self.server_addr = (socket.gethostbyname(self.server_name),
                            self.server_port)

        if socket.gethostname() == "cad0021":
            self.server_host = "172.21.38.192"
            print("Selected Creo PC")
        elif socket.gethostname() == "PC-SA4110204580":
            self.server_host = "172.21.115.144"
            print("Selected Old Let's note")

        elif os.uname()[1] == "ProSalad13.local":
            self.server_host = "192.168.1.5"
            print("Selected MacBook Pro")
        else:
            self.server_host = "192.168.1.5"
            print("Selected unknouwn PC")

        print("Server name: " + self.server_name)
        print("Server addr: " + str(self.server_addr))
        print("")

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
