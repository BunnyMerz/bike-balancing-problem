from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation
from examples.Simulation import Simulations

from src.sim import SimUser
from src.program import Main

from random import randint as rng, seed

from utils.debug import Debug
print = Debug.print
seed(1348923042372304723489)

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
    docks, bikes, adj = Simulations.BigGrid.build(bike_amount=2)
    

    users: list[SimUser] = []
    for x in range(100):
        sim = SimUser(
            (rng(0,1000), rng(0,1000), 0),
            (rng(0,1000), rng(0,1000), 0),
            offset_timer=((x%10)+1) * 200
        )
        users.append(sim)


    copy_users = users[:]
    copy_users = order_by_time(copy_users)
    while(len(copy_users) > 0):
        user = copy_users.pop(0)
        print()
        print(f"=====", user)
        user.act()
        print(f"=====", user)

        if not user.done():
            copy_users = insert_by_time(user, copy_users)

    print()
    for user in users:
        print(user)
    print(len([x for x in users if x.state == x.CantStart]))
    print(len([x for x in users if x.state == x.CantPick]))
    print(len([x for x in users if x.state == x.CantStartRun]))
    print(len([x for x in users if x.state == x.CantDeliver]))

    Main.plot()

if __name__ == "__main__":
    main()