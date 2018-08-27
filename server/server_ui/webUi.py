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
        def gameStart(row, column, symmetry_id):
            if "gameStart" in self.events:
                self.events["gameStart"](row, column, symmetry_id)

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
    def showBoard(cell_scores: list):
        eel.showBoard(cell_scores)

    @staticmethod
    def editCellAttrs(row: int, column: int, attr: str, value: bool):
        eel.editCellAttrs(row, column, attr, value)

    @staticmethod
    def getCellScore(row, column):
        return eel.getCellScore(row, column)()
