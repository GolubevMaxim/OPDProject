import copy

from typing import Optional

from parking import Parking
from placeTypes import PlaceTypes
from collections import deque
from place import Place


def calculateDistance(place: Place, car_place: Place, parking_places: Parking) -> Parking:
    parking_places[car_place] = PlaceTypes.blocked

    min_distance: Parking = Parking(
        parking_places.width,
        parking_places.height,
        [[float("inf") for _ in range(parking_places.width)] for _ in range(parking_places.height)]
    )

    min_distance[place]: int = 0

    q: deque = deque()
    q.append(place)

    while len(q) != 0:
        current_place: Place = q.popleft()
        deltas: list[Place] = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]

        for delta in deltas:
            new_place: Place = current_place + delta

            if min_distance.check_existence(new_place) and parking_places[new_place] != PlaceTypes.blocked:
                if min_distance[current_place] + 1 < min_distance[new_place]:
                    min_distance[new_place] = min_distance[current_place] + 1
                    q.append(new_place)

    parking_places[car_place] = PlaceTypes.full

    return min_distance


def findEmptyPlaces(parking: Parking) -> list[Place]:
    empty_places: list[Place] = []

    for y in range(parking.height):
        for x in range(parking.width):
            if parking[Place(x, y)] == PlaceTypes.empty:
                empty_places.append(Place(x, y))

    return empty_places


def save_path(distance: Parking, end_place: Place, delta: Place) -> list[Place]:
    path: list[Place] = [-delta]
    current_place: Place = end_place
    count: int = distance[end_place]

    while count != 0:
        deltas: list[Place] = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]
        for _delta in deltas:
            new_place: Place = current_place + _delta

            if distance.check_existence(new_place):
                if distance[new_place] == count - 1:
                    path.append(Place(-_delta.x, -_delta.y))
                    count -= 1
                    current_place = new_place
                    break
    return path


class Algorithm:
    def __init__(self, parking: Parking, exit_place: Place, car_place: Place) -> None:
        self.parking: Parking = parking
        self.exit_place: Place = exit_place
        self.car_place: Place = car_place

        self.global_move_price: Parking = Parking(
            parking.width,
            parking.height,
            [[[float("inf") for _ in range(4)] for _ in range(parking.width)] for _ in range(parking.height)]
        )

        self.save_way: Parking = Parking(
            parking.width,
            parking.height,
            [[[None for _ in range(4)] for _ in range(parking.width)] for _ in range(parking.height)]
        )

        self.save_final_state: list[Optional[Parking]] = [None for _ in range(4)]

        self.global_move_price[self.car_place] = [0, 0, 0, 0]

        self.empty_places: list[Place] = findEmptyPlaces(parking)

    def run(self) -> None:
        self.moveAlgorithm(self.car_place)

    def moveAlgorithm(self, car_place: Place, edc=0) -> None:
        free_place: Place = self.empty_places[0]

        distance: Parking = calculateDistance(free_place, car_place, self.parking)

        deltas: list[Place] = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]

        for delta_index, delta in enumerate(deltas):
            new_place: Place = car_place + delta

            if distance.check_existence(new_place) and self.parking[new_place] != PlaceTypes.blocked:
                if distance[new_place] + self.global_move_price[car_place][edc] + 1 \
                        < self.global_move_price[new_place][delta_index]:

                    self.global_move_price[new_place][delta_index] = \
                        distance[new_place] + self.global_move_price[car_place][edc] + 1

                    self.save_way[new_place][delta_index] = save_path(distance, new_place, delta)

                    self.parking[free_place] = PlaceTypes.full
                    self.parking[car_place] = PlaceTypes.empty
                    self.empty_places[0] = car_place

                    if new_place == self.exit_place:
                        self.save_final_state[delta_index] = copy.deepcopy(self.parking)

                    self.moveAlgorithm(new_place, delta_index)

                    self.parking[free_place] = PlaceTypes.empty
                    self.parking[car_place] = PlaceTypes.full
                    self.empty_places[0] = free_place

    def buildAnswer(self) -> list[Place]:
        deltas: list[Place] = [Place(-1, 0), Place(1, 0), Place(0, -1), Place(0, 1)]

        final_ans: list[Place] = []

        car_place: Place = self.exit_place

        min_price, min_ind = float("inf"), - 1

        for i in range(4):
            price = self.global_move_price[car_place][i]
            if price < min_price:
                min_price = price
                min_ind = i

        dt: Place = deltas[min_ind]
        end_state: Parking = self.save_final_state[deltas.index(dt)]
        end_state[self.exit_place] = 5

        empty_place = None
        for x in range(end_state.width):
            for y in range(end_state.height):
                if end_state[Place(x, y)] == 0:
                    empty_place = Place(x, y)

        while True:
            for delta in self.save_way[car_place][deltas.index(dt)]:
                end_state[empty_place - delta], end_state[empty_place] = \
                    end_state[empty_place], end_state[empty_place - delta]

                empty_place -= delta
                final_ans = [delta] + final_ans

            for x in range(end_state.width):
                for y in range(end_state.height):
                    if end_state[Place(x, y)] == 5:
                        car_place = Place(x, y)

            dt = empty_place - car_place

            if car_place == self.car_place:
                break

        return final_ans
