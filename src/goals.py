from src.bikes import Dock
ENUM = int

class PickBike:
    """Describes what a bike must have to be elegible, when withdrawing it"""
    def __init__(self, min_battery_level: float, max_battery_level: float):
        self.min_battery_level = min_battery_level
        self.max_battery_level = max_battery_level

class DeliverBike(PickBike):
    """Describes what a bike must have to be elegible, when delivering it"""
    pass

class Destination:
    EITHER = -1
    NON_CHARGEABLE = 0
    CHARGEABLE = 1
    """Describes what a destination must have to be elegible. Will have all suitable docks form when it was first instanced"""
    def __init__(self, chargable: ENUM, min_capacity: int, max_capacity: int, suitable: list[Dock], must_contain_bike: PickBike | DeliverBike):
        self.min_capacity: int = min_capacity
        self.max_capacity: int = max_capacity

        self.chargable: ENUM = chargable

        self.must_contain_bike: PickBike | DeliverBike | None = must_contain_bike
        self.suitable: list[Dock] = suitable # Options that were valid when instantiating the class

    def __repr__(self) -> str:
        return f"<Dest[{['C/N','N','C'][self.chargable+1]}]: Capacity: {self.min_capacity}..{self.max_capacity}, Suitable: {self.suitable}>"