#!/usr/bin/python

import nose

from cards import PointCard, FaceDownCard
from decks import FakeDeck
from grid import Grid

class TestGrid():
    def setUp(self):
        self.deck = FakeDeck()
        self.grid = Grid(self.deck)
        
        self.cardChanged_locations = []
        def cardChanged_spy(location):
            self.cardChanged_locations.append(location)
        self.grid.cardChanged.connect(cardChanged_spy)
        
    def test_newGame_shuffles_deck(self):
        self.grid.newGame()
        assert (self.deck.shuffle_called)
    
    def test_newGame_sets_point_cards(self):
        for location in Grid.POINT_CARD_LOCATIONS:
            yield (self.check_newGame_sets_point_cards, location)
    def check_newGame_sets_point_cards(self, location):
        self.grid.newGame()
        card = self.grid.card(location)
        assert (isinstance(card, PointCard))
    
    def test_newGame_sets_face_down_cards(self):
        for location in Grid.allGridLocations():
            if location not in Grid.POINT_CARD_LOCATIONS:
                yield (self.check_newGame_sets_face_down_cards, location)
    def check_newGame_sets_face_down_cards(self, location):
        self.grid.newGame()
        card = self.grid.card(location)
        assert (isinstance(card, FaceDownCard))
    
    def test_newGame_emits_cardChanged_signal_for_each_location(self):
        self.grid.newGame()
        for location in Grid.allGridLocations():
            assert (location in self.cardChanged_locations)
    
    # def test_nextCard
    
if __name__ == '__main__':
    nose.main()
