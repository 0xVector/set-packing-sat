#!/usr/bin/env python3
import subprocess
from itertools import combinations, product, chain
from subprocess import CompletedProcess

# Constants
DEFAULT_FILENAME = "encoding.cnf"
DEFAULT_SOLVER = "glucose"

FALSE_CNF = frozenset((frozenset([1]), frozenset([-1])))  # 2 clauses with just opposite literals - false in CNF
LINE_ENDING = "0"


# Returns the input in a form of a triple (n, t, S), where n is the size of the universe U, t is the desired
# packing size and S is a set of the possible subsets. Elements of U are represented by integers 0...(n-1)
def load(file_name: str) -> tuple[int, int, list[set[int]]]:
    with open(file_name) as file:
        n, k, t = map(int, file.readline())
        subsets = [set(map(int, file.readline().split())) for _ in range(k)]
    return n, t, subsets


# Returns the encoding as a pair (variables, CNF)
def encode(t: int, subsets: list[set[int]]) -> tuple[int, frozenset[frozenset[int]]]:
    k = len(subsets)
    cnf = set()
    cnf.update(encode_disjoint(subsets))
    print("disjoint done")
    cnf.update(encode_exactly_t(t, k))
    print("exactly t done")
    return k, frozenset(cnf)


def encode_disjoint(subsets: list[set[int]]) -> frozenset[frozenset[int]]:
    cnf = set()
    for a_i, a in enumerate(subsets):
        for b_i, b in enumerate(subsets[a_i + 1:], start=a_i + 1):  # skip self + duplicates
            if a.isdisjoint(b):
                continue
            clause = frozenset((-var(a_i), -var(b_i)))
            cnf.add(clause)
    return frozenset(cnf)


# Encode that exactly t variables (from k variables in total) have their value set to 1
def encode_exactly_t(t: int, k: int) -> frozenset[frozenset[int]]:
    # dnf = frozenset(frozenset(subset) for subset in combinations(range(k), t))
    dnf = set()
    for selected in combinations(range(k), t):
        conj = frozenset(var(v) if v in selected else -var(v) for v in range(k))
        dnf.add(conj)
    return to_cnf(frozenset(dnf)) if len(dnf) > 0 else FALSE_CNF  # empty DNF is an empty disjunction, thus false


def to_cnf(dnf: frozenset[frozenset[int]]) -> frozenset[frozenset[int]]:
    cnf = set()
    for prod in product(*dnf):
        cnf.add(frozenset(prod))
    return frozenset(cnf)


def var(subset_index: int) -> int:
    return subset_index + 1


def var_to_set_index(var_: int) -> int:
    return var_ - 1


# Decodes the model into a pair (selected, subsets), where selected are the indices of the selected subsets from input
# and subsets are the subsets themselves
def decode(model: list[int], subsets: list[set[int]]) -> tuple[list[int], list[set[int]]]:
    selected = list(map(var_to_set_index, filter(lambda x: x > 0, model)))
    subsets_chosen = []
    for v in model:
        if v > 0:
            subsets_chosen.append(subsets[var_to_set_index(v)])
    return selected, subsets_chosen


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

def print_report(subsets: list[set[int]], result: CompletedProcess):
    print_sat_result(result)
    if is_sat(result):
        print(f"Input: {subsets}")
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
    subsets = [{0, 1, 2}, {0, 2, 4}, {50}, {2, 0}, {7},{8}]
    v, cnf = encode(2, subsets)

    pretty_print(cnf)
    store_cnf(v, cnf)
    # pretty_print(encode_exactly_t(3, 5))
    result = run_sat()
    print_report(subsets, result)



if __name__ == "__main__":
    run()
