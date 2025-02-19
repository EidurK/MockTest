# Fact

Consider a relation 𝑅(𝐴, 𝐵, 𝐶, 𝐷, 𝐸) and a collection of functional
dependencies (FD’s) 𝐹 = {𝐵 → 𝐸, 𝐵 → 𝐴, 𝐶𝐸 → 𝐵, 𝐶 → 𝐷}
What are all the candidate keys of 𝑅?

# Question
Given a relation $R(A, B, C, D, E)$ with the functional dependencies $F = \{B \to A, B \to C, DE \to B, D \to E\}$, which of the following options represent candidate key(s) for the relation $R$? Select and justify why each option could or could not be a candidate key.

- [ ] DE (DE can determine B, A, C, and E, therefore it covers all attributes, making it a candidate key).
- [ ] BD (BD cannot determine all other attributes, thus it is not a candidate key).
- [ ] BE (BE cannot determine D, hence it fails to cover all attributes and is not a candidate key).
- [ ] BDE (BDE trivially determines all attributes, but it is not minimal as DE alone is sufficient).
