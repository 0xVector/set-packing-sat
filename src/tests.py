from random import randint

def chance(val: int) -> bool:
    return randint(1, 100) <= val

def random_problem(n: int, k: int) -> list[set[int]]:
    u = list(range(n))
    return list(filter(lambda x: len(x) > 0, (set(i for i in u if chance(20)) for _ in range(k))))
