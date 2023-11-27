from src.bikes import Dock, Bike
ENUM = int

class PickBike:
    """Describes what a bike must have to be elegible, when withdrawing it"""
    def __init__(self, min_battery_level: float, max_battery_level: float, suitable: list[Bike]):
        self.min_battery_level = min_battery_level
        self.max_battery_level = max_battery_level

        self.suitable = suitable

class DeliverBike(PickBike):
    """Describes what a bike must have to be elegible, when delivering it"""
    pass

class Destination:
    EITHER = -1
    NON_CHARGEABLE = 0
    CHARGEABLE = 1
    """Describes what a destination must have to be elegible. Will have all suitable docks form when it was first instanced"""
    def __init__(self, chargable: ENUM, min_capacity: int, max_capacity: int, suitable: list[Dock]):
        self.min_capacity: int = min_capacity
        self.max_capacity: int = max_capacity

        self.chargable: ENUM = chargable

        self.suitable: list[Dock] = suitable # Options that were valid when instantiating the class

    def __repr__(self) -> str:
        return f"<Dest[{['C/N','N','C'][self.chargable+1]}]: Capacity: {self.min_capacity}..{self.max_capacity}, Suitable: {self.suitable}>"
    
class Goal:
    def __init__(self, initial_dest: Destination, initial_bike: PickBike = None, sub_dest: Destination = None, bike_swap: PickBike = None, end_dest: Destination = None) -> None:
        self.initial_dest: Destination = initial_dest
        self.initial_bike: PickBike    = initial_bike
        self.sub_dest:     Destination = sub_dest
        self.bike_swap:    PickBike    = bike_swap
        self.end_dest:     Destination = end_dest