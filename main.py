from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation

from utils.debug import Debug

from src.program import Main
print = Debug.print


def main():
    ChooseStartingStation.OneSuggestion.run()
    path, dist = Main.depth_search(
        Main.docks[0], Main.docks[1], Main.docks[3]
    )
    print(path, dist)
    Main.plot()

if __name__ == "__main__":
    main()