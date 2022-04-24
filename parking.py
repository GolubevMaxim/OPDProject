from place import Place
from typing import Optional, Any


class Parking:
    def __init__(self, width: int, height: int, places: Optional[list[list[Any]]] = None) -> None:
        self.width = width
        self.height = height

        if places is None:
            self.places = [[0 for _ in range(width)] for _ in range(height)]
        else:
            self.places = places

    def __getitem__(self, place: Place) -> Any:
        return self.places[place.y][place.x]

    def __setitem__(self, place: Place, value: Any) -> None:
        self.places[place.y][place.x] = value
