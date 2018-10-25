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
        self.connected_player = {"A": False, "B": False}
        self.was_recieved = False
        self.rcv_msg = []

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
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):  # Takes client socket as argument.
        player = client.recv(self.bufsize).decode("utf8")
        if self.connected_player[player]:
            print("Player {} was connedted.".format(player))
            client.close()
            return
        self.connected_player[player] = True
        self.clients[client] = player
        print("Player %s has joined." % player)

        while True:
            msg = client.recv(self.bufsize)
            if msg != bytes("{quit}", "utf8"):
                    self.was_recieved = True
                    self.rcv_msg = [msg.decode('utf8'), self.clients[client]]
            else:
                self.connected_player[player] = False
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]

    def broadcast(self, msg):  # prefix is for name identification.
        for sock in self.clients:
            sock.send(msg)

    def isConnected(self):
        return all(self.connected_player.values())

    def read(self):
        self.was_recieved = False
        return self.rcv_msg

    def isRecieved(self):
        return self.was_recieved


def call():
    server = ServerAPI()
    server.makeSocket('', 25565)


if __name__ == "__main__":
    call()
