import random
import sys

from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.arrayPainter = None
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

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(p)

        # Add paint widget and paint
        arr = [[random.randint(0, 1) for _ in range(10)] for _ in range(10)]
        self.arrayPainter = PaintWidget(array=arr, parent=self)

        self.arrayPainter.move(0, 0)

        self.show()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.arrayPainter.resize(self.size().width(), self.size().height())


class PaintColors:
    carColor = QColor(80, 80, 80)
    emptyColor = QColor(255, 255, 255)


class PaintWidget(QWidget):

    def __init__(self, array, parent=None):
        super().__init__(parent)
        self.array = array

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        qp = QPainter(self)
        qp.setPen(QColor(0, 0, 0))

        size = self.size()

        # Draw array
        for i, row in enumerate(self.array):
            for j, elem in enumerate(row):
                qp.setBrush(PaintColors.carColor if elem else PaintColors.emptyColor)

                qp.drawRect(
                    int((i / len(self.array)) * size.width()),
                    int((j / len(self.array)) * size.height()),
                    int(((i + 1) / len(self.array)) * size.width()),
                    int(((j + 1) / len(self.array)) * size.height())
                )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec()
