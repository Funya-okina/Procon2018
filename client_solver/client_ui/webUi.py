import eel


class WebUi:
    def __init__(self):
        eel.init("client_solver/client_ui/web")
        self.events = {}

        @eel.expose
        def connectServer(port, team):
            if "connectServer" in self.events:
                self.events["connectServer"](port, team)

        @eel.expose
        def cellClicked(row, column, isRemoveMode):
            if "cellClicked" in self.events:
                self.events["cellClicked"](row, column, isRemoveMode)

        @eel.expose
        def getBoardScores():
            if "getBoardScores" in self.events:
                self.events["getBoardScores"]()

    def addEvent(self, event_name: str, func: object):
        self.events[event_name] = func

    @staticmethod
    def showWindow(port):
        web_app_options = {
            'mode': 'chrome-app',
            'host': 'localhost',
            'port': port
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

    @staticmethod
    def updateCellAttrs(tile_a: list, tile_b: list, agents: list):
        eel.updateCellAttrs(tile_a, tile_b, agents)
