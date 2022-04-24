import sys
from typing import Optional

from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton

from paintWidget import PaintWidget

from place import Place
from algorithm import Algorithm
from parking import Parking


class App(QMainWindow):

    def __init__(self, n=4):
        super().__init__()

        self.current_step = None
        self.playButton = None
        self.steps = None
        self.buttonPanel = None
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

        self.buttonPanel = QFrame(parent=self)
        self.buttonPanel.setGeometry(0, int(self.height * 0.9), self.width, int(self.height * 0.1))

        self.playButton = QPushButton("start", parent=self.buttonPanel)
        self.playButton.setGeometry(0, 0, self.width, int(self.height * 0.1))
        self.playButton.clicked.connect(self.startButtonPressed)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(p)

        arr = [[1 for _ in range(self.n)] for _ in range(self.n)]
        self.arrayPainter = PaintWidget(array=arr, parent=self.mainFrame)

        self.show()

    def startButtonPressed(self):
        car_place, exit_place = None, None
        for i in range(len(self.arrayPainter.array)):
            for j in range(len(self.arrayPainter.array[i])):
                if self.arrayPainter.array[i][j] == 2:
                    car_place = Place(j, i)
                if self.arrayPainter.array[i][j] == 3:
                    exit_place = Place(j, i)

        places = Parking(
            len(self.arrayPainter.array),
            len(self.arrayPainter.array),
            [[0 if elem == 0 else 1 for elem in line] for line in self.arrayPainter.array]
        )

        alg = Algorithm(places, exit_place, car_place)
        alg.run()

        self.current_step = 0
        self.steps = alg.buildAnswer()

        self.playButton.clicked.disconnect(self.startButtonPressed)
        self.playButton.clicked.connect(self.nextStep)
        self.playButton.setText("next")

    def nextStep(self):
        free_place = None

        for i in range(len(self.arrayPainter.array)):
            for j in range(len(self.arrayPainter.array[i])):
                if self.arrayPainter.array[i][j] == 0:
                    free_place = Place(j, i)

        delta = self.steps[self.current_step]
        next_place = free_place + delta
        self.arrayPainter.array[free_place.y][free_place.x], self.arrayPainter.array[next_place.y][next_place.x] = \
            self.arrayPainter.array[next_place.y][next_place.x], self.arrayPainter.array[free_place.y][free_place.x]
        self.arrayPainter.repaint()
        self.current_step += 1

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.mainFrame.resize(self.size().width(), int(self.size().height() * 0.9))
        self.arrayPainter.resize(self.mainFrame.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
