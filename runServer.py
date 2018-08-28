import sys
import numpy as np
import socket
from server.server_ui.webUi import WebUi
from control.gameController import GameController
from server.QRdecode import QRdecoder

np.set_printoptions(threshold=np.inf)


class Server(object):
    player_turn = 'A'

    def __init__(self, parent=None):
        self.webUi = WebUi()

        self.webUi.addEvent("cellClicked", self.wasClicked)
        self.webUi.addEvent("gameStart", self.gameStart)
        self.webUi.addEvent("genScores", self.genScores)
        self.webUi.addEvent("getMyIPAddress", self.getMyIPAddress)
        self.webUi.addEvent("readQR", self.readQR)

        self.row = 12
        self.column = 12
        self.first_agent_cell_a = [[0, 0], [0, 1]]
        self.first_agent_cell_b = [[1, 0], [1, 1]]

    def wasClicked(self, board_row, board_column):
        print(board_row, board_column)
        print(self.webUi.getCellScore(board_row, board_column))
        self.webUi.editCellAttrs(board_row, board_column, "a0-present", True)

    def gameStart(self, board_row, board_column, symmetry_id=0):
        pass

    def genScores(self, row, column, symmetry=0, agent_a=[[0, 0], [0, 1]]):
        controller = GameController()
        board_cell_scores = controller.genScores_py(row, column, symmetry)
        print(board_cell_scores)
        self.registerAgentCell(agent_a, int(row)-1, int(column)-1)
        self.webUi.showBoard(board_cell_scores.tolist(), self.first_agent_cell_a, self.first_agent_cell_b)

    def registerAgentCell(self, agents_a, row, column):
        self.first_agent_cell_a[0] = agents_a[0]
        self.first_agent_cell_a[1] = agents_a[1]
        if self.first_agent_cell_a[0][0] == self.first_agent_cell_a[1][0]:
            self.first_agent_cell_b[0] = [row-self.first_agent_cell_a[0][0], self.first_agent_cell_a[0][1]]
            self.first_agent_cell_b[1] = [row-self.first_agent_cell_a[1][0], self.first_agent_cell_a[1][1]]
        elif self.first_agent_cell_a[0][1] == self.first_agent_cell_a[1][1]:
            self.first_agent_cell_b[0] = [self.first_agent_cell_a[0][0], column-self.first_agent_cell_a[0][1]]
            self.first_agent_cell_b[1] = [self.first_agent_cell_a[1][0], column-self.first_agent_cell_a[1][1]]
        else:
            self.first_agent_cell_b[0] = [self.first_agent_cell_a[1][0], self.first_agent_cell_a[0][1]]
            self.first_agent_cell_b[1] = [self.first_agent_cell_a[0][0], self.first_agent_cell_a[1][1]]


    def readQR(self, camera_id):
        qr = QRdecoder(camera_id)
        read_code = qr.reader()
        if read_code is None:
            return
        code_list = read_code.split(":")
        row, column = code_list[:1][0].split()
        agents_a = [list(map(lambda x: x - 1, map(int, code_list[-3].split()))), list(map(lambda x: x - 1, map(int, code_list[-2].split())))]
        self.registerAgentCell(agents_a, row, column)

        score_data = code_list[1:][:-3]
        board_cell_scores = []
        for row_scores in score_data:
            row_scores_list = list(map(int, row_scores.split()))
            print(row_scores_list)
            board_cell_scores.append(row_scores_list)
        print(self.first_agent_cell_a, self.first_agent_cell_b)
        self.webUi.showBoard(board_cell_scores, self.first_agent_cell_a, self.first_agent_cell_b)

    def moveAgent(self, agent_name, movement):
        pass

    def initAgent(self, agents_dict):
        pass

    def showWeb(self):
        self.webUi.showWindow()

    def getMyIPAddress(self):
        return socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    window = Server()
    window.showWeb()
    sys.exit()
