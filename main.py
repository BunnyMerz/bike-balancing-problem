from utils.debug import Debug
from examples.Case1 import ChooseStartingStation
from src.program import Main
print = Debug.print


def main():
    ChooseStartingStation.Example1.run()
    Main.plot()

if __name__ == "__main__":
    main()