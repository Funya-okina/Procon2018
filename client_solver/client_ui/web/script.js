'use strict';

const app = new Vue({
    el: '#app',
    data: {
        isDisplaying: false,
        isRemoveMode: false,
        cellScores: [],
        boardRotate: 0,
        port: 25565,
        team: "A",
        mouseoverCell: {
            row: null,
            column: null
        },
    },
    methods: {
        connectServer: function(){
            eel.connectServer(this.port, this.team);
        },

        show: function (preparedCellScores) {
            this.cellScores = preparedCellScores;
            this.isDisplaying = true;
        },

        cellClicked: function (row, column) {
            eel.cellClicked(row, column, this.isRemoveMode);
            this.isRemoveMode = false;
        },

        cellMouseover: function (row, column) {
            this.mouseoverCell.row = row;
            this.mouseoverCell.column = column;
        },

        cellMouseout: function (row, column) {
            this.mouseoverCell.row = this.mouseoverCell.row === row
                ? null : this.mouseoverCell.row;
            this.mouseoverCell.column = this.mouseoverCell.column === column
                ? null : this.mouseoverCell.column;
        },

        isMouseoverCell: function (row, column) {
            return this.mouseoverCell.row === row
                && this.mouseoverCell.column === column
               && row !== null
                && column !== null;
        },

        isMouseoverRelatedCell: function (row, column) {
            return !this.isMouseoverCell(row, column)
                && ((this.mouseoverCell.row === row && row !== null)
                    || (this.mouseoverCell.column === column && column !== null)
                );
        },
    }
});

function showBoard(cellScores, firstAgentsA, firstAgentsB) {
    const preparedCellScores = [];
    for (let i = 0; i < cellScores.length; i++) {
        preparedCellScores[i] = [];
        for (let j = 0; j < cellScores[i].length; j++) {
            preparedCellScores[i][j] = {
                number: cellScores[i][j],
                isA0Present: false,
                isA1Present: false,
                isB0Present: false,
                isB1Present: false,
                isAArea: false,
                isBArea: false,
                isATile: false,
                isBTile: false,
            };
        }
    }
    app.show(preparedCellScores);
    editCellAttrs(firstAgentsA[0][0], firstAgentsA[0][1], "a0-present", true);
    editCellAttrs(firstAgentsA[1][0], firstAgentsA[1][1], "a1-present", true);
    editCellAttrs(firstAgentsB[0][0], firstAgentsB[0][1], "b0-present", true);
    editCellAttrs(firstAgentsB[1][0], firstAgentsB[1][1], "b1-present", true);
}

function editCellAttrs(row, column, attr, value) {
    const editCell = app.cellScores[row][column];
    switch (attr) {
        case 'a-area':
            editCell.isAArea = value;
            break;
        case 'b-area':
            editCell.isBArea = value;
            break;
        case 'a-tile':
            editCell.isATile = value;
            break;
        case 'b-tile':
            editCell.isBTile = value;
            break;
        case 'a0-present':
            editCell.isA0Present = value;
            break;
        case 'a1-present':
            editCell.isA1Present = value;
            break;
        case 'b0-present':
            editCell.isB0Present = value;
            break;
        case 'b1-present':
            editCell.isB1Present = value;
            break;
    }
}

function updateCellAttrs(tileA, tileB, agents) {
    console.log(agents);
    for (let i = 0; i < tileA.length; i++) {
        for (let j = 0; j < tileA[i].length; j++) {
            editCellAttrs(i, j, 'a-tile', tileA[i][j] === 1);
        }
    }
    for (let i = 0; i < tileB.length; i++) {
        for (let j = 0; j < tileB[i].length; j++) {
            editCellAttrs(i, j, 'b-tile', tileB[i][j] === 1);
        }
    }

    for (let i = 0; i < app.cellScores.length; i++) {
        for (let j = 0; j < app.cellScores[i].length; j++) {
            app.cellScores[i][j].isA0Present = false;
            app.cellScores[i][j].isA1Present = false;
            app.cellScores[i][j].isB0Present = false;
            app.cellScores[i][j].isB1Present = false;
        }
    }
    for (let i = 0; i < 2; i++) {
        for (let j = 0; j < 2; j++) {
            console.log(agents[i][j][0], agents[i][j][1]);

            editCellAttrs(
                agents[i][j][0],
                agents[i][j][1],
                `${(i === 0 ? 'a' : 'b') + j}-present`,
                true
            );
        }
    }
}

function getCellScore(row, column) {
    return app.cellScores[row][column].number
}

function closeWindow() {
    window.close();
}

eel.expose(showBoard);
eel.expose(editCellAttrs);
eel.expose(getCellScore);
eel.expose(closeWindow);
eel.expose(updateCellAttrs);
