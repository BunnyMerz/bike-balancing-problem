from utils.debug import Debug
from examples.Subroutes import ChooseSubStation
from src.program import Main
print = Debug.print


def main():
    ChooseSubStation.LowBattery_ChargeableEnd.run()
    Main.plot()

if __name__ == "__main__":
    main()