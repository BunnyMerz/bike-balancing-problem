from random import randint as rng

from utils.vis import Point
from utils.debug import Debug
from src.bikes import Dock, Bike, to_map
from src.goals import Destination, Goal, PickBike
print_d = Debug.labeld_print("depth")
print_count = Debug.labeld_print("count")


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
    max_extra_distance : tuple[float, int] = None # [0.2, 90] would mean 120% of normal distance, clampped to 90
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
        max_extra_distance = [2, 450]
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
    def show(cls):
        from utils.vis import to_graph
        to_graph()

    @classmethod
    def to_map(cls):
        values = []
        for dock in cls.docks:
            long, lat = dock.longitude, dock.latitude
            w = len(dock.bikes)
            if w == 0: continue
            values.append((long, lat, w))
        return values

    @classmethod
    def plot(cls):
        Point.clear_points()
        points: list[Point] = []
        for dock in cls.docks:
            label = (
                    ["[N]", "[C]"][dock.charges]
                    +"\n"+
                    f"{len(dock.bikes)}/{dock.capacity}"
                )
            
            label = str(len(dock.bikes))
            p = Point(
                x=dock.latitude, y=dock.longitude,
                color = ['red','orange'][int(dock.charges)],
                label = label
            )
            points.append(p)

        y = 0
        t = len(cls.adj)
        while(y < t):
            x = 0
            while(x < t):
                if cls.adj[y][x]:
                    # Point.add_edge(points[x].id, points[y].id, int(cls.distances[y][x]))
                    Point.add_edge(points[x].id, points[y].id, int(Dock.euclidian_distance(cls.docks[x], cls.docks[y])))
                x += 1
            y += 1

    ############
    ###### Strategies
    ############

    @classmethod
    def find_natural_and_suitable(cls, lat: float, long: float, alt: float, cant_be_full: bool) -> tuple[Dock, list[Dock]]:
        """
        Returns the nearest dock and a list of suitable docks

        lat, long, alt: float
            Anchort coordinate
        """
        cant_be_empty = not cant_be_full
        suitable: list[Dock] = []
        smallest: Dock = cls.docks[0]
        smallest_value: float = Dock.euclidian_distance_point(cls.docks[0], lat, long, alt)

        x = 0
        for dock in cls.docks:
            d = Dock.euclidian_distance_point(dock, lat, long, alt)
            if d > cls.max_radius: continue
            if ( # 
                cant_be_full and not dock.full(bias=Dock.DeliverBias)
                or
                cant_be_empty and not dock.empty(bias=Dock.PickBias)
            ): 
                suitable.append(dock) # Finds all docks that may fit being a suggestion

            if cant_be_full and dock.full(): continue
            if not cant_be_full and dock.empty(): continue
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
        natural, suitable = cls.find_natural_and_suitable(lat, long, alt, cant_be_full=False)
        if natural is None: return None, None
        
        target_occupancy = min(
            cls.max_occupancy + cls.occupancy_margin,
            natural.occupancy(Dock.PickBias) + cls.occupancy_margin
        )
        
        # Here comes the logic for choosing what's better than the natural option
        #  For now, it only cares about occupancy, not what bikes are in it.
        #  Caring about bikes in it would require a logic for determing how much occupancy weights versus bicicle battery
        suitable = [dock for dock in suitable if dock.occupancy(Dock.PickBias) > target_occupancy][:cls.number_of_suggestions]

        return natural, Goal(initial_dest=Destination(Destination.EITHER, min_capacity=target_occupancy, max_capacity=100, suitable=suitable[:cls.number_of_suggestions]))
    
    @classmethod
    def find_strategy(cls, lat: float, long: float, alt: float, chosen_dock: Dock) -> tuple[Dock, Goal]:
        """
        Returns a natural choice and a Goal with suitable docks as possible goal achievment
        """
        natural, suitable = cls.find_natural_and_suitable(lat, long, alt, cant_be_full=True)
        if natural is None: return None, None

        available_bikes = chosen_dock.bikes
        suitable_bikes = []
        suitable_docks = []
        
        if chosen_dock.charges is False: # Doesn't charge
            if natural.charges is True:
                suitable_docks.append(natural) # Bike+Natural is part of the strategy this time
            # Find low battery
            suitable_bikes += [b for b in available_bikes if b.battery_level < cls.bike_low_batery] # TODO: Check if every bike is suitable? If so, don't suggest anything but the destination.
            # Find destinations that can charge that are better than the natural one
            suitable_docks += [d for d in suitable if d.charges is True and d.occupancy() < natural.occupancy()] # TODO: Sort by occupancy

        if suitable_bikes != [] and suitable_docks != []:
            # Simple bike deliver!
            ## Must pick a certain type of bike
            pb = PickBike(min_battery_level=0, max_battery_level=cls.bike_low_batery, suitable=suitable_bikes)
            ## Must return to a certain destination
            dst = Destination(Destination.CHARGEABLE, min_capacity=0, max_capacity=natural.occupancy(), suitable=suitable_docks[:cls.number_of_suggestions])
            return natural, Goal(initial_bike=pb, end_dest=dst)
        
        # If code reached here it means
        # No way of picking a specific bike and carrying it to the end, either no bike or no destination. 
        # If no destiantion and no bike, nothing to do here. Run find_ending_dock
        # If only no destiantion, search for cheargeble sub-route
        # If only no bike, search for sub-route with low batter bike

        if suitable_docks == [] and suitable_bikes == []:
            return cls.find_ending_dock(lat, long, alt) # Try to find a good ending dock at least. (Dock suggestion only, no bike)
        
        ## Search for sub-routes here
        if suitable_bikes != []: # Low battery at start, serach for chargeable sub-station
            pass
        else:  # No Low battery at start, serach for chargeable sub-station
            pass
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
        natural, suitable = cls.find_natural_and_suitable(lat, long, alt, cant_be_full=True)
        if natural is None: return None, None

        chargeable = Destination.EITHER
        target_occupancy = min(
            cls.max_occupancy - cls.occupancy_margin,
            natural.occupancy(Dock.DeliverBias) - cls.occupancy_margin
        )

        if suitable == []:
            return natural, Goal(end_dest=Destination(chargeable, min_capacity=0, max_capacity=target_occupancy, suitable=[])) # No sugestion

        
        # Here comes the logic for choosing what's better than the natural option
        #  Occupancy has higher priority. It will filter based on chargeability only if possible.

        # Filter docks by occupancy
        suitable = [dock for dock in suitable if dock.occupancy(Dock.DeliverBias) < target_occupancy][:cls.number_of_suggestions]

        # If bike is too low, filter all docks to chargeables, unless there are none.
        if current_bike is not None and current_bike.battery_level < cls.bike_low_batery:
            chargeable_suitable = [dock for dock in suitable if dock.charges]
            if chargeable_suitable != [] or natural.charges: # If no options are found, don't attribute it to suitable, except if the natural dock is chargeable
                suitable = chargeable_suitable
                chargeable = Destination.CHARGEABLE

        return natural, Goal(end_dest=Destination(chargeable, min_capacity=0, max_capacity=target_occupancy, suitable=suitable))

    ############
    ###### Utils
    ############
    @classmethod
    def find_dock_index(cls, target_dock: Dock):
        x = 0
        for dock in cls.docks:
            if dock.id == target_dock.id:
                return x
            x += 1

    @classmethod
    def depth_search(cls, start: Dock, middle: Dock, end: Dock) -> tuple[list[Dock], float]:
        start_i = cls.find_dock_index(start)
        middle_i = cls.find_dock_index(middle)
        end_i = cls.find_dock_index(end)

        mult, clamp = Main.max_extra_distance
        max_distance = Dock.euclidian_distance(start, end)
        max_distance += min(mult * max_distance, clamp)

        start_middle_path, dist = cls._depth_search(start_i, middle_i, max_distance, 0, set([start_i]))
        if start_middle_path == [] and dist == -1: return [], -1
        middle_end_path, dist = cls._depth_search(middle_i, end_i, max_distance, dist, set(start_middle_path))
        if middle_end_path == [] and dist == -1: return [], -1
        return [cls.docks[x] for x in list(start_middle_path) + list(middle_end_path)], dist
    @classmethod
    def _depth_search(cls, current_i: int, end_i: int, max_distance: int, accumulated_dist: int, already_visited: set[int]) -> tuple[list[int], float] | tuple[list, -1]:
        """
        Search for the shortest (first, for now) path between current and end, that don't exceed `max_distance`.
        Returns `[((DockIndex, ...), TotalDistance),...]` or None when there isn't a path that meets the requirements
        """
        # TODO: Implement A* search instead.

        print_d("=======", current_i, end_i)
        if current_i == end_i:
            print_d("=== end with", already_visited, accumulated_dist)
            return already_visited, accumulated_dist

        neighs = []
        neighs_dists = []
        for x in range(len(cls.docks)): # Escolha apenas nós vizinhos que não ultrapassem o limite de distancia
            print_d("=======--", x, bool(cls.adj[current_i][x]), already_visited, cls.adj[current_i][x] == True, x not in already_visited)
            if cls.adj[current_i][x] == True and x not in already_visited:
                to_neigh_dist = Dock.euclidian_distance(cls.docks[x], cls.docks[current_i])
                print_d("=======---", x, accumulated_dist+to_neigh_dist, max_distance)
                if accumulated_dist + to_neigh_dist < max_distance:
                    print_d("=======--- +", x)
                    neighs.append(x)
                    neighs_dists.append(to_neigh_dist)

        print_d(neighs)
        for x in range(len(neighs)):
            neigh = neighs[x]
            neigh_dist = neighs_dists[x]

            already_visited.add(neigh)
            print_d(f"== ({neigh} -> {end_i} with {accumulated_dist + neigh_dist} and {already_visited})")
            path, dist = cls._depth_search(neigh, end_i, max_distance, accumulated_dist + neigh_dist, already_visited)
            if path != []:
                print_d("== recursive return")
                return path, dist
            already_visited.remove(neigh)
        return [], -1