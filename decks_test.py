#!/usr/bin/python

import unittest

from decks import Deck, DefaultDeck, DeckEmptyException
from cards import Card, FakeCard

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.fake_cards = [ FakeCard(), FakeCard(), FakeCard() ]
        self.deck.cards = self.fake_cards[:]

    def test_shuffle_randomizes_card_order(self):
        # arrange
        sorted_cards = []
        for i in xrange(10000):
            sorted_cards.append(FakeCard())
        self.deck.cards = sorted_cards[:]
        # act
        self.deck.shuffle()
        # assert
        self.assertEqual(len(self.deck.cards), len(sorted_cards))
        self.assertNotEqual(self.deck.cards, sorted_cards)
    
    def test_shuffle_flips_cards(self):
        # arrange
        Deck.SHUFFLE_FLIP_PROBABILITY = 1.0
        # act
        self.deck.shuffle()
        # assert
        for card in self.fake_cards:
            self.assertTrue(card.flip_called)
    
    def test_nextCard_returns_cards_in_correct_order(self):
        # arrange
        next_cards = []
        # act
        for i in range(len(self.fake_cards)):
            next_cards.append(self.deck.nextCard())
        # assert
        self.assertEqual(next_cards, self.fake_cards)

    def test_nextCard_throws_exception_when_deck_empty(self):
        # arrange
        try:
            # act
            for i in range(len(self.fake_cards) + 1):
                self.deck.nextCard()
        except DeckEmptyException:
            pass

class TestDefaultDeck(unittest.TestCase):
    def setUp(self):
        self.deck = DefaultDeck()
    
    def test_deck_is_correct_size(self):
        """ Ensure the deck contains 44 cards """
        self.assertEqual(len(self.deck.cards), 44)
    
    def test_deck_contains_correct_cards(self):
        """ Ensure the deck contains four of each default card type """
        card_type_counts = {}
        for card_type in DefaultDeck.DEFAULT_CARD_ENDPOINTS:
            card_type_counts[str(card_type)] = 0
        
        for card in self.deck.cards:
            card_type_counts[str(card.getConnectedEndpoints())] += 1
        
        for card_type in card_type_counts.keys():
            self.assertEqual(card_type_counts[card_type], 4)

if __name__ == '__main__':
    unittest.main()
