from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation
from examples.Simulation import Simulations

from src.sim import SimUser, SimulationResults, run as run_simulation
from src.program import Main

from random import randint as rng, seed

from utils.debug import Debug
# print = Debug.print
# seed(1923812938914922304923729987698877576)


def main():
    # print(f"Users have {SimUser.chance_to_follow_suggestion * 100}% chance to follow suggestion")
    docks, bikes, adj = Simulations.BigGrid.build()
    users = Simulations.BigGrid.create_users()

    run_simulation(users)

    for dock in docks:
        assert dock.interested_delivery == 0
        assert dock.interested_picking == 0

    # print(label="step")
    # for user in users:
        # print(user, label="step")
    # print(f"""
    # Problems reported:
    #     CantStart:    {len([x for x in users if x.state == x.CantStart])}
    #     CantPick:     {len([x for x in users if x.state == x.CantPick])}
    #     CantStartRun: {len([x for x in users if x.state == x.CantStartRun])}
    #     CantDeliver:  {len([x for x in users if x.state == x.CantDeliver])}""")
    print([
        len([x for x in users if x.state == x.CantStart]),
        len([x for x in users if x.state == x.CantPick]),
        len([x for x in users if x.state == x.CantStartRun]),
        len([x for x in users if x.state == x.CantDeliver]),
    ])
    print([
        int(sum([x.distance_travelled_walk for x in users])/len(users)),
        int(sum([x.distance_travelled_bike for x in users])/len(users)),
        int(sum([x.time_inside_system() for x in users])/len(users)),
    ])
    # print(f"""
    # Suggestions:
    #     Made:      {SimulationResults.total_suggestion_made}
    #     Acepted:   {SimulationResults.total_suggestion_taken}
    #     Completed: {SimulationResults.total_suggestion_completed}
    # Total Angry Users: {SimulationResults.angry_users}""")
    print([
        SimulationResults.total_suggestion_made,
        SimulationResults.total_suggestion_taken,
        SimulationResults.total_suggestion_completed,
        SimulationResults.angry_users,
    ])
    
    hist = [0 for _ in range(docks[0].capacity + 1)]
    for dock in docks:
        hist[dock.bike_count()] += 1
    # print(f"Bike amount histogram 0..{docks[0].capacity}:", hist)
    print(hist)

    # Main.plot()

if __name__ == "__main__":
    repeat = 1
    for x in [0, 0.5, 0.8]:
        SimUser.chance_to_follow_suggestion = x
        print(SimUser.chance_to_follow_suggestion * 100)
        print(repeat)
        for _ in range(repeat):
            main()
            SimulationResults.reset()