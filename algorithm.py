import copy

from collections import deque
from typing import Optional, Any

from parking import Parking
from place import Place
from placeTypes import PlaceTypes


def calculateDistance(place: Place, car_place: Place, parking_places: Parking):
    parking_places[car_place] = PlaceTypes.blocked

    min_distance: Parking = Parking(
        parking_places.width,
        parking_places.height,
        [[float("inf") for _ in range(parking_places.width)] for _ in range(parking_places.height)]
    )

    previous_positions: Parking = Parking(
        parking_places.width,
        parking_places.height,
        [[float("inf") for _ in range(parking_places.width)] for _ in range(parking_places.height)]
    )

    previous_positions[car_place] = [None for _ in range(4)]

    min_distance[place]: int = 0
    previous_positions[place] = None

    price_to_car = [float("inf") for _ in range(4)]

    q: deque = deque()
    q.append(place)

    while len(q) != 0:
        current_place: Place = q.popleft()

        for delta_x in range(1, parking_places.width):
            price: int = 25
            new_place = current_place + Place(delta_x, 0)

            if new_place == car_place and min_distance[current_place] + price < price_to_car[0]:
                price_to_car[0] = min_distance[current_place] + price
                previous_positions[car_place][0] = current_place

            if not parking_places.check_existence(new_place) or parking_places[new_place] == PlaceTypes.blocked:
                break
            elif min_distance[current_place] + price < min_distance[new_place]:
                previous_positions[new_place] = current_place
                min_distance[new_place] = min_distance[current_place] + price
                q.append(new_place)

        for delta_x in range(1, parking_places.width):
            price: int = 25
            new_place = current_place + Place(-delta_x, 0)

            if new_place == car_place and min_distance[current_place] + price < price_to_car[1]:
                price_to_car[1] = min_distance[current_place] + price
                previous_positions[car_place][1] = current_place

            if not parking_places.check_existence(new_place) or parking_places[new_place] == PlaceTypes.blocked:
                break
            elif min_distance[current_place] + price < min_distance[new_place]:
                previous_positions[new_place] = current_place
                min_distance[new_place] = min_distance[current_place] + price
                q.append(new_place)

        for delta_y in range(1, parking_places.height):
            price: int = 15
            new_place = current_place + Place(0, delta_y)

            if new_place == car_place and min_distance[current_place] + price < price_to_car[2]:
                price_to_car[2] = min_distance[current_place] + price
                previous_positions[car_place][2] = current_place

            if not parking_places.check_existence(new_place) or parking_places[new_place] == PlaceTypes.blocked:
                break
            elif min_distance[current_place] + price < min_distance[new_place]:
                previous_positions[new_place] = current_place
                min_distance[new_place] = min_distance[current_place] + price
                q.append(new_place)

        for delta_y in range(1, parking_places.height):
            price: int = 15
            new_place = current_place + Place(0, -delta_y)

            if new_place == car_place and min_distance[current_place] + price < price_to_car[3]:
                price_to_car[3] = min_distance[current_place] + price
                previous_positions[car_place][3] = current_place

            if not parking_places.check_existence(new_place) or parking_places[new_place] == PlaceTypes.blocked:
                break
            elif min_distance[current_place] + price < min_distance[new_place]:
                previous_positions[new_place] = current_place
                min_distance[new_place] = min_distance[current_place] + price
                q.append(new_place)

    parking_places[car_place] = PlaceTypes.full
    ways = [None, None, None, None]

    for i in range(4):
        current_position = car_place
        previous_position = previous_positions[current_position][i]

        if previous_position is None:
            continue

        way = [current_position, previous_position]

        while True:
            current_position = previous_position

            if current_position == place:
                break

            previous_position = previous_positions[current_position]
            way.append(previous_position)

        ways[i] = way

    return price_to_car, ways


def findEmptyPlaces(parking: Parking) -> list[Place]:
    empty_places: list[Place] = []

    for y in range(parking.height):
        for x in range(parking.width):
            if parking[Place(x, y)] == PlaceTypes.empty:
                empty_places.append(Place(x, y))

    return empty_places


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

        distance, ways = calculateDistance(free_place, car_place, self.parking)

        deltas: list[Place] = [Place(-1, 0), Place(1, 0), Place(0, -1), Place(0, 1)]

        for delta_index, delta in enumerate(deltas):
            new_place: Place = car_place + delta

            if self.parking.check_existence(new_place) and self.parking[new_place] != PlaceTypes.blocked:
                if distance[delta_index] + self.global_move_price[car_place][edc]\
                        < self.global_move_price[new_place][delta_index]:

                    self.global_move_price[new_place][delta_index] = \
                        distance[delta_index] + self.global_move_price[car_place][edc]

                    self.save_way[new_place][delta_index] = ways[delta_index]

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
        deltas: list[Place] = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]

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
            for delta in self.save_way[car_place][deltas.index(dt)][:]:
                while empty_place.y < delta.y:
                    next_place = copy.deepcopy(empty_place)
                    next_place.y += 1
                    end_state[empty_place], end_state[next_place] = end_state[next_place], end_state[empty_place]
                    empty_place = next_place

                while empty_place.y > delta.y:
                    next_place = copy.deepcopy(empty_place)
                    next_place.y -= 1
                    end_state[empty_place], end_state[next_place] = end_state[next_place], end_state[empty_place]
                    empty_place = next_place

                while empty_place.x < delta.x:
                    next_place = copy.deepcopy(empty_place)
                    next_place.x += 1
                    end_state[empty_place], end_state[next_place] = end_state[next_place], end_state[empty_place]
                    empty_place = next_place

                while empty_place.x > delta.x:
                    next_place = copy.deepcopy(empty_place)
                    next_place.x -= 1
                    end_state[empty_place], end_state[next_place] = end_state[next_place], end_state[empty_place]
                    empty_place = next_place

                empty_place = delta
                if len(final_ans) == 0 or final_ans[0] != delta:
                    final_ans = [delta] + final_ans

            for x in range(end_state.width):
                for y in range(end_state.height):
                    if end_state[Place(x, y)] == 5:
                        car_place = Place(x, y)

            dt = empty_place - car_place

            if car_place == self.car_place:
                break

        return final_ans
