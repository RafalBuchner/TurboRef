from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from turbo import TurboGraphicView, TurboGraphicScene
from turbo.ui.framelessMainWindow import FramelessMainWindow




class MainWindow(FramelessMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        canvasSize = (22500,22500)
        
        self.m_scene = TurboGraphicScene(QtCore.QRectF(0, 0, canvasSize[0], canvasSize[1]), self)
        self.m_graphicsview = TurboGraphicView(self.m_scene)
        self.m_scene.setView(self.m_graphicsview)
        self.resize(640, 480)
        self.setCentralWidget(self.m_graphicsview)

        self.setStyleSheet("QMainWindow{background-color: black;border: 1px solid black}")


    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

    # def mousePressEvent(self, event):

    #     if event.button() == QtCore.Qt.RightButton:
            # print("dupa")
            # self.oldPos = event.globalPos()
    # def eventFilter(self, obj, event):

    # def mouseMoveEvent(self, event):
    #     print("allegro")
    # #         delta = QPoint (event.globalPos() - self.oldPos)
    # #         self.move(self.x() + delta.x(), self.y() + delta.y())
    # #         self.oldPos = event.globalPos()
        


    




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())