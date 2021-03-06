
from PyQt4 import QtCore

from decks import Deck
from cards import PointCard, FaceDownCard

class CardAlreadyFaceUpException(Exception):
    """ Exception raised when an attempt is made to turn a card face up that is already face up """
    pass

class Grid(QtCore.QObject):
    """
    """
    
    GRID_SIZE = 6
    POINT_CARD_LOCATIONS = [ (1,1), (4,4), (4,1), (1,4) ]
    
    cardChanged = QtCore.pyqtSignal(tuple)
    
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
    
    def turnCardFaceUp(self, location):
        """ Turns the card at location face up.  If it is already face up, throw an exception """
        if not isinstance(self.grid[location], FaceDownCard):
            raise CardAlreadyFaceUpException
        self.grid[location] = self.deck.nextCard()
        self.cardChanged.emit(location)
    
    @staticmethod
    def allGridLocations():
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
            self.cardChanged.emit(location)
    
    def _setFaceDownCards(self):
        for location in self.allGridLocations():
            self.grid[location] = FaceDownCard()
            self.cardChanged.emit(location)
    

