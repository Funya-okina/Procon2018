import eel


class WebUi:
    def __init__(self):
        eel.init("server/server_ui/web")
        self.events = {}

        @eel.expose
        def cellClicked(row, column):
            if "cellClicked" in self.events:
                self.events["cellClicked"](row, column)

        @eel.expose
        def gameStart(row, column, symmetry):
            if "gameStart" in self.events:
                self.events["gameStart"](row, column, symmetry)

        @eel.expose
        def genScores(row, column, symmetry, agent_cell):
            if "genScores" in self.events:
                self.events["genScores"](row, column, symmetry, agent_cell)

        @eel.expose
        def readQR(camera_id):
            if "readQR" in self.events:
                self.events["readQR"](int(camera_id))

        @eel.expose
        def getBoardScores():
            if "getBoardScores" in self.events:
                self.events["getBoardScores"]()

    def addEvent(self, event_name: str, func: object):
        self.events[event_name] = func

    @staticmethod
    def showWindow():
        web_app_options = {
            'mode': 'chrome-app',
            'host': 'localhost'
        }
        eel.start("main.html", options=web_app_options)
        eel.closeWindow()

    @staticmethod
    def showBoard(cell_scores: list, first_agents_a: list, first_agents_b: list):
        eel.showBoard(cell_scores, first_agents_a, first_agents_b)

    @staticmethod
    def editCellAttrs(row: int, column: int, attr: str, value: bool):
        eel.editCellAttrs(row, column, attr, value)

    @staticmethod
    def getCellScore(row, column):
        return eel.getCellScore(row, column)()
