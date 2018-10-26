import sys
import numpy as np
from control.Board import Board
from threading import Thread
from solver import Solver
import json
import socket
import time
import math
import copy

np.set_printoptions(threshold=np.inf)

class Client(object):

    def __init__(self):
        self.host = 'localhost'

        self.agent_behavior_step = 0
        self.new_agent_locations = [[0, 0], [0, 0]]
        self.remove_tile_locations = []

        self.board = Board()
        self.playng_thread = None

        self.solver = Solver()

        # connections
        self.team = "A" # "A" or "B"
        self.client_socket = None
        self.bsize = 1024
        self.receive_thread = None
        self.input_thread = None
        self.was_recieved = False
        self.rcv_msg = ''

    def isAroundCell(self, cell1, cell2):
        return math.sqrt((cell1[0]-cell2[0])**2+(cell1[1]-cell2[1])**2) <= math.sqrt(2)

    def moveAgent(self):
        if self.team == "A":
            pass
        elif self.team == "B":
            pass

    def remomveTile(self):
        if self.team == "A":
            pass
        elif self.team == "B":
            pass

    def getBoardScores(self):
        return self.board.getBoardScores()

    # connections method
    def connectServer(self, port, team):
        self.team = team
        addr = (self.host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(addr)

        self.receive_thread = Thread(target=self.recieve)
        self.receive_thread.start()
        self.send(self.team)

    def recieve(self):
        while True:
            try:
                msg = self.client_socket.recv(self.bsize).decode("utf8")
                rcv_dict = json.loads(msg)
                order = rcv_dict['order']
                if order == 'board_scores':
                    self.board.initBoardSize(*rcv_dict['size'])
                    self.board.setFirstAgentCell(rcv_dict['agents'][0])
                    self.board.initBoardScores(rcv_dict['scores'])
                    self.board.printBoardScore()
                    self.solver.set_board(self.board)
                elif order == 'next_turn':
                    self.board.setCurrentAgentLocations(rcv_dict['agents'][0], "A")
                    self.board.setCurrentAgentLocations(rcv_dict['agents'][1], "B")
                    self.board.team_a = copy.copy(rcv_dict['tiles_a'])
                    self.board.team_b = copy.copy(rcv_dict['tiles_b'])
                    if self.team == "A":
                        self.board.printTiles_A()
                        self.board.printTiles_B()

            except OSError:
                break

    def send(self, msg):  # event is passed by binders.
        self.client_socket.send(bytes(msg, "utf8"))
        time.sleep(1e-3)
        if msg == "{quit}":
            self.client_socket.close()

    def solve(self):
        self.solver.set_state()
        self.solver.get_state()
        self.solver.get_lake_score()

def call():
    client = Client()
    port = int(input('接続ポートを入力:'))
    team = input('チーム(A or B):')
    client.connectServer(port, team)

if __name__ == "__main__":
    call()
    sys.exit()
