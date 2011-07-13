#!/usr/bin/python

import unittest

from cards import Card, PointCard, FaceDownCard

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card()
        
        self.connectionsChanged_count = 0
        def connectionsChanged_spy():
            self.connectionsChanged_count += 1
        self.card.connectionsChanged.connect(connectionsChanged_spy)
    
    def test_defaults(self):
        """ The card initially consists of dead ends with no point value """
        for i in range(6):
            self.assertEqual(self.card.connections[i], Card.DEAD_END)
            self.assertEqual(self.card.point_values[i], 0)
    
    def test_constructor_with_endpoint_list(self):
        """ You can pass in a list of endpoint connections to the constructor """
        # arrange
        endpoint_connections = [ [0, 1], [3, 4, 5] ]
        # act
        self.card = Card(endpoint_connections)
        # assert
        self.assertEqual(self.card.getConnectedEndpoints(), endpoint_connections)
    
    def test_connectEndpoints_emits_signal(self):
        """ connectionsChanged signal should be emitted every time connectEndpoints() is called """
        # arrange
        # act
        self.card.connectEndpoints([0])
        # assert
        self.assertEqual(self.connectionsChanged_count, 1)
    
    def test_basic_connectEndpoints_is_symmetric(self):
        """ When a basic straight connection is made, both endpoints point to one another """
        # arrange
        source = 3
        target = 4
        # act
        self.card.connectEndpoints([source, target])
        # assert
        self.assertEqual(self.card.connections[source], [target])
        self.assertEqual(self.card.connections[target], [source])
    
    def test_multiple_connectEndpoints_is_symmetric(self):
        """ When a non-straight connection is made, all involved endpoints point to all other involved endpoints """
        # arrange
        endpoints = [2, 4, 3]
        exp_connections = self.card.connections[:]
        exp_connections[2] = [3, 4]
        exp_connections[3] = [2, 4]
        exp_connections[4] = [2, 3]
        # act
        self.card.connectEndpoints(endpoints)
        # assert
        self.assertEqual(self.card.connections, exp_connections)
    
    def test_flip_emits_signal(self):
        """ connectionsChanged signal should be emitted every time flip() is called """
        # arrange
        # act
        self.card.flip()
        # assert
        self.assertEqual(self.connectionsChanged_count, 1)
    
    def test_flip_maintains_connections(self):
        """ When a card is flipped, connections are maintained correctly """
        # arrange
        self.card.connections = [[4], [5], [3], [2], [0], [1]]
        exp_connections = [[5], [3], [4], [1], [2], [0]]
        # act
        self.card.flip()
        # assert
        self.assertEqual(self.card.connections, exp_connections)
    
    def test_getConnectedEndpoints(self):
        """ getConnectedEndpoints() should return a list of endpoint groupings """
        # arrange
        exp_endpoint_connections = [ [0, 1], [3, 4, 5] ]
        for connection in exp_endpoint_connections:
            self.card.connectEndpoints(connection)
        # act
        endpoint_connections = self.card.getConnectedEndpoints()
        # assert
        self.assertEqual(endpoint_connections, exp_endpoint_connections)
    
    def test_eq_with_non_card_object(self):
        """ Ensure that the equality operator returns false for non-card objects """
        # arrange
        non_card = 3
        # act
        equal = (self.card == non_card)
        # assert
        self.assertFalse(equal)
    
    def test_eq_with_identical_cards(self):
        """ Ensure that cards which are the same evaluate as equal """
        # arrange
        endpoints = [ [0, 1], [2, 5] ]
        self.card = Card(endpoints)
        card2 = Card(endpoints)
        # act
        equal = (self.card == card2)
        # assert
        self.assertTrue(equal)
    
    def test_ne_with_non_card_object(self):
        """ Ensure that the inequality operator returns true for non-card objects """
        # arrange
        non_card = 3
        # act
        not_equal = (self.card != non_card)
        # assert
        self.assertTrue(not_equal)
    
    def test_ne_with_identical_cards(self):
        """ Ensure that cards which are the same evaluate as equal """
        # arrange
        endpoints = [ [0, 1], [2, 5] ]
        self.card = Card(endpoints)
        card2 = Card(endpoints)
        # act
        not_equal = (self.card != card2)
        # assert
        self.assertFalse(not_equal)
    
class TestPointCard(unittest.TestCase):
    def setUp(self):
        self.card = PointCard()
    
    def test_all_connections_are_dead_ends(self):
        """ All connections should be dead ends """
        for i in range(6):
            self.assertEqual(self.card.connections[i], Card.DEAD_END)
    
    def test_point_values_are_correct(self):
        """ Ensure all the point values are set correctly """
        values = [ 4, 3, 2, 4, 3, 2 ]
        self.assertEqual(self.card.point_values, values)

class TestFaceDownCard(unittest.TestCase):
    def setUp(self):
        self.card = FaceDownCard()
    
    def test_all_connections_are_straight_through(self):
        """ All connections should be straight through to the other side of the card """
        exp_connections = [ [0,3], [1,5], [2,4] ]
        self.assertEqual(self.card.getConnectedEndpoints(), exp_connections)

if __name__ == '__main__':
    unittest.main()
