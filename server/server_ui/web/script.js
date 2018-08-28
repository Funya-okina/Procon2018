'use strict';

const app = new Vue({
  el: '#app',
  data: {
    isDisplaying: false,
    cellScores: [],
    mouseoverCell: {
      row: null,
      column: null
    },
    options: {
      row: 12,
      column: 12,
      symmetry_v: true,
      symmetry_h: false,
      player_A_port: "25565",
      player_B_port: "25566",
      agent_row: 0,
      agent_column: 0,
      agent_symmetry_v: true,
      agent_symmetry_h: false,
      camera_id: 0,
    }
  },
  methods: {
    gameStart: function() {
    },
      
    genScores: function(){
      if(((this.options.symmetry_v == this.options.agent_symmetry_v)
          && !this.options.symmetry_h && !this.options.agent_symmetry_h)
            || ((this.options.symmetry_h == this.options.agent_symmetry_h)
              && !this.options.symmetry_v && !this.options.agent_symmetry_v)){
        alert("ルールに適合しない設定です．");
        exit();
      }

      let board_symmetry = 0;
      if(this.options.symmetry_v && this.options.symmetry_h){
        board_symmetry = 2
      }else if(this.options.symmetry_v){
        board_symmetry = 1
      }else if(this.options.symmetry_h){
        board_symmetry = 0
      }else{
        alert("対称設定が行われていません");
        exit();
      }

      let agent_cell = [];
      agent_cell[0] = [Number(this.options.agent_row), Number(this.options.agent_column)];
      if(this.options.agent_symmetry_v && this.options.agent_symmetry_h){
          agent_cell[1] = [Number(this.options.row-this.options.agent_row-1), Number(this.options.column-this.options.agent_column-1)]
      }else if(this.options.agent_symmetry_v){
          agent_cell[1] = [Number(this.options.row-this.options.agent_row-1), Number(this.options.agent_column)]
      }else if(this.options.agent_symmetry_h){
          agent_cell[1] = [Number(this.options.agent_row), Number(this.options.column-this.options.agent_column-1)]
      }else{
        alert("対称設定が行われていません");
        exit();
      }
      eel.genScores(this.options.row, this.options.column, board_symmetry, agent_cell);
    },
    readQR: function(){
      eel.readQR(this.options.camera_id);
    },

    show: function(preparedCellScores) {
      this.cellScores = preparedCellScores;
      this.isDisplaying = true;
    },

    cellClicked: function(row, column) {
      eel.cellClicked(row, column);
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

    isMouseoverCell: function(row, column) {
      return this.mouseoverCell.row === row 
        && this.mouseoverCell.column === column
        && row !== null
        && column !== null;
    },

    isMouseoverRelatedCell: function(row, column) {
      return !this.isMouseoverCell(row, column)
        && ((this.mouseoverCell.row === row && row !== null)
              || (this.mouseoverCell.column === column && column !== null)
          );
    }

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
  editCellAttrs(firstAgentsA[0][0], firstAgentsA[0][1], "a-tile", true);
  editCellAttrs(firstAgentsA[1][0], firstAgentsA[1][1], "a-tile", true);
  editCellAttrs(firstAgentsB[0][0], firstAgentsB[0][1], "b-tile", true);
  editCellAttrs(firstAgentsB[1][0], firstAgentsB[1][1], "b-tile", true);
}

function editCellAttrs(row, column, attr, value) {
  const editCell = app.cellScores[row][column];
  switch (attr) {
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

