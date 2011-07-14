
from PyQt4 import QtGui, QtCore

from grid import Grid

class CardWidget(QtGui.QWidget):
    
    doubleClicked = QtCore.pyqtSignal()
    
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
        self._updateEndpointCoordinates()
    
    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
    
    def _updateEndpointCoordinates(self):
        size = self.size()
        width = size.width()
        height = size.height()
        half_height = height / 2
        third_width = width / 3
        
        self.endpoint_coords = [(width, half_height), (2 * third_width, height),
                                (third_width, height), (0, half_height),
                                (third_width, 0), (2 * third_width, 0)
                               ]

class GridWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(GridWidget, self).__init__(parent)
        self.grid = None
        self.widgets_to_locations = {}
        self.locations_to_widgets = {}
        
        self.signal_mapper = QtCore.QSignalMapper(self)
        self.connect(self.signal_mapper, QtCore.SIGNAL('mapped(QWidget*)'),
                     self._handleWidgetDoubleClicked)
    
    def setGrid(self, grid):
        if self.grid is not None:
            self.grid.cardChanged.disconnect(self._handleGridCardChanged)
        self.grid = grid
        if self.grid is not None:
            self.grid.cardChanged.connect(self._handleGridCardChanged)
            self._updateWidgets()
    
    def _updateWidgets(self):
        self._unmapWidgetSignals()
        self._createWidgetsFromGrid()
        self._mapWidgetSignals()
    
    def _mapWidgetSignals(self):
        for widget in self._widgets():
            self.signal_mapper.setMapping(widget, widget)
            widget.doubleClicked.connect(self.signal_mapper.map)
    
    def _unmapWidgetSignals(self):
        for widget in self._widgets():
            widget.doubleClicked.disconnect(self.signal_mapper.map)
            self.signal_mapper.removeMappings(widget)
    
    def _createWidgetsFromGrid(self):
        layout = QtGui.QGridLayout(self)
        for location in Grid.allGridLocations():
            card_widget = CardWidget(self)
            card_widget.setCard(self.grid.card(location))
            layout.addWidget(card_widget, location[1], location[0])
            self._linkWidgetAndLocation(card_widget, location)
    
    def _linkWidgetAndLocation(self, widget, location):
        self.widgets_to_locations[widget] = location
        self.locations_to_widgets[location] = widget
    
    def _widgets(self):
        for widget in self.widgets_to_locations.keys():
            yield widget
    
    def _handleGridCardChanged(self, location):
        widget = self.locations_to_widgets[location]
        widget.setCard(self.grid.card(location))
    
    def _handleWidgetDoubleClicked(self, widget):
        location = self.widgets_to_locations[widget]
        self.grid.turnCardFaceUp(location)
    
