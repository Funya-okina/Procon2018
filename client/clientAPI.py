#!/usr/bin/env python3
import socket
import time
from threading import Thread


class ClientAPI:

    def __init__(self, player):
        self.player = player # "A" or "B"
        self.client_socket = None
        self.bsize = 1024
        self.receive_thread = None
        self.input_thread = None

    def connect(self, host, port):
        addr = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(addr)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()
        self.send(str(self.player))
        # self.input_thread= Thread(target=self.inputf)
        # self.input_thread.start()

    # def inputf(self):
    #     while True:
    #         msg = input()
    #         self.send(msg)

    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(self.bsize).decode("utf8")
                print(msg)
            except:
                break

    def send(self, msg):  # event is passed by binders.
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def on_closing(self):
        self.send("{quit}")


def call():
    client = ClientAPI("A")
    client.connect('localhost', 25565)
    for i in range(10):
        time.sleep(1)
        client.send("Hello {}".format(i))



if __name__ == "__main__":
    call()

