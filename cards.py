
from PyQt4 import QtCore

class Card(QtCore.QObject):
    """
    
    Connections are numbered clockwise from the top of a vertical card:
            0
          5   1
          4   2
            3
    Initially, all connections are a simple dead end.
    
    """
    
    INVALID = [-1]
    DEAD_END = [-100]
    
    connectionsChanged = QtCore.pyqtSignal()
    
    def __init__(self, endpoint_connections = None):
        super(Card, self).__init__()
        self.connections = [self.DEAD_END] * 6
        self.point_values = [0] * 6
        
        if endpoint_connections is not None:
            for e in endpoint_connections: self.connectEndpoints(e)
    
    def connectEndpoints(self, endpoint_list):
        """ Connect the endpoints given in endpoint_list """
        endpoint_list.sort()
        for endpoint in endpoint_list:
            new_list = endpoint_list[:]
            new_list.remove(endpoint)
            self.connections[endpoint] = new_list
        self.connectionsChanged.emit()

    def flip(self):
        """ Flip the card 180 degrees, so that its top is now at its bottom """
        endpoint_mapping = [3, 4, 5, 0, 1, 2]
        new_connections = [self.INVALID] * 6
        
        # move the endpoint lists around to match the new order
        for i in range(6):
            new_connections[i] = self.connections[endpoint_mapping[i]]
        
        # change all the endpoint values to match the flipped values
        for connection in new_connections:
            for i in range(len(connection)):
                if connection[i] >= 0:
                    connection[i] = endpoint_mapping[connection[i]]
        
        self.connections = new_connections
        self.connectionsChanged.emit()

    def getConnectedEndpoints(self):
        """ Return a list of endpoint connections """
        groups = []
        for i in range(6):
            in_a_group = [True for group in groups if i in group]
            connected = (self.connections[i] != self.DEAD_END and
                         self.connections[i] != self.INVALID)
            if connected and not in_a_group:
                group = self.connections[i] + [i]
                group.sort()
                groups.append(group)
        
        return groups


class PointCard(Card):
    """
    Represents one of the point cards.
    """
    
    def __init__(self):
        super(PointCard, self).__init__()
        self.point_values = [ 4, 3, 2, 4, 3, 2 ]
