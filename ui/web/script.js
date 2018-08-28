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
      symmetry_v: false,
      symmetry_h: true
    }
  },
  methods: {
    checkSymmetryOption: function() {
      if (this.options.symmetry_v && this.options.symmetry_h) {
        return 2;
      } else if (this.options.symmetry_v) {
        return 1;
      } else if(this.options.symmetry_h) {
        return 0;
      } else {
        return null
      }
    },

    areGeneratableOptions: function() {
      return this.options.row !== ""
        && this.options.column !== ""
        && this.checkSymmetryOption() !== null
    },

    gameStart: function() {
      eel.gameStart(this.options.row, this.options.column, this.checkSymmetryOption());
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



function showBoard(cellScores) {
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
