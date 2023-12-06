from examples.graphs.graph_loader import Interest

a = Interest((30, 3), 0, 0, 0, [(1,10)])
b = Interest((30, 3), 0, 0, 0, [(1,10)])
c = Interest((30, 3), 0, 0, 0, [(11,12)])

Interest.decide(11, [a,b,c])