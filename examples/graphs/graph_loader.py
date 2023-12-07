from random import random, randint as rng

from src.bikes import Bike, Dock

class Interest:
    def __init__(
            self,
            w: tuple[int, int],
            radius: tuple[int, int],
            x: int, y: int, z: int,
            time_active: list[tuple[int, int]]
        ):
        self.weights: tuple[int, int] = w # Weight when most active and whenever else
        self.radius: tuple[float,float] = radius # How spread out users can be generated at
        self.x = x
        self.y = y
        self.z = z
        self.time_active: list[tuple[int, int]] = time_active # [(6,11), (13,15)] # 6am as 11am, e 1pm a 3pm

    def weight(self, time: float):
        assert time >= 0 and time <= 24
        for start_active, end_active in self.time_active:
            if start_active <= time and time <= end_active:
                return self.weights[0]
        return self.weights[1]

    def geo_position(self):
        return (self.x, self.y, self.z)
    def rng_geo_position(self):
        rx, ry = self.radius
        return (self.x + rng(-rx, rx), self.y + rng(-ry, ry), self.z)
    
    @classmethod
    def decide(cls, time: float, options: list["Interest"]):
        total = 0
        for opt in options:
            total += opt.weight(time)

        choice = rng(0, total)
        x = 0
        option_w = options[x].weight(time)
        while(option_w < choice and x < len(options)):
            choice -= option_w
            x += 1
            option_w = options[x].weight(time)
        return options[x]

class EndInterest(Interest):
    pass
class StartInterest(Interest):
    def __init__(
            self,
            w: tuple[int, int],
            radius: tuple[int, int],
            x: int, y: int, z: int,
            time_active: list[tuple[int, int]],
            often_leads_to: list[EndInterest], 
            how_often_is_random: float,
        ):
        super().__init__(w, radius, x, y, z, time_active)
        self.often_leads_to: list[EndInterest] = often_leads_to
        self.how_often_is_random: float = how_often_is_random # 30% of the time, the end destinations are not within .often_leads_to
    def suggest_end(self, time: float, all_ends: list[EndInterest]):
        x = random()
        if x < self.how_often_is_random:
            return self.decide(time, all_ends)
        else:
            return self.decide(time, self.often_leads_to)
    @classmethod
    def decide(cls, time: float, options: list["StartInterest"]) -> "StartInterest":
        return super().decide(time, options)

def find_dock(id, docks):
    for dock in docks:
        if dock.dock_id == id:
            return dock
