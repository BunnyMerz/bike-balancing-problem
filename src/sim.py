from random import random
from typing import Callable

from src.bikes import Dock, Bike, User
from src.goals import Goal, PickBike
from src.program import Main

from utils.debug import Debug
print = Debug.labeld_print("Simulator")


class Clock:
    dist_to_time_walk = 10/10 # 10 seconds = 10 meters
    dist_to_time_bike = 2/10  # 2  seconds = 10 meters
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
        t = Dock.euclidian_distance(dock1, dock2) * [Clock.dist_to_time_walk, Clock.dist_to_time_bike][has_bike]
        self.delay(t)
    
    def add_time_taken_from_to_point(self, dock1: Dock, lat: float, long: float, alt: float, has_bike: bool):
        t = Dock.euclidian_distance_point(dock1, lat, long, alt) * [Clock.dist_to_time_walk, Clock.dist_to_time_bike][has_bike]
        self.delay(t)


GeoPosition = tuple[float, float, float]
class SimUser:
    Start  = 0
    ToInitialDock = 1
    ToSubWithFull = 2
    ToSubWithEmpty = 3
    ToEnd  = 4
    Done = 5

    state_names = [
        "At Start",
        "InitDock",
        "SubWFull",
        "SubWEmpt",
        "ToTheEnd",
        "--Done--",
    ]

    chance_to_follow_suggestion = 0.5
    def __init__(self, current_location: GeoPosition, destination: GeoPosition, user_obj: User | None = None) -> None:
        self.user_obj: User | None = user_obj

        self.dest: GeoPosition = destination
        self.current_location: GeoPosition = current_location
        self.current_bike: Bike = None
        self.current_dock: Dock = None

        self.internal_clock = Clock()
        self.state = SimUser.Start

        self.active_goal = None
        self.achieved_goals = []

    def __str__(self) -> str:
        base          = f"<User[t:{int(self.internal_clock.t)}][{self.state_names[self.state]}]:"
        pos           = f"{self.current_location} -> {self.dest}"
        current_dock  = f"{', CurrentDock: '+self.current_dock.simple() if self.current_dock is not None else ''}>"
        return base + pos + current_dock

    def follow_suggestion(self, natural: Dock, suggestion: Goal):
        return random() < self.chance_to_follow_suggestion

    def act(self):
        [
            self.StateStart,
            self.StateToInitialDock,
            self.StateToSubWithFull,
            self.StateToSubWithEmpty,
            self.StateToEnd
        ][self.state]()

    def StateStart(self):
        print("Start")
        print(self.current_location)
        natural, suggestion = Main.find_starting_dock(*self.current_location)
        if (
            self.follow_suggestion(natural, suggestion)
            and suggestion.initial_dest.suitable != []
        ):                    # Will follow suggestion and go to random suggestion
            print("Suggested Start")
            self.state = SimUser.ToInitialDock

            self.current_dock = suggestion.initial_dest.suitable[0]
            self.active_goal = suggestion

            self.internal_clock.add_time_taken_from_to_point(self.current_dock, *self.current_location, has_bike=False)
            self.current_location = self.current_dock.coords()
        elif natural != None: # User will go straight to starting Dock
            print("Natural Start")
            self.state = SimUser.ToInitialDock

            self.current_dock = natural

            self.internal_clock.add_time_taken_from_to_point(self.current_dock, *self.current_location, has_bike=False)
            self.current_location = self.current_dock.coords()
            print("/////",self.current_dock.simple(), self.current_location, self.internal_clock.t)
        else:                 # No Option. User gets upset and gives up on using system
            print("No option")
            self.state = SimUser.Done

    def StateToInitialDock(self):
        print("ToInitialDock")
        if self.active_goal is not None: # User took a suggestion, check if he succeded
            # Only previous state was Start, thus only check self.current_dock
            if self.active_goal.validate(self.current_dock, self.active_goal.initial_dest):
                self.achieved_goals.append(self.active_goal)
                self.active_goal = None

        self.state = SimUser.Done
        # natural, suggestion = Main.find_strategy(*self.current_location, self.current_dock)

    def StateToSubWithFull(self):
        return
    def StateToSubWithEmpty(self):
        return
    def StateToEnd(self):
        return