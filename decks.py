
import random
import copy

from PyQt4 import QtCore

from cards import Card, FakeCard

class DeckEmptyException(Exception):
    """ Exception thrown when an attempt is made to get the next card from an empty deck """
    pass

class Deck(QtCore.QObject):
    """
    """
    
    SHUFFLE_FLIP_PROBABILITY = 0.5
    
    def __init__(self):
        super(Deck, self).__init__()
        self.cards = []
        self.next_index = 0
    
    def shuffle(self):
        self.next_index = 0
        random.shuffle(self.cards)
        for card in self.cards:
            if random.random() <= Deck.SHUFFLE_FLIP_PROBABILITY:
                card.flip()
    
    def nextCard(self):
        if self.next_index >= len(self.cards):
            raise DeckEmptyException
        card = self.cards[self.next_index]
        self.next_index += 1
        return card

class DefaultDeck(Deck):
    """
    The default deck that is included in the original game.
    (does not include the point cards)
    """
    
    DEFAULT_CARD_ENDPOINTS = [
        [ [1,3], [2,5] ], [ [1,4], [3,5] ],                 # crisscross with 2 dead ends
        [ [0,1], [2,4], [3,5] ], [ [0,5], [1,3], [2,4] ],   # crisscross with no dead ends
        [ [0,5], [1,3] ], [ [0,1], [3,5] ],                 # corners with 2 dead ends
        [ [0,5], [1,4], [2,3] ], [ [0,1], [2,5], [3,4] ],   # corners with swerve in the middle
        [ [0,5], [1,2], [3,4] ],                            # corners with a U-turn
        [ [0,3], [1,5], [2,4] ],                            # 3 straights
        [ [0,1,5], [2,3,4] ]                                # tees
    ]
    
    def __init__(self):
        super(DefaultDeck, self).__init__()
        for card_endpoints in DefaultDeck.DEFAULT_CARD_ENDPOINTS:
            for i in range(4):
                self.cards.append(Card(card_endpoints))

class FakeDeck(Deck):
    def __init__(self):
        super(FakeDeck, self).__init__()
        self.shuffle_called = False
        self.next_cards = []
    
    def shuffle(self):
        self.shuffle_called = True
    
    def nextCard(self):
        self.next_cards.append(FakeCard())
        return self.next_cards[-1]
