from typing import Any

import networkx as nx
import matplotlib.pyplot as plt
from utils.debug import Debug
print = Debug.labeld_print("vis")


class Point:
    _id = 0

    points: list["Point"] = []
    edges: list[tuple[int, int, int]] = []
    def next_id(self): Point._id += 1; return Point._id - 1
    def __init__(self, x: int, y: int, color: str, label: str, width: float = 1.0):
        self.id = self.next_id()
        self.x = x + 0.00001 * self.id
        self.y = y + 0.00001 * self.id
        self.color = color
        self.label = label
        self.width = width

        Point.points.append(self)

    # Points derived from Dock are only created at Main.plot()
    # @classmethod
    # def dock(cls, dock: "Dock", **kws):
    #     cls.find(dock.id?)
    #     for kw in kws:
    #         dock.__setattr__(kw, kws[kw])

    # @classmethod
    # def find(self, _id: int):
    #     return Point.points[_id]

    def coords(self):
        return (self.x, self.y)
    @classmethod
    def add_edge(cls, u_id: int, v_id: int, w: int):
        cls.edges.append((u_id, v_id, w))
    @classmethod
    def color_map(cls):
        return [p.color for p in cls.points]
    @classmethod
    def labels(cls):
        resp = {p.coords(): p.label for p in cls.points}
        if len(resp.keys()) < len(cls.points):
            Debug.print("There are points with the same coordinates, resulting in less labels than points", label='warning')
        return resp
    @classmethod
    def clear_points(cls):
        cls._id = 0
        cls.points = []
    @classmethod
    def keys(cls):
        return [p.coords() for p in cls.points]

# def to_graph(points: list[tuple[int, int]], points_labels: dict[tuple[int, int], Any], edges: list[tuple[int, int, int]], color_map: list[str]):
def to_graph():
    G = nx.Graph()

    points = Point.keys()
    edges = Point.edges
    color_map = Point.color_map()
    points_labels = Point.labels()

    G.add_nodes_from(points)
    for i in range(len(edges)):
        G.add_edge(points[edges[i][0]], points[edges[i][1]], weight=edges[i][2])

    # you want your own layout
    # pos = nx.spring_layout(G)
    pos = {point: point for point in points}

    # add axis
    _, ax = plt.subplots()
    nx.draw(G, pos=pos, node_color=color_map, node_size=[1500*x.width for x in Point.points], ax=ax)  # draw nodes and edges
    nx.draw_networkx_labels(G, pos=pos, labels=points_labels)  # draw node labels/names
    # draw edge weights
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    plt.axis("on")

    _x = [x for x,y in points]
    _y = [y for x,y in points]

    ax.set_xlim(min(_x) - 20, max(_x) + 20)
    ax.set_ylim(min(_y) - 20, max(_y) + 20)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()