class GraphLoader:
    graph_folder = "examples/graphs"
    def __init__(self, folder_name) -> None:
        self.folder_name = folder_name
        self.bikes: list[Bike] = []
        self.docks: list[Dock] = []
        self.adj: list[list[bool]] = []
        self.dist: list[list[int]] = []
        self.min_dist: list[list[int]] = []

        self.start_interests: list[StartInterest] = []
        self.end_interests: list[EndInterest] = []

        self.load()

        barcas = find_dock(19, self.docks)
        ponto_final = find_dock(20, self.docks)
        casa_icarai = find_dock(37, self.docks)
        casa_centro = centro = find_dock(16, self.docks)
        pv = find_dock(32, self.docks)
        grag = find_dock(24, self.docks)

        end_manha = [
            # Manhã
            EndInterest((20, 10), (30,35),*centro.geo_position(),        [(7, 13)]), # Centro (Rua principal): 16
            EndInterest((20, 2), (10,10), *pv.geo_position(),            [(7, 11)]), # PV (Faculdade): 32
            EndInterest((20, 6), (10,10), *grag.geo_position(),          [(7, 13)]), # Gragoatá (Faculdade): 24
            EndInterest((30, 3), (10,10), *barcas.geo_position(),        [(7, 12)]), # Barcas: 19
            EndInterest((30, 3), (10,10), *ponto_final.geo_position(),   [(7, 12)]), # Barcas: 19
        ]
        start_manha = [
            # Manhã
            StartInterest((30, 3), (10,10), *barcas.geo_position(),      [(7, 11)],          end_manha, 0.3), # Barcas: 19
            StartInterest((30, 3), (10,10), *ponto_final.geo_position(), [(7, 11)],          end_manha, 0.3), # Barcas: 19
            StartInterest((15, 1), (30,40), *casa_icarai.geo_position(), [(7, 11)],          end_manha, 0.5), # Casa (Icarai): 37
            StartInterest((5, 1),  (10,10), *casa_centro.geo_position(), [(7, 11)],          end_manha, 0.5), # Casa (Centro): 16
        ]

        end_noite = [
            # Noite
            EndInterest((20, 3), (10,10), *barcas.geo_position(),      [(17, 22)]), # Barcas: 19
            EndInterest((15, 1), (30,40), *casa_icarai.geo_position(), [(17, 21)]), # Casa (Icarai): 37
            EndInterest((5, 1),  (10,10), *casa_centro.geo_position(), [(17, 22)]), # Casa (Centro): 16
        ]
        start_noite = [
            # Noite
            StartInterest((30, 3), (10,10), *barcas.geo_position(),      [(17, 21)],          end_noite, 0.3), # Barcas: 19
            StartInterest((20, 1),  (10,10),*casa_centro.geo_position(), [(17, 20)],          end_noite, 0.5), # Casa (Centro): 16
            StartInterest((15, 2), (10,10), *pv.geo_position(),          [(17, 21)],          end_noite, 0.2), # PV (Faculdade): 32
            StartInterest((15, 6), (10,10), *grag.geo_position(),        [(17, 21)],          end_noite, 0.2), # Gragoatá (Faculdade): 24
        ]

        self.start_interests = start_manha + start_noite
        self.end_interests = end_manha + end_noite

    @classmethod
    def int(cls, _v: str) -> int:
        if isinstance(_v, int): return _v
        return int(_v.strip(' '))
    @classmethod
    def bool(cls, _v: str) -> bool:
        if isinstance(_v, bool): return _v
        return _v.strip(' ').lower() in ["true", "1", True]
    

    def decode_node(self, args: list[str]) -> tuple[int, int, int, int, bool]:
        x, y, _id, *args = args
        capacity = 23
        amount_now = 9
        charges = True
        if len(args) == 1:
            capacity = args[0]
        if len(args) == 2:
            capacity, amount_now = args
        if len(args) == 3:
            capacity, amount_now, charges = args
        return self.int(x),-self.int(y), self.int(_id), self.int(capacity), self.int(amount_now), self.bool(charges)

    def load(self):
        graph = self.folder_name + '.graph'
        dists = self.folder_name + '.distances'

        edges: list[tuple[int, int, int]] = []
        with open(f"{self.graph_folder}/{self.folder_name}/{graph}", 'r') as __Graph__:
            for line in __Graph__.readlines():
                line = line.strip('\n').strip(" ")
                if len(line) == 0 or line[0] == '#': continue
                obj_type, *args = line.split(';')
                if obj_type == "node":
                    x, y, _id, capacity, amount_now, charges = self.decode_node(args)
                    dock = Dock(_id, x, y, 0, k=capacity, charges=charges)
                    for _ in range(amount_now):
                        bike = Bike()
                        dock.add_bike(bike)
                        self.bikes.append(bike)
                    self.docks.append(dock)

                elif obj_type == "edge":
                    source_id, target_id, w = args
                    source_id, target_id, w = int(source_id), int(target_id), int(w)*300
                    edges.append((source_id, target_id, w))

        adj = [[0 for _ in range(len(self.docks))][:] for _ in range(len(self.docks))]
        dist = [[None for _ in range(len(self.docks))][:] for _ in range(len(self.docks))]
        for egde in edges:
            source_id, target_id, w = egde
            adj[source_id][target_id] = 1
            dist[source_id][target_id] = w

        min_dist = []
        with open(f"{self.graph_folder}/{self.folder_name}/{dists}", 'r') as __Dists__:
            for line  in __Dists__:
                line = line.strip(" ").strip("\n")
                if line != "":
                    line = line.split(",")
                    line = list(map(int, line))
                    min_dist.append(line)

        self.adj = adj
        self.dist = dist
        self.min_dist = min_dist