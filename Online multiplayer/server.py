import socket
from _thread import *
import sys

server = "192.168.1.39"
# This port is usually open to use
port = 5555

# Setting Up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# listening for connections
s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    # Run continously while client is connected
    while True:
        try:
            # 2048 = amount of information recieving(in bits)
            data = conn.recv(2048)
            # We will receive encode info, so we have to decode it
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Recieved: ", reply)
                print("Sending: ", reply)

            # Always encoded information should be sent through server
            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


# Continuously look for connection
while True:
    # s.accept() will accept any incoming connections
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, ))



