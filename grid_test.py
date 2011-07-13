#!/usr/bin/python

import unittest

from cards import PointCard, FaceDownCard
from decks import FakeDeck
from grid import Grid

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.deck = FakeDeck()
        self.grid = Grid(self.deck)
        
    def test_newGame_shuffles_deck(self):
        """ Ensures a new game shuffles the deck """
        # arrange
        # act
        self.grid.newGame()
        # assert
        self.assertTrue(self.deck.shuffle_called)
    
    def test_newGame_sets_point_cards(self):
        """ Ensures a new game has the point cards set correctly """
        # arrange
        # act
        self.grid.newGame()
        # assert
        for location in Grid.POINT_CARD_LOCATIONS:
            card = self.grid.card(location)
            self.assertTrue(isinstance(card, PointCard))
    
    def test_newGame_sets_face_down_cards(self):
        """ Ensures a new game has all non-point cards face-down """
        # arrange
        # act
        self.grid.newGame()
        # assert
        for i in range(Grid.GRID_SIZE):
            for j in range(Grid.GRID_SIZE):
                location = (i,j)
                if location not in Grid.POINT_CARD_LOCATIONS:
                    card = self.grid.card(location)
                    self.assertTrue(isinstance(card, FaceDownCard))
    
    # def test_nextCard
    
if __name__ == '__main__':
    unittest.main()
