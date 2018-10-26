from control.Board import Board

def genScores(row, column, symmetry, agents_a):
    print("生成受け渡しデータ:", row, column)
    board.initBoardSize(row, column)
    print(agents_a)
    board.genScores(symmetry)
    board.setFirstAgentCell(agents_a)
    board.printBoardScore()
    # board.printTiles_A()
    # board.printTiles_B()

def printBoardScore_sq(level):
    for row_socres in board.board_scores:
        for score in row_socres:
            if score > level:
                print("██", end="")
            else:
                print("  ", end="")
        print("")

board = Board()
genScores(10, 10, 0, [[1, 1], [9-1, 9-1]])
level = sum(map(sum, board.getBoardScores())) / 100
print(level)
print("")
printBoardScore_sq(level)
print("")
print("")
print("")
print("")
print("")
printBoardScore_sq(level-2)




