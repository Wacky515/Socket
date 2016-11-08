# !/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        tcpclient.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     29/09/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10012
# -----------------------------------------------------------------------------

# モジュールインポート
# from __future__ import print_function
import os
import time
import socket
from contextlib import closing


class TcpCliCom:
    """ TCP/IP通信 クライアント """
    def __init__(self):
        self.client_port = 9000
        self.server_port = 60001
        self.client_name = socket.gethostname()
        sgb = socket.gethostbyname
        self.client_addr = (sgb(self.client_name), self.client_port)

        self.dic_host_addr = {"cad0021": "172.21.38.192",
                              "mcad1037": "172.21.38.31",
                              "ProSalad13.local": "10.0.1.33",
                              "saladserver.com": "10.0.1.31",
                              "IAI_Robo": "192.168.1.5"
                              }
        scn = self.client_name
        d_ha = self.dic_host_addr

        if os.name == "nt":
            if scn == "cad0021":
                self.server_host = d_ha["cad0021"]
                # self.server_host = d_ha["mcad1037"]
                # self.server_host = d_ha["IAI_Robo"]
                print("Selected Creo PC")
            elif scn == "mcad1037":
                # self.server_host = d_ha["mcad1037"]
                # self.server_host = d_ha["cad0021"]
                self.server_host = d_ha["IAI_Robo"]
                print("Selected DR PC")
            elif scn == "PC-SA4110204580":
                self.server_host = d_ha["IAI_Robo"]
                print("Selected Old Let's note")
            elif scn == "NOT0053":
                self.server_host = d_ha["IAI_Robo"]
                print("Selected New Let's note")
            else:
                self.server_host = d_ha["IAI_Robo"]
                print("In PXI")

        elif os.name == "posix":
            if scn == "xacti":
                self.server_host = d_ha["IAI_Robo"]
                print("Selected Debian8 in cad0021 Virtual Box")
            elif scn == "ProSalad13.local":
                self.server_host = d_ha["saladserver.com"]
                print("Selected MacBook Pro")
            elif scn == "saladserver.com":
                self.server_host = d_ha["ProSalad13.local"]
                print("Selected Mac mini")
            else:
                self.server_host = d_ha["IAI_Robo"]
                print("Selected unknouwn PC")
        print("")

        print("Host(this PC) name: " + self.client_name)
        print("Local(this PC) addr: " + str(self.client_addr))
        print("")

    def read_client(self, host=None, port=None, bufsize=4096,
                    onetime=False, prefix=None, reply=None, delay=0.1):
        """ クライアント側 受信 """
        if host is None:
            host = self.server_host
        if port is None:
            port = self.server_port
        read_data = None

        print("Connect to(addr): " + host)
        print("Connect to(port): " + str(port))
        print("")

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
    # host = tcc.dic_host_addr["IAI_ROBO"]
    server_addr = tcc.dic_host_addr["cad0021"]
    # host = tcc.dic_host_addr["mcad1037"]

    # sended = tcc.send_client(host="192.168.1.5", port=60001, send_data="OK")
    # print("Send from python: " + str(sended))

    readed = tcc.read_client(host=server_addr,
                             onetime=True, prefix="OK", reply="OK")
    print("Read from python: " + str(readed))

if __name__ == "__main__":
    main()
