from PyQt5 import QtWidgets, QtGui, QtCore

class TurboImageItem(QtWidgets.QGraphicsPixmapItem):
    """docstring for TurboImageItem"""
    def __init__(self, pixmap, position):
        # pixmap = pixmap.scaled(QtCore.QSize(1000, 1000))
        super().__init__(pixmap)
        self.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.setPos(*position)
        self.setFlags(
            self.flags() | QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable
        )


        
class TurboTextItem(QtWidgets.QGraphicsTextItem):
    """docstring for TurboImageItem"""
    def __init__(self, text, font, position):
        # pixmap = pixmap.scaled(QtCore.QSize(1000, 1000))
        super().__init__(text)
        self.setFont(font)
        self.setPos(*position)
        self.setFlags(
            self.flags() | QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable
        )



        
