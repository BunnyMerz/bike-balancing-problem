from datetime import datetime as date


class Entity:
    _id = 0
    @classmethod
    def next_id(cls): cls._id += 1; return cls._id - 1

    def __init__(self) -> None:
        self.id = self.next_id()
class Bike(Entity):
    def __init__(self, battery_level=100.0) -> None:
        super().__init__()
        self.mileage: float = 0.0
        self.battery_level: float = battery_level
        self.last_full_charge: date = date.now()

        self.dock: "Dock" | None = None

    def __repr__(self) -> str:
        return f"<Bike[{self.id}]: {int(self.battery_level)}%, {self.mileage}km>"

class Dock(Entity):
    def __init__(self, lat: float, lon: float, alt: float, k: int, charges: bool = True) -> None:
        super().__init__()
        self.latitude: float = lat
        self.longitude: float = lon
        self.altitude: float = alt

        self.capacity: int = k
        self.bikes: list[Bike] = []
        self.charges: bool = charges

    def __repr__(self) -> str:
        return f"<Dock[{self.id}]({['N', 'C'][int(self.charges)]}): {self.bikes}>"

    @classmethod
    def distance(cls, dock_1: "Dock", dock_2: "Dock"):
        return
    @classmethod
    def euclidian_distance(cls, dock_1: "Dock", dock_2: "Dock"):
        x = dock_1.latitude - dock_2.latitude
        z = dock_1.longitude - dock_2.longitude
        y = dock_1.altitude - dock_2.altitude
        return (x*x + y*y + z*z)**(1/2)


    def retrieve(self, bike: Bike):
        assert len(self.bikes) < self.capacity
        bike.dock = self
        self.bikes.append(bike)
    def pick(self, bike_i: int | Bike):
        if isinstance(bike_i, Bike): bike_i = self.bikes.index(bike_i)
        bike = self.bikes.pop(bike_i)
        bike.dock = None
        return bike

class User(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.reputation: int = None
        