from random import randint as rng
from utils.debug import Debug
from src.bikes import Dock, Bike
from src.goals import Destination, Goal, PickBike
print = Debug.print


class Main:
    """
    Capable of deciding what streategies are best and will seng fragments of them.
    The User interace must handle users performing or not these fragements and concatenate them as needed.
    """
    docks:     list[Dock]        = None
    bikes:     list[Bike]        = None
    adj:       list[list[bool]]  = None
    distances: list[list[float]] = None

    extra_points_to_plot: list[tuple[int, int]] = None

    max_radius: float = None
    number_of_suggestions: int = None

    # === Suggest starting station === #
    # Represents the max occupancy a dock must have to become a suggestion
    max_occupancy: float = None # in percent %
    # Represents the occupancy a dock must have less than the target occupancy
    occupancy_margin: float = None # in percent %
    # ===                          === #

    # === Suggest Ending station === #
    # Represents the max battery a bike must have to become 'too low'
    bike_low_batery: float = None # in percent %:
    bike_high_batery: float = None # in percent %:
    # ===                        === #

    # ===  Suggest Sub station   === #
    max_extra_distance : tuple[float, int] = None # [1.2, 90] would mean 120% of normal distance, clampped to 90
    # ===                        === #

    @classmethod
    def init_from_basic(
        cls, docks, bikes, adj,
        max_radius = 145, number_of_suggestions = 1,
        max_occupancy = 80, occupancy_margin = 10,
        bike_low_batery = 20, bike_high_batery = 90,
        max_extra_distance = [1.2, 90]
    ):
        distances = []
        y = 0
        for adj_line in adj:
            dis_line = []
            x = 0
            for adj_element in adj_line:
                if adj_element == 0 or x == y:
                    dis_line.append(None)
                else:
                    dist = Dock.euclidian_distance(docks[x], docks[y])
                    dis_line.append(dist)
                x += 1
            distances.append(dis_line)
            y += 1
        cls.init(docks, bikes, adj, distances, max_radius, number_of_suggestions, max_occupancy, occupancy_margin, bike_low_batery, bike_high_batery, max_extra_distance)

    @classmethod
    def init(
        cls, docks, bikes, adj, distances,
        max_radius = 145, number_of_suggestions = 1,
        max_occupancy = 80, occupancy_margin = 10,
        bike_low_batery = 20, bike_high_batery = 90,
        max_extra_distance = [1.2, 90]
    ):
        cls.docks =     docks
        cls.bikes =     bikes
        cls.adj =       adj
        cls.distances = distances

        cls.max_radius = max_radius
        cls.number_of_suggestions = number_of_suggestions
        
        cls.max_occupancy = max_occupancy
        cls.occupancy_margin = occupancy_margin

        cls.bike_low_batery = bike_low_batery
        cls.bike_high_batery = bike_high_batery

        cls.max_extra_distance = max_extra_distance

    @classmethod
    def plot(cls):
        from utils.vis import to_graph, Point
        points: list[Point] = []
        for dock in cls.docks:
            p = Point(
                x=dock.latitude, y=dock.longitude,
                color = ['red','orange'][dock.charges],
                label = ["[N]", "[C]"][dock.charges]
                        +"\n"+
                        f"{len(dock.bikes)}/{dock.capacity}"
            )
            points.append(p)

        y = 0
        t = len(cls.adj)
        while(y < t):
            x = 0
            while(x < t):
                if cls.adj[y][x]:
                    Point.add_edge(points[x].id, points[y].id, int(cls.distances[y][x]))
                x += 1
            y += 1
        to_graph()

    ############
    ###### Strategies
    ############

    @classmethod
    def find_natural_and_suitable(cls, lat: float, long: float, alt: float) -> tuple[Dock, list[Dock]]:
        """
        Returns the nearest dock and a list of suitable docks

        lat, long, alt: float
            Anchort coordinate
        """
        suitable: list[Dock] = []
        smallest: Dock = cls.docks[0]
        smallest_value: float = Dock.euclidian_distance_point(cls.docks[0], lat, long, alt)

        x = 0
        for dock in cls.docks:
            d = Dock.euclidian_distance_point(dock, lat, long, alt)
            if d < cls.max_radius:
                suitable.append(dock) # Finds all docks that may fit being a suggestion
            if d < smallest_value: # Finds the closest dock, even if not suitable
                smallest = dock
                smallest_value = d
            x += 1

        if smallest in suitable: suitable.remove(smallest)
        return smallest, suitable

    @classmethod
    def find_starting_dock(cls, lat: float, long: float, alt: float) -> tuple[Dock, Goal]:
        """
        Returns the nearest dock and a destination that describes any valid suggestion along with a list of suggestions based on some parameters defined inside Main

        lat, long, alt: float
            User's current coordinates
        """
        natural, suitable = cls.find_natural_and_suitable(lat, long, alt)
        
        target_occupancy = min(
            cls.max_occupancy + cls.occupancy_margin,
            natural.occupancy() + cls.occupancy_margin
        )
        
        # Here comes the logic for choosing what's better than the natural option
        #  For now, it only cares about occupancy, not what bikes are in it.
        #  Caring about bikes in it would require a logic for determing how much occupancy weights versus bicicle battery
        suitable = [dock for dock in suitable if dock.occupancy() > target_occupancy][:cls.number_of_suggestions]

        return natural, Goal(initial_dest=Destination(Destination.EITHER, min_capacity=target_occupancy, max_capacity=100, suitable=suitable[:cls.number_of_suggestions]))
    
    @classmethod
    def find_strategy(cls, lat: float, long: float, alt: float, chosen_dock: Dock) -> tuple[Dock, Goal]:
        """
        Returns list of goals as suggestions to user
        """
        natural, suitable = cls.find_natural_and_suitable(lat, long, alt)

        available_bikes = chosen_dock.bikes
        suitable_bikes = []
        suitable_docks = []
        
        if chosen_dock.charges is False: # Doesn't charge
            if natural.charges is True:
                suitable_docks.append(natural) # Bike+Natural is part of the strategy this time
            # Find low battery
            suitable_bikes = [b for b in available_bikes if b.battery_level < cls.bike_low_batery] # TODO: Check if every bike is suitable? If so, don't suggest anything but the destination.
            # Find destinations that can charge that are better than the natural one
            suitable_docks += [d for d in suitable if d.charges is True and d.occupancy() < natural.occupancy()]

        if suitable_bikes != [] and suitable_docks != []:
            # Simple bike deliver!
            ## Must pick a certain type of bike
            pb = PickBike(min_battery_level=0, max_battery_level=cls.bike_low_batery, suitable=suitable_bikes)
            ## Must return to a certain destination
            dst = Destination(Destination.CHARGEABLE, min_capacity=0, max_capacity=natural.occupancy(), suitable=suitable_docks[:cls.number_of_suggestions])
            return natural, Goal(initial_bike=pb, end_dest=dst)
        
        # No way of picking a specific bike and carrying it to the end, either no bike or no destination. 
        # If no destiantion, nothing to do here. 
        # If no bike, search for sub-route

        if suitable_docks == []:
            return cls.find_ending_dock(lat, long, alt) # Try to find a good ending dock at least.
        
        ## Search for sub-routes here

        # Here comes the logic for choosing what's better than the natural option
        # suitable = [dock for dock in suitable if dock.occupancy() > target_occupancy][:cls.number_of_suggestions]
        
        return None, None

    @classmethod
    def find_ending_dock(cls, lat: float, long: float, alt: float, current_bike: Bike = None) -> tuple[Dock, Goal]:
        """
        Returns the nearest suitable dock and a list of suggestions

        lat, long, alt: float
            User's destination coordinates

        current_bike: Bike
            User's current bike
        """
        natural, suitable = cls.find_natural_and_suitable(lat, long, alt)
        if suitable == []:
            return natural, [] # No sugestion
        

        target_occupancy = min(
            cls.max_occupancy - cls.occupancy_margin,
            natural.occupancy() - cls.occupancy_margin
        )
        
        # Here comes the logic for choosing what's better than the natural option
        #  Occupancy has higher priority. It will filter based on chargeability only if possible.

        # Filter docks by occupancy
        suitable = [dock for dock in suitable if dock.occupancy() < target_occupancy][:cls.number_of_suggestions]

        # If bike is too low, filter all docks to chargeables, unless there are none.
        chargeable = Destination.EITHER
        if current_bike is not None and current_bike.battery_level < cls.bike_low_batery:
            chargeable_suitable = [dock for dock in suitable if dock.charges]
            if chargeable_suitable != [] or natural.charges: # If no options are found, don't attribute it to suitable, except if the natural dock is chargeable
                suitable = chargeable_suitable
                chargeable = Destination.CHARGEABLE

        return natural, Goal(end_dest=Destination(chargeable, min_capacity=0, max_capacity=target_occupancy, suitable=suitable))
