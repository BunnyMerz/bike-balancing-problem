from heatmapper.values_to_maps import save_to_file_maps

from examples.graphs.graph_loader import GraphLoader

from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation
from examples.Simulation import Simulations

from src.bikes import to_map
from src.sim import SimUser, SimulationResults, run as run_simulation
from src.program import Main

from utils.vis import Point

from random import randint as rng, seed, random
from numpy import array as np_array, mean as np_mean
from scipy.stats import sem, t


from utils.debug import Debug
log_print = lambda *a, **b: None
# log_print = print
# print = Debug.print
# seed(1923812938914922304923729987698877576)

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np_array(data)
    n = len(a)
    mean, se = np_mean(a), sem(a)
    error = se * t.ppf((1 + confidence) / 2., n-1)
    return round(mean, 4), round(se, 4)

class Results:
    def __init__(
            self, CantStart, CantPick, CantStartRun, CantDeliver, angry_users,
            total_suggestion_made, total_suggestion_taken, total_suggestion_completed,
            total_trips, completed_trips,
            distance_travelled_walk, distance_travelled_walk_success, distance_travelled_walk_failed,
            distance_travelled_bike, distance_travelled_bike_success, distance_travelled_bike_failed,
            time_inside_system,
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

        self.total_trips = total_trips
        self.completed_trips = completed_trips

        self.distance_travelled_walk = distance_travelled_walk
        self.distance_travelled_walk_success = distance_travelled_walk_success
        self.distance_travelled_walk_failed = distance_travelled_walk_failed

        self.distance_travelled_bike = distance_travelled_bike
        self.distance_travelled_bike_success = distance_travelled_bike_success
        self.distance_travelled_bike_failed = distance_travelled_bike_failed
        
        self.time_inside_system = time_inside_system

        self.dock_capacity = dock_capacity
        self.histogram = histogram


    @classmethod
    def avg_users(cls, users: list[SimUser], get_attr):
        if len(users) == 0: return 0
        return sum([get_attr(x) for x in users])/len(users)

    @classmethod
    def average(cls, results: list["Results"]):
        size = len(results)
        def avg_hist(histograms: list[list[int]]):
            size = len(histograms)
            w = len(histograms[0])
            medias = [0 for _ in range(w)]
            erros = [0 for _ in range(w)]
            for c in range(w):
                values = []
                for h in histograms:
                    values.append(h[c])
                mean, error = mean_confidence_interval(values)
                medias[c] = mean
                erros[c] = error
            return medias, erros
        return MeanResults(
            CantStart= mean_confidence_interval([r.CantStart for r in results]),
            CantPick= mean_confidence_interval([r.CantPick for r in results]),
            CantStartRun= mean_confidence_interval([r.CantStartRun for r in results]),
            CantDeliver= mean_confidence_interval([r.CantDeliver for r in results]),

            angry_users = mean_confidence_interval([r.angry_users for r in results]),
            total_suggestion_made = mean_confidence_interval([r.total_suggestion_made for r in results]),
            total_suggestion_taken = mean_confidence_interval([r.total_suggestion_taken for r in results]),
            total_suggestion_completed = mean_confidence_interval([r.total_suggestion_completed for r in results]),

            total_trips=mean_confidence_interval([r.total_trips for r in results]),
            completed_trips=mean_confidence_interval([r.completed_trips for r in results]),

            distance_travelled_walk = mean_confidence_interval([r.distance_travelled_walk for r in results]),
            distance_travelled_walk_success = mean_confidence_interval([r.distance_travelled_walk_success for r in results]),
            distance_travelled_walk_failed = mean_confidence_interval([r.distance_travelled_walk_failed for r in results]),
            
            distance_travelled_bike = mean_confidence_interval([r.distance_travelled_bike for r in results]),
            distance_travelled_bike_success = mean_confidence_interval([r.distance_travelled_bike_success for r in results]),
            distance_travelled_bike_failed = mean_confidence_interval([r.distance_travelled_bike_failed for r in results]),

            time_inside_system = mean_confidence_interval([r.time_inside_system for r in results]),

            dock_capacity = mean_confidence_interval([r.dock_capacity for r in results]),
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
        
        print(f"""  Trips:
            Total:     {self.total_trips}
            Completed: {self.completed_trips}""")

        print(f"""  Averages:
            Distance walking total:   {self.distance_travelled_walk}
            Distance walking succe:   {self.distance_travelled_walk_success}
            Distance walking fail:    {self.distance_travelled_walk_failed}

            Distance cycling total:   {self.distance_travelled_bike}
            Distance cycling succe:   {self.distance_travelled_bike_success}
            Distance cycling fail:   {self.distance_travelled_bike_failed}

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

class MeanResults(Results):
    pass

def main():
    # print(f"Users have {SimUser.chance_to_follow_suggestion * 100}% chance to follow suggestion")
    nikiti = GraphLoader('niteroi')
    docks = nikiti.docks
    s_intes = nikiti.start_interests
    e_intes = nikiti.end_interests
    Main.init(docks=nikiti.docks, bikes=nikiti.bikes, adj=nikiti.adj, distances=nikiti.dist)
    Main.plot()
    SimUser.show()
    users = Simulations.BigGrid.create_users(s_intes, e_intes)

    run_simulation(users)
    SimUser.reset_points()

    for dock in docks:
        assert dock.interested_delivery == 0
        assert dock.interested_picking == 0

    hist = [0 for _ in range(36)]
    for dock in docks:
        hist[min(35, dock.bike_count())] += 1

    
    r = Results(
        CantStart =    len([x for x in users if x.state == x.CantStart]),
        CantPick =     len([x for x in users if x.state == x.CantPick]),
        CantStartRun = len([x for x in users if x.state == x.CantStartRun]),
        CantDeliver =  len([x for x in users if x.state == x.CantDeliver]),

        angry_users = SimulationResults.angry_users,
        total_suggestion_made = SimulationResults.total_suggestion_made,
        total_suggestion_taken = SimulationResults.total_suggestion_taken,
        total_suggestion_completed = SimulationResults.total_suggestion_completed,

        total_trips=len(users),
        completed_trips=len([x for x in users if x.state == x.Idle]),

        distance_travelled_walk =         Results.avg_users([user for user in users                                                    ], lambda x: x.distance_travelled_walk),
        distance_travelled_walk_success = Results.avg_users([user for user in users if len(user.achieved_goals) > 0                    ], lambda x: x.distance_travelled_walk),
        distance_travelled_walk_failed =  Results.avg_users([user for user in users if user.angry > 0 and len(user.achieved_goals) == 0], lambda x: x.distance_travelled_walk),

        distance_travelled_bike         =  Results.avg_users([user for user in users                                                    ], lambda x: x.distance_travelled_bike),
        distance_travelled_bike_success =  Results.avg_users([user for user in users if len(user.achieved_goals) > 0                    ], lambda x: x.distance_travelled_bike),
        distance_travelled_bike_failed  =  Results.avg_users([user for user in users if user.angry > 0 and len(user.achieved_goals) == 0], lambda x: x.distance_travelled_bike),

        time_inside_system = sum([x.time_inside_system() for x in users]),

        dock_capacity= max(dock.capacity for dock in docks),
        histogram=hist
    )

    
    return r

if __name__ == "__main__":
    repeat = 2
    global_seed = random()
    global_seed = 0.4294814496825895
    averages: list[MeanResults] = []
    for x in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        SimUser.chance_to_follow_suggestion = x
        log_print(SimUser.chance_to_follow_suggestion * 100)
        log_print(repeat)
        print('=====---------=====')
        print(f"{SimUser.chance_to_follow_suggestion * 100}% on {repeat} times")
        try_round = []
        cap = [0, 0]
        seed(global_seed)
        for _ in range(repeat):
            SimulationResults.reset()
            Point.clear_points()
            results = main()
            try_round.append(results)
            for d in Main.docks:
                if d.empty():
                    cap[0] += 1
                if d.full():
                    cap[1] += 1
        print("cap", cap)
        # Main.show()
        # input("Next? Press enter...")
        save_to_file_maps(Main.to_map())
        print("Avg")
        avg_r = Results.average(try_round)
        # avg_r.print()
        averages.append(avg_r)
        print('=====---------=====')

    CantPick= [[], []]
    CantDeliver= [[], []]

    angry_users = [[], []]

    total_suggestion_made = [[], []]
    total_suggestion_taken = [[], []]
    total_suggestion_completed = [[], []]

    completed_trips = [[], []]

    distance_travelled_walk = [[], []]
    distance_travelled_walk_success = [[], []]
    distance_travelled_walk_failed = [[], []]

    distance_travelled_bike = [[], []]
    distance_travelled_bike_success = [[], []]
    distance_travelled_bike_failed = [[], []]
    for v in averages:
        CantPick[0].append(v.CantPick[0])
        CantPick[1].append(v.CantPick[1])
        CantDeliver[0].append(v.CantDeliver[0])
        CantDeliver[1].append(v.CantDeliver[1])

        angry_users[0].append(v.angry_users[0])
        angry_users[1].append(v.angry_users[1])
        total_suggestion_made[0].append(v.total_suggestion_made[0])
        total_suggestion_made[1].append(v.total_suggestion_made[1])
        total_suggestion_taken[0].append(v.total_suggestion_taken[0])
        total_suggestion_taken[1].append(v.total_suggestion_taken[1])
        total_suggestion_completed[0].append(v.total_suggestion_completed[0])
        total_suggestion_completed[1].append(v.total_suggestion_completed[1])

        completed_trips[0].append(v.completed_trips[0])
        completed_trips[1].append(v.completed_trips[1])

        distance_travelled_walk[0].append(v.distance_travelled_walk[0])
        distance_travelled_walk[1].append(v.distance_travelled_walk[1])
        distance_travelled_walk_success[0].append(v.distance_travelled_walk_success[0])
        distance_travelled_walk_success[1].append(v.distance_travelled_walk_success[1])
        distance_travelled_walk_failed[0].append(v.distance_travelled_walk_failed[0])
        distance_travelled_walk_failed[1].append(v.distance_travelled_walk_failed[1])

        distance_travelled_bike[0].append(v.distance_travelled_bike[0])
        distance_travelled_bike[1].append(v.distance_travelled_bike[1])
        distance_travelled_bike_success[0].append(v.distance_travelled_bike_success[0])
        distance_travelled_bike_success[1].append(v.distance_travelled_bike_success[1])
        distance_travelled_bike_failed[0].append(v.distance_travelled_bike_failed[0])
        distance_travelled_bike_failed[1].append(v.distance_travelled_bike_failed[1])

    print("CantPick:", CantPick)
    print("CantDeliver:", CantDeliver)

    print("angry_users:", angry_users)
    print("total_suggestion_made:", total_suggestion_made)
    print("total_suggestion_taken:", total_suggestion_taken)
    print("total_suggestion_completed:", total_suggestion_completed)

    print("completed_trips:", completed_trips)

    print("distance_travelled_walk:", distance_travelled_walk)
    print("distance_travelled_walk_success:", distance_travelled_walk_success)
    print("distance_travelled_walk_failed:", distance_travelled_walk_failed)

    print("distance_travelled_bike:", distance_travelled_bike)
    print("distance_travelled_bike_success:", distance_travelled_bike_success)
    print("distance_travelled_bike_failed:", distance_travelled_bike_failed)
        