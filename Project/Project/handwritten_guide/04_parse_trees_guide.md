# Parse Trees for NumPat - Examples with Explanation

## How to Draw Parse Trees

### Step-by-Step Guide

**Process:**
1. Start with the program at the root
2. For each non-terminal, expand using grammar rules
3. Leaf nodes are terminals (tokens)
4. Keep expanding until all leaves are terminals

**Example: `let x = 5`**

```
Step 1: Start with Program
Step 2: Program → statements
Step 3: First statement: Declaration
Step 4: Declaration → let identifier = expr
Step 5: Expr → term → factor → number
Step 6: All done - all leaves are terminals!

Final Tree:
        Declaration
       /     |     \
      let   id=x   Expr
              |     |
            Expr   Term
             |     |
            Term  Factor
             |     |
           Factor Number
             |     |
             5     5
```

---

## Example 1: Simple Variable Declaration

**Program:** `let result = 42`

**Derivation:**
```
Program
  → StatementList
    → Statement
      → Declaration
        → let identifier = expr
        → let result = 42
```

**Parse Tree:**
```
                Program
                  |
            StatementList
                  |
             Statement
                  |
           Declaration
          /  |  |  \
        let id = Expr
             |    |
          result Term
                  |
                Factor
                  |
                Number
                  |
                 42
```

**How to derive this:**
1. Program → StatementList → Statement
2. Statement → Declaration
3. Declaration → "let" IDENTIFIER "=" Expr
4. Expr → Term → Factor → Number
5. Fill in values: IDENTIFIER = "result", NUMBER = 42

---

## Example 2: Simple Function Call

**Program:** `print add(3, 4)`

**Parse Tree:**
```
              Program
                |
          StatementList
                |
            Statement
                |
            PrintStmt
                |
              Expr
                |
            Term
                |
              Factor
                |
           FunctionCall
          /    |    \
        id    (  ArgList  )
        |      |    |
       add  Args   Expr
              |     |
           Expr Term
            |   |
           Term Factor
            |    |
           Factor Number
            |    |
           3    (sep)
                Expr
                 |
                Term
                 |
               Factor
                 |
               Number
                 |
                 4
```

**How to derive:**
1. ParseStatement() sees "print" → PrintStmt
2. PrintStmt → "print" Expr
3. Expr → Term → Factor → FunctionCall
4. FunctionCall → id "(" ArgList ")"
5. ArgList → Expr, Expr
6. Each Expr → Term → Factor → Number

---

## Example 3: Binary Operation (Operator Precedence)

**Program:** `let x = a + b * c`

**Key Point:** Parse tree shows that `*` has higher precedence than `+`

**Parse Tree:**
```
                    Declaration
                   /  |  |  \
                 let  id = Expr
                     |    |
                    x    Expr'
                    |    |
                  Term  Expr'
                  |      |
                Factor   +
                  |      |
                  a     Term
                         |
                       Factor
                         |
                         * (mul)
                       /   \
                     Factor Factor
                      |      |
                      b      c

Interpretation: (a + (b * c))
Because multiplication is parsed at TERM level (higher precedence)
```

**How to understand precedence:**

Grammar structure:
```
Expr     → Term Expr'  (low precedence - addition level)
Expr'    → + Term Expr' | ε

Term     → Factor Term' (high precedence - multiplication level)
Term'    → * Factor Term' | ε

Factor   → primary (highest precedence - literals)
```

**Tree construction:**
1. Parse expression starts at Expr (lowest precedence)
2. Expr parses Term, then checks for +
3. Finds +, so parses another Term
4. That Term contains *, which is handled at Term level
5. Result: mult binds tighter than addition ✓

---

## Example 4: Conditional Statement

**Program:**
```
if n < 2 {
    return n
}
```

**Parse Tree:**
```
                    IfStmt
                   /  |  \
                  if Cond  {  StmtList  }
                     |      |
                  Comparison  ReturnStmt
                 /    |    \     |
              Expr  LT  Expr   ReturnValue
              |      |  |      |
            Term    <  Term    Expr
             |           |    |
           Factor       Factor Term
             |           |     |
             n           2    Factor
                              |
                              n

Meaning: if (n < 2) { return n }
```

**Derivation:**
1. IfStmt → "if" Condition "{" StatementList "}"
2. Condition → Expr CompOp Expr
3. First Expr → Term → Factor → n
4. CompOp → <
5. Second Expr → Term → Factor → 2
6. StatementList → ReturnStmt
7. ReturnStmt → "return" Expr
8. Expr → Term → Factor → n

---

## Example 5: Recursive Function Call

