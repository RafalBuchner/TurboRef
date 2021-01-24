from PyQt5 import QtWidgets, QtGui, QtCore


SELECTION_COLOR = QtGui.QColor(0,240,100) ###SETTINGS
CORNER_SIZE = 12
STROKE_WIDTH = 3

def itemSelectionPaint(self, painter, option, index):
        if self.isSelected():

            boundingRect = self.boundingRect()
            pen = QtGui.QPen()
            pen.setWidth(STROKE_WIDTH / self.scene.view.getScale())
            pen.setColor(SELECTION_COLOR)
            painter.setPen(pen)
            painter.drawRect(boundingRect)
            painter.setPen(QtGui.QPen())

            cornerSize = CORNER_SIZE / self.scene.view.getScale()
            brush = QtGui.QBrush()
            brush.setColor(SELECTION_COLOR)
            brush.setStyle(QtCore.Qt.SolidPattern)
            painter.setBrush(brush)

            for point in ( boundingRect.topLeft(), 
                                    boundingRect.topRight(), 
                                    boundingRect.bottomLeft(), 
                                    boundingRect.bottomRight() 
                                    ):

                startingPoint = point-QtCore.QPoint(cornerSize/2, cornerSize/2)
                size = QtCore.QSize(cornerSize, cornerSize)
                cornerRect = QtCore.QRect(startingPoint.toPoint(), size)
                painter.drawRect(cornerRect)


            self.scene.update()

class TurboImageItem(QtWidgets.QGraphicsPixmapItem):
    """docstring for TurboImageItem"""
    def __init__(self, path, position, scene):
        # pixmap = pixmap.scaled(QtCore.QSize(1000, 1000))
        self.scene = scene
        self.path = path
        pixmap = QtGui.QPixmap(path)
        super().__init__(pixmap)
        self.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.setPos(*position)
        self.setFlags(
            self.flags() | QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable
        )
        self.setAcceptHoverEvents(True)
    
    def __repr__(self):
        return f"< TurboImageItem - {self.path} >"

    def hoverEnterEvent(self, event):
        self.scene.sceneItemHover(True)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.scene.sceneItemHover(False)
        super().hoverEnterEvent(event)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        itemSelectionPaint(self, painter, option, index)
   



        
class TurboTextItem(QtWidgets.QGraphicsTextItem):
    """docstring for TurboTextItem"""
    def __init__(self, text, font, position, scene):
        self.scene = scene
        # pixmap = pixmap.scaled(QtCore.QSize(1000, 1000))
        super().__init__(text)
        self.setFont(font)
        self.setPos(*position)
        self.setFlags(
            self.flags() | QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable
        )
        self.setAcceptHoverEvents(True)

    def __repr__(self):
        return f"< TurboImageItem - {self.toPlainText()} >"

    def hoverEnterEvent(self, event):
        self.scene.sceneItemHover(True)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.scene.sceneItemHover(False)
        super().hoverEnterEvent(event)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        itemSelectionPaint(self, painter, option, index)

        
