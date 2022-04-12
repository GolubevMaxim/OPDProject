class Place:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) != Place:
            raise TypeError

        x = self.x + other.x
        y = self.y + other.y

        return Place(x, y)

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    def __eq__(self, other):
        if type(other) != Place:
            raise TypeError
        return other.x == self.x and self.y == other.y

    def __ne__(self, other):
        if type(other) != Place:
            raise TypeError
        return other.x != self.x or self.y != other.y
