from random import randint, shuffle

def chance(val: int) -> bool:
    return randint(1, 100) <= val

def random_problem(n: int, k: int) -> list[set[int]]:
    u = list(range(n))
    return list(filter(lambda x: len(x) > 0, (set(i for i in u if chance(20)) for _ in range(k))))

def random_problem_sparse(n: int, k: int) -> list[set[int]]:
    SIZE = 4
    u = list(range(n))
    problem = set()
    while len(problem) < k:
        size = randint(1, SIZE)
        shuffle(u)
        problem.add(frozenset(u[:size]))
    return [set(s) for s in problem]
