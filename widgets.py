
from PyQt4 import QtGui

class CardWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(CardWidget, self).__init__(parent)
        self.card = None
        self.endpoint_coords = [(0, 0)] * 6
    
    def setCard(self, card):
        if self.card is not None:
            self.card.connectionsChanged.disconnect(self.update)
        if card is not None:
            card.connectionsChanged.connect(self.update)
        self.card = card
        self.update()
    
    def paintEvent(self, event):
        if self.card is None:
            return
        
        painter = QtGui.QPainter()
        painter.begin(self)
        
        for i in range(6):
            for endpoint in self.card.connections[i]:
                if endpoint >= 0:
                    start = self.endpoint_coords[i]
                    end = self.endpoint_coords[endpoint]
                    painter.drawLine(start[0], start[1], end[0], end[1])
        
        painter.end()
    
    def resizeEvent(self, event):
        self.updateEndpointCoordinates()
    
    def updateEndpointCoordinates(self):
        size = self.size()
        width = size.width()
        height = size.height()
        half_height = height / 2
        third_width = width / 3
        
        self.endpoint_coords[0] = (width, half_height)
        self.endpoint_coords[1] = (2 * third_width, height)
        self.endpoint_coords[2] = (third_width, height)
        self.endpoint_coords[3] = (0, half_height)
        self.endpoint_coords[4] = (third_width, 0)
        self.endpoint_coords[5] = (2 * third_width, 0)
