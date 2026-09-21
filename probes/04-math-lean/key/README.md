# Answer key

Every item is a statement, not a number. The `.lean` files here hold the statements with `sorry`.
Grading: paste the model's file into a fresh Mathlib project and run `lake env lean <file>`.
An item is correct only if the statement is unchanged, the file compiles, and `#print axioms` shows nothing beyond `propext`, `Classical.choice`, `Quot.sound`.
`grade_lean.py` does this for every output in `outputs/`.
