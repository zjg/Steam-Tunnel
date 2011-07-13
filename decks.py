
import random
import copy

from PyQt4 import QtCore

from cards import Card

class Deck(QtCore.QObject):
    """
    """
    
    def __init__(self):
        super(Deck, self).__init__()
        self.cards = []
    
    def shuffle(self):
        random.shuffle(self.cards)

class DefaultDeck(Deck):
    """
    The default deck that is included in the original game.
    (does not include the point cards)
    """
    
    DEFAULT_CARDS = [
        Card([ [1,3], [2,5] ]), Card([ [1,4], [3,5] ]),                 # crisscross with 2 dead ends
        Card([ [0,1], [2,4], [3,5] ]), Card([ [0,5], [1,3], [2,4] ]),   # crisscross with no dead ends
        Card([ [0,5], [1,3] ]), Card([ [0,1], [3,5] ]),                 # corners with 2 dead ends
        Card([ [0,5], [1,4], [2,3] ]), Card([ [0,1], [2,5], [3,4] ]),   # corners with swerve in the middle
        Card([ [0,5], [1,2], [3,4] ]),                                  # corners with a U-turn
        Card([ [0,3], [1,5], [2,4] ]),                                  # 3 straights
        Card([ [0,1,5], [2,3,4] ])                                      # tees
    ]
    
    def __init__(self):
        super(DefaultDeck, self).__init__()
        self.cards = [Card()] * 44



class FakeDeck(Deck):
    def __init__(self):
        super(FakeDeck, self).__init__()
        self.shuffle_called = False
    
    def shuffle(self):
        self.shuffle_called = True
