#!/usr/bin/python

from PyQt4 import QtGui

from decks import DefaultDeck
from widgets import GridWidget
from grid import Grid

def main():
    app = QtGui.QApplication([])
    
    deck = DefaultDeck()
    grid = Grid(deck)
    
    grid.newGame()
    
    gw = GridWidget(None)
    gw.setGrid(grid)
    
    gw.resize(1000, 750)
    gw.show()
    
    app.exec_()


if __name__ == '__main__':
    main()

