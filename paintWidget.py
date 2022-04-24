from PyQt6 import QtGui
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget


class PaintColors:
    carColor = QColor(80, 80, 80)
    emptyColor = QColor(255, 255, 255)
    targetCarColor = QColor(200, 0, 0)
    exitColor = QColor(0, 200, 0)
    blockColor = QColor(0, 0, 0)


class PaintWidget(QWidget):

    def __init__(self, array: list[list[int]], parent: QWidget = None):
        super().__init__(parent)
        self.array = array

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == event.button().LeftButton:
            list_index_x = int(event.position().x() * len(self.array) // self.size().width())
            list_index_y = int(event.position().y() * len(self.array) // self.size().height())

            self.array[list_index_y][list_index_x] = (self.array[list_index_y][list_index_x] + 1) % 5
            self.repaint()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        qp = QPainter(self)
        qp.setPen(QColor(0, 0, 0))

        size = self.size()

        for j, row in enumerate(self.array):
            for i, elem in enumerate(row):

                color = PaintColors.emptyColor
                if elem == 0:
                    color = PaintColors.emptyColor
                elif elem == 1:
                    color = PaintColors.carColor
                elif elem == 2:
                    color = PaintColors.targetCarColor
                elif elem == 3:
                    color = PaintColors.exitColor
                elif elem == 4:
                    color = PaintColors.blockColor

                qp.setBrush(color)

                qp.drawRect(
                    int((i / len(self.array)) * size.width()),
                    int((j / len(self.array)) * size.height()),
                    int(((i + 1) / len(self.array)) * size.width()),
                    int(((j + 1) / len(self.array)) * size.height())
                )
