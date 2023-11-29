from src.bikes import Dock, Bike
ENUM = int

class PickBike:
    """Describes what a bike must have to be elegible, when withdrawing it"""
    def __init__(self, min_battery_level: float, max_battery_level: float, suitable: list[Bike]):
        self.min_battery_level = min_battery_level
        self.max_battery_level = max_battery_level

        self.suitable = suitable
    
    def validate(self, obj: Bike):
        return (
            (obj.battery_level >= self.min_battery_level and
            obj.battery_level <= self.max_battery_level)
            or
            (obj in self.suitable) # In case obj stopped being valid, but was suggested at somepoint
        )
    
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
    
    def validate(self, obj: Dock):
        return (
            (
            obj.capacity >= self.min_capacity and
            obj.capacity <= self.max_capacity and 
            (self.chargable == Destination.EITHER or int(self.chargable) == int(obj.charges))
            )
            or
            (obj in self.suitable) # In case Dock was ever a valid option
        )
    
class Goal:
    OnlyStart = 0
    OnlyEnd = 1
    SimpleDeliverNatural = 2 
    SimpleDeliverNonNatural = 3 
    SubRouteNatural = 4 # Fig 12
    SubRouteNonNatural = 5 # Fig 14
    def __init__(self, initial_dest: Destination = None, initial_bike: PickBike = None, sub_dest: Destination = None, bike_swap: PickBike = None, end_dest: Destination = None) -> None:
        self.initial_dest: Destination | None = initial_dest
        self.initial_bike: PickBike    | None = initial_bike
        self.sub_dest:     Destination | None = sub_dest
        self.bike_swap:    PickBike    | None = bike_swap
        self.end_dest:     Destination | None = end_dest

        self.type = None
        if(self.initial_dest):                  # Recommend a specific start
            self.type = Goal.OnlyStart
        elif(
            self.initial_bike is not None and
            self.sub_dest     is not None and
            self.bike_swap    is not None
        ):                                      # SubRoute
            if(self.end_dest is not None):          # Diferente Station
                self.type = Goal.SubRouteNonNatural
            else:                                   # Natural Station
                self.type = Goal.SubRouteNatural
        elif(self.initial_bike is not None):    # Simple Bike Deliver
            if(self.end_dest is not None):          # Diferente Station 
                self.type = Goal.SimpleDeliverNatural
            else:                                   # Natural Station
                self.type = Goal.SimpleDeliverNonNatural
        elif(self.end_dest):                    # Only recommend a specific end
            self.type = Goal.OnlyEnd

    def __str__(self) -> str:
        def to_str(attr: Destination | PickBike):
            if attr is None:
                return False
            return len(attr.suitable)
            
        return f"<Goal: Init[{to_str(self.initial_dest)}], BikeInit[{to_str(self.initial_bike)}], SubDest[{to_str(self.sub_dest)}], BikeSwap[{to_str(self.bike_swap)}], EndDest[{to_str(self.end_dest)}]>"
    
    def validate(self, obj: Bike | Dock, attr: Destination | PickBike):
        return attr.validate(obj)