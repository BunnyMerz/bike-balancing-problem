from utils.debug import Debug
from src.bikes import Dock, Bike
from src.program import Main
from utils.vis import Point
print = Debug.labeld_print(label="CaseStudy")


class ChooseEndStation:
    class Example1:
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
            bk = [1,4,5,4]
            bb = [50,20,10,100,30]
            i = 0
            for dock in docks:
                for x in range(bk[i]):
                    bike = Bike(battery_level=bb[x])
                    bikes.append(bike)
                    dock.add_bike(bike)
                i += 1

            Main.init_from_basic(docks, bikes, adj)

            x = 60
            y = 60
            z = 0
            natural, suggestions = Main.find_ending_dock(60, 60, 0, Bike(10))
            Point(x,y, "Gray", "Dest", width=0.6)
            assert natural == docks[1]
            assert suggestions.end_dest.suitable == [docks[0]]