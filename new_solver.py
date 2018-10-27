import sys
import queue
from control.Board import Board
import copy

class NewSolver(object):
    def __init__(self, team):
        self.board = Board()
        self.state = []
        self.threshold = 0
        self.team = team

    def calcScoreAverage(self):
        num_of_cells = 0
        for row in self.board.getBoardScores():
            for cell in row:
                if cell >= 0:
                    self.threshold += cell
                    num_of_cells += 1

        self.threshold /= num_of_cells

    def update_boad(self, input_board):
        self.board = input_board

    def gen_state_list(self):
        if self.team == 'A':
            my_board = copy.deepcopy(self.board.team_a)
            enemy_board = copy.deepcopy(self.board.team_b)
        elif self.team == 'B':
            my_board = copy.deepcopy(self.board.team_b)
            enemy_board = copy.deepcopy(self.board.team_a)

        self.state = [[0] * self.board.getBoardSize()[1] for i in range(self.board.getBoardSize()[0])]

        for x in range(self.board.getBoardSize()[0]):
            for y in range(self.board.getBoardSize()[1]):
                if my_board[x][y]:
                    self.state[x][y] = 0
                else:
                    if self.board.getBoardScores()[x][y] >= self.threshold:
                        if enemy_board[x][y]:
                            self.state[x][y] = 3
                        else:
                            self.state[x][y] = 2
                    elif self.board.getBoardScores()[x][y] >= 0:
                        if enemy_board[x][y]:
                            self.state[x][y] = -1
                        else:
                            self.state[x][y] = 1
                    else:
                        self.state[x][y] = -2

    def search_around(self, row, column):
        destination = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
        que = []
        board_size = self.board.getBoardSize()
        for a in destination:
            if (0 <= row + a[0] < self.board.getBoardSize()[0]) and (0 <= column + a[1] < self.board.getBoardSize()[1]) :
                state_cache1 = copy.deepcopy(self.state)
                first_step = self.state[row+a[0]][column+a[1]]
                state_cache1[row+a[0]][column+a[1]] = 0

                for b in destination:
                    if (0 <= row + a[0] + b[0] < self.board.getBoardSize()[0]) and (0 <= column + a[1] + b[1] < self.board.getBoardSize()[1]):
                        state_cache2 = copy.deepcopy(state_cache1)
                        second_step = state_cache1[row+a[0]+b[0]][column+a[1]+b[1]]
                        state_cache2[row+a[0]+b[0]][column+a[1]+b[1]] = 0

                        for c in destination:
                            if (0 <= (row+a[0]+b[0]+c[0]) < board_size[0]) and (0 <= (column+a[1]+b[1]+c[1]) < board_size[1]):
                                third_step = state_cache2[row+a[0]+b[0]+c[0]][column+a[1]+b[1]+c[1]]
                                que.append((first_step + second_step + third_step,
                                            self.board.getBoardScores()[row+a[0]][column+a[1]] + self.board.getBoardScores()[row+a[0]+b[0]][column+a[1]+b[1]] + self.board.getBoardScores()[row+a[0]+b[0]+c[0]][column+a[1]+b[1]+c[1]],
                                            (a, b, c)
                                            ))
        practice = [0, 0] #[forのiを代入, 評価値を代入]
        practices = []

        for i, element in enumerate(que):
            if element[0] > practice[1]:
                practice = [i, element[0]]
                practices = []
                practices.append(practice)
            elif element[0]== practice[1]:
                practice = [i, element[0]]
                practices.append(practice)

        best_practice = [0, (0, 0)]
        for a in practices:
            if que[a[0]][1] > best_practice[0]:
                best_practice = [que[a[0]][1], que[a[0]][2][0]]
        return [row + best_practice[1][0], column + best_practice[1][1]]



#これより下デバッグ用テスト実行コード
def call():
    solver = NewSolver('A')
    solver.board.initBoardSize(11, 11)
    solver.board.genScores(0)
    # solver.board.team_b = [[1]*11 for l in range(11)]
    solver.calcScoreAverage()
    solver.gen_state_list()

    for x in solver.board.getBoardScores():
        for y in x:
            print(format(y, '3d'), end="")
        print("")
    print("")

    for x in solver.state:
        for y in x:
            print(format(y, '3d'), end="")
        print("")
    print("")

    print(solver.search_around(0, 10))


if __name__ == '__main__':
    call()
    sys.exit()
