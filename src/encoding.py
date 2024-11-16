from itertools import combinations, product

FALSE_CNF = frozenset((frozenset([1]), frozenset([-1])))  # 2 clauses with just opposite literals - false in CNF


# Returns the encoding as a pair (variables, CNF)
def encode(t: int, subsets: list[set[int]]) -> tuple[int, frozenset[frozenset[int]]]:
    k = len(subsets)
    cnf = set()
    cnf.update(encode_disjoint(subsets))
    print("disjoint done")
    cnf.update(encode_at_least_t(k, t))
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


# Encode that at least t variables (from k variables in total) have their value set to 1
# This method goes through all models and forbids each non-model
def encode_at_least_t(k: int, t: int) -> frozenset[frozenset[int]]:
    cnf = set()
    total = 2 ** k
    p = total // 10
    for n in range(total):
        if n % p == 0: print(f"{int(round(n/total*100))}% ", end="")
        bits = f"{n:0{k}b}"
        if bits.count("1") >= t:
            continue
        clause = frozenset(-var(i) if b == "1" else var(i) for i, b in enumerate(bits))
        cnf.add(clause)

    return frozenset(cnf)


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
