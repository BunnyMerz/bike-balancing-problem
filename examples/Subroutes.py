from utils.debug import Debug
from src.bikes import Dock, Bike
from src.program import Main
print = Debug.labeld_print(label="CaseStudy")


class ChooseSubStation:
    class LowBattery_ChargeableSubRoute_AnyEnd:
        """Low battery bike at starting dock, chargeable sub-route with normal battery bike in it, with non-chargeable end"""

    class HighBattery_LowOnSubRoute_ChargeableEnd:
        """Normal battery bike at starting dock, Low battery at sub-route, with chargeable end"""

    class LowBattery_ChargeableEnd:
        """Low battery bike at starting dock, with ending as charging"""
        @classmethod
        def run(cls, k = 5):
            docks = [
                Dock(0  , 0  , 0  , k, charges=False),
                Dock(100, 100, 0  , k, charges=True),
                Dock(200, 200, 0  , k, charges=True),
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
                [100,10,100,15],
                [100,10],
                [100],
                [50,20,10],8
            ]
            i = 0
            for dock in docks:
                for x in range(len(bb[i])):
                    bike = Bike(battery_level=bb[i][x])
                    bikes.append(bike)
                    dock.retrieve(bike)
                i += 1

            Main.init_from_basic(docks, bikes, adj, number_of_suggestions=2)

            natural, suggestions = Main.find_strategy(300, 100, 0, docks[0])
            assert natural == docks[3]
            assert suggestions.initial_bike.suitable == [docks[0].bikes[1], docks[0].bikes[3]]
            assert suggestions.end_dest.suitable == [docks[3]]