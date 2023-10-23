# Name:        Data:
import random, pickle, math, time
from collections import OrderedDict
from math import pi, acos, sin, cos
from tkinter import *
import heapq


def calc_edge_cost(y1, x1, y2, x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    R = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R
    #


# NodeLocations, NodeToCity, CityToNode, Neighbors, EdgeCost
# Node: (lat, long) or (y, x), node: city, city: node, node: neighbors, (n1, n2): cost
def make_graph(nodes="rrNodes.txt", node_city="rrNodeCity.txt", edges="rrEdges.txt"):
    nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost = {}, {}, {}, {}, {}
    map = {}  # have screen coordinate for each node location
    with open(nodes) as f:
        for line in f:
            n, y, x = line.split()
            nodeLoc[n] = (float(y), float(x))
    with open(node_city) as f:
        for line in f:
            n, city = line.split(" ", 1)
            city = city.strip()
            nodeToCity[n] = city
            cityToNode[city] = n
    with open(edges) as f:
        for line in f:
            n, nei = line.split()
            if n not in neighbors:
                neighbors[n] = {nei}
            else:
                neighbors[n].add(nei)
            if nei not in neighbors:
                neighbors[nei] = {n}
            else:
                neighbors[nei].add(n)
    for k, v in neighbors.items():
        for i in v:
            ec = calc_edge_cost(*nodeLoc[k], *nodeLoc[i])
            edgeCost[k, i] = ec
            edgeCost[i, k] = ec
    for node in nodeLoc:  # checks each
        lat = float(nodeLoc[node][0])  # gets latitude
        long = float(nodeLoc[node][1])  # gets long
        modlat = (lat - 10) / 60  # scales to 0-1
        modlong = (long + 130) / 70  # scales to 0-1
        map[node] = [modlat * 800, modlong * 1200]  # scales to fit 800 1200
    return [nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost, map]


# Return the direct distance from node1 to node2
# Use calc_edge_cost function.
def dist_heuristic(n1, n2, graph):
    return calc_edge_cost(*graph[0][n1], *graph[0][n2])


# Create a city path.
# Visit each node in the path. If the node has the city name, add the city name to the path.
# Example: ['Charlotte', 'Hermosillo', 'Mexicali', 'Los Angeles']
def display_path(path, graph):
    disp = []
    for i in path:
        if i in graph[1]:
            disp.append(graph[1][i])
    print(disp)


# Using the explored, make a path by climbing up to "s"
# This method may be used in your BFS and Bi-BFS algorithms.
def generate_path(state, explored, graph):
    path = [state]
    cost = 0
    while explored[path[-1]] != "s":
        # print(path)
        path.append(explored[path[-1]])
        cost += graph[4][(path[-2], path[-1])]
    return path[::-1], cost


def drawLine(canvas, y1, x1, y2, x2, col):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    canvas.create_line(x1, 800 - y1, x2, 800 - y2, fill=col)


# Draw the final shortest path.
# Use drawLine function.
def draw_final_path(ROOT, canvas, path, graph, col='red'):
    for i in range(len(path) - 1):
        drawLine(canvas, *graph[5][path[i]], *graph[5][path[i + 1]], col)
    ROOT.update()


def draw_all_edges(ROOT, canvas, graph):
    ROOT.geometry("1200x800")  # sets geometry
    canvas.pack(fill=BOTH, expand=1)  # sets fill expand
    for n1, n2 in graph[4]:  # graph[4] keys are edge set
        drawLine(canvas, *graph[5][n1], *graph[5][n2], 'white')  # graph[5] is map dict
    ROOT.update()


def bfs(start, goal, graph, col):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    counter = 0
    frontier, explored = [], {start: "s"}
    frontier.append(start)
    nexp = 0
    while frontier:
        s = frontier.pop(0)
        nexp += 1
        if s == goal:
            path, cost = generate_path(s, explored, graph)
            draw_final_path(ROOT, canvas, path, graph)
            print(f'The number of explored nodes of BFS: {nexp}')
            print(f'The whole path: {path}')
            print(f'The length of the whole path: {len(path)}')
            return path, cost
        for a in graph[3][s]:  # graph[3] is neighbors
            if a not in explored:
                explored[a] = s
                frontier.append(a)
                drawLine(canvas, *graph[5][s], *graph[5][a], col)
        counter += 1
        if counter % 1000 == 0: ROOT.update()
    return None


def bi_bfs(st, goal, graph, col):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    counter = 0
    if st == goal:
        return []
    expF = {st: "s"}
    expB = {goal: "s"}
    qF = [st]
    qB = [goal]
    nexp = 0
    while qF and qB:
        crF = qF.pop(0)
        crB = qB.pop(0)
        nexp += 2
        for a in graph[3][crF]:
            if a not in expF:
                expF[a] = crF
                qF.append(a)
                drawLine(canvas, *graph[5][crF], *graph[5][a], col)
        for a in graph[3][crB]:
            if a not in expB:
                expB[a] = crB
                qB.append(a)
                drawLine(canvas, *graph[5][crB], *graph[5][a], col)
        for i in qF:
            for j in qB:
                if i == j:
                    p1, c1 = generate_path(i, expF, graph)
                    p2, c2 = generate_path(j, expB, graph)
                    path, cost = p1 + p2[::-1], c1 + c2
                    draw_final_path(ROOT, canvas, path, graph)
                    print(f'The number of explored nodes of Bi-BFS: {nexp}')
                    print(f'The whole path: {path}')
                    print(f'The length of the whole path: {len(path)}')
                    return path, cost
        counter += 1
        if counter % 1000 == 0:
            ROOT.update()
    return None


def a_star(start, goal, graph, col, h=dist_heuristic):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    nodes = []
    heapq.heapify(nodes)
    gmap = {start: 0}
    heapq.heappush(nodes, (h(start, goal, graph), [start], start))
    counter = 0
    while nodes:
        cr = heapq.heappop(nodes)
        if cr[2] == goal:
            path = cr[1]
            cost = gmap[goal]
            draw_final_path(ROOT, canvas, path, graph)
            print(f'The number of explored nodes of A star: {counter}')
            print(f'The whole path: {path}')
            print(f'The length of the whole path: {len(path)}')
            return path, cost
        for child in graph[3][cr[2]]:
            tg = gmap[cr[2]] + calc_edge_cost(*graph[0][cr[2]], *graph[0][child])
            if child not in gmap or tg < gmap[child]:
                gmap[child] = tg
                if child not in cr[1]:
                    drawLine(canvas, *graph[5][cr[2]], *graph[5][child], col)
                    heapq.heappush(nodes, (tg + h(child, goal, graph), cr[1] + [child], child))
        counter += 1
        if counter % 1000 == 0:
            ROOT.update()
    return None


def bi_a_star(start, goal, graph, col, h=dist_heuristic):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    forw = []
    heapq.heapify(forw)
    fGMap = {start: 0}
    heapq.heappush(forw, (h(start, goal, graph), [start], start))
    bGMap = {goal: 0}
    bw = []
    heapq.heapify(bw)
    heapq.heappush(bw, (h(start, goal, graph), [goal], goal))
    counter = 0
    while forw and bw:
        crF = heapq.heappop(forw)
        for nei in graph[3][crF[2]]:
            tg = fGMap[crF[2]] + calc_edge_cost(*graph[0][crF[2]], *graph[0][nei])
            if nei not in fGMap or tg < fGMap[nei]:
                fGMap[nei] = tg
                if nei not in crF[1]:
                    drawLine(canvas, *graph[5][crF[2]], *graph[5][nei], col)
                    heapq.heappush(forw, (tg + h(nei, goal, graph), crF[1] + [nei], nei))
        crB = heapq.heappop(bw)
        for nei in graph[3][crB[2]]:
            tg = bGMap[crB[2]] + calc_edge_cost(*graph[0][crB[2]], *graph[0][nei])
            if nei not in bGMap or tg < bGMap[nei]:
                bGMap[nei] = tg
                if nei not in crB[1]:
                    drawLine(canvas, *graph[5][crB[2]], *graph[5][nei], col)
                    heapq.heappush(bw, (tg + h(nei, goal, graph), crB[1] + [nei], nei))
        for i in forw:
            for j in bw:
                if i[2] == j[2]:
                    path, cost = i[1] + j[1][::-1], fGMap[i[2]] + bGMap[j[2]]
                    draw_final_path(ROOT, canvas, path, graph)
                    print(f'The number of explored nodes of Bi-A star: {counter * 2}')
                    print(f'The whole path: {path}')
                    print(f'The length of the whole path: {len(path)}')
                    return path, cost
        counter += 1
        if counter % 1000 == 0:
            ROOT.update()
    return None


def tri_directional(city1, city2, city3, graph, col, h=dist_heuristic):
    od = [(calc_edge_cost(*graph[0][city2], *graph[0][city3]), city1),
          (calc_edge_cost(*graph[0][city1], *graph[0][city3]), city2),
          (calc_edge_cost(*graph[0][city1], *graph[0][city2]), city3)]
    od.sort()
    st, a1, a2 = od[2][1], od[1][1], od[0][1]
    ROOT = Tk()  # creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)
    he1 = []
    heapq.heapify(he1)
    gMap1 = {st: 0}
    heapq.heappush(he1, (h(st, a1, graph), [st], st))
    gMap2 = {st: 0}
    he2 = []
    heapq.heapify(he2)
    heapq.heappush(he2, (h(st, a2, graph), [st], st))
    counter = 0
    flag = False
    path = []
    cost = 0
    while he1 and he2:
        crF = heapq.heappop(he1)
        if crF[2] == a1:
            path = path[1:]
            path += crF[1]
            cost += gMap1[a1]
            if flag:
                draw_final_path(ROOT, canvas, path[1:], graph)
                print(f'The number of explored nodes of Tridirectional Search: {counter * 2}')
                print(f'The whole path: {path[1:]}')
                print(f'The length of the whole path: {len(path[1:])}')
                return path[1:], cost
            else:
                flag = True
        for nei in graph[3][crF[2]]:
            tg = gMap1[crF[2]] + calc_edge_cost(*graph[0][crF[2]], *graph[0][nei])
            if nei not in gMap1 or tg < gMap1[nei]:
                gMap1[nei] = tg
                if nei not in crF[1]:
                    drawLine(canvas, *graph[5][crF[2]], *graph[5][nei], col)
                    heapq.heappush(he1, (tg + h(nei, a1, graph), crF[1] + [nei], nei))
        crB = heapq.heappop(he2)
        if crB[2] == a2:
            path = path[1:]
            path += crB[1]
            cost += gMap2[a2]
            if flag:
                draw_final_path(ROOT, canvas, path, graph)
                print(f'The number of explored nodes of Bi-A star: {counter * 2}')
                print(f'The whole path: {path}')
                print(f'The length of the whole path: {len(path)}')
                return path, cost
            else:
                flag = True
        for nei in graph[3][crB[2]]:
            tg = gMap2[crB[2]] + calc_edge_cost(*graph[0][crB[2]], *graph[0][nei])
            if nei not in gMap2 or tg < gMap2[nei]:
                gMap2[nei] = tg
                if nei not in crB[1]:
                    drawLine(canvas, *graph[5][crB[2]], *graph[5][nei], col)
                    heapq.heappush(he2, (tg + h(nei, a2, graph), crB[1] + [nei], nei))
        counter += 1
        if counter % 1000 == 0:
            ROOT.update()
    return None, 0


def main():
    start, goal = input("Start city: "), input("Goal city: ")
    third = input("Third city for tri-directional: ")
    graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")  # Task 1

    cur_time = time.time()
    path, cost = bfs(graph[2][start], graph[2][goal], graph, 'yellow')  # graph[2] is city to node
    if path is not None:
        display_path(path, graph)
    else:
        print("No Path Found.")
    print('BFS Path Cost:', cost)
    print('BFS duration:', (time.time() - cur_time))
    print()

    # cur_time = time.time()
    # path, cost = bi_bfs(graph[2][start], graph[2][goal], graph, 'green')
    # if path is not None:
    #     display_path(path, graph)
    # else:
    #     print("No Path Found.")
    # print('Bi-BFS Path Cost:', cost)
    # print('Bi-BFS duration:', (time.time() - cur_time))
    # print()

    # cur_time = time.time()
    # path, cost = a_star(graph[2][start], graph[2][goal], graph, 'blue')
    # if path is not None:
    #     display_path(path, graph)
    # else:
    #     print("No Path Found.")
    # print('A star Path Cost:', cost)
    # print('A star duration:', (time.time() - cur_time))
    # print()
    #
    # cur_time = time.time()
    # path, cost = bi_a_star(graph[2][start], graph[2][goal], graph, 'orange')
    # if path is not None:
    #     display_path(path, graph)
    # else:
    #     print("No Path Found.")
    # print('Bi-A star Path Cost:', cost)
    # print("Bi-A star duration: ", (time.time() - cur_time))
    # print()

    # print("Tri-Search of ({}, {}, {})".format(start, goal, third))
    # cur_time = time.time()
    # path, cost = tri_directional(graph[2][start], graph[2][goal], graph[2][third], graph, 'pink')
    # if path is not None:
    #     display_path(path, graph)
    # else:
    #     print("No Path Found.")
    # print('Tri-A star Path Cost:', cost)
    # print("Tri-directional search duration:", (time.time() - cur_time))

    mainloop()  # Let TK windows stay still


if __name__ == '__main__':
    main()
