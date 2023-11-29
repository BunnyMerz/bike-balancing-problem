from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation

from src.sim import SimUser
from src.program import Main

from random import randint as rng

from utils.debug import Debug
print = Debug.print


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
    docks, bikes, adj = ChooseStartingStation.OneSuggestion.build()
    

    users: list[SimUser] = []
    for x in range(7):
        sim = SimUser(
            (rng(0,40), rng(0,40), 0),
            (rng(200,300), rng(150,200), 0)
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

    Main.plot()

if __name__ == "__main__":
    main()