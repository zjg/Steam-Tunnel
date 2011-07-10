
import unittest

from tunnel_cards import Card

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card()
        
        self.connectionsChanged_count = 0
        def connectionsChanged_spy():
            self.connectionsChanged_count += 1
        self.card.connectionsChanged.connect(connectionsChanged_spy)
    
    def test_defaults(self):
        """ The card initially consists of dead ends """
        for i in range(6):
            self.assertEqual(self.card.connections[i], Card.DEAD_END)
    
    def test_connectEndpoints_emits_signal(self):
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
        expConnections = self.card.connections[:]
        expConnections[2] = [3, 4]
        expConnections[3] = [2, 4]
        expConnections[4] = [2, 3]
        # act
        self.card.connectEndpoints(endpoints)
        # assert
        self.assertEqual(self.card.connections, expConnections)
    
    def test_flip_emits_signal(self):
        # arrange
        # act
        self.card.flip()
        # assert
        self.assertEqual(self.connectionsChanged_count, 1)
    
    def test_flip_maintains_connections(self):
        """ When a card is flipped, connections are maintained correctly """
        # arrange
        self.card.connections = [[4], [5], [3], [2], [0], [1]]
        expConnections = [[5], [3], [4], [1], [2], [0]]
        # act
        self.card.flip()
        # assert
        self.assertEqual(self.card.connections, expConnections)
    
if __name__ == '__main__':
    unittest.main()
