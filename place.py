from __future__ import annotations


class Place:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Place) -> Place:
        if type(other) != Place:
            raise TypeError

        x = self.x + other.x
        y = self.y + other.y

        return Place(x, y)

    def __sub__(self, other: Place) -> Place:
        return self.__add__(-other)

    def __neg__(self):
        return Place(-self.x, -self.y)

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    def __repr__(self) -> str:
        return f"[{self.x}, {self.y}]"

    def __eq__(self, other: Place) -> bool:
        if type(other) != Place:
            raise TypeError
        return other.x == self.x and self.y == other.y

    def __ne__(self, other: Place) -> bool:
        if type(other) != Place:
            raise TypeError
        return other.x != self.x or self.y != other.y
