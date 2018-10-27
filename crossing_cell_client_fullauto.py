import sys
import numpy as np
from client_solver.client_ui.webUi import WebUi
from control.Board import Board
from threading import Thread
import json
import socket
import time
import math
import copy
from new_solver import NewSolver

np.set_printoptions(threshold=np.inf)
argv = sys.argv


class Client(object):
    def __init__(self, port):
        self.host = 'localhost'

        self.webUi = WebUi()
        self.port_ui = port

        self.webUi.addEvent("cellClicked", self.wasClicked)
        self.webUi.addEvent("getBoardScores", self.getBoardScores)
        self.webUi.addEvent("connectServer", self.connectServer)

        self.agent_behavior_step = 0
        self.new_agent_locations = [[0, 0], [0, 0]]
        self.new_agent_diff = [[0, 0], [0, 0]]
        self.remove_tile_locations = []

        self.board = Board()
        self.playng_thread = None

        self.solving_engine = NewSolver()

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

    def wasClicked(self, board_row, board_column):
        if self.team == "A":
            i = 0
            tile_color = "a-tile"
            agent_color = "a{}-present".format(self.agent_behavior_step)
            opponent_color = "b-tile"
            my_tiles = copy.deepcopy(self.board.team_a)
            opponent_tiles = copy.deepcopy(self.board.team_b)
        elif self.team == "B":
            i = 1
            tile_color = "b-tile"
            agent_color = "b{}-present".format(self.agent_behavior_step)
            opponent_color = "a-tile"
            my_tiles = copy.deepcopy(self.board.team_b)
            opponent_tiles = copy.deepcopy(self.board.team_a)

        agent = self.board.getCurrentAgentLocations()[i][self.agent_behavior_step]
        if self.isAroundCell([board_row, board_column], agent):

            if self.agent_behavior_step >= 1:
                if opponent_tiles[board_row][board_column] == 1:
                    if opponent_tiles[board_row][board_column] == 1:
                        self.new_agent_locations[self.agent_behavior_step] = [agent[0], agent[1]]
                        self.remove_tile_locations.append([board_row, board_column])
                        self.webUi.editCellAttrs(board_row, board_column, opponent_color, False)
                else:
                    self.webUi.editCellAttrs(agent[0], agent[1], tile_color, True)
                    self.webUi.editCellAttrs(board_row, board_column, agent_color, True)
                    self.new_agent_locations[self.agent_behavior_step] = [board_row, board_column]

                diff = [self.new_agent_locations[1][0]-agent[0],
                        self.new_agent_locations[1][1]-agent[1]]

                self.agent_behavior_step = 0
                print("黒:", self.chooseTramp(diff))

                json_data = json.dumps({
                    "order": "client_update",
                    "from": self.team,
                    "agent_location": self.new_agent_locations,
                    "remove_tiles": self.remove_tile_locations
                })
                self.send(json_data)
                self.new_agent_locations = [[0, 0], [0, 0]]
                self.remove_tile_locations = []
            else:
                if opponent_tiles[board_row][board_column] == 1:
                    if opponent_tiles[board_row][board_column] == 1:
                        self.new_agent_locations[self.agent_behavior_step] = [agent[0], agent[1]]
                        self.remove_tile_locations.append([board_row, board_column])
                        self.webUi.editCellAttrs(board_row, board_column, opponent_color, False)
                else:
                    self.webUi.editCellAttrs(agent[0], agent[1], tile_color, True)
                    self.webUi.editCellAttrs(board_row, board_column, agent_color, True)
                    self.new_agent_locations[self.agent_behavior_step] = [board_row, board_column]

                self.agent_behavior_step += 1
                diff = [self.new_agent_locations[0][0]-agent[0],
                        self.new_agent_locations[0][1]-agent[1]]
                print("赤:", self.chooseTramp(diff))
        else:
            print("八近傍以外のセルには移動できません")

    def chooseTramp(self, diff):
        if diff == [-1, 0]:
            return 1
        elif diff == [-1, 1]:
            return 2
        elif diff == [0, 1]:
            return 3
        elif diff == [1, 1]:
            return 4
        elif diff == [1, 0]:
            return 5
        elif diff == [1, -1]:
            return 6
        elif diff == [0, -1]:
            return 7
        elif diff == [-1, -1]:
            return 8


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

    def showWeb(self):
        self.webUi.showWindow(self.port_ui)

    def setUIBoard(self):
        self.webUi.showBoard(self.board.board_scores, self.board.first_agent_cells_a, self.board.first_agent_cells_b)

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

        # これよりソルバー
        self.solving_engine.set_team(self.team)

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
                    self.setUIBoard()

                    # これよりソルバー
                    if self.team == 'A':
                        agent_pos = self.board.current_agent_cells_a
                    elif self.team == 'B':
                        agent_pos = self.board.current_agent_cells_b

                    self.solving_engine.update_board(self.board)
                    self.solving_engine.calcScoreAverage()

                    self.solving_engine.gen_state_list()

                    agent0_next = self.solving_engine.search_around(*agent_pos[0])
                    self.wasClicked(*agent0_next)
                    agent1_next = self.solving_engine.search_around(*agent_pos[1])
                    self.wasClicked(*agent1_next)
                    time.sleep(1.0)

                elif order == 'next_turn':
                    self.board.setCurrentAgentLocations(rcv_dict['agents'][0], "A")
                    self.board.setCurrentAgentLocations(rcv_dict['agents'][1], "B")
                    self.board.team_a = copy.deepcopy(rcv_dict['tiles_a'])
                    self.board.team_b = copy.deepcopy(rcv_dict['tiles_b'])
                    self.webUi.updateCellAttrs(self.board.team_a, self.board.team_b, self.board.getCurrentAgentLocations())
                    # ソルバー
                    if self.team == 'A':
                        agent_pos = self.board.current_agent_cells_a
                    elif self.team == 'B':
                        agent_pos = self.board.current_agent_cells_b

                    self.solving_engine.update_board(self.board)
                    self.solving_engine.gen_state_list()

                    agent0_next = self.solving_engine.search_around(*agent_pos[0])
                    self.wasClicked(*agent0_next)
                    agent1_next = self.solving_engine.search_around(*agent_pos[1])
                    self.wasClicked(*agent1_next)
                    time.sleep(1.0)

                elif order == 'reject_turn':
                    self.board.setCurrentAgentLocations(rcv_dict['agents'][0], "A")
                    self.board.setCurrentAgentLocations(rcv_dict['agents'][1], "B")
                    self.board.team_a = copy.deepcopy(rcv_dict['tiles_a'])
                    self.board.team_b = copy.deepcopy(rcv_dict['tiles_b'])
                    self.webUi.updateCellAttrs(self.board.team_a, self.board.team_b, self.board.getCurrentAgentLocations())


            except OSError:
                break

    def send(self, msg):  # event is passed by binders.
        self.client_socket.send(bytes(msg, "utf8"))
        time.sleep(1e-3)
        if msg == "{quit}":
            self.client_socket.close()


if __name__ == "__main__":
    window = Client(int(argv[1]))
    window.showWeb()
    sys.exit()
