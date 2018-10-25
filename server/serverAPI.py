#!/usr/bin/env python3
import socket
from threading import Thread


class ServerAPI:

    def __init__(self):
        self.clients = {}
        self.addresses = {}
        self.bufsize = 1024
        self.server = None
        self.accept_thread = None

    def makeSocket(self, host, port):
        addr = (host, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen(2)
        print("waiting connection...")
        self.accept_thread = Thread(target=self.accept_incoming_connections)
        self.accept_thread.start()
        self.accept_thread.join()
        self.server.close()

    def accept_incoming_connections(self):
        while True:
            client, client_address = self.server.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes("Now type your name and press enter!", "utf8"))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):  # Takes client socket as argument.
        name = client.recv(self.bufsize).decode("utf8")
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat." % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name

        while True:
            msg = client.recv(self.bufsize)
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes("%s has left the chat." % name, "utf8"))
                break

    def broadcast(self, msg, prefix=""):  # prefix is for name identification.
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8")+msg)


def call():
    server = ServerAPI()
    server.makeSocket('', 25565)


if __name__ == "__main__":
    call()
