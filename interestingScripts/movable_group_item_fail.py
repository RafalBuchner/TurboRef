import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QApplication, QGraphicsItemGroup, QGraphicsEllipseItem


class MyDisk(QGraphicsEllipseItem):
    def __init__(self, top_left_x, top_left_y, radius, color):
        super().__init__(top_left_x, top_left_y, radius, radius)
        self.setBrush(color)
        self.setFlag(QGraphicsItem.ItemIsMovable)


class MyGroup(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.disk1 = MyDisk(50, 50, 20, Qt.red)
        self.disk2 = MyDisk(150, 150, 20, Qt.red)
        self.addToGroup(self.disk1)
        self.addToGroup(self.disk2)
        self.setFlag(QGraphicsItemGroup.ItemIsMovable)


class MyView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setWindowTitle('Red disks are not movable')
        self.setSceneRect(0, 0, 250, 250)
        self.group = MyGroup()
        self.scene.addItem(self.group)
        self.scene.addItem(MyDisk(150, 50, 20, Qt.green))


if __name__ == '__main__':
    app = QApplication([])
    f = MyView()
    f.show()
    sys.exit(app.exec_())