**Program:** `fib(n - 1) + fib(n - 2)`

**Parse Tree (showing recursion handling):**
```
                      Expr
                     /  \
                  Term   Expr'
                   |     |
                 Factor  +
                   |     |
            FunctionCall Term
           /    |   \    |
         fib   (  ArgList )  Factor
               |   |        |
             Expr  - (sub) FunctionCall
              |     |     /  |   \
            Term    1   fib  (  ArgList  )
             |           |   |
           Factor        Expr - (sub)
             |           |   |
             n         Term   2
                        |
                      Factor
                        |
                        n

Meaning: fib(n-1) + fib(n-2)

Note: Each function call is handled as Factor level
      Arithmetic inside parentheses is recursive
```

**How to trace:**
1. Top-level: Expr → Term Expr'
2. Expr' sees + → continue with + Term
3. First Term → Factor → FunctionCall
4. Function call expands ArgList
5. ArgList contains Expr (the n-1)
6. That Expr shows subtraction at Expr' level
7. Second part (after +) similar structure

---

## Example 6: Assignment with Expression

**Program:** `result = result * i`

**Parse Tree:**
```
                  Assignment
                 /  |  |  \
               id  = 
                |    Expr
              result |
                    Term
                   /  \
                Factor Term'
                  |   |
                result *
                     |
                   Factor
                     |
                     i

Meaning: result = (result * i)
```

**Reading the tree:**
- Root is Assignment (not Declaration, no "let")
- Left side: identifier "result"
- Right side: expression
- Expression: term with multiplication
- Operands: result (factor), i (factor)

---

## Example 7: Nested Function Calls

**Program:** `print double(add(3, 4))`

**Parse Tree:**
```
                      PrintStmt
                        |
                      Expr
                        |
                      Term
                        |
                      Factor
                        |
                  FunctionCall (double)
                  /    |    \
                double (  ArgList  )
                       |    |
                      Expr  (args)
                       |
                      Term
                       |
                      Factor
                        |
                  FunctionCall (add)
                  /    |    \
                 add  (  ArgList  )
                      |    |
                    Expr   ,   Expr
                     |         |
                    Term      Term
                     |         |
                   Factor    Factor
                     |         |
                     3         4

Meaning: print(double(add(3, 4)))

Order of evaluation:
1. Inner-most: add(3,4) = 7
2. Middle: double(7) = 14
3. Outer: print(14)
```

---

## How to Construct Parse Tree from Code

### Algorithm

```
For any statement:

1. Identify statement type (Declaration, IfStmt, PrintStmt, etc.)
2. Create that node as root
3. For each grammar component:
   a. Create child node for that component
   b. Recursively expand non-terminals
   c. Leave terminals as leaves
4. Label all leaves with token values
5. Label all internal nodes with grammar rule names
```

### Common Patterns

**Pattern 1: Operator Precedence**
```
- Lower precedence operators appear higher in tree
- Higher precedence appear lower in tree
- Result: high precedence computed first ✓
```

**Pattern 2: Right Recursion (Our Grammar)**
```
Expr' rules show right-recursive structure
- Expr → Term Expr'
- Expr' → + Term Expr' | ε
- This creates left-associative trees (correct!)
```

**Pattern 3: Function Calls**
```
Always at Factor level (highest precedence)
- Function arguments are full expressions
- Allows nested function calls ✓
```

---

## Verification: Check Your Trees

After drawing a tree, verify:

1. **No terminals are internal nodes** ✓ (only leaves)
2. **All non-terminals are expanded** ✓ (until reaching terminals)
3. **Terminal sequence reads left-to-right = original input** ✓
4. **Operator precedence is correct** ✓ (check vs grammar)
5. **Associativity is correct** ✓ (should be left-associative)

---

## Practice Exercises

Try drawing parse trees for:

1. `let x = 10` - simple declaration
2. `print x + 5` - expression with operator
3. `print add(2, 3)` - function call
4. `if x > 0 { print x }` - conditional
5. `let y = a * b + c` - precedence test
6. `fib(5)` - function call with literal
7. `print max(a, b)` - function with parameters

---

## Summary

**Key Points:**
- Parse tree = visual representation of how input is parsed
- Shape reflects grammar structure
- Internal nodes = non-terminals, Leaves = terminals
- Operator precedence = reflected in tree depth
- Each path from root to leaf = one rule application

**For NumPat:**
- All expressions follow Expr → Term Expr' pattern
- Ensures correct precedence: * before +
- Ensures correct associativity: left-to-right
- Enables recursive function calls

Your teammates can copy these examples and draw similar trees for different programs!
