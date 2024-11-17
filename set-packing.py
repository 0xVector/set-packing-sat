#!/usr/bin/env python3

from argparse import ArgumentParser

from set_packing.input import load_problem
from set_packing.input import configure_input_parser
from set_packing.runner import solve_print_report
from set_packing.tests import random_problem_sparse, random_problem


def run():
    # subsets = [{0, 1, 2}, {0, 2, 4}, {50}, {2, 0}, {7}, {8}, {3, 5, 1}, {7, 4,1}]
    # subsets = [{0, 1, 4}, {0, 2}, {1, 3}, {2, 5}, {1, 2, 5}]
    # subsets = [{0,1,2},{0,1,3},{1,2,4},{0,1,2,3,4,5},{2},{2,3,4,5},{0,2,5},{3,6,7},{6,7},{3,5,8},{5,2,8}]
    # n=8, k=28, t=6 unsat big ~30s

    parser = ArgumentParser()
    configure_input_parser(parser)
    args = parser.parse_args()
    problem = load_problem(args.input)

    # n, k, t = 30, 28, 6 # big cnf file, long encoding, long sat
    # n, k, t = 10, 20, 7  # mid cnf file, very quick encoding, mid sat
    n, k, t = 15, 22, 8
    # problem = (n, t, random_problem(n, k))
    # problem = (n, t, random_problem_sparse(n, k))
    # problem = load_problem("instances/problem-unsat-small.in")

    solve_print_report(problem, args)


if __name__ == "__main__":
    run()
