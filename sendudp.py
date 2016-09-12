import socket

dstip = "127.0.0.1"
dstport = 4001
message = "From Python"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (dstip, dstport))
