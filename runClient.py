import sys
import os
import numpy as np
from ui.webUi import WebUi
from controll.gameController import GameController

np.set_printoptions(threshold=np.inf)


class UiPanel(object):
    player_turn = 'A'

    def __init__(self, parent=None):
        self.webUi = WebUi()

        self.webUi.addEvent("cellClicked", self.wasClicked)
        self.webUi.addEvent("gameStart", self.gameStart)

    def wasClicked(self, board_row, board_column):
        print(board_row, board_column)
        print(self.webUi.getCellScore(board_row, board_column))
        self.webUi.editCellAttrs(board_row, board_column, "a-area", True)

    def gameStart(self, board_row, board_column):
        # 本当はboard_cell_scoresはサーバープロセスから渡される
        controller = GameController()
        board_cell_scores = controller.genScores_py(board_row, board_column)
        # -------------------------------------------------------------------
        print(board_cell_scores)
        self.webUi.showBoard(board_cell_scores.tolist())

    def showWeb(self):
        self.webUi.showWindow()


if __name__ == "__main__":
    window = UiPanel()
    window.showWeb()
    sys.exit()
