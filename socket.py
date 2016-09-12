# -*- coding: utf-8 -*-
import socket


def read_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 指定したホスト(IP)とポートをソケットに設定
    sock.bind(("localhost", 4001))
    # 1つの接続要求を待つ
    sock.listen(1)
    # 要求が来るまでブロック
    soc, addr = sock.accept()
    # サーバ側の合図
    print("Conneted by"+str(addr))

    while (1):
        # サーバー側入力待機
        data = raw_input("Server>")
        # ソケットにデータを送信
        soc.send(data)
        # データを受信（1024バイトまで）
        data = soc.recv(1024)
        # サーバー側の書き込みを表示
        print "Client>", data
        # qが押されたら終了
        if data == "q":
            soc.close()
            break

if __name__ == "__main__":
    read_udp()
