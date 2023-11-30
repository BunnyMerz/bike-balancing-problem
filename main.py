from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation
from examples.Simulation import Simulations

from src.sim import SimUser, SimulationResults
from src.program import Main

from random import randint as rng, seed

from utils.debug import Debug
print = Debug.print
# seed(192381293891492729)

def order_by_time(users: list[SimUser]):
    return sorted(users, key=lambda x: x.internal_clock.t)
def insert_by_time(user: SimUser, users: list[SimUser]):
    x = 0
    while(x < len(users)):
        if user.internal_clock.t < users[x].internal_clock.t:
            users.insert(x, user)
            return users
        x += 1
    users.append(user)
    return users

def main():
    docks, bikes, adj = Simulations.BigGrid.build()
    

    users: list[SimUser] = []
    for x in range(100):
        sim = SimUser(
            (rng(0,1000), rng(0,1000), 0),
            (rng(0,1000), rng(0,1000), 0),
            offset_timer=((x%30)+1) * 400
        )
        users.append(sim)


    copy_users = users[:]
    copy_users = order_by_time(copy_users)
    while(len(copy_users) > 0):
        user = copy_users.pop(0)
        print(label="step")
        print(f"=====", user, label="step")
        user.act()
        print(f"=====", user, label="step")

        if not user.done():
            copy_users = insert_by_time(user, copy_users)

    for dock in docks:
        assert dock.interested_delivery == 0
        assert dock.interested_picking == 0

    print(label="step")
    for user in users:
        print(user, label="step")
    print(f"""
        CantStart:    {len([x for x in users if x.state == x.CantStart])}
        CantPick:     {len([x for x in users if x.state == x.CantPick])}
        CantStartRun: {len([x for x in users if x.state == x.CantStartRun])}
        CantDeliver:  {len([x for x in users if x.state == x.CantDeliver])}""")
    print(f"""
        Made:      {SimulationResults.total_suggestion_made}
        Taken:     {SimulationResults.total_suggestion_taken}
        Completed: {SimulationResults.total_suggestion_completed}
        Angry: {SimulationResults.angry_users}""")

    Main.plot()

if __name__ == "__main__":
    main()