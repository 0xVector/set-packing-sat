#!/usr/bin/env python3
import subprocess
from itertools import chain
from subprocess import CompletedProcess

from input import load_problem, store_problem
from encoding import encode, decode
from tests import random_problem

# Constants
DEFAULT_CNF_FILENAME = "encodings/encoding.cnf"
DEFAULT_SOLVER = "glucose-syrup"
SOLVER_OPTIONS = "-maxnbthreads=8 -maxmemory=200000 -verb=2"

LINE_ENDING = "0"


def store_cnf(variables: int, cnf: frozenset[frozenset[int]], file_name: str = "encodings/encoding.cnf"):
    with open(file_name, "w") as file:
        print(f"p cnf {variables} {len(cnf)}", file=file, flush=False)
        lines = (" ".join(chain(map(str, clause), LINE_ENDING)) for clause in cnf)
        for line in lines:
            print(line, file=file, flush=False)


def run_sat(cnf_file: str = DEFAULT_CNF_FILENAME, solver: str = DEFAULT_SOLVER) -> tuple[int, list[str]]:
    command = [f"./{solver}", "-model", SOLVER_OPTIONS, cnf_file]
    stdout = []
    with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
        for line in process.stdout:
            line = line.decode().strip()
            stdout.append(line)
            print(line, flush=True)

    err_code = process.wait()
    return err_code, stdout


def parse_model(out: list[str]) -> list[int]:
    model = []
    for line in out:
        if line.startswith("v"):
            values = list(map(int, line[1:].split()))
            model.extend(values)
    model.remove(0)
    return model


def pretty_print(ss):
    print(*[list(s) for s in ss], sep='\n')


def print_report(t: int, subsets: list[set[int]], result: [int, list[str]]):
    err_code, out = result
    # for line in out:
    #     print(line)

    if err_code == 10:
        print(f"Input: t={t}, {subsets}")
        model = parse_model(out)
        print("Model: ", model)
        selected, subsets_selected = decode(model, subsets)
        print(f"That means these subsets were selected: {selected}")
        print(*subsets_selected)
    elif err_code == 20:
        print("Unsat :(")
    else:
        print("BIG ERROR")


def solve_print_report(problem: tuple[int, int, list[set[int]]], problem_file_name="input/problem.txt"):
    store_problem(problem, problem_file_name)
    n, t, subsets = problem
    v, cnf = encode(t, subsets)
    store_cnf(v, cnf)
    result = run_sat()
    print_report(t, subsets, result)


def run():
    # subsets = [{0, 1, 2}, {0, 2, 4}, {50}, {2, 0}, {7}, {8}, {3, 5, 1}, {7, 4,1}]
    # subsets = [{0, 1, 4}, {0, 2}, {1, 3}, {2, 5}, {1, 2, 5}]
    # subsets = [{0,1,2},{0,1,3},{1,2,4},{0,1,2,3,4,5},{2},{2,3,4,5},{0,2,5},{3,6,7},{6,7},{3,5,8},{5,2,8}]
    # n=8, k=28, t=6 unsat big ~30s

    # n, k, t = 30, 28, 6 # big cnf file, long encoding, long sat
    n, k, t = 10, 20, 7 # mid cnf file, very quick encoding, mid sat
    problem = (n, t, random_problem(n, k))
    solve_print_report(problem)


if __name__ == "__main__":
    run()
