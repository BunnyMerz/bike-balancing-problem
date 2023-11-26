from debug import Debug
from bikes import Dock, Bike
print = Debug.print


class Main:
    docks =     []
    bikes =     []
    adj =       []
    distances = []

    @classmethod
    def find_starting_dock(cls, lat: float, long: float, alt: float) -> tuple[Dock, list[Dock]]:
        """
        Returns the nearest suitable dock and a list of suggestions

        lat, long, alt: float
            User's current coordinates
        """
        return
    
    def find_strategy(cls):
        """
        Returns 
        """
        return
    
    @classmethod
    def find_ending_dock(cls, x: float, y: float) -> tuple[Dock, list[Dock]]:
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
main()