# SAT project - Set packing problem

## Set packing

For the universe $\cal{U}$ and a family $\cal{S}$ of subsets of $\cal{U}$, we're asking if there is a packing
$\cal{P} \subseteq \cal{S}$ such that all sets in $\cal{P}$ are pairwise disjoint and $|\cal{P}|=t$ for some
input integer $t$.  
Let $n=|\cal{U}|$ and $k=|\cal{S}|$.

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
We could enforce this by, e.g., specifying all models with at least $t$ positive variables (as conjunctions in DNF) and
converting to CNF. A simpler method is to directly specify all non-models in CNF, i.e. add a clause
with the negated elementary expression for each non-model. This method also seems to be faster,
since the conversion to DNF is more complicated.  
Example: for variables $p_1, p_2, p_3, p_4$ and $t=2$, the model $v=(1, 0, 0, 0)$ has just 1 positive variable,
thus it's not a model of our theory. By adding a clause $C={\neg p_1, p_2, p_3, p_4}$, we ensure that exactly this model
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

- The subsets have to be pairwise disjoint *(this is just encoded in a different way in comparison to the previous encoding)*  
We can enforce this by allowing an element to be in at most one subset, i.e.
for the $i$-th element: $\forall p_{i,j}, p_{i,l}, j \neq l: (u_i \in s_j \land u_i \in s_l) \implies \neg p_{i,j} \lor \neg p_{i,l}$.  
Do note that an element doesn't have to be selected to be a part of any subset in the packing.


- Either the whole subset, or nothing from it has to be selected *(this is an extra constraint created by different
variable selection, in the previous encoding we get this for free)*  
We can enforce this by a set of equivalences:
for the $j$-th subset: $\forall p_{i,j}, p_{l,j}, i \neq l: (u_i \in s_j \land u_l \in s_j) \implies (p_{i,j} \iff p_{l,j})$


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

### Big

#### Satisfiable

- [problem-sat-68k.in](./instances/problem-sat-68k.in): 68,553 clauses, ENCODE?, takes ~15s to solve
4.98 MB encoded file size

- [problem-sat-122k.in](./instances/problem-sat-122k.in): 68,553 clauses, ENCODE?, takes ~55s to solve
10.01 MB encoded file size

- [problem-sat-110k-7.in](./instances/problem-sat-110k-7.in): ??? clauses, ENCODE?, takes ~???s to solve
???? MB encoded file size, finds solution of size 7

#### Unsatisfiable

- [problem-unsat-280k.in](./instances/problem-unsat-280k.in): 280,687 clauses, quick to encode, takes ~160s to run   
18.36 MB encoded file size
## Experiments