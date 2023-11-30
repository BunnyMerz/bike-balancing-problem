from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation
from examples.Simulation import Simulations

from src.sim import SimUser, SimulationResults, run as run_simulation
from src.program import Main

from utils.vis import Point

from random import randint as rng, seed, random

from utils.debug import Debug
log_print = lambda *a, **b: None
# log_print = print
# print = Debug.print
# seed(1923812938914922304923729987698877576)

class Results:
    def __init__(
            self, CantStart, CantPick, CantStartRun, CantDeliver, angry_users,
            total_suggestion_made, total_suggestion_taken, total_suggestion_completed,
            distance_travelled_walk, distance_travelled_bike, time_inside_system,
            dock_capacity, histogram
        ) -> None:
        self.CantStart= CantStart
        self.CantPick= CantPick
        self.CantStartRun= CantStartRun
        self.CantDeliver= CantDeliver

        self.angry_users = angry_users
        self.total_suggestion_made = total_suggestion_made
        self.total_suggestion_taken = total_suggestion_taken
        self.total_suggestion_completed = total_suggestion_completed

        self.distance_travelled_walk = distance_travelled_walk
        self.distance_travelled_bike = distance_travelled_bike
        self.time_inside_system = time_inside_system

        self.dock_capacity = dock_capacity
        self.histogram = histogram

    @classmethod
    def average(cls, results: list["Results"]):
        size = len(results)
        def avg_hist(histograms: list[list[int]]):
            size = len(histograms)
            w = len(histograms[0])
            r = [0 for _ in range(w)]
            for h in histograms:
                for c in range(w):
                    r[c] += h[c]
            r = [round(v/size, 2) for v in r]
            return r
        return Results(
            CantStart= sum([r.CantStart for r in results])/size,
            CantPick= sum([r.CantPick for r in results])/size,
            CantStartRun= sum([r.CantStartRun for r in results])/size,
            CantDeliver= sum([r.CantDeliver for r in results])/size,

            angry_users = sum([r.angry_users for r in results])/size,
            total_suggestion_made = sum([r.total_suggestion_made for r in results])/size,
            total_suggestion_taken = sum([r.total_suggestion_taken for r in results])/size,
            total_suggestion_completed = sum([r.total_suggestion_completed for r in results])/size,

            distance_travelled_walk = sum([r.distance_travelled_walk for r in results])/size,
            distance_travelled_bike = sum([r.distance_travelled_bike for r in results])/size,
            time_inside_system = sum([r.time_inside_system for r in results])/size,

            dock_capacity = sum([r.dock_capacity for r in results])/size,
            histogram = avg_hist([r.histogram for r in results]),
        )

    def print(self):
        print(f"""  Problems reported:
        CantStart:    {self.CantStart}
        CantPick:     {self.CantPick}
        CantStartRun: {self.CantStartRun}
        CantDeliver:  {self.CantDeliver}

        Total Angry Users: {self.angry_users}""")
        print(f"""  Suggestions:
            Made:      {self.total_suggestion_made}
            Acepted:   {self.total_suggestion_taken}
            Completed: {self.total_suggestion_completed}""")

        print(f"""  Averages:
            Distance walking:   {self.distance_travelled_walk}
            Distance cycling:   {self.distance_travelled_bike}
            Time inside system: {self.time_inside_system}""")
        print(f"Bike amount histogram 0..{self.dock_capacity}:", self.histogram)
    # def log_print(self):
    #     log_print([
    #         len([x for x in users if x.state == x.CantStart]),
    #         len([x for x in users if x.state == x.CantPick]),
    #         len([x for x in users if x.state == x.CantStartRun]),
    #         len([x for x in users if x.state == x.CantDeliver]),
    #     ])
    #     log_print([
    #         int(sum([x.distance_travelled_walk for x in users])/len(users)),
    #         int(sum([x.distance_travelled_bike for x in users])/len(users)),
    #         int(sum([x.time_inside_system() for x in users])/len(users)),
    #     ])
    #     log_print([
    #         SimulationResults.total_suggestion_made,
    #         SimulationResults.total_suggestion_taken,
    #         SimulationResults.total_suggestion_completed,
    #         SimulationResults.angry_users,
    #     ])
    #     log_print(hist)


def main():
    # print(f"Users have {SimUser.chance_to_follow_suggestion * 100}% chance to follow suggestion")
    docks, bikes, adj = Simulations.BigGrid.build()
    users = Simulations.BigGrid.create_users()

    run_simulation(users)

    for dock in docks:
        assert dock.interested_delivery == 0
        assert dock.interested_picking == 0

    hist = [0 for _ in range(docks[0].capacity + 1)]
    for dock in docks:
        hist[dock.bike_count()] += 1
    r = Results(
        CantStart =    len([x for x in users if x.state == x.CantStart]),
        CantPick =     len([x for x in users if x.state == x.CantPick]),
        CantStartRun = len([x for x in users if x.state == x.CantStartRun]),
        CantDeliver =  len([x for x in users if x.state == x.CantDeliver]),

        angry_users = SimulationResults.angry_users,
        total_suggestion_made = SimulationResults.total_suggestion_made,
        total_suggestion_taken = SimulationResults.total_suggestion_taken,
        total_suggestion_completed = SimulationResults.total_suggestion_completed,

        distance_travelled_walk = sum([x.distance_travelled_walk for x in users]),
        distance_travelled_bike = sum([x.distance_travelled_bike for x in users]),
        time_inside_system = sum([x.time_inside_system() for x in users]),

        dock_capacity= max(dock.capacity for dock in docks),
        histogram=hist
    )

    Main.plot()
    return r

if __name__ == "__main__":
    repeat = 1
    global_seed = random()
    for x in [0, 0.5, 0.8, 1]:
        SimUser.chance_to_follow_suggestion = x
        log_print(SimUser.chance_to_follow_suggestion * 100)
        log_print(repeat)
        print('=====---------=====')
        print(f"{SimUser.chance_to_follow_suggestion * 100}% on {repeat} times")
        try_round = []
        seed(global_seed)
        for _ in range(repeat):
            results = main()
            try_round.append(results)
            SimulationResults.reset()
            Point.clear_points()
        print("Avg")
        avg_r = Results.average(try_round)
        avg_r.print()
        print('=====---------=====')
        