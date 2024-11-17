# Returns the input in a form of a triple (n, t, S), where n is the size of the universe U, t is the desired
# packing size and S is a set of the possible subsets. Elements of U are represented by integers 0...(n-1)
#
# Expects input file in the following format, with one subset on each line (k+1 lines):
# n k t
# < elements of 1st subset, space separated >
# ...
def load_problem(file_name: str) -> tuple[int, int, list[set[int]]]:
    with open(file_name) as file:
        n, k, t = map(int, file.readline().split())
        subsets = [set(map(int, file.readline().split())) for _ in range(k)]
    return n, t, subsets


# Stores the problem in the format readable by load_problem
def store_problem(problem: tuple[int, int, list[set[int]]], file_name: str):
    n, t, subsets = problem
    k = len(subsets)
    with open(file_name, "w") as file:
        print(n, k, t, sep=" ", file=file, flush=True)
        for subset in subsets:
            print(*subset, sep=" ", file=file, flush=True)

