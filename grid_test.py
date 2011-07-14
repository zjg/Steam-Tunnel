#!/usr/bin/python

import nose

from cards import PointCard, FaceDownCard
from decks import FakeDeck
from grid import Grid, CardAlreadyFaceUpException

class TestGrid():
    def setUp(self):
        self.deck = FakeDeck()
        self.grid = Grid(self.deck)
        
        self.cardChanged_locations = []
        def cardChanged_spy(location):
            self.cardChanged_locations.append(location)
        self.grid.cardChanged.connect(cardChanged_spy)
        
        self.grid.newGame()
        
    def test_newGame_shuffles_deck(self):
        assert (self.deck.shuffle_called)
    
    def test_newGame_sets_point_cards(self):
        for location in Grid.POINT_CARD_LOCATIONS:
            yield (self.check_newGame_sets_point_cards, location)
    def check_newGame_sets_point_cards(self, location):
        card = self.grid.card(location)
        assert (isinstance(card, PointCard))
    
    def test_newGame_sets_face_down_cards(self):
        for location in Grid.allGridLocations():
            if location not in Grid.POINT_CARD_LOCATIONS:
                yield (self.check_newGame_sets_face_down_cards, location)
    def check_newGame_sets_face_down_cards(self, location):
        card = self.grid.card(location)
        assert (isinstance(card, FaceDownCard))
    
    def test_newGame_emits_cardChanged_signal_for_each_location(self):
        for location in Grid.allGridLocations():
            assert (location in self.cardChanged_locations)
    
    def test_turnCardFaceUp_draws_next_card_from_deck(self):
        location = (3,4)
        self.grid.turnCardFaceUp(location)
        grid_card = self.grid.card(location)
        assert (grid_card is self.deck.next_cards[-1])
    
    def test_turnCardFaceUp_emits_cardChanged_signal(self):
        location = (3,4)
        self.grid.turnCardFaceUp(location)
        emitted_location = self.cardChanged_locations[-1]
        assert (emitted_location == location)
    
    def test_turnCardFaceUp_throws_exception_on_point_card(self):
        nose.tools.assert_raises(CardAlreadyFaceUpException,
                                 self.grid.turnCardFaceUp,
                                 Grid.POINT_CARD_LOCATIONS[0])
    
    def test_turnCardFaceUp_throws_exception_on_already_face_up_card(self):
        self.grid.turnCardFaceUp((3,2))
        nose.tools.assert_raises(CardAlreadyFaceUpException,
                                 self.grid.turnCardFaceUp,
                                 Grid.POINT_CARD_LOCATIONS[0])
    
    # def test_nextCard
    
if __name__ == '__main__':
    nose.main()
