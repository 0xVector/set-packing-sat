# SAT project - Set packing problem

## Problem description

according to [Wikipedia](https://en.wikipedia.org/wiki/Set_packing):

> **Set packing** is a classical NP-complete problem in computational complexity theory and combinatorics,
> and was one of Karp's 21 NP-complete problems.
> Suppose one has a finite set S and a list of subsets of S.
> Then, the set packing problem asks if some k subsets in the list are pairwise disjoint
> (in other words, no two of them share an element).

Formally,
for the universe $\cal{U}$ and a family $\cal{S}$ of subsets of $\cal{U}$, we're asking if there is a packing
$\cal{P} \subseteq \cal{S}$ such that all sets in $\cal{P}$ are pairwise disjoint and $|\cal{P}|=t$ for some
input integer $t$.  
Let $n=|\cal{U}|$ and $k=|\cal{S}|$.

## Usage

The script can be run from terminal or imported into existing python scripts. Do note that when running in terminal,
the `set_packing` directory with the python sources has to be in the same location as the script.

### Terminal

Basic usage:

```shell
./set-packing.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

- `-h`, `--help` : Show a help message and exit.
- `-i INPUT`, `--input INPUT` : The instance file. *Default: `instances/problem.in`.*
- `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula).
  *Default: `encodings/encoding.cnf`.*
- `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used. *Default: `glucose-syrup`.*
- `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.

## Input

The input for the problem are three parameters - $n, k, t$ and the family of subsets, $S$.

The script expects an input file in the following format, with one subset on each line (exactly $k+1$ lines):

```
n k t
< elements of the 1st subset, space separated >
< elements of the 2nd subset, space separated >
...
< elements of the k-th subset, space separated >
```

The elements are natural numbers from $0$ to $k-1$.

Example input:

```
5 3 2
0 1 2
3 4
1 2 3 4
```

## Encoding

### Variables

Let $s_i \in \cal{S}$ denote the $i$-th subset in $\cal{S}$ in an arbitrary
ordering. We have $k$ variables $p_1, ..., p_k$.
Variable $p_i$ means that subset $s_i \in \cal{P}$ was selected for the packing.
(i.e. when $p_i=1$, the subset $s_i$ was selected for the packing $\cal{P}$).

### Constraints

- The subsets have to be pairwise disjoint  
  We can enforce this by forbidding selecting both elements in each pair that is not disjoint, i.e.
  $\forall s_a, s_b \in \cal{S}: (s_a \cap s_b \neq \emptyset) \implies (\neg s_a \lor \neg  s_b)$


- There have to be at least $t$ selected subsets  
  i.e. models must have at least $t$ positive variables.  
  We could enforce this by, e.g., specifying all models with at least $t$ positive variables (as conjunctions in DNF)
  and
  converting to CNF. A simpler method is to directly specify all non-models in CNF, i.e. add a clause
  with the negated elementary expression for each non-model. This method also seems to be faster,
  since the conversion to DNF is more complicated.  
  Example: for variables $p_1, p_2, p_3, p_4$ and $t=2$, the model $v=(1, 0, 0, 0)$ has just 1 positive variable,
  thus it's not a model of our theory. By adding a clause $C={\neg p_1, p_2, p_3, p_4}$, we ensure that exactly this
  model
  can't be a model that the SAT solver finds.

### Alternative encodings

I strongly considered a second encoding, but decided against it with a simpler implementation in mind.

This encoding differs in dealing with the subset pairwise disjunction by encoding it as a part of the formula instead
of checking it directly and forbidding offending pairs.

#### Variables

Let $p_{i,j}$ denote that $u_i \in \cal{U}$ (the $i$-th element of the universe, in some ordering) is selected
to be a part of the $j$-th subset in $\cal{S}$ (in an arbitrary ordering), i.e. $u_i \in s_j$ for $s_j \in \cal{S}$.  
We have $\sum^{k}_{i=1}{|s_i|}$ variables in total.

#### Constraints

- The subsets have to be pairwise disjoint *(this is just encoded in a different way in comparison to the previous
  encoding)*  
  We can enforce this by allowing an element to be in at most one subset, i.e.
  for the $i$-th
  element: $\forall p_{i,j}, p_{i,l}, j \neq l: (u_i \in s_j \land u_i \in s_l) \implies \neg p_{i,j} \lor \neg p_{i,l}$.  
  Do note that an element doesn't have to be selected to be a part of any subset in the packing.


- Either the whole subset, or nothing from it has to be selected *(this is an extra constraint created by different
  variable selection, in the previous encoding we get this for free)*  
  We can enforce this by a set of equivalences:
  for the $j$-th
  subset: $\forall p_{i,j}, p_{l,j}, i \neq l: (u_i \in s_j \land u_l \in s_j) \implies (p_{i,j} \iff p_{l,j})$


