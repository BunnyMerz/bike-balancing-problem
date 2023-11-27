from random import randint as rng
from debug import Debug
from bikes import Dock, Bike
from goals import Destination, PickBike, DeliverBike
print = Debug.print


class Main:
    docks:     list[Dock]        = []
    bikes:     list[Bike]        = []
    adj:       list[list[bool]]  = []
    distances: list[list[float]] = []

    max_radius = 145
    number_of_suggestions = 1

    #########
    #### Suggest starting station
    # Represents the max occupancy a dock must have to become a suggestion
    max_occupancy = 80 # in percent %
    # Represents the occupancy a dock must have less than the target occupancy
    occupancy_maring = 10 # in percent %

    @classmethod
    def init(cls, docks, bikes, adj, distances):
        cls.docks =     docks
        cls.bikes =     bikes
        cls.adj =       adj
        cls.distances = distances

    @classmethod
    def find_starting_dock(cls, lat: float, long: float, alt: float) -> tuple[Dock, list[Destination]]:
        """
        Returns the nearest suitable dock and a list of suggestions

        lat, long, alt: float
            User's current coordinates
        """
        suitable: list[Dock] = []
        smallest: Dock = cls.docks[0]
        smallest_value: float = Dock.euclidian_distance_point(cls.docks[0], lat, long, alt)

        x = 0
        for dock in cls.docks:
            d = Dock.euclidian_distance_point(dock, lat, long, alt)
            if d < cls.max_radius:
                suitable.append(dock) # Finds all docks that may fit being a suggestion
            if d < smallest_value: # Finds the closest dock, even if not suitable
                smallest = dock
                smallest_value = d
            x += 1

        if smallest in suitable: suitable.remove(smallest)
        if suitable == []:
            return smallest, [] # No sugestion
        
        target_occupancy = min(
            cls.max_occupancy + cls.occupancy_maring,
            smallest.occupancy() + cls.occupancy_maring
        )
        print(target_occupancy)
        print([dock.occupancy() for dock in suitable])
        suitable = [dock for dock in suitable if dock.occupancy() > target_occupancy]

        return smallest, suitable
    
    @classmethod
    def find_strategy(cls, chosen_dock: Dock) -> tuple[Dock, list[Destination]]:
        """
        Returns list of goals as suggestions to user
        """
        return

    @classmethod
    def find_ending_dock(cls, lat: float, long: float, alt: float, current_bike: Bike) -> tuple[Dock, list[Destination]]:
        """
        Returns the nearest suitable dock and a list of suggestions

        lat, long, alt: float
            User's destination coordinates
        """
        return

def main(k: int = 5):
    docks = [
        Dock(0  , 0  , 0  , k),
        Dock(100, 0  , 100, k),
        Dock(200, 0  , 200, k),
        Dock(300, 100, 100, k),
    ]

    adj = [
        [0,1,0,1],
        [1,0,1,1],
        [0,1,0,1],
        [1,1,1,0],
    ]

    dis = []
    y = 0
    for adj_line in adj:
        dis_line = []
        x = 0
        for adj_element in adj_line:
            if adj_element == 0 or x == y:
                dis_line.append(None)
            else:
                dist = Dock.euclidian_distance(docks[x], docks[y])
                dis_line.append(dist)
            x += 1
        dis.append(dis_line)
        y += 1

    bikes = []
    bk = [1,4,5,4]
    bb = [50,20,10,100]
    i = 0
    for dock in docks:
        for x in range(bk[i]):
            bike = Bike(battery_level=bb[i])
            bikes.append(bike)
            dock.retrieve(bike)
        i += 1

    Main.init(docks, bikes, adj, dis)

    for dock in docks:
        print(dock)

    print(dis)
    print(Main.find_starting_dock(20, 30, 0))
main()