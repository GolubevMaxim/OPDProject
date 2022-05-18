import copy
import sys

from time import sleep
from typing import Optional

from PyQt6 import QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton

from paintWidget import PaintWidget

from place import Place
from algorithm import Algorithm
from parking import Parking


class App(QMainWindow):

    def __init__(self, n=6):
        super().__init__()

        self.price = None
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

        self.playButton = QPushButton("generate", parent=self.buttonPanel)
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

        array = []
        for line in self.arrayPainter.array:
            array.append([])
            for elem in line:
                value = 1
                if elem == 0:
                    value = 0
                if elem == 4:
                    value = 2

                array[-1].append(value)

        places = Parking(
            len(self.arrayPainter.array),
            len(self.arrayPainter.array),
            array
        )

        alg = Algorithm(places, exit_place, car_place)
        alg.run()

        self.steps, self.price = alg.buildAnswer()

        self.playButton.clicked.disconnect(self.startButtonPressed)
        self.playButton.clicked.connect(self.nextStep)
        self.playButton.setText("start")

    def nextStep(self):
        self.playButton.clicked.disconnect(self.nextStep)

        current_step = 0
        current_time = 0

        self.playButton.setText(f"current step: {current_step}, "
                                f"time spend: {current_time}, "
                                f"all time:{self.price}, "
                                f"completed: {current_time / self.price:.2f}")

        while current_step < len(self.steps):
            free_place = None

            for i in range(len(self.arrayPainter.array)):
                for j in range(len(self.arrayPainter.array[i])):
                    if self.arrayPainter.array[i][j] == 0:
                        free_place = Place(j, i)

            next_place = self.steps[current_step]

            if next_place.x != free_place.x:
                current_time += 25
            if next_place.y != free_place.y:
                current_time += 15

            while next_place.y > free_place.y:
                next_step = copy.deepcopy(free_place)
                next_step.y += 1
                self.arrayPainter.array[free_place.y][free_place.x], self.arrayPainter.array[next_step.y][next_step.x] = \
                    self.arrayPainter.array[next_step.y][next_step.x], self.arrayPainter.array[free_place.y][free_place.x]
                free_place = next_step

            while next_place.y < free_place.y:
                next_step = copy.deepcopy(free_place)
                next_step.y -= 1
                self.arrayPainter.array[free_place.y][free_place.x], self.arrayPainter.array[next_step.y][next_step.x] = \
                    self.arrayPainter.array[next_step.y][next_step.x], self.arrayPainter.array[free_place.y][free_place.x]
                free_place = next_step

            while next_place.x > free_place.x:
                next_step = copy.deepcopy(free_place)
                next_step.x += 1
                self.arrayPainter.array[free_place.y][free_place.x], self.arrayPainter.array[next_step.y][next_step.x] = \
                    self.arrayPainter.array[next_step.y][next_step.x], self.arrayPainter.array[free_place.y][free_place.x]
                free_place = next_step

            while next_place.x < free_place.x:
                next_step = copy.deepcopy(free_place)
                next_step.x -= 1
                self.arrayPainter.array[free_place.y][free_place.x], self.arrayPainter.array[next_step.y][next_step.x] = \
                    self.arrayPainter.array[next_step.y][next_step.x], self.arrayPainter.array[free_place.y][free_place.x]
                free_place = next_step

            current_step += 1
            self.playButton.setText(f"current step: {current_step - 1}, "
                                    f"time spend: {current_time}, "
                                    f"all time:{self.price}, "
                                    f"completed: {current_time / self.price:.2f}")

            self.arrayPainter.repaint()
            sleep(1)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.mainFrame.resize(self.size().width(), int(self.size().height() * 0.9))
        self.arrayPainter.resize(self.mainFrame.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
