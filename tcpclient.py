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
import time
import socket
from contextlib import closing


class TcpCliCom:
    """ TCP/IP通信 """
    def __init__(self):
        self.client_port = 9000
        self.server_port = 60001

        if os.name == "nt":
            self.client_name = socket.gethostname()
            self.client_addr = (socket.gethostbyname(self.client_name),
                                self.client_port)
            if self.client_name == "cad0021":
                self.server_host = "172.21.38.192"
                # self.server_host = "172.21.38.31"
                print("Selected Creo PC")
            elif self.client_name == "PC-SA4110204580":
                self.server_host = "192.168.1.5"
                print("Selected Old Let's note")
            elif self.client_name == "":
                self.server_host = "192.168.1.5"
                print("Selected New Let's note")
            else:
                self.server_host = "192.168.1.5"
                print("In PXI")

        elif os.name == "posix":
            self.client_name = os.uname()[1]
            if self.client_name == "ProSalad13.local":
                self.server_host = "10.0.1.5"
                print("Selected MacBook Pro")
            else:
                # TODO: "client_addr" を設定する
                # self.server_host = client_addr
                print("Selected unknouwn PC")

        print("Host name: " + self.client_name)
        print("Local addr: " + str(self.client_addr))
        print("")

    def read_client(self, host=None, port=None, bufsize=4096,
                    onetime=False, prefix=None, reply=None, delay=0.1):
        """ クライアント側 受信 """
        if host is None:
            host = self.server_host
        if port is None:
            port = self.server_port
        read_data = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with closing(sock):
                sock.connect((host, port))

                if prefix is not None:
                    sock.send(prefix)
                    print("Send prefix from TCP/IP: " + str(prefix))
                    print("")

                while True:
                    read_data = sock.recv(bufsize).strip()
                    print("Get data from TCP/IP: " + read_data)
                    print("")

                    if reply is not None:
                        time.sleep(delay)
                        sock.send(reply)
                        print("Send reply from TCP/IP: " + str(reply))
                        print("")
                        time.sleep(delay)

                    if onetime is True and read_data is not None:
                        break
                    if read_data == "q":
                        break

            return read_data

        except socket.timeout:
            print("Time out")
            print("")

    def send_client(self, host=None, port=None, bufsize=4096,
                    send_data="From Python"):
        """ クライアント側 送信 """
        if host is None:
            host = self.server_host
        if port is None:
            port = self.server_port

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            with closing(sock):
                sock.connect((host, port))

                sock.send(send_data)
                print("Send data from TCP/IP: " + str(send_data))
                print("")
            return send_data

        except socket.timeout:
            print("Time out")
            print("")


def main():
    tcc = TcpCliCom()
    # sended = tcc.send_client(host="192.168.1.5", port=60001, send_data="OK")
    # print("Send from python: " + str(sended))

    # readed = tcc.read_client(host="192.168.1.5", port=60001,
    #                          onetime=True, prefix="OK", reply="OK")
    # print("Read from python: " + str(readed))

if __name__ == "__main__":
    main()
