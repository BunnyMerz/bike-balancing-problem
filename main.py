from debug import Debug
from bikes import Dock, Bike
from goals import Destination, PickBike, DeliverBike
print = Debug.print


class Main:
    docks:     list[Dock]        = []
    bikes:     list[Bike]        = []
    adj:       list[list[bool]]  = []
    distances: list[list[float]] = []

    @classmethod
    def init(cls, docks, bikes, adj, distances):
        docks =     docks
        bikes =     bikes
        adj =       adj
        distances = distances

    @classmethod
    def find_starting_dock(cls, lat: float, long: float, alt: float) -> tuple[Dock, list[Destination]]:
        """
        Returns the nearest suitable dock and a list of suggestions

        lat, long, alt: float
            User's current coordinates
        """
        return
    
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
    for dock in docks:
        for x in range(k):
            bike = Bike()
            bikes.append(bike)
            dock.retrieve(bike)

    Main.init(docks, bikes, adj, dist)
main()