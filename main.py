from bikes import Dock, Bike

k = 5 # Dock capacity
def main():
    docas = [
        Dock(0 , 0 , 0 , k),
        Dock(100, 0 , 100, k),
        Dock(200, 0 , 200, k),
        Dock(300, 100, 100, k),
    ]

    adj = [
        [0,1,0,1],
        [1,0,1,1],
        [0,1,0,1],
        [1,1,1,0],
    ]

    dis = []
    y = 0
    for adj_line in adj:
        dis_line = []
        x = 0
        for adj_element in adj_line:
            if adj_element == 0 or x == y:
                dis_line.append(None)
            else:
                dist = Dock.distance(docas[x], docas[y])
                dis_line.append(dist)
            x += 1
        y += 1