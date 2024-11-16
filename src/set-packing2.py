#!/usr/bin/env python3

# Globals
SUBSET_COUNT = 0

# Returns the input in a form of a triple (n, t, S), where n is the size of the universe U, t is the desired
# packing size and S is a set of the possible subsets. Elements of U are represented by integers 0...(n-1)
def load(file_name: str) -> tuple[int, int, list[list[int]]]:
    with open(file_name) as file:
        n, k, t = map(int, file.readline())
        subsets = [list(map(int, file.readline().split())) for _ in range(k)]
    return n, t, subsets


# Returns the encoding as a pair (variables, CNF)
def encode(n: int, t: int, subsets: list[list[int]]) -> tuple[int, list[list[int]]]:
    ...


def encode_disjoint(n: int, subsets: list[list[int]]) -> list[list[int]]:
    cnf = []
    for u in range(n):
        in_subsets = [i for i, s in enumerate(subsets) if u in s]
        for i, a in enumerate(in_subsets):
            for b in in_subsets[i + 1:]:  # skip self + duplicates
                clause = [-var_id(u, a), -var_id(u, b)]
                cnf.append(clause)
    return cnf

def var_id(element: int, subset: int):
    return element + subset*10

def subset_id(subset_index: int) -> int:
    return subset_index


def decode():
    ...


def store_cnf():
    ...


def run():
    subsets = [[1,2,3,4,5], [1,2], [3, 4]]
    n = 5
    print(encode_disjoint(n, subsets))


if __name__ == "__main__":
    run()
