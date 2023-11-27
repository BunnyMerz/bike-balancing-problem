from utils.debug import Debug
from examples.Case1 import ChooseEndingStation, ChooseStartingStation
from src.program import Main
print = Debug.print


def main():
    ChooseEndingStation.Example1.run()
    Main.plot()

if __name__ == "__main__":
    main()