from typing import Any
import networkx as nx
import matplotlib.pyplot as plt


def to_graph(points: list[tuple[int, int]], points_labels: dict[tuple[int, int], Any], edges: list[tuple[int, int, int]], color_map: list[str]):
    G = nx.Graph()

    for i in range(len(edges)):
        G.add_edge(points[edges[i][0]], points[edges[i][1]], weight=edges[i][2])

    # you want your own layout
    # pos = nx.spring_layout(G)
    pos = {point: point for point in points}

    # add axis
    fig, ax = plt.subplots()
    nx.draw(G, pos=pos, node_color=color_map, node_size=1500, ax=ax)  # draw nodes and edges
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