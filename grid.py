
from PyQt4 import QtCore

from decks import Deck
from cards import PointCard, FaceDownCard

class Grid(QtCore.QObject):
    """
    """
    
    GRID_SIZE = 6
    POINT_CARD_LOCATIONS = [ (1,1), (4,4), (4,1), (1,4) ]
    
    # todo : signal for when a location's card has changed
    
    def __init__(self, deck):
        super(Grid, self).__init__()
        self.deck = deck
        self.grid = self._blankGrid()
    
    def newGame(self):
        """ Sets the grid to the new game state """
        self.deck.shuffle()
        self._setFaceDownCards()
        self._setPointCards()
    
    def card(self, location):
        """ Return the Card instance at the given location in the grid """
        return self.grid[location]
    
    def nextCard(self, location, exit_endpoint):
        """ Return the Card instance that is reached by leaving from exit_endpoint of the Card at location """
        return None
    
    def allGridLocations(self):
        for i in range(Grid.GRID_SIZE):
            for j in range(Grid.GRID_SIZE):
                yield (i,j)
        return
    
    def _blankGrid(self):
        blank_grid = {}
        for location in self.allGridLocations():
            blank_grid[location] = None
        return blank_grid
    
    def _setPointCards(self):
        for location in Grid.POINT_CARD_LOCATIONS:
            self.grid[location] = PointCard()
    
    def _setFaceDownCards(self):
        for location in self.allGridLocations():
            self.grid[location] = FaceDownCard()
    

