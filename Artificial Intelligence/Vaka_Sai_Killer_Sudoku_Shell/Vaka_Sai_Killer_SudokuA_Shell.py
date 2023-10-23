from time import perf_counter


def isValid(neighbors, assignment, var, val):
    pass
    # check neighbors of the var


def recBacktrack(assignment, neighbors, sums, keyind, valind, cursum):
    pass
    # select a var
    # iterate through values
    # check isValid
    # if valid, check if you have met the sum
    # otherwise recur deeper

def main():
    t_start = perf_counter()
    neighbors = []
    # create neighbors, you can generate it or paste it in
    sums = []
    with open("input.txt", "r") as file:
        while line := file.readline().rstrip():
            pass
            # process the input into sums and neighbors
    sol = recBacktrack([0] * 81, neighbors, sums, 0, 0, 0)
    if sol is None:
        print("No Solution")
    else:
        for i in range(0, len(sol), 9):
            print(sol[i: i + 9])
    print(f'Time Elapsed: {perf_counter() - t_start}')
    # outputs the solution and time elapsed


if __name__ == "__main__":
    main()
