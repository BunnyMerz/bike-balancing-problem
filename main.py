from utils.debug import Debug
from examples.Case1 import ChooseStation
from src.program import Main
print = Debug.print


def main():
    ChooseStation.Example1.run()
    Main.plot()

if __name__ == "__main__":
    main()