#!/usr/bin/env python3
import socket
from threading import Thread


def inputf():
    while True:
        msg = input()
        send(msg)


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
        except OSError:
            break


def send(msg):  # event is passed by binders.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()


def on_closing():
    send("{quit}")


PORT = 25565
BUFSIZ = 1024

if __name__ == "__main__":
    host = input('Enter host: ')
    addr = (host, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(addr)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    input_thread= Thread(target=inputf)
    input_thread.start()
