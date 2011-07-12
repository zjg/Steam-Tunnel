
import unittest

from decks import Deck, DefaultDeck
from cards import Card

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_shuffle_randomizes_card_order(self):
        # arrange
        sorted_cards = [0, 1, 2, 3, 4, 5]
        self.deck.cards = sorted_cards[:]
        # act
        self.deck.shuffle()
        # assert
        self.assertEqual(len(self.deck.cards), len(sorted_cards))
        self.assertNotEqual(self.deck.cards, sorted_cards)

class TestDefaultDeck(unittest.TestCase):
    def setUp(self):
        self.deck = DefaultDeck()
    
    def test_deck_is_correct_size(self):
        """ Ensure the deck contains 44 cards """
        # arrange
        # act
        # assert
        self.assertEqual(len(self.deck.cards), 44)
    
    def test_deck_contains_correct_cards(self):
        """ Ensure the deck contains at least one of each default card type """
        # arrange
        
        # act
        
        # assert
        pass

if __name__ == '__main__':
    unittest.main()
