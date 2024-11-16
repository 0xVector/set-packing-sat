from random import randint


def random_problem(n: int, k: int) -> list[set[int]]:
    u = list(range(n))
    return list(filter(lambda x: len(x) > 0, (set(i for i in u if randint(1, 10) <= 3) for _ in range(k))))
