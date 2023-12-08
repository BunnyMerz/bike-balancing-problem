from datetime import datetime as date
from random import randint as rng


def to_map(long, lat):
    ox, oy = -373, 202
    mac_x, mac_y = -22.907314, -43.126263
    dx, dy = 0.0014*(mac_x/ox), -0.000429*(mac_y/oy)
    # Translate and zoom in/out
    return ((long - ox) * dx  ) + mac_x, ((lat - oy) * dy ) + mac_y

class Entity:
    _id = 0
    @classmethod
    def next_id(cls): cls._id += 1; return cls._id - 1
    def __init__(self): self.id = self.next_id()

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
    PickBias = -1 # When picking. Considers Bike Delivering a good thing, and Bike Pick bad 
    NeitherBias = 0 # For natural stations
    DeliverBias = 1 # Used when delivering. Considers Bike Pick a good thing, and Bike Delivering bad
    def __init__(self, dock_id:int, lat: float, lon: float, alt: float, k: int, charges: bool = True) -> None:
        super().__init__()
        self.dock_id = dock_id

        self.latitude: float = lat
        self.longitude: float = lon
        self.altitude: float = alt

        self.capacity: int = k
        self.bikes: list[Bike] = []
        self.charges: bool = charges

        self.interested_delivery = 0
        self.interested_picking = 0

        self.times_picked = 0
        self.times_retrieved = 0

    def __repr__(self) -> str:
        return f"<Dock[{self.id}]({['N', 'C'][int(self.charges)]}): ({int(self.latitude)}, {int(self.longitude)}, {int(self.altitude)}) {self.bikes}>"
    def simple(self) -> str:
        return f"<Dock[{self.id}]({['N', 'C'][int(self.charges)]}): ({int(self.latitude)}, {int(self.longitude)}, {int(self.altitude)}) {len(self.bikes)} Bikes>"

    def geo_position(self):
        return (self.latitude, self.longitude, self.altitude)
    def rng_geo_position(self, radius):
        return (self.latitude + rng(-radius, radius), self.longitude + rng(-radius, radius), self.altitude)

    @classmethod
    def distance(cls, dock_1: "Dock", dock_2: "Dock"):
        return
    @classmethod
    def euclidian_distance(cls, dock_1: "Dock", dock_2: "Dock"):
        return Dock.euclidian_distance_point(dock_1, dock_2.latitude, dock_2.longitude, dock_2.altitude) * 9 # TODO: wrong proportion. times 9 is just a quick hack to fix it
    @classmethod
    def euclidian_distance_point(cls, dock_1: "Dock",  latitude: float, longitude: float, altitude: float) -> float:
        x = dock_1.latitude - latitude
        z = dock_1.longitude - longitude
        y = dock_1.altitude - altitude
        return (x*x + y*y + z*z)**(1/2)
    

    def show_deliver_interest(self):
        self.interested_delivery += 1
    def lose_deliver_interest(self):
        self.interested_delivery -= 1
    def done_with_deliver_interest(self):
        self.interested_delivery -= 1

    def show_picking_interest(self):
        self.interested_picking += 1
    def lose_picking_interest(self):
        self.interested_picking -= 1
    def done_with_picking_interest(self):
        self.interested_picking -= 1

    def bike_count(self, bias: int = NeitherBias, ttt=False):
        bike_amount = len(self.bikes)
        if bias == self.NeitherBias:
            return bike_amount
        
        if ((bias == self.DeliverBias and bike_amount == self.capacity) or (bias == self.PickBias and bike_amount == 0)):
                return bike_amount # This avoids making users try to deliver to a future-empty or future-full dock
        
        prediction = bike_amount - self.interested_picking + self.interested_delivery
        return min(max(prediction, 0), self.capacity)

    def occupancy(self, bias: int = NeitherBias):
        return self.bike_count(bias)/self.capacity * 100
    def full  (self, bias: int = NeitherBias): return self.bike_count(bias) >= self.capacity
    def empty (self, bias: int = NeitherBias): return self.bike_count(bias) == 0
    def coords(self): return (self.latitude, self.longitude, self.altitude)

    def retrieve(self, bike: Bike):
        self.times_retrieved += 1
        return self.add_bike(bike)
    def add_bike(self, bike: Bike):
        # assert len(self.bikes) < self.capacity
        bike.dock = self
        self.bikes.append(bike)

    def pick(self, bike_i: int | Bike):
        self.times_picked += 1
        return self.remove_bike(bike_i)
    def remove_bike(self, bike_i: int | Bike):
        if isinstance(bike_i, Bike): bike_i = self.bikes.index(bike_i)
        bike = self.bikes.pop(bike_i)
        bike.dock = None
        return bike
    def pick_any(self):
        bike_i = 0
        x = 1
        while(x < len(self.bikes)):
            if self.bikes[x].battery_level > self.bikes[bike_i].battery_level:
                bike_i = x
            x+=1
        return self.pick(bike_i)

class User(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.reputation: int = None
        