import subprocess
from itertools import chain

from set_packing.encoding import encode, decode
from set_packing.input import store_problem

# Constants
DEFAULT_CNF_FILENAME = "encodings/encoding.cnf"
DEFAULT_INSTANCE_FILENAME = "instances/problem.in"
DEFAULT_SOLVER = "glucose-syrup"
SOLVER_OPTIONS = []#["-maxnbthreads=8", "-maxmemory=200000"]
LINE_ENDING = "0"


def store_cnf(variables: int, cnf: frozenset[frozenset[int]], file_name: str = DEFAULT_CNF_FILENAME):
    with open(file_name, "w") as file:
        print(f"p cnf {variables} {len(cnf)}", file=file, flush=False)
        lines = (" ".join(chain(map(str, clause), LINE_ENDING)) for clause in cnf)
        for line in lines:
            print(line, file=file, flush=False)


def run_sat(cnf_file: str = DEFAULT_CNF_FILENAME, solver: str = DEFAULT_SOLVER, verbosity: int = 1) -> tuple[
    int, list[str]]:
    command = [f"./{solver}", "-model", f"-verb={verbosity}", *SOLVER_OPTIONS, cnf_file]
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
    print(f"Input: t={t}, {subsets}")
    if err_code == 10:
        print("Satisfiable!")
        model = parse_model(out)
        print("Model: ", model)
        selected, subsets_selected = decode(model, subsets)
        print(f"That means these subsets were selected (indexed from 0): {', '.join(map(str, selected))}")
        print(*subsets_selected)
    elif err_code == 20:
        print("Not satisfiable.")
    else:
        print("Error occurred.")


def solve_print_report(problem: tuple[int, int, list[set[int]]], args, store: bool = False):
    if store:
        store_problem(problem, args.input)
        print(f"Stored the problem to {args.input}")
    n, t, subsets = problem
    print("Encoding...")
    v, cnf = encode(t, subsets)
    print("...done.")

    store_cnf(v, cnf, file_name=args.output)
    print(f"Stored the encoding CNF file to {args.output}")

    print(f"Running solver {args.solver}...")
    result = run_sat(cnf_file=args.output, solver=args.solver, verbosity=args.verb)
    print()
    print_report(t, subsets, result)
