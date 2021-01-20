from functools import partial
# from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.m_scene = QtWidgets.QGraphicsScene(QtCore.QRectF(0, 0, 400, 400), self)
        self.m_graphicsview = QtWidgets.QGraphicsView(self.m_scene)
        self.setCentralWidget(self.m_graphicsview)
        self.resize(640, 480)

        self.m_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(-50, -50, 100, 100))
        self.m_item.setFlags(
            self.m_item.flags() | QtWidgets.QGraphicsItem.ItemIsMovable
        )
        self.m_item.setBrush(QtGui.QColor("salmon"))
        self.m_item.setPos(100, 100)
        self.m_scene.addItem(self.m_item)

        #QtCore.QTimer.singleShot(1000, self.emulate_move_item)

    def emulate_move_item(self):
        sp = self.m_item.mapToScene(self.m_item.boundingRect().center())
        lp = self.m_graphicsview.mapFromScene(sp)
        end_pos = lp + QtCore.QPoint(100, 100)

        self.press(lp)

        animation = QtCore.QVariantAnimation(
            self,
            startValue=lp,
            endValue=end_pos
        )
        animation.valueChanged.connect(self.moveTo)
        animation.finished.connect(partial(self.release, end_pos))
        animation.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def press(self, pos):
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonPress,
            pos,
            self.m_graphicsview.mapToGlobal(pos),
            QtCore.Qt.LeftButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier,
        )
        QtCore.QCoreApplication.postEvent(self.m_graphicsview.viewport(), event)

    def moveTo(self, pos):
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseMove,
            pos,
            self.m_graphicsview.viewport().mapToGlobal(pos),
            QtCore.Qt.LeftButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier,
        )
        QtCore.QCoreApplication.postEvent(self.m_graphicsview.viewport(), event)

    def release(self, pos):
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease,
            pos,
            self.m_graphicsview.viewport().mapToGlobal(pos),
            QtCore.Qt.LeftButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier,
        )
        QtCore.QCoreApplication.postEvent(self.m_graphicsview.viewport(), event)

    def double_click(self, pos):
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonDblClick,
            pos,
            self.m_graphicsview.viewport().mapToGlobal(pos),
            QtCore.Qt.LeftButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier,
        )
        QtCore.QCoreApplication.postEvent(self.m_graphicsview.viewport(), event)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())