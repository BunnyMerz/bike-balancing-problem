from bikes import Dock, Bike, User


class Clock:
    def __init__(self) -> None:
        self.t = 0.0

    def delay(self, _o: float):
        self.t += _o
    def set(self, _o: float):
        self.t = _o
    def wait_until(self, _o: float):
        if _o > self.t:
            self.t = _o

class Trip:
    def __init__(self, dests, start_time):
        self.dest = dests
        self.start_time = start_time

    def cost(self) -> tuple[float, float]:
        return # Get the cost btw each dest and retur. Distance and Time
    @property
    def end_location(self):
        return self.dest[-1]

class Schedule:
    def __init__(self, current_location, destinations: list[Trip]):
        self.current_location = current_location
        self.destinations = destinations
        self.i = 0

    def get_bike(self) -> Bike:
        start = self.current_location
        end = self.destination.end_location
        dock = Dock() ## start.dock
        if dock != None:
            # algorithm call, returns Bike
            # bike = decide(dock, start, end, user)
            pass
        return Bike()

    @property
    def destination(self):
        if self.ended:
            return None
        return self.destinations[self.i]
    def next_dest(self):
        self.current_location = self.destination
        self.i += 1
    @property
    def ended(self):
        return self.i >= len(self.destinations)

class Entity:
    def __init__(self, user: User, schedule: Schedule, starting_location):
        self.bike = None
        self.user = user
        self.schedule = schedule
        self.c = Clock()
        self.buffered_actions = [["NextEvent"]]

    def __call__(self):
        if self.buffered_actions != []:
            return self.act()
        if self.schedule.ended:
            return
        
        # If it isn't the time for the next destination, raise an exception or warning, for debugging
        if self.schedule.destination.start_time != self.c.t:
            self.buffered_actions += [
                ["NextEvent"]
            ]
            return
        
        possible_bike = self.schedule.get_bike()
        if possible_bike != None:
            distance_cost, time_cost = self.schedule.destination.cost()
            possible_bike.travel(distance_cost, time_cost)
            self.buffered_actions += [
                ["ReleaseBike", self.c.t + time_cost]
            ]
        self.schedule.next_dest()
        self.buffered_actions += [
            ["NextEvent"]
        ]

        

    def act(self):
        action = self.buffered_actions.pop(0)

        if action[0] == "NextEvent":
            if self.schedule.destination == None: return
            self.buffered_actions += [
                ["WaitUntil", self.schedule.destination.start_time]
            ]
        if action[0] == "WaitUntil":
            self.c.wait_until(action[1])
        # if NextDest, buffer WaitUntil, release bike if any, schedule.next_dest()