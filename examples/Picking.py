from utils.debug import Debug
from src.bikes import Dock, Bike
from src.program import Main
from utils.vis import Point
print = Debug.labeld_print(label="CaseStudy")


class ChooseStartingStation:
    class NoSuggestion:
        @classmethod
        def run(cls, k = 5):
            docks = [
                Dock(0  , 0  , 0  , k, charges=True),
                Dock(100, 100, 0  , k, charges=True),
                Dock(200, 200, 0  , k, charges=False),
                Dock(300, 100, 100, k, charges=True),
            ]

            adj = [
                [0,1,0,1],
                [1,0,1,1],
                [0,1,0,1],
                [1,1,1,0],
            ]

            bikes = []
            bb = [
                [100],
                [100,10,100,15],
                [100,10,10,10,10],
                [50,20,10,10],
            ]
            i = 0
            for dock in docks:
                for x in range(len(bb[i])):
                    bike = Bike(battery_level=bb[i][x])
                    bikes.append(bike)
                    dock.add_bike(bike)
                i += 1

            Main.init_from_basic(docks, bikes, adj)

            x = 60
            y = 60
            natural, suggestions = Main.find_starting_dock(x, y, 0)
            assert natural == docks[1]
            assert suggestions.initial_dest.suitable == []
            Point(x,y, "Gray", "User", width=0.5)
            Point(natural.latitude,natural.longitude, "Gray", "Nat", width=0.5)
            

    class OneSuggestion:
        @classmethod
        def build(cls) -> tuple[list[Dock], list[Bike], list[list[int]]]:
            docks = [
                Dock(0  , 0  , 0  , 5, charges=True),
                Dock(100, 100, 0  , 5, charges=True),
                Dock(200, 200, 0  , 5, charges=False),
                Dock(300, 100, 0, 5, charges=True),
            ]

            adj = [
                [0,1,0,1],
                [1,0,1,1],
                [0,1,0,1],
                [1,1,1,0],
            ]

            bikes = []
            bb = [
                [100,10,100,15],
                [100],
                [100,10],
                [50,20,10,10],
            ]
            i = 0
            for dock in docks:
                for x in range(len(bb[i])):
                    bike = Bike(battery_level=bb[i][x])
                    bikes.append(bike)
                    dock.add_bike(bike)
                i += 1

            Main.init_from_basic(docks, bikes, adj)
            return docks, bikes, adj
        @classmethod
        def run(cls):
            docks, bikes, adj = cls.build()

            x = 60
            y = 60
            natural, suggestions = Main.find_starting_dock(x, y, 0)
            assert natural == docks[1]
            assert suggestions.initial_bike          == None
            assert suggestions.initial_dest.suitable == [docks[0]]
            assert suggestions.end_dest              == None
            assert suggestions.bike_swap             == None
            
            Point(x,y, "Gray", "User", width=0.5)
            Point(natural.latitude,natural.longitude, "Gray", "Nat\n\n\n", width=0.5)
            for sug in suggestions.initial_dest.suitable:
                Point(sug.latitude,sug.longitude, "Gray", "Sg\n\n\n", width=0.5)