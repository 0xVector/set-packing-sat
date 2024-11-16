#!/usr/bin/env python3
import subprocess
from itertools import chain
from subprocess import CompletedProcess

from encoding import encode, decode, encode_at_least_t
from tests import random_problem

# Constants
DEFAULT_FILENAME = "encoding.cnf"
DEFAULT_SOLVER = "glucose"

LINE_ENDING = "0"


# Returns the input in a form of a triple (n, t, S), where n is the size of the universe U, t is the desired
# packing size and S is a set of the possible subsets. Elements of U are represented by integers 0...(n-1)
def load(file_name: str) -> tuple[int, int, list[set[int]]]:
    with open(file_name) as file:
        n, k, t = map(int, file.readline())
        subsets = [set(map(int, file.readline().split())) for _ in range(k)]
    return n, t, subsets


def store_cnf(variables: int, cnf: frozenset[frozenset[int]], file_name: str = "encoding.cnf"):
    with open(file_name, "w") as file:
        print(f"p cnf {variables} {len(cnf)}", file=file, flush=False)
        lines = (" ".join(chain(map(str, clause), LINE_ENDING)) for clause in cnf)
        for line in lines:
            print(line, file=file, flush=False)


def run_sat(cnf_file: str = DEFAULT_FILENAME, solver: str = DEFAULT_SOLVER):
    return subprocess.run([f"./{solver}", "-model", cnf_file], stdout=subprocess.PIPE)


def print_sat_result(result: CompletedProcess):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)


def is_sat(result: CompletedProcess) -> bool:
    return result.returncode == 10


def parse_model(result: CompletedProcess) -> list[int]:
    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):
            values = list(map(int, line[1:].split()))
            model.extend(values)
    model.remove(0)
    return model


def pretty_print(ss):
    print(*[list(s) for s in ss], sep='\n')


def print_report(t: int, subsets: list[set[int]], result: CompletedProcess):
    print_sat_result(result)
    if is_sat(result):
        print(f"Input: t={t}, {subsets}")
        model = parse_model(result)
        print("Model: ", model)
        selected, subsets_selected = decode(model, subsets)
        print(f"That means these subsets were selected: {selected}")
        print(*subsets_selected)
    elif result.returncode == 20:
        print("Unsat :(")
    else:
        print("BIG ERROR")


def run():
    # subsets = [{0, 1, 2}, {0, 2, 4}, {50}, {2, 0}, {7}, {8}, {3, 5, 1}, {7, 4,1}]
    # subsets = [{0, 1, 4}, {0, 2}, {1, 3}, {2, 5}, {1, 2, 5}]
    # subsets = [
    #     {0,1,2},{0,1,3},{1,2,4},{0,1,2,3,4,5},{2},{2,3,4,5},{0,2,5},{3,6,7},{6,7},{3,5,8},{5,2,8},
    # ]
    subsets = random_problem(8, 28)
    # n=8, k=28, t=6 unsat big ~30s

    t = 5
    v, cnf = encode(t, subsets)

    # pretty_print(cnf)
    store_cnf(v, cnf)
    result = run_sat()
    print_report(t, subsets, result)

    # pretty_print(encode_exactly_t(10, 5))


if __name__ == "__main__":
    run()
