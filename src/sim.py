from random import random, randint as rng
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

class SimulationResults:
    total_suggestion_made = 0
    total_suggestion_taken = 0
    total_suggestion_completed = 0
    angry_users = 0

GeoPosition = tuple[float, float, float]
class SimUser:
    Start  = 0
    ToInitialDock = 1
    ToSubWithFull = 2
    ToSubWithEmpty = 3
    ToEnd  = 4
    Done = 5
    Idle = 6
    CantStart = 7
    CantPick = 8
    CantStartRun = 9
    CantDeliver = 10

    state_names = [
        "At Start",
        "InitDock",
        "SubWFull",
        "SubWEmpt",
        "ToTheEnd",
        "--Done--",
        "--Idle--",
        "--CtSt--",
        "--CtPi--",
        "--CtSR--",
        "--CtDe--",
    ]

    chance_to_follow_suggestion = 1
    def __init__(self, current_location: GeoPosition, destination: GeoPosition, user_obj: User | None = None, offset_timer: float = 0) -> None:
        self.user_obj: User | None = user_obj

        self.dest: GeoPosition = destination
        self.current_location: GeoPosition = current_location
        self.current_bike: Bike = None
        self.current_dock: Dock = None

        self.internal_clock = Clock()
        self.internal_clock.set(offset_timer)
        self.state = SimUser.Start

        self.active_goal: Goal = None
        self.achieved_goals = []

        self.system_entry_time: float = None
        self.system_exit_time: float = None

    def __str__(self) -> str:
        base          = f"<User[t:{int(self.internal_clock.t)}][{self.state_names[self.state]}]({len(self.achieved_goals)}):"
        pos           = f"{self.current_location} -> {self.dest}"
        current_dock  = f"{', CurrentDock: '+self.current_dock.simple() if self.current_dock is not None else ''}"
        time = ''
        if self.system_entry_time is not None and self.system_exit_time is not None:
            if self.canceled_use():
                time          = f", Canceled trip!"
            else:
                time          = f", Total time taken {int(self.system_entry_time)}..{int(self.system_exit_time)}"
        else:
            if self.current_bike is not None:
                time = f', Bike: {self.current_bike}'
        end = '>'
        return base + pos + current_dock + time + end
    
    def canceled_use(self):
        return self.system_entry_time is not None and self.system_exit_time is not None and self.system_entry_time - self.system_exit_time == 0

    def done(self):
        return self.state >= 6

    def follow_suggestion(self, natural: Dock, suggestion: Goal):
        return random() < self.chance_to_follow_suggestion

    def act(self):
        if self.done(): return
        [
            self.StateStart,
            self.StateToInitialDock,
            self.StateToSubWithFull,
            self.StateToSubWithEmpty,
            self.StateToEnd,
            self.StateDone
        ][self.state]()

    def StateStart(self):
        print("Start")
        natural, suggestion = Main.find_starting_dock(*self.current_location)
        if suggestion.initial_dest.suitable != []: SimulationResults.total_suggestion_made += 1
        if (
            self.follow_suggestion(natural, suggestion)
            and suggestion.initial_dest.suitable != []
        ):                    # Will follow suggestion and go to random suggestion
            print("Suggested Start")
            SimulationResults.total_suggestion_taken += 1
            self.state = SimUser.ToInitialDock

            s = suggestion.initial_dest.suitable
            self.current_dock = s[rng(0, len(s)-1)]
            self.active_goal = suggestion

            self.internal_clock.add_time_taken_from_to_point(self.current_dock, *self.current_location, has_bike=False)
            self.current_location = self.current_dock.coords()
            self.current_dock.show_picking_interest()
        elif natural != None: # User will go straight to starting Dock
            print("Natural Start")
            self.state = SimUser.ToInitialDock

            self.current_dock = natural

            self.internal_clock.add_time_taken_from_to_point(self.current_dock, *self.current_location, has_bike=False)
            self.current_location = self.current_dock.coords()
        else:                 # No Option. User gets upset and gives up on using system
            print("No option")
            self.state = SimUser.CantStart # TODO: Better behaviour in case of upsetting the user. Save to some variable later?
            SimulationResults.angry_users += 1

    def StateToInitialDock(self):
        print("ToInitialDock")
        if self.active_goal is not None: # User took a suggestion, check if he succeded
            # Only previous state was Start, thus only check self.current_dock
            if self.active_goal.validate(self.current_dock, self.active_goal.initial_dest):
                self.achieved_goals.append(self.active_goal)
                self.active_goal = None
                SimulationResults.total_suggestion_completed += 1
                self.current_dock.done_with_picking_interest()
            else:
                self.current_dock.lose_picking_interest()


        if not self.current_dock.empty():
            self.current_bike = self.current_dock.pick_any()
            natural, suggestion = Main.find_ending_dock(*self.dest, self.current_bike)
            if suggestion.type == suggestion.OnlyEnd and suggestion.end_dest.suitable != []: SimulationResults.total_suggestion_made += 1
            if (
                suggestion.type == suggestion.OnlyEnd
                and suggestion.end_dest.suitable != []
                and self.follow_suggestion(natural, suggestion)
            ):                    # Will follow suggestion and go to random suggestion
                print("Suggested End")
                SimulationResults.total_suggestion_taken += 1
                self.state = SimUser.ToEnd

                s = suggestion.end_dest.suitable
                self.current_dock = s[rng(0, len(s)-1)]
                self.active_goal = suggestion

                self.system_entry_time = self.internal_clock.t
                self.internal_clock.add_time_taken_from_to_point(self.current_dock, *self.current_location, has_bike=True)
                self.current_location = self.current_dock.coords()
                self.current_dock.show_deliver_interest()
            elif natural != None: # User will go straight to ending Dock
                print("Natural End")
                self.state = SimUser.ToEnd

                self.current_dock = natural

                self.system_entry_time = self.internal_clock.t
                self.internal_clock.add_time_taken_from_to_point(self.current_dock, *self.current_location, has_bike=False)
                self.current_location = self.current_dock.coords()
            else:                 # No Option. User gets upset and gives up on using system
                print("No option")
                self.current_dock.retrieve(self.current_bike)
                self.current_bike = None
                self.current_dock = None
                self.state = SimUser.CantStartRun # TODO: Better behaviour in case of upsetting the user. Save to some variable later?
        else: # User reached an Empty Dock. User gets upset and gives up on using system
            self.state = SimUser.CantPick # TODO: Better behaviour in case of upsetting the user. Save to some variable later?

    def StateToSubWithFull(self):
        return
    def StateToSubWithEmpty(self):
        return
    def StateToEnd(self):
        print("ToEnd")
        if self.active_goal is not None and self.active_goal.type == Goal.OnlyEnd:
            if self.active_goal.validate(self.current_dock, self.active_goal.end_dest):
                SimulationResults.total_suggestion_completed += 1
                self.achieved_goals.append(self.active_goal)
                self.active_goal = None
                self.current_dock.done_with_deliver_interest()
            else:
                self.current_dock.lose_deliver_interest()

        if not self.current_dock.full():
            print("Not full end, retrieving.")
            self.current_dock.retrieve(self.current_bike)
            self.current_bike = None
            self.current_dock = None
            self.state = SimUser.Done
        else:
            # TODO: Fix this later, he should look for another dock to leave his Bike. Find_ending_dock should do the trick
            self.state = SimUser.CantDeliver
            SimulationResults.angry_users += 1
            

    def StateDone(self):
        self.system_exit_time = self.internal_clock.t
        self.state = self.Idle