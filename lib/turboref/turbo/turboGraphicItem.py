from PyQt5 import QtWidgets, QtGui, QtCore

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
   

        
