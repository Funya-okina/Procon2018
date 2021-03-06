'use strict';

const app = new Vue({
    el: '#app',
    data: {
        isDisplaying: false,
        cellScores: [],
        boardRotate: 0,
        mouseoverCell: {
            row: null,
            column: null
        },
        options: {
            row: 12,
            column: 12,
            symmetry_v: true,
            symmetry_h: false,
            server_port: 25565,
            agent_row: 0,
            agent_column: 0,
            agent_symmetry_v: false,
            agent_symmetry_h: true,
            camera_id: 0,
        }
    },
    methods: {
        gameStart: function () {
            eel.gameStart();
        },

        genScores: function () {
            if (((this.options.symmetry_v == this.options.agent_symmetry_v)
                && !this.options.symmetry_h && !this.options.agent_symmetry_h)
                || ((this.options.symmetry_h == this.options.agent_symmetry_h)
                    && !this.options.symmetry_v && !this.options.agent_symmetry_v)) {
                alert("ルールに適合しない設定です．");
                exit();
            }

            let board_symmetry = 0;
            if (this.options.symmetry_v && this.options.symmetry_h) {
                board_symmetry = 2
            } else if (this.options.symmetry_v) {
                board_symmetry = 1
            } else if (this.options.symmetry_h) {
                board_symmetry = 0
            } else {
                alert("対称設定が行われていません");
                return;
            }

            let agent_cell = [];
            agent_cell[0] = [Number(this.options.agent_row), Number(this.options.agent_column)];
            if (this.options.agent_symmetry_v && this.options.agent_symmetry_h) {
                agent_cell[1] = [Number(this.options.row - this.options.agent_row - 1), Number(this.options.column - this.options.agent_column - 1)]
            } else if (this.options.agent_symmetry_v) {
                agent_cell[1] = [Number(this.options.row - this.options.agent_row - 1), Number(this.options.agent_column)]
            } else if (this.options.agent_symmetry_h) {
                agent_cell[1] = [Number(this.options.agent_row), Number(this.options.column - this.options.agent_column - 1)]
            } else {
                alert("対称設定が行われていません");
                exit();
            }
            eel.genScores(this.options.row, this.options.column, board_symmetry, agent_cell);
        },
        readQR: function () {
            eel.readQR(this.options.camera_id);
        },

        getBoardScores: function () {
            eel.getBoardScores();
        },

        encodeQR: function () {
            eel.encodeQR();
        },

        standby: function(){
            eel.standbyServer(this.options.server_port);
        },

        show: function (preparedCellScores) {
            this.cellScores = preparedCellScores;
            this.isDisplaying = true;
        },

        nextTurn: function () {
            document.getElementById("next-confirm").style.display="none";
            eel.nextTurn()
        },

        rejectTurn: function () {
            document.getElementById("next-confirm").style.display="none";
            eel.rejectTurn()
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

function setTurnConfirmView(state) {
    if(state == true){
        document.getElementById("next-confirm").style.display="block";
    }else{
        document.getElementById("next-confirm").style.display="none";
    }
}

eel.expose(showBoard);
eel.expose(editCellAttrs);
eel.expose(getCellScore);
eel.expose(closeWindow);
eel.expose(updateCellAttrs);
eel.expose(setTurnConfirmView);
