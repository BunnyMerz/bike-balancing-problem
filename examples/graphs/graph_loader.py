from src.bikes import Bike, Dock


class GraphLoader:
    graph_folder = "examples/graphs"
    def __init__(self, folder_name) -> None:
        self.folder_name = folder_name
        self.bikes: list[Bike] = []
        self.docks: list[Dock] = []
        self.adj: list[list[bool]] = []
        self.dist: list[list[int]] = []
        self.load()

    @classmethod
    def int(cls, _v: str) -> int:
        return int(_v.strip(' '))
    @classmethod
    def bool(cls, _v: str) -> bool:
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
                    dock = Dock(x, y, 0, k=capacity, charges=charges)
                    for _ in range(amount_now):
                        bike = Bike()
                        dock.retrieve(bike)
                        self.bikes.append(bike)
                    self.docks.append(dock)

                elif obj_type == "edge":
                    source_id, target_id, w = args
                    source_id, target_id, w = int(source_id), int(target_id), int(w)*300
                    edges.append((source_id, target_id, w))

        adj = [[0 for _ in range(len(self.docks))][:] for _ in range(len(self.docks))]
        min_dist = [[None for _ in range(len(self.docks))][:] for _ in range(len(self.docks))]
        for egde in edges:
            source_id, target_id, w = egde
            adj[source_id][target_id] = 1
            min_dist[source_id][target_id] = w

        self.adj = adj
        self.dist = min_dist