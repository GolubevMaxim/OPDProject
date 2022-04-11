import copy
from typing import Optional
import time


class PlaceTypes:
    empty = 0
    full = 1
    blocked = 2


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) != Position:
            raise TypeError

        x = self.x + other.x
        y = self.y + other.y

        return Position(x, y)


def calculateDistance(place: Position, car_place, lst):
    lst[car_place.y][car_place.x] = PlaceTypes.blocked
    x, y = place.x, place.y

    dist = [[float("inf") for _ in range(len(lst[i]))] for i in range(len(lst))]
    dist[y][x] = 0

    def go(x, y):
        delta = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for dx, dy in delta:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < len(dist[0]) and 0 <= ny < len(dist):
                if dist[y][x] + 1 < dist[ny][nx] and lst[ny][nx] != PlaceTypes.blocked:
                    dist[ny][nx] = dist[y][x] + 1
                    go(nx, ny)

    go(x, y)

    lst[car_place.y][car_place.x] = PlaceTypes.full

    return dist

N = 10

places = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

exit_pos = Position(0, 0)
car_pos = Position(9, 9)

global_move_price = [[float("inf") for _ in range(len(places[i]))] for i in range(len(places))]


def moveAlgorithm(places: list[list[int]], car_pos: Position):
    free_place: Optional[Position] = None

    for y in range(len(places)):
        for x in range(len(places[y])):
            if places[y][x] == PlaceTypes.empty:
                free_place = Position(x, y)

    dist = calculateDistance(free_place, car_pos, places)

    delta = [Position(1, 0), Position(-1, 0), Position(0, 1), Position(0, -1)]

    for d in delta:
        new_pos = car_pos + d
        if 0 <= new_pos.x < len(dist[0]) and 0 <= new_pos.y < len(dist):
            if dist[new_pos.y][new_pos.x] + global_move_price[car_pos.y][car_pos.x] + 1 <= \
                    global_move_price[new_pos.y][new_pos.x] and places[new_pos.y][new_pos.x] != PlaceTypes.blocked:

                global_move_price[new_pos.y][new_pos.x] = dist[new_pos.y][new_pos.x] + global_move_price[car_pos.y][car_pos.x] + 1

                places[free_place.y][free_place.x] = PlaceTypes.full
                places[car_pos.y][car_pos.x] = PlaceTypes.empty

                moveAlgorithm(places, new_pos)

                places[free_place.y][free_place.x] = PlaceTypes.empty
                places[car_pos.y][car_pos.x] = PlaceTypes.full


global_move_price[car_pos.y][car_pos.x] = 0

st = time.time()
moveAlgorithm(places, car_pos)
et = time.time()

[print(*i) for i in global_move_price]
print(et - st)
