
from PyQt5.QtCore import QEvent, QPoint, QPointF, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QPainter
from PyQt5.QtWidgets import QPinchGesture, QScrollArea, QGraphicsView, QSizePolicy, QWidget
import sys

"""
widget based on 
https://github.com/trufont/trufont/blob/master/Lib/defconQt/controls/glyphView.py

todo:
- implement fitScaleBBox method, for selected Bounding Box
"""

def scaleModifier():
    if sys.platform == "darwin":
        return Qt.AltModifier
    return Qt.ControlModifier

class TurboWidget(QWidget):
    canvasScaleModified = pyqtSignal(int)

    def __init__(self,  parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # drawing data cache
        self._drawingRect = None
        self._scale = 1.0
        self._inverseScale = 0.1
        self._impliedPointSize = 1000

        # drawing calculation
        self._noPointSizePadding = 200
        self._verticalCenterYBuffer = 0

        self._backgroundColor = Qt.white

        self._scrollArea = None

    # --------------
    # Custom Methods
    # --------------

    def drawingRect(self):
        return self._drawingRect

    def inverseScale(self):
        return self._inverseScale

    def scale(self):
        return self._scale

    def setScale(self, scale):
        self._scale = scale
        if self._scale <= 0:
            self._scale = 0.01
        self._inverseScale = 1.0 / self._scale
        self.adjustSize()

    def scrollArea(self):
        return self._scrollArea

    def setScrollArea(self, scrollArea):
        scrollArea.setWidget(self)
        self._scrollArea = scrollArea
    # fitting

    def centerOn(self, pos):
        """
        Centers this widget’s *scrollArea* on QPointF_ *pos*.
        .. _QPointF: http://doc.qt.io/qt-5/qpointf.html
        """
        scrollArea = self._scrollArea
        if scrollArea is None:
            return
        hSB = scrollArea.horizontalScrollBar()
        vSB = scrollArea.verticalScrollBar()
        viewport = scrollArea.viewport()
        hValue = hSB.minimum() + hSB.maximum() - (pos.x() - viewport.width() / 2)
        hSB.setValue(hValue)
        vSB.setValue(pos.y() - viewport.height() / 2)


    def _calculateDrawingRect(self):
        # calculate and store the drawing rect
        # TODO: we only need the width here
        glyphWidth = self._getGlyphWidthHeight()[0] * self._scale
        diff = self.width() - glyphWidth
        xOffset = round((diff / 2) * self._inverseScale)

        yOffset = self._verticalCenterYBuffer * self._inverseScale
        yOffset -= self._descender

        w = self.width() * self._inverseScale
        h = self.height() * self._inverseScale
        self._drawingRect = (-xOffset, -yOffset, w, h)


    def zoom(self, step, anchor="center"):
        """
        Zooms the view by *step* increments (with a scale factor of
        1.2^*step*), anchored to *anchor*:
        - QPoint_: center on that point
        - "cursor": center on the mouse cursor position
        - "center": center on the viewport
        - None: don’t anchor, i.e. stick to the viewport’s top-left.
        # TODO: improve docs from QGraphicsView descriptions.
        The default is "center".
        .. _QPoint: http://doc.qt.io/qt-5/qpoint.html
        """
        oldScale = self._scale
        newScale = self._scale * pow(1.2, step)
        scrollArea = self._scrollArea
        if newScale < 1e-2 or newScale > 1e3:
            return
        if scrollArea is not None:
            # compute new scrollbar position
            # http://stackoverflow.com/a/32269574/2037879
            hSB = scrollArea.horizontalScrollBar()
            vSB = scrollArea.verticalScrollBar()
            viewport = scrollArea.viewport()
            if isinstance(anchor, QPoint):
                pos = anchor
            elif anchor == "cursor":
                pos = self.mapFromGlobal(QCursor.pos())
            elif anchor == "center":
                pos = self.mapFromParent(
                    QPoint(viewport.width() / 2, viewport.height() / 2)
                )
            else:
                raise ValueError(f"invalid anchor value: {anchor}")
            scrollBarPos = QPointF(hSB.value(), vSB.value())
            deltaToPos = pos / oldScale
            delta = deltaToPos * (newScale - oldScale)
        self.setScale(newScale)
        self.update()
        if scrollArea is not None:
            hSB.setValue(scrollBarPos.x() + delta.x())
            vSB.setValue(scrollBarPos.y() + delta.y())

    # position mapping

    def mapFromCanvas(self, pos):
        """
        Maps *pos* from image canvas to this widget’s coordinates.
        Note that canvas coordinates are scale-independent while widget
        coordinates are not.
        """
        if self._drawingRect is None:
            self._calculateDrawingRect()
        xOffsetInv, yOffsetInv, _, _ = self._drawingRect
        x = (pos.x() - xOffsetInv) * self._scale
        y = (pos.y() - yOffsetInv) * (-self._scale) + self.height()
        return pos.__class__(x, y)

    def mapToCanvas(self, pos):
        """
        Maps *pos* from this widget’s to image canvas coordinates.
        Note that canvas coordinates are scale-independent while widget
        coordinates are not.
        """
        if self._drawingRect is None:
            self._calculateDrawingRect()
        xOffsetInv, yOffsetInv, _, _ = self._drawingRect
        x = pos.x() * self._inverseScale + xOffsetInv
        y = (pos.y() - self.height()) * (-self._inverseScale) + yOffsetInv
        return pos.__class__(x, y)

    def mapRectFromCanvas(self, rect):
        x, y, w, h = rect.getRect()
        origin = self.mapFromCanvas(QPointF(x, y))
        w *= self._scale
        h *= self._scale
        return rect.__class__(origin.x(), origin.y() - h, w, h)

    def mapRectToCanvas(self, rect):
        x, y, w, h = rect.getRect()
        origin = self.mapToCanvas(QPointF(x, y))
        w *= self._inverseScale
        h *= self._inverseScale
        return rect.__class__(origin.x(), origin.y() - h, w, h)

    def wheelEvent(self, event):
        print("wheelEvent<widget")
        if event.modifiers() & scaleModifier():
            print("should zoom")
            step = event.angleDelta().y() / 120.0
            self.zoom(step, event.pos())
            self.canvasScaleModified.emit(self._scale)
            event.accept()
        else:
            super().wheelEvent(event)

# class TurboView(QScrollArea):
class TurboView(QGraphicsView):
    turboWidgetClass = TurboWidget

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grabGesture(Qt.PinchGesture)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.setWidgetResizable(True)

        self._turboWidget = self.turboWidgetClass(self)
        # self._turboWidget.setScrollArea(self)

        # self.pointSizeModified = self._turboWidget.pointSizeModified

    # -------------
    # Public Methods
    # -------------

    def scale(self):
        return self._turboWidget.scale()

    def setScale(self, pointSize):
        self._turboWidget.setScale(pointSize)

    def setImage(self, image):
        NotImplemented

    def fitScaleBBox(self):
        self._turboWidget.fitScaleBBox()

    def zoom(self, factor, anchor="center"):
        self._turboWidget.zoom(factor, anchor=anchor)

    # convenience

    def showGrid(self):
        # return self.drawingAttribute("showGrid")
        NotImplemented

    def backgroundColor(self):
        return self._turboWidget.backgroundColor()

    def setBackgroundColor(self, color):
        self._turboWidget.setBackgroundColor(color)

    def wheelEvent(self, event):
        print("wheelEvent<view")
        self._turboWidget.wheelEvent(event)




