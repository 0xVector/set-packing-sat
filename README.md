# SAT project - Set packing problem

## Set packing

For the universe $\cal{U}$ and a family $\cal{S}$ of subsets of $\cal{U}$, we're asking if there is a packing
$\cal{P} \subseteq \cal{S}$ such that all sets in $\cal{P}$ are pairwise disjoint and $|\cal{P}|=t$ for some
input integer $t$.  
Let $n=|\cal{U}|$ and $k=|\cal{S}|$.

### Encoding

#### Variables

Let $v_{i,j}$ denote that $u_i \in \cal{U}$ (the $i$-th element of the universe, in some ordering) is selected
to be a part of the $j$-th subset in $\cal{S}$ (in an arbitrary ordering), i.e. $u_i \in s_j$ for $s_j \in \cal{S}$.  
We have $n=|\cal{S}|$ variables $p_1, ..., p_n$.
Variable $p_i$ means that subset $s_i \in \cal{P}$
(i.e. when $p_i=1$, the subset $s_i$ was picked for the packing $\cal{P}$). 

#### Constraints

- The subsets have to be pairwise disjoint  
We can enforce this by allowing an element to be in at most one subset, i.e.
for the $i$-th element: $\forall v_{i,j}, v_{i,l}: (u_i \in s_j \land u_i \in s_l) \implies \neg v_{i,j} \lor \neg v_{i,l}$.  
Do note that an element doesn't have to be selected to be a part of any subset in the packing.


- Either the whole subset, or nothing from it has to be selected
We can enforce this by a set of equivalences:
for the $j$-th subset: $\forall v_{i,j}, v_{l,j}: (u_i \in s_j \land u_l \in s_j) \implies (v_{i,j} \iff v_{k,l})$


- There has to be exactly $t$ selected subsets  
Thanks to previous constraint, any variable from a single subset says if the whole subset was selected or not. We can just
use the first one from each subset to mean that the subset was selected,
i.e. if $u_i \in s_j$, $v_{i,j}$ says whether subset $s_j$ was selected. We pick $n$ such variables and ensure exactly $t$
of have value $1$ by considering all subsets of size $t$, then forcing that particular model by a big conjunction
and finally adding all of these elementary conjunctions together to form a big disjunction selecting any suitable model.


We will of course only generate those constraints that have their left side of the implication fulfilled,
e.g. equivalences only amongst elements of a single subset.
