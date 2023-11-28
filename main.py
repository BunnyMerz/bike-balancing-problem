from examples.Picking import ChooseStartingStation
from examples.Subroutes import ChooseSubStation
from examples.Delivering import ChooseEndStation

from utils.debug import Debug

from src.program import Main
print = Debug.print


def main():
    ChooseStartingStation.OneSuggestion.run()
    Main.plot()

if __name__ == "__main__":
    main()