# SAT project - Set packing problem

## Set packing

For the universe $\cal{U}$ and a family $\cal{S}$ of subsets of $\cal{U}$,
we're looking for a packing $\cal{P} \subseteq \cal{S}$ such that all sets
in $\cal{P}$ are pairwise disjoint.

### Encoding

#### Variables

Let $s_i \in \cal{S}$ denote the $i$-th subset in $\cal{S}$ in an arbitrary
ordering. We have $n=|\cal{S}|$ variables $p_1, ..., p_n$.
Variable $p_i$ means that subset $s_i \in \cal{P}$
(i.e. when $p_i=1$, the subset $s_i$ was picked for the packing $\cal{P}$). 

#### Constraints

- The subsets have to be pairwise disjoint  
We can enforce this by forbidding selecting both elements in each pair that is not disjoint, i.e.
$\forall s_a, s_b \in \cal{S}:\neg(s_a \land s_b)$


- There has to be exactly $k$ selected subsets  
i.e. models must have exactly $k$ variables with the value $1$.

(subset of size k)or(subset of size k)or(subset of size k)