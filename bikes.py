from datetime import datetime as date


class Bike:
    def __init__(self) -> None:
        self.mileage: int = 0
        self.battery_level: int = 0
        self.last_full_charge: date = date.now()

class Dock:
    def __init__(self, lat: float, lon: float, alt: float, k: int) -> None:
        self.latitude: float = lat
        self.longitude: float = lon
        self.altitude: float = alt

        self.capacity: int = k
        self.bikes: list[Bike] = []

    def retrieve(self, bike: Bike):
        assert len(self.bikes) < self.capacity
        self.bikes.append(bike)
    def pick(self, bike_i: int | Bike):
        if isinstance(bike_i, Bike): bike_i = self.bikes.index(bike_i)
        return self.bikes.pop(bike_i)

class User:
    def __init__(self) -> None:
        self.reputation: int = None
        