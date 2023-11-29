from utils.debug import Debug
from src.bikes import Dock, Bike
from src.program import Main
from utils.vis import Point
print = Debug.labeld_print(label="CaseStudy")

def in_bounds(x, y, _x, _y):
    return (
        (x >= 0 and x < _x) and
        (y >= 0 and y < _y)
    )
class Simulations:
    class BigGrid:
        @classmethod
        def build(cls, k = 10, bike_amount = 2):
            docks: list[Dock] = []
            adj: list[list[int]] = []
            x_w = 6
            y_w = 6
            for y in range(0, y_w):
                for x in range(0, x_w):
                    docks.append(
                        Dock(x*100, y*100, 0, k, charges= bool(x%2))
                    )
                    connections = [0 for _ in range(x_w*y_w)] # TODO: Use numpy
                    up = (x, y+1)
                    down = (x, y-1)
                    right = (x+1, y)
                    left = (x-1, y)
                    for place in [up, down, right, left]:
                        local_x, local_y = place
                        if in_bounds(local_x, local_y, x_w, y_w):
                            connections[local_x + (local_y*x_w)] = 1
                    adj.append(connections)

            bikes = []
            i = 0
            for dock in docks:
                for x in range(bike_amount):
                    bike = Bike(battery_level=50)
                    bikes.append(bike)
                    dock.retrieve(bike)
                i += 1

            Main.init_from_basic(docks, bikes, adj)
            return docks, bikes, adj