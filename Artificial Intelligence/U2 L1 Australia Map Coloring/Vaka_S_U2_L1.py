from tkinter import *
from graphics import *


def check_complete(assignment, vars, adjs):
    for i in vars:
        if i not in assignment:
            return False
    return True


def select_unassigned_var(assignment, vars, adjs):
    # Select an unassigned variable - forward checking, MRV, or LCV
    # returns a variable
    for i in vars:
        if i not in assignment:
            return i


def isValid(value, var, assignment, variables, adjs):
    # value is consistent with assignment
    # check adjacents to check 'var' is working or not.
    if var in adjs:
        for a in adjs[var]:
            if a in assignment and assignment[a] == value:
                return False
    return True


def backtracking_search(variables, adjs, shapes, frame):
    assignment = recursive_backtracking({}, variables, adjs, shapes, frame)
    for s, points in shapes.items():
        draw_shape(points, frame, assignment[s])
    return assignment


def recursive_backtracking(assignment, variables, adjs, shapes, frame):
    # Refer the pseudo code given in class.
    if check_complete(assignment, variables, adjs):
        return assignment
    uv = select_unassigned_var(assignment, variables, adjs)
    for i in variables[uv]:
        if isValid(i, uv, assignment, variables, adjs):
            assignment[uv] = i
            result = recursive_backtracking(assignment, variables, adjs, shapes, frame)
            if result is not None:
                return result
    return None


# return shapes as {region:[points], ...} form
def read_shape(filename):
    infile = open(filename)
    region, points, shapes = "", [], {}
    for line in infile.readlines():
        line = line.strip()
        if line.isalpha():
            if region != "":
                shapes[region] = points
            region, points = line, []
        else:
            x, y = line.split(" ")
            points.append(Point(int(x), 300 - int(y)))
    shapes[region] = points
    return shapes


# fill the shape
def draw_shape(points, frame, color):
    shape = Polygon(points)
    shape.setFill(color)
    shape.setOutline("black")
    shape.draw(frame)
    time.sleep(.15)


def main():
    regions, variables, adjacents = [], {}, {}
    # Read mcNodes.txt and store all regions in regions list
    with open("mcNodes.txt") as file:
        for line in file:
            regions.append(line.rstrip())
    # Fill variables by using regions list -- no additional code for this part
    for r in regions:
        variables[r] = {'red', 'green', 'blue'}
    # Read mcEdges.txt and fill the adjacents. Edges are bi-directional.
    with open("mcEdges.txt") as file:
        for line in file:
            a, b = line.rstrip().split()
            if a in adjacents:
                adjacents[a].add(b)
            else:
                adjacents[a] = {b}
            if b in adjacents:
                adjacents[b].add(a)
            else:
                adjacents[b] = {a}
    # Set graphics -- no additional code for this part
    frame = GraphWin('Map', 300, 300)
    frame.setCoords(0, 0, 299, 299)
    shapes = read_shape("mcPoints.txt")
    for s, points in shapes.items():
        draw_shape(points, frame, 'white')
    # solve the map coloring problem by using backtracking_search -- no additional code for this part
    solution = backtracking_search(variables, adjacents, shapes, frame)
    print(solution)
    mainloop()


if __name__ == '__main__':
    main()

''' Sample output:
{'WA': 'red', 'NT': 'green', 'SA': 'blue', 'Q': 'red', 'NSW': 'green', 'V': 'red', 'T': 'red'}
By using graphics functions, visualize the map.
'''