- There have to be at least $t$ selected subsets *(exactly the same as previous encoding, we just have to pick
  one variable from each to represent the subset as a whole)*  
  Thanks to previous constraint, any variable from a single subset says if the whole subset was selected or not.
  We can just use the first one from each subset to mean that the subset was selected,
  i.e. if $u_i \in s_j$, then $p_{i,j}$ says whether subset $s_j$ was selected. We pick $k$ such variables and ensure
  exactly $t$ of them are positive by the same system as in previous encoding.

We will of course only generate those constraints that have their left side of the implication fulfilled,
e.g. equivalences only amongst elements of a single subset.

### Efficiency

The main bottleneck of the encoding algorithm is that at least $t$ variables have to be positive, i.e. a cardinality
constraint. The used encoding enumerates all models to find the ones not satisfying it, which means that its complexity
is $O(2^k)$.  
More efficient encoding would entail a study of better ways to encode this constraint, which is beyond the scope
of this project.

## Test instances

In `instances/`

### Human-sized

- [problem-sat-small.in](./instances/problem-sat-small.in)

- [problem-unsat-small.in](./instances/problem-unsat-small.in)

### Big

Run times are measured on the same computer as in [Experiments](#Experiments).

#### Satisfiable

- [problem-sat-68k.in](./instances/problem-sat-68k.in): 68,553 clauses, takes ~15s to solve
  4.98 MB encoded file size

- [problem-sat-122k.in](./instances/problem-sat-122k.in): 68,553 clauses, takes ~55s to solve
  10.01 MB encoded file size

- [problem-sat-110k.in](./instances/problem-sat-110k.in): 110k clauses, finds solution of size 7

- [problem-sat-280k.in](./instances/problem-sat-280k.in): 280,675 clauses, ~2.8 s to encode, takes ~155 s to solve  
  18.36 MB encoded file size, finds solution of size 8

#### Unsatisfiable

- [problem-unsat-280k.in](./instances/problem-unsat-280k.in): 280,687 clauses, quick to encode, takes ~160s to run   
  18.36 MB encoded file size

## Experiments

The experiments were run on AMD Ryzen 5 7600X (12) @ 5.453 GHz and 32 GB RAM on Arch Linux.
The solver used was `glucose-syrup`.
Time was measured with `hyperfine`.

### Time to solve

This experiment measured the time to solve based on the input parameters.  
These 3 parameters are just a rough estimation of the problem complexity, as the choice of subset family
is equally significant. This approach was chosen because of its relative simplicity.

The inputs were generated randomly by the functions in [set_packing/tests.py](./set_packing/tests.py).

#### Solvable instances

Sparse subsets (max size 4), $k$ vs time

| $n$ | $k$ | $t$ | CNF clauses | encoding time | solving time | instance                                                                    |
|-----|-----|-----|-------------|---------------|--------------|-----------------------------------------------------------------------------|
| 10  | 24  | 5   | 13113       | 3.746 s       | 719.2 ms     | [time-sat-sparse-1.in](instances/experiments/time-sat/time-sat-sparse-1.in) |
| 10  | 25  | 5   | 15460       | 8.277 s       | 909.3 ms     | [time-sat-sparse-2.in](instances/experiments/time-sat/time-sat-sparse-2.in) |
| 10  | 26  | 5   | 18070       | 15.001 s      | 1.411 s      | [time-sat-sparse-3.in](instances/experiments/time-sat/time-sat-sparse-3.in) |
| 10  | 27  | 5   | 21048       | 29.611 s      | 1.827 s      | [time-sat-sparse-4.in](instances/experiments/time-sat/time-sat-sparse-4.in) |

We can conclude that in this range of the input parameters, the encoding phase dominates the computation time, which is
to be
expected, as it's complexity is $O(2^k)$.

Sparse subsets (max size 4), smaller $\cal U$, $t$ vs time

| $n$ | $k$ | $t$ | CNF clauses | encoding time | solving time | instance                                                                       |
|-----|-----|-----|-------------|---------------|--------------|--------------------------------------------------------------------------------|
| 15  | 22  | 4   | 1881        | 953.4 ms      | 38.6 ms      | [time-sat2-sparse-1.in](instances/experiments/time-sat2/time-sat2-sparse-1.in) |
| 15  | 22  | 5   | 9196        | 998.2 ms      | 396.4 ms     | [time-sat2-sparse-2.in](instances/experiments/time-sat2/time-sat2-sparse-2.in) |
| 15  | 22  | 6   | 35,536      | 1.161 s       | 3.923 s      | [time-sat2-sparse-3.in](instances/experiments/time-sat2/time-sat2-sparse-3.in) |
| 15  | 22  | 7   | 110,159     | 1.643 s       | 33.350 s     | [time-sat2-sparse-4.in](instances/experiments/time-sat2/time-sat2-sparse-4.in) |
| 15  | 22  | 8   | 280,675     | 2.891 s       | 155.895 s    | [time-sat2-sparse-5.in](instances/experiments/time-sat2/time-sat2-sparse-5.in) |