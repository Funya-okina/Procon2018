import sys
from control.Board import Board

class Solver(object):

    def __init__(self):
        self.board = Board()
        self.state = []
        #stateの値は-3が囲むことのできない平均値未満の領域、-2が平均値以上の領域、-1が平均値以下で点数の計算が行われていない領域、0以上は点数計算が終わり、lake_scoreに点数が代入し終わった領域。
        self.lake_score = list()

    def calcScoreAverage(self):
        return sum(map(sum, self.board.board_scores)) / ((self.board.row+1)*(self.board.column+1))

    def state_init(self):
        self.state = [[0] * self.board.getBoardSize()[1] for i in range(self.board.getBoardSize()[0])]
        print(len(self.state), len(self.state))
        for x in range(self.board.getBoardSize()[0]):
            for y in range(self.board.getBoardSize()[1]):
                if self.board.getBoardScores()[x][y] < self.calcScoreAverage():
                    self.state[x][y] = -1
                else:
                    self.state[x][y] = -2

    def find_lakes(self, x, y, num):
        self.state[x][y] = num
        self.lake_score_buffer = 0

        self.utl = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for diff in self.utl:
            if (0 <= x + diff[0] < self.board.getBoardSize()[0] and 0 <= y + diff[1] < self.board.getBoardSize()[1]) and self.state[x+diff[0]][y+diff[1]] == -1:
                self.lake_score_buffer += self.find_lakes(x+diff[0], y+diff[1], num)
        return abs(self.board.getBoardScores()[x][y]) + self.lake_score_buffer

    def set_state(self):
        self.state_init()
        for i in (0, self.board.getBoardSize()[0]-1):
            for j in range(self.board.getBoardSize()[1]):
                if self.state[i][j] == -1:
                    self.find_lakes(i, j, -3)

        for i in range(self.board.getBoardSize()[0]):
            for j in (0, self.board.getBoardSize()[1]-1):
                if self.state[i][j] == -1:
                    self.find_lakes(i, j, -3)

        count = 0
        for i in range(self.board.getBoardSize()[0]):
            for j in range(self.board.getBoardSize()[1]):
                if self.state[i][j] == -1:
                    self.lake_score.append(self.find_lakes(i, j, count))
                    count += 1

    def set_board(self, in_board):
        self.board = in_board

    def get_state(self):
        return self.state

    def print_state(self):
        for row in self.state:
            for cell in row:
                print(format(cell, '3d'), end="")
            print("")

    def print_state_and_score(self, direction=0):
        if direction == 0:
            for row in self.state:
                for cell in row:
                    if cell < 0:
                        print(format(0, '3d'), end="")
                    else:
                        print(format(self.lake_score[cell], '3d'), end="")
                print("")
            print("")
            print("")
        elif direction == 1:
            for y in range(self.board.getBoardSize()[1]):
                for x in range(self.board.getBoardSize()[0]):
                    if self.state[x][y] < 0:
                        print(format(0, '3d'), end="")
                    else:
                        print(format(self.lake_score[self.state[x][y]], '3d'), end="")
                print("")
            print("")
            print("")
        elif direction == 2:
            for x in range(self.board.getBoardSize()[1])[::-1]:
                for y in range(self.board.getBoardSize()[0]):
                    if self.state[x][y] < 0:
                        print(format(0, '3d'), end="")
                    else:
                        print(format(self.lake_score[self.state[x][y]], '3d'), end="")
                print("")
            print("")
            print("")
        elif direction == 3:
            for y in range(self.board.getBoardSize()[1]):
                for x in range(self.board.getBoardSize()[0])[::-1]:
                    if self.state[x][y] < 0:
                        print(format(0, '3d'), end="")
                    else:
                        print(format(self.lake_score[self.state[x][y]], '3d'), end="")
                print("")
            print("")
            print("")


def call():
    solver = Solver()
    solver.board.genScores(0)
    solver.board.printBoardScore()
    solver.state_init()

    for row in solver.state:
        for cell in row:
            print(format(cell, '3d'), end="")
        print("")

    for i in (0, solver.board.getBoardSize()[0]-1):
        for j in range(solver.board.getBoardSize()[1]):
            if solver.state[i][j] == -1:
                solver.find_lakes(i, j, -3)

    for i in range(solver.board.getBoardSize()[0]):
        for j in (0, solver.board.getBoardSize()[1]-1):
            if solver.state[i][j] == -1:
                solver.find_lakes(i, j, -3)

    count = 0
    for i in range(solver.board.getBoardSize()[0]):
        for j in range(solver.board.getBoardSize()[1]):
            if solver.state[i][j] == -1:
                solver.lake_score.append(solver.find_lakes(i, j, count))
                count += 1

    print("")

    for row in solver.state:
        for cell in row:
            print(format(cell, '3d'), end="")
        print("")

    for item in solver.lake_score:
        print(item)


if __name__ == "__main__":
    call()
    sys.exit()
