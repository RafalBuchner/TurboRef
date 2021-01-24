from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from turbo import TurboGraphicView, TurboGraphicScene
from turbo.ui.framelessMainWindow import FramelessMainWindow




class MainWindow(FramelessMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        canvasSize = (40000,40000)
        
        self.m_scene = TurboGraphicScene(QtCore.QRectF(0, 0, canvasSize[0], canvasSize[1]), self)
        self.m_graphicsview = TurboGraphicView(self.m_scene)
        self.m_scene.setView(self.m_graphicsview)
        self.resize(640, 480)
        self.setCentralWidget(self.m_graphicsview)

        self.setStyleSheet("""FramelessMainWindow{
                                    background-color: rgb(25,25,25);
                                    border: 1px solid black;
                                }""")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())