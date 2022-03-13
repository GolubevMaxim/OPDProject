from PyQt6 import QtGui
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget


class PaintColors:
    carColor = QColor(80, 80, 80)
    emptyColor = QColor(255, 255, 255)
    targetCarColor = QColor(200, 0, 0)
    liftColor = QColor(0, 200, 0)


class PaintWidget(QWidget):

    def __init__(self, array: list[list[int]], parent: QWidget = None):
        super().__init__(parent)
        self.array = array

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == event.button().LeftButton:
            list_index_x = int(event.position().x() * len(self.array) // self.size().width())
            list_index_y = int(event.position().y() * len(self.array) // self.size().height())

            self.array[list_index_x][list_index_y] = (self.array[list_index_x][list_index_y] + 1) % 4
            self.repaint()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        qp = QPainter(self)
        qp.setPen(QColor(0, 0, 0))

        size = self.size()

        # Draw array
        for i, row in enumerate(self.array):
            for j, elem in enumerate(row):

                color = PaintColors.emptyColor
                if elem == 0:
                    color = PaintColors.emptyColor
                elif elem == 1:
                    color = PaintColors.carColor
                elif elem == 2:
                    color = PaintColors.targetCarColor
                elif elem == 3:
                    color = PaintColors.liftColor

                qp.setBrush(color)

                qp.drawRect(
                    int((i / len(self.array)) * size.width()),
                    int((j / len(self.array)) * size.height()),
                    int(((i + 1) / len(self.array)) * size.width()),
                    int(((j + 1) / len(self.array)) * size.height())
                )
