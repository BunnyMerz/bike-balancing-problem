from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation

from src.sim import SimUser

from utils.debug import Debug

from src.program import Main
print = Debug.print


def main():
    docks, bikes, adj = ChooseStartingStation.OneSuggestion.build()
    
    ts = SimUser(
        (90, 90, 0),
        (200, 100, 100)
    )

    print(f"=====",ts)
    while(ts.state != ts.Idle):
        ts.act()
        print(f"=====",ts)

    Main.plot()

if __name__ == "__main__":
    main()