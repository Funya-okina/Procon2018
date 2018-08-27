import sys
import numpy as np
np.set_printoptions(threshold=np.inf)
from main_ui import Ui_Dialog


class uiPanel(QDialog):
    def __init__(self, parent=None):
        super(uiPanel, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.playBoard.cellClicked.connect(self.wasClicked)
        self.ui.startButton.clicked.connect(self.gameStart)

    def wasClicked(self, row, column):
        print(row, column)
        print(self.ui.playBoard.item(row, column).text())
        self.ui.playBoard.item(row, column).setBackground(QColor(100,100,100))

    def gameStart(self):
        row = self.ui.setRow.value()
        column = self.ui.setColumn.value()

        self.ui.playBoard.setRowCount(row)
        self.ui.playBoard.setColumnCount(column)

        boardScores = control.genScores_py(row, column)
        for r in range(row):
            for c in range(column):
                self.ui.playBoard.setItem(r, c, QTableWidgetItem(str((int(boardScores[r][c])))))
                self.ui.playBoard.item(r, c).setTextAlignment(Qt.AlignHCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = uiPanel()
    window.show()
    sys.exit(app.exec_())
