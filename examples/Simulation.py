from random import randint as rng, random

from examples.graphs.graph_loader import EndInterest, StartInterest

from src.sim import SimUser, Clock
from src.bikes import Dock, Bike, to_map
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
        def create_users(cls, start_interests: list[StartInterest], end_interest: list[EndInterest]):
            docks = Main.docks
            wd = len(docks)-1
            users: list[SimUser] = []

            user_amount = 8000
            start_time = Clock.from_hours(6) # 6am
            end_time = Clock.from_hours(23) # 6am

            time_spam = end_time - start_time
            group_size = 30
            group_amount = user_amount/group_size
            step = time_spam/group_amount

            for x in range(user_amount):
                timer = (x//group_size * step) + start_time # Start at 6am
                hours_timer = Clock.to_hours(timer)
                if random() > 0.6:
                    _s = docks[rng(0,wd)]
                    _f = docks[rng(0,wd)]
                    while(_f == _s): _f = docks[rng(0,wd)]
                    _s = _s.rng_geo_position(30)
                    _f = _f.rng_geo_position(30)
                else:
                    _s = StartInterest.decide(hours_timer, start_interests)
                    _f = _s.suggest_end(hours_timer, end_interest).rng_geo_position()
                    _s = _s.rng_geo_position()
                sim = SimUser(
                    _s,
                    _f,
                    offset_timer = timer
                )
                # Main.later_to_map.append(
                #     (*_s[:2], 1)
                # )
                # Main.later_to_map.append(
                #     (*_f[:2], 1)
                # )
                # SimUser.custom_plot(*_s[:2], 'green', ',', 0.1)
                # SimUser.custom_plot(*_f[:2], 'blue', ',', 0.1)
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
                    dock.add_bike(bike)
                i += 1

            Main.init_from_basic(docks, bikes, adj)
            return docks, bikes, adj