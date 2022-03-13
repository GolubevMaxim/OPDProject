import sys
from typing import Optional

from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame

from paintWidget import PaintWidget


class App(QMainWindow):

    def __init__(self, n=10):
        super().__init__()

        self.n = n

        self.mainFrame: Optional[QFrame] = None
        self.arrayPainter: Optional[PaintWidget] = None

        self.title = 'OPD Project'

        # screen settings
        self.left = 100
        self.top = 100
        self.width = 440
        self.height = 280

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.mainFrame = QFrame(parent=self)
        self.mainFrame.setGeometry(0, 0, self.width, int(self.height * 0.9))

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(p)

        # Add paint widget and paint
        arr = [[1 for _ in range(self.n)] for _ in range(self.n)]
        self.arrayPainter = PaintWidget(array=arr, parent=self.mainFrame)

        self.show()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.mainFrame.resize(self.size().width(), int(self.size().height() * 0.9))
        self.arrayPainter.resize(self.mainFrame.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
