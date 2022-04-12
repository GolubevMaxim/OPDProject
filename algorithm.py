from placeTypes import PlaceTypes
from place import Place


def calculateDistance(place: Place, car_place, lst) -> list[list[float]]:
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


def findEmptyPlaces(places: list[list[int]]) -> list[Place]:
    empty_places = []

    for y in range(len(places)):
        for x in range(len(places[y])):
            if places[y][x] == PlaceTypes.empty:
                empty_places.append(Place(x, y))

    return empty_places


class Algorithm:
    def __init__(self, places, exit_position, car_position):
        self.places = places

        self.exit_position = exit_position
        self.car_position = car_position

        self.global_move_price = [[[float("inf") for _ in range(4)] for _ in range(len(places[line]))]
                                  for line in range(len(places))]

        self.save_way = [[[None for _ in range(4)] for _ in range(len(places[line]))] for line in range(len(places))]

        self.global_move_price[self.car_position.y][self.car_position.x] = [0, 0, 0, 0]

        self.empty_places = findEmptyPlaces(places)

        self.moveAlgorithm(self.car_position)

    def moveAlgorithm(self, car_pos: Place, edc=0) -> None:
        free_place = self.empty_places[0]

        dist = calculateDistance(free_place, car_pos, places)

        deltas = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]

        for delta_index, delta in enumerate(deltas):
            new_pos = car_pos + delta

            if 0 <= new_pos.x < len(dist[0]) and 0 <= new_pos.y < len(dist):
                if dist[new_pos.y][new_pos.x] + self.global_move_price[car_pos.y][car_pos.x][edc] + 1 < \
                        self.global_move_price[new_pos.y][new_pos.x][delta_index] and places[new_pos.y][
                              new_pos.x] != PlaceTypes.blocked:

                    self.global_move_price[new_pos.y][new_pos.x][delta_index] = dist[new_pos.y][new_pos.x] + \
                                                                           self.global_move_price[car_pos.y][car_pos.x][
                                                                               edc] + 1

                    pos = new_pos
                    cnt = dist[pos.y][pos.x]
                    ans = [Place(-delta.x, -delta.y)]

                    while cnt != 0:
                        deltas = [Place(1, 0), Place(-1, 0), Place(0, 1), Place(0, -1)]
                        for de in deltas:
                            newp = pos + de

                            if 0 <= newp.x < len(dist[0]) and 0 <= newp.y < len(dist):
                                if dist[newp.y][newp.x] == cnt - 1:
                                    ans.append(Place(-de.x, -de.y))
                                    cnt -= 1
                                    pos = newp
                                    break

                    self.save_way[new_pos.y][new_pos.x][delta_index] = ans

                    places[free_place.y][free_place.x] = PlaceTypes.full
                    places[car_pos.y][car_pos.x] = PlaceTypes.empty
                    self.empty_places[0] = car_pos

                    self.moveAlgorithm(new_pos, delta_index)

                    places[free_place.y][free_place.x] = PlaceTypes.empty
                    places[car_pos.y][car_pos.x] = PlaceTypes.full
                    self.empty_places[0] = free_place

    def buildAnswer(self):
        deltas = [Place(-1, 0), Place(1, 0), Place(0, -1), Place(0, 1)]

        ans = []
        p = self.exit_position

        while p != self.car_position:
            min_price, min_ind = float("inf"), - 1

            for i in range(4):
                price = self.global_move_price[p.y][p.x][i]
                if price < min_price:
                    min_price = price
                    min_ind = i

            ans.append(self.save_way[p.y][p.x][min_ind])

            p += deltas[min_ind]

        print(*ans)


places = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 0, 1]
]

car_pos = Place(2, 1)
exit_pos = Place(0, 0)

Algorithm(places, exit_pos, car_pos).buildAnswer()
