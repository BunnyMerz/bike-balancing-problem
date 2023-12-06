from random import randint as rng

from src.sim import SimUser
from src.bikes import Dock, Bike
from src.program import Main

from utils.debug import Debug
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
        def create_users(cls):
            docks = Main.docks
            wd = len(docks)-1
            users: list[SimUser] = []
            for x in range(10000):
                _s = docks[rng(0,wd)]
                _f = docks[rng(0,wd)]
                while(_f == _s): _f = docks[rng(0,wd)]
                sim = SimUser(
                    (_s.latitude + rng(-100,100), _s.longitude + rng(-100,100), _s.latitude),
                    (_f.latitude + rng(-100,100), _f.longitude + rng(-100,100), _f.latitude),
                    offset_timer= x//30 * 500
                )
                users.append(sim)
            return users
        @classmethod
        def build(cls, k = 9):
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
                for x in range(4):
                    bike = Bike(battery_level=50)
                    bikes.append(bike)
                    dock.retrieve(bike)
                i += 1

            Main.init_from_basic(docks, bikes, adj)
            return docks, bikes, adj