import copy

from typing import Optional

from parking import Parking
from placeTypes import PlaceTypes
from collections import deque
from place import Place


def calculateDistance(place: Place, car_place: Place, parking_places: Parking) -> Parking:
    parking_places[car_place] = PlaceTypes.blocked

    min_distance = Parking(
        parking_places.width,
        parking_places.height,
        [[float("inf") for _ in range(parking_places.width)] for _ in range(parking_places.height)]
    )

    min_distance[place] = 0

    q = deque()
    q.append(place)

    while len(q) != 0:
        current_place: Place = q.popleft()
        deltas = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]

        for delta in deltas:
            new_place = current_place + delta

            if 0 <= new_place.x < min_distance.width and 0 <= new_place.y < min_distance.height:
                if min_distance[current_place] + 1 < min_distance[new_place] and parking_places[new_place] != PlaceTypes.blocked:
                    min_distance[new_place] = min_distance[current_place] + 1
                    q.append(new_place)

    parking_places[car_place] = PlaceTypes.full

    return min_distance


def findEmptyPlaces(parking: Parking) -> list[Place]:
    empty_places = []

    for y in range(parking.height):
        for x in range(parking.width):
            if parking[Place(x, y)] == PlaceTypes.empty:
                empty_places.append(Place(x, y))

    return empty_places


class Algorithm:
    def __init__(self, parking: Parking, exit_place: Place, car_place: Place) -> None:
        self.parking = parking
        self.exit_place = exit_place
        self.car_place = car_place

        self.global_move_price = Parking(
            parking.width,
            parking.height,
            [[[float("inf") for _ in range(4)] for _ in range(parking.width)] for _ in range(parking.height)]
        )

        self.save_way = Parking(
            parking.width,
            parking.height,
            [[[None for _ in range(4)] for _ in range(parking.width)] for _ in range(parking.height)]
        )

        self.save_final_state: list[Optional[Parking]] = [None for _ in range(4)]

        self.global_move_price[self.car_place] = [0, 0, 0, 0]

        self.empty_places = findEmptyPlaces(parking)

    def run(self) -> None:
        self.moveAlgorithm(self.car_place)

    def moveAlgorithm(self, car_place: Place, edc=0) -> None:
        free_place = self.empty_places[0]

        dist = calculateDistance(free_place, car_place, self.parking)

        deltas = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]

        for delta_index, delta in enumerate(deltas):
            new_pos = car_place + delta

            if 0 <= new_pos.x < dist.width and 0 <= new_pos.y < dist.height:
                if dist[new_pos] + self.global_move_price[car_place][edc] + 1 < \
                        self.global_move_price[new_pos][delta_index] and \
                        self.parking[new_pos] != PlaceTypes.blocked:

                    self.global_move_price[new_pos][delta_index] = dist[new_pos] + \
                                                                   self.global_move_price[car_place][edc] + 1

                    pos = new_pos
                    cnt = dist[pos]
                    ans = [Place(-delta.x, -delta.y)]

                    while cnt != 0:
                        deltas = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]
                        for de in deltas:
                            newp = pos + de

                            if 0 <= newp.x < dist.width and 0 <= newp.y < dist.height:
                                if dist[newp] == cnt - 1:
                                    ans.append(Place(-de.x, -de.y))
                                    cnt -= 1
                                    pos = newp
                                    break

                    self.save_way[new_pos][delta_index] = ans

                    self.parking[free_place] = PlaceTypes.full
                    self.parking[car_place] = PlaceTypes.empty
                    self.empty_places[0] = car_place

                    if new_pos == self.exit_place:
                        self.save_final_state[delta_index] = copy.deepcopy(self.parking)

                    self.moveAlgorithm(new_pos, delta_index)

                    self.parking[free_place] = PlaceTypes.empty
                    self.parking[car_place] = PlaceTypes.full
                    self.empty_places[0] = free_place

    def buildAnswer(self) -> None:
        deltas = [Place(-1, 0), Place(1, 0), Place(0, -1), Place(0, 1)]

        final_ans = []

        car_place = self.exit_place

        min_price, min_ind = float("inf"), - 1

        for i in range(4):
            price = self.global_move_price[car_place][i]
            if price < min_price:
                min_price = price
                min_ind = i

        dt = deltas[min_ind]
        end_state = self.save_final_state[deltas.index(dt)]
        end_state[self.exit_place] = 2

        empty_place = None
        for x in range(end_state.width):
            for y in range(end_state.height):
                if end_state[Place(x, y)] == 0:
                    empty_place = Place(x, y)

        while True:
            for delta in self.save_way[car_place][deltas.index(dt)]:
                end_state[empty_place - delta], end_state[empty_place] = end_state[empty_place], end_state[empty_place - delta]
                empty_place -= delta
                final_ans = [delta] + final_ans

            for x in range(end_state.width):
                for y in range(end_state.height):
                    if end_state[Place(x, y)] == 2:
                        car_place = Place(x, y)

            dt = empty_place - car_place

            if car_place == self.car_place:
                break

        return final_ans
