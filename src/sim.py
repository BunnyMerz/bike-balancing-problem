from random import random
from typing import Callable

from src.bikes import Dock, Bike, User
from src.goals import Goal, PickBike
from src.program import Main


class Clock:
    dist_to_time_walk = 4 # 4 meter = 1 minute
    dist_to_time_bike = 1 # 1 meter = 1 minute
    def __init__(self) -> None:
        self.t = 0.0

    def delay(self, _o: float):
        self.t += _o
    def set(self, _o: float):
        self.t = _o
    def wait_until(self, _o: float):
        if _o > self.t:
            self.t = _o

    def add_time_taken_from_to_dock(self, dock1: Dock, dock2: Dock, has_bike: bool):
        return Dock.euclidian_distance(dock1, dock2) * [Clock.dist_to_time_walk, Clock.dist_to_time_bike][has_bike]
    
    def add_time_taken_from_to_point(self, dock1: Dock, lat: float, long: float, alt: float, has_bike: bool):
        return Dock.euclidian_distance_point(dock1, lat, long, alt) * [Clock.dist_to_time_walk, Clock.dist_to_time_bike][has_bike]


GeoPosition = tuple[float, float, float]
class SimUser:
    Start  = 0
    ToInitialDock = 1
    ToSubWithFull = 2
    ToSubWithEmpty = 3
    ToEnd  = 4
    Done = 5

    chance_to_follow_suggestion = 0.5
    def __init__(self) -> None:
        self.dest: Dock = None
        self.user_obj: User = None

        self.current_location: GeoPosition = None
        self.current_bike: Bike = None
        self.current_dock: Dock = None

        self.swap_bike_desc: PickBike = None

        self.internal_clock = Clock()
        self.state = 0

        self.active_goal = None
        self.achieved_goals = []

    def follow_suggestion(self, suggestion: Goal):
        return random() < self.chance_to_follow_suggestion

    def act(self):
        [
            self.StateStart,
            self.StateToInitialDock,
            self.StateToSubWithFull,
            self.StateToSubWithEmpty,
            self.StateToEnd
        ]
        [self.state]()

    def StateStart(self):
        natural, suggestion = Main.find_starting_dock(*self.current_location)
        if (
            self.follow_suggestion(natural, suggestion)
            and suggestion.initial_dest.suitable != []
        ):                    # Will follow suggestion and go to random suggestion
            self.state = SimUser.ToInitialDock

            self.current_dock = suggestion.initial_dest.suitable[0]
            self.active_goal = suggestion

            self.internal_clock.add_time_taken_from_to_point(self.current_dock, *self.current_location)
            self.current_location = self.current_dock.coords()
        elif natural != None: # User will go straight to starting Dock
            self.state = SimUser.ToInitialDock

            self.current_dock = natural

            self.internal_clock.add_time_taken_from_to_point(self.current_dock, *self.current_location)
            self.current_location = self.current_dock.coords()
        else:                 # No Option. User gets upset and gives up on using system
            self.state = SimUser.Done

    def StateToInitialDock(self):
        if self.active_goal is not None: # User took a suggestion, check if he succeded
            # Only previous state was Start, thus only check self.current_dock
            if self.active_goal.validate(self.current_dock, self.active_goal.initial_dest):
                self.achieved_goals.append(self.active_goal)
                self.active_goal = None

        natural, suggestion = Main.find_strategy(*self.current_location, self.current_dock)

    def StateToSubWithFull(self):
        return
    def StateToSubWithEmpty(self):
        return
    def StateToEnd(self):
        return