import sys
import os
import numpy as np
import socket
from datetime import datetime
from server.server_ui.webUi import WebUi
from server.QRLib import decodeQR
from server.QRLib import encodeQR
from control.Board import Board

np.set_printoptions(threshold=np.inf)


class Server(object):
    player_turn = 'A'

    def __init__(self, parent=None):
        self.webUi = WebUi()

        self.webUi.addEvent("cellClicked", self.wasClicked)
        self.webUi.addEvent("gameStart", self.gameStart)
        self.webUi.addEvent("genScores", self.genScores)
        self.webUi.addEvent("getMyIPAddress", self.getMyIPAddress)
        self.webUi.addEvent("readQR", self.decodeQR)
        self.webUi.addEvent("getBoardScores", self.getBoardScores)
        self.webUi.addEvent("encodeQR", self.encodeQR)

        self.board = Board()

    def wasClicked(self, board_row, board_column):
        print(board_row, board_column)
        print(self.webUi.getCellScore(board_row, board_column))
        self.webUi.editCellAttrs(board_row, board_column, "a0-present", True)

    def gameStart(self, board_row, board_column, symmetry_id=0):
        pass

    def genScores(self, row, column, symmetry, agents_a):
        self.board.initBoardSize(row, column)
        self.board.genScores(symmetry)
        # agents_a = [list(map(lambda x: x-1, agents_a[0])), list(map(lambda x: x-1, agents_a[1]))]
        self.board.setFirstAgentCell(agents_a)
        self.board.printBoardScore()
        self.setUIBoard()


    def decodeQR(self, camera_id):
        qr = decodeQR(camera_id)
        read_code = qr.decoder()
        if read_code is None:
            return
        code_list = read_code.split(":")
        row, column = list(map(int, code_list[:1][0].split()))
        self.board.initBoardSize(row-1, column-1)
        agents_a = [list(map(lambda x: x-1, map(int, code_list[-3].split()))), list(map(lambda x: x-1, map(int, code_list[-2].split())))]
        self.board.setFirstAgentCell(agents_a)

        score_data = code_list[1:][:-3]
        board_cell_scores = []
        for row_scores in score_data:
            row_scores_list = list(map(int, row_scores.split()))
            board_cell_scores.append(row_scores_list)
        self.board.initBoardScores(board_cell_scores)
        self.board.printBoardScore()
        self.setUIBoard()

    def encodeQR(self):
        qr = encodeQR()
        board_scores = self.board.getBoardScores()
        board_size = self.board.getBoardSize()
        agents_a = self.board.getFirstAgentsLocation()[0]
        data_list = []
        data_list.append(" ".join(map(str, map(lambda x:x+1, board_size))))
        for row_scores in board_scores:
            data_list.append(" ".join(map(str, row_scores)))
        for agent in agents_a:
            data_list.append(" ".join(map(str, map(lambda x:x+1, agent))))

        data = "{}:".format(":".join(data_list))
        qr.encoder(data, "{}/QRcodes".format(os.getcwd()), datetime.now().strftime("%Y%m%d%H%M%S_QR.png"))

    def moveAgent(self, agent_name, movement):
        pass

    def showWeb(self):
        self.webUi.showWindow()

    def setUIBoard(self):
        self.webUi.showBoard(self.board.board_scores, self.board.first_agent_cell_a, self.board.first_agent_cell_b)

    def getMyIPAddress(self):
        return socket.gethostbyname(socket.gethostname())

    def getBoardScores(self):
        return self.board.getBoardScores()


if __name__ == "__main__":
    window = Server()
    window.showWeb()
    sys.exit()
