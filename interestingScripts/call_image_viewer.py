from image_viewer import *
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap
import os
import sys


class TurboRef_App(QDialog):
	def __init__(self):
		super().__init__()
		self.ui = CanvasUI()
		self.ui.setupUi(self)

		self.ui.pushButton.clicked.connect(self.checkPath)

	def checkPath(self):
		image_path = self.ui.lineEdit.text()
		if os.path.isfile(image_path):
			scene = QtWidgets.QGraphicsScene(self)
			pixmap = QPixmap(image_path)
			help(pixmap)
			item = QtWidgets.QGraphicsPixmapItem(pixmap)
			scene.addItem(item)
			self.ui.graphicsView.setScene(scene)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	class_instance = TurboRef_App()
	class_instance.show()
	sys.exit(app.exec_())