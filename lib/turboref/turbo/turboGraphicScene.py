from PyQt5 import QtWidgets, QtGui, QtCore
from turbo.turboGraphicItem import TurboImageItem, TurboTextItem
from turbo.turboSettingsParser import TurboSettingsParser, colorFloatsToRGBA
from copy import deepcopy
SETTINGS = TurboSettingsParser() # most of the settings will be defined in the turbo files, those should be used as a fallback

class TurboGraphicScene(QtWidgets.QGraphicsScene):
    
    scrollMargin = SETTINGS.getSetting('scrollMargin')
    
    def __init__(self, rect, parent, backgroundColor=None):
        sceneRect = deepcopy(rect)
        rect.setWidth(self.scrollMargin + rect.width())
        rect.setHeight(self.scrollMargin + rect.height())
        super().__init__( rect, parent)
        self.imageItemsDict = {}
        self.textItemsDict = {}
        self.isCursorHovering = False

        if backgroundColor is None:
            # fallback
            self._backgroundColor = SETTINGS.getSetting('backgroundColor')
        else:
            # setting from the file
            self._backgroundColor = backgroundColor
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30.5, 30.5, 30.5))) # background color
        # rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(0, 0, 100, 100))
        # rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

        sceneRect.setX(sceneRect.x() + self.scrollMargin)
        sceneRect.setY(sceneRect.y() + self.scrollMargin)

        self.addRect(sceneRect, brush=QtGui.QBrush(QtGui.QColor(30.5, 10.5, 30.5))) 
        ## test
        image_path = '/Users/workstatiWorkstationon/Dropbox/game-art-stuff/anatomy/face-ref/skull/EuropeanSkull-2.jpg'
        self.addImageItem(image_path, (100,100))
        self.addTextItem("Nogi", (100,100))


    def setView(self, view):
        self.view = view

    def setCanvasSize(self, w, h):
        pass

    def getBackgroundColor(self):
        return self._backgroundColor


    def addTextItem(self, text, position, fontProperties=None):
        """
        -   adds text item to the scene,
        -   adds text item to TurboGraphicScene.textItemsDict directory, where
            > key is an index and text parameter wrapped together as a tuple
            > the value is text Item itself
            TurboGraphicScene.textItemsDict[(textIndex, text)] = txtItem

        """
        font = QtGui.QFont()
        if fontProperties is None:
            font.setPointSize(5000)
        x,y = position
        x += self.scrollMargin
        y += self.scrollMargin
        txtItem = TurboTextItem(text, font, (x, y), self)
        
        textIndex = len(list(self.textItemsDict.keys()))
        self.textItemsDict[(textIndex, text)] = txtItem
        self.addItem(txtItem)

    def sceneItemHover(self, isHovering):
        self.isCursorHovering = isHovering

    def addImageItem(self, image_path, position):
        """
        -   adds image item to the scene,
        -   adds image item to TurboGraphicScene.imageItemsDict directory, where
            > key is an index and image parameter wrapped together as a tuple
            > the value is an image Item itself
            TurboGraphicScene.imageItemsDict[(imageIndex, image)] = imgItem

        """

        
        x,y = position
        x += self.scrollMargin
        y += self.scrollMargin
        imgItem = TurboImageItem(image_path, (x, y), self)
        
        imageIndex = len(list(self.imageItemsDict.keys()))
        self.imageItemsDict[(imageIndex, image_path)] = [imgItem]
        self.addItem(imgItem)

    # -------------------------------------------
    # events
    # -------------------------------------------

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
