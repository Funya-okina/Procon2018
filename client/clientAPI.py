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
        self.was_recieved = False
        self.rcv_msg = ''

    def connect(self, host, port):
        addr = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(addr)

        self.receive_thread = Thread(target=self.recieve)
        self.receive_thread.start()
        self.send(self.player)
        # self.input_thread= Thread(target=self.inputf)
        # self.input_thread.start()

    # def inputf(self):
    #     while True:
    #         msg = input()
    #         self.send(msg)

    def recieve(self):
        while True:
            try:
                self.was_recieved = True
                self.rcv_msg = self.client_socket.recv(self.bsize).decode("utf8")
                print("recv:", self.rcv_msg)
            except OSError:
                break

    def send(self, msg):  # event is passed by binders.
        self.client_socket.send(bytes(msg, "utf8"))
        time.sleep(1e-3)
        if msg == "{quit}":
            self.client_socket.close()

    def read(self):
        self.was_recieved = False
        return self.rcv_msg

    def isRecieved(self):
        return self.was_recieved


def call():
    client = ClientAPI("A")
    client.connect('localhost', 25565)
    for i in range(1000):
        client.send("Hello {}".format(i))
    client.send("{quit}")



if __name__ == "__main__":
    call()

