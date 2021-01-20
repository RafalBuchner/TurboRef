import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5 import QtWidgets
from PyQt5.QtGui import *

from PyQt5.QtWidgets import *


class ScrollArea(QWidget):

    _style = '''
            QScrollArea{
                background: white;
            }
            
            QScrollBar:handle{
                background: gray;
                max-width: 20px;
                color:green;
            
            }
            '''

    factor = 1.5

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__()

        self.v_layout = QVBoxLayout(self)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.setSpacing(0)

        self.container_widget = QWidget()

        # Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(False)
        self.scroll.setWidget(self.container_widget)
        self.scroll.setStyleSheet(ScrollArea._style)

        # l = QLabel('Hello world', self.container_widget)
        # l.setStyleSheet('color: red; font-size: 30px')

        # lame zooming
        self.label = QLabel('Hello world', self.container_widget)
        self.font_size = 30
        self.label.setStyleSheet(f'color: red; font-size: {self.font_size}px')
      
        self.container_widget.setGeometry(0, 0, self.width(), self.height())


        self.v_layout.addWidget(self.scroll)
        self.setLayout(self.v_layout)

        self._zoom = 0
        self.mousepos = QPoint(0, 0)
        self.setMouseTracking(True)
        self.showMaximized()

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def wheelEvent(self, wheel_event):

        if wheel_event.modifiers() == Qt.ControlModifier:
            delta = wheel_event.angleDelta().y()
            if delta > 0:
                self.zoom_in()

            elif delta < 0:
                self.zoom_out()

        else:
            return super().wheelEvent(wheel_event)

    def mousePressEvent(self, event):
        cursor = self.container_widget.cursor().pos()
        print(cursor)
        if event.button() == Qt.MidButton:
            self.setCursor(Qt.OpenHandCursor)
            self.mousepos = event.localPos() # <== add this

        super(ScrollArea, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):

        delta = event.localPos() - self.mousepos

        # panning area
        if event.buttons() == Qt.MidButton:
            h = self.scroll.horizontalScrollBar().value()
            v = self.scroll.verticalScrollBar().value()

            self.scroll.horizontalScrollBar().setValue(int(h - delta.x()))
            self.scroll.verticalScrollBar().setValue(int(v - delta.y()))

        self.mousepos = event.localPos()

        super(ScrollArea, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        self.unsetCursor()
        self.mousepos = event.localPos()
        super(ScrollArea, self).mouseReleaseEvent(event)

    def resizeEvent(self, event):
        self.container_widget.resize(self.width(), self.height())

        super(ScrollArea, self).resizeEvent(event)

    def resize_container(self, option):

        option = int(option)

        if option == 0:
            self.container_widget.resize(self.width()+50, self.height())

        elif option == 1:
            self.container_widget.resize(self.width()+50, self.height())

        elif option == 2:
            self.container_widget.resize(self.width()+50, self.height()+50)

    @QtCore.pyqtSlot()
    def zoom_in(self):
        # self.container_widget.setGeometry(200, 200, self.container_widget.width() + 4, self.container_widget.height() + 4)

        # lame zooming
        self.font_size = min(1000, self.font_size + 1)
        self.label.setStyleSheet(f'color: red; font-size: {self.font_size}px')
        self.label.adjustSize()

    @QtCore.pyqtSlot()
    def zoom_out(self):
   
        # self.container_widget.setGeometry(0, 0, self.container_widget.width() - 4, self.container_widget.height() - 4)

        # lame zooming
        self.font_size = max(2, self.font_size - 1)
        self.label.setStyleSheet(f'color: red; font-size: {self.font_size}px')
        self.label.adjustSize()


if __name__ == '__main__':
    a = QtWidgets.QApplication(sys.argv)
    q = ScrollArea()
    q.show()
    sys.exit(a.exec_())