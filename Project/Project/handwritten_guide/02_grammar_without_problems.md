# NumPat Grammar - WITHOUT Left Recursion and WITHOUT Left Factoring

## This document shows the CORRECTED grammar - READY for Top-Down Parsing

---

## 1. How We Fixed The Problems

### Technique 1: Removing Left Recursion

**Algorithm:**
```
For left-recursive rule:
  A ::= A α | β
  
Transform to:
  A ::= β A'
  A' ::= α A' | ε
  
This replaces left recursion with right recursion (OK for top-down)
```

### Technique 2: Left Factoring

**Algorithm:**
```
For rules with common prefix:
  A ::= α β | α γ
  
Transform to:
  A ::= α A'
  A' ::= β | γ
  
This delays decision until after parsing common prefix
```

---

## 2. Corrected Grammar - Removal of Left Recursion

### Step 1: Function List (Was Left Recursive)

**BEFORE (Problem):**
```bnf
<function_list> ::= <function_def> <function_list>        [LEFT RECURSIVE!]
                  | ε
```

**AFTER (Fixed):**
```bnf
<function_list>     ::= <function_def> <function_list'>

<function_list'>    ::= <function_def> <function_list'>
                      | ε
```

**Why this works:**
- No rule starts with `<function_list>` on RHS
- Top-down parser can parse function definitions sequentially
- The prime (`'`) symbol indicates "rest of the list"

---

### Step 2: Parameter List (Was Left Recursive)

**BEFORE (Problem):**
```bnf
<param_list> ::= <identifier> <param_list>               [LEFT RECURSIVE!]
               | ε
```

**AFTER (Fixed):**
```bnf
<param_list>      ::= <identifier> <param_list'>

<param_list'>     ::= "," <identifier> <param_list'>
                    | ε
```

**Transformation Details:**
1. Recognize pattern: A ::= A α | β becomes A ::= β A'; A' ::= α A' | ε
2. Apply: param_list ::= identifier param_list becomes...
3. Result: params "," params can be right-recursive

**Why this works:**
- Parameters parsed left-to-right: `a, b, c`
- Each comma triggers parsing next parameter
- Finally reaches epsilon when no more commas

---

### Step 3: Statement List (Was Left Recursive)

**BEFORE (Problem):**
```bnf
<statement_list> ::= <statement> <statement_list>        [LEFT RECURSIVE!]
                   | ε
```

**AFTER (Fixed):**
```bnf
<statement_list>    ::= <statement> <statement_list'>

<statement_list'>   ::= <statement> <statement_list'>
                      | ε
```

**Why this works:**
- Parses first statement, then rest of statements
- Right recursion: safe for top-down parser
- Similar structure to function list

---

### Step 4: Argument List (Was Left Recursive)

**BEFORE (Problem):**
```bnf
<arg_list> ::= <expr> <arg_list>                        [LEFT RECURSIVE!]
             | ε
```

**AFTER (Fixed):**
```bnf
<arg_list>      ::= <expr> <arg_list'>

<arg_list'>     ::= "," <expr> <arg_list'>
                  | ε
```

**Same pattern as parameter list**

---

### Step 5: Expression (Was Left Recursive) - MOST IMPORTANT

**BEFORE (Problem):**
```bnf
<expr> ::= <expr> "+" <term>                           [LEFT RECURSIVE!]
         | <expr> "-" <term>                           [LEFT RECURSIVE!]
         | <term>
```

**AFTER (Fixed) - Using Precedence Climbing:**
```bnf
<expr>         ::= <term> <expr'>

<expr'>        ::= "+" <term> <expr'>
                 | "-" <term> <expr'>
                 | ε
```

**Example - Parse `a + b - c`:**
```
parse_expr()
  parse_term() → parse_primary() → a
  parse_expr'() 
    See "+"
    parse_term() → b
    parse_expr'()
      See "-"
      parse_term() → c
      parse_expr'()
        See ")" (not + or -)
        ε (epsilon)
        Return
      Return
    Return
  Return

Result: ((a + b) - c)  ← Correct left-to-right associativity!
```

---

### Step 6: Term (Was Left Recursive) - Multiplication/Division

**BEFORE (Problem):**
```bnf
<term> ::= <term> "*" <factor>                         [LEFT RECURSIVE!]
         | <term> "/" <factor>                         [LEFT RECURSIVE!]
         | <term> "%" <factor>                         [LEFT RECURSIVE!]
         | <factor>
```

**AFTER (Fixed):**
```bnf
<term>         ::= <factor> <term'>

<term'>        ::= "*" <factor> <term'>
                 | "/" <factor> <term'>
                 | "%" <factor> <term'>
                 | ε
```

**Same technique as expressions**

**Precedence hierarchy preserved:**
```
parse_expr()    → handles +, - (lower precedence)
  parse_term()  → handles *, /, % (higher precedence)
    parse_factor() → handles literals, identifiers, parentheses
```

---

## 3. Corrected Grammar - Left Factoring Fixes

### Step 1: If Statement (Had Common Prefix "if")

**BEFORE (Problem):**
```bnf
<if_stmt> ::= "if" <condition> "{" <statement_list> "}" "else" "{" <statement_list> "}"
            | "if" <condition> "{" <statement_list> "}"
```

**Common prefix:** `"if" <condition> "{" <statement_list> "}"`

**AFTER (Fixed):**
```bnf
<if_stmt>   ::= "if" <condition> "{" <statement_list> "}" <else_part>

<else_part> ::= "else" "{" <statement_list> "}"
              | ε
```

**Why this works:**
1. Parser parses `"if" <condition> "{" <statement_list> "}"`
2. Then checks if next token is "else"
3. If yes: parse else block
4. If no: epsilon (nothing)

**Example - Parse `if x > 5 { print x }`:**
```
parse_if_stmt()
  Consume "if"
  parse_condition() → x > 5
  Consume "{"
  parse_statement_list() → print x
  Consume "}"
  parse_else_part()
    Look at next token
    Not "else" → epsilon
    Return
  Return
```

---

### Step 2: Return Statement (Had Common Prefix "return")

**BEFORE (Problem):**
```bnf
<return_stmt> ::= "return" <expr>
                | "return"
```

**Common prefix:** `"return"`

**AFTER (Fixed):**
```bnf
<return_stmt> ::= "return" <return_value>

<return_value> ::= <expr>
                 | ε
```

**Why this works:**
1. Parser consumes "return"
2. Checks if next token can start an expression
3. If yes: parse expression
4. If no (e.g., "}", end of function): epsilon

**Example - Parse `return n * 2`:**
```
parse_return_stmt()
  Consume "return"
  parse_return_value()
    Can parse expression? YES (starts with identifier 'n')
    parse_expr() → n * 2
  Return
```

**Example - Parse `return` (alone):**
```
parse_return_stmt()
  Consume "return"
  parse_return_value()
    Can parse expression? NO (next is "}", "}", or EOF)
    ε (epsilon)
  Return
```

---

## 4. Complete Corrected Grammar (LL(1) Compatible)

```bnf
<program>           ::= <function_list> <statement_list>

<function_list>     ::= <function_def> <function_list'>

<function_list'>    ::= <function_def> <function_list'>
                      | ε

<function_def>      ::= <return_type> <identifier> "(" <param_list> ")" "{" <statement_list> "}"

<return_type>       ::= "int" | "void"

<param_list>        ::= <identifier> <param_list'>

<param_list'>       ::= "," <identifier> <param_list'>
                      | ε

<statement_list>    ::= <statement> <statement_list'>

<statement_list'>   ::= <statement> <statement_list'>
                      | ε

<statement>         ::= <declaration>
                      | <assignment>
                      | <print_stmt>
                      | <if_stmt>
                      | <while_stmt>
                      | <return_stmt>
                      | <function_call>

<declaration>       ::= "let" <identifier> "=" <expr>

<assignment>        ::= <identifier> "=" <expr>

<print_stmt>        ::= "print" <expr>

<if_stmt>           ::= "if" <condition> "{" <statement_list> "}" <else_part>

<else_part>         ::= "else" "{" <statement_list> "}"
                      | ε

<while_stmt>        ::= "while" <condition> "{" <statement_list> "}"

<return_stmt>       ::= "return" <return_value>

<return_value>      ::= <expr>
                      | ε

<function_call>     ::= <identifier> "(" <arg_list> ")"

<arg_list>          ::= <expr> <arg_list'>

<arg_list'>         ::= "," <expr> <arg_list'>
                      | ε

<expr>              ::= <term> <expr'>

<expr'>             ::= "+" <term> <expr'>
                      | "-" <term> <expr'>
                      | ε

<term>              ::= <factor> <term'>

<term'>             ::= "*" <factor> <term'>
                      | "/" <factor> <term'>
                      | "%" <factor> <term'>
                      | ε

<factor>            ::= <number>
                      | <identifier>
                      | <function_call>
                      | "(" <expr> ")"

<condition>         ::= <expr> <comp_op> <expr>

<comp_op>           ::= "<" | ">" | "==" | "!=" | "<=" | ">="

<number>            ::= [0-9]+

<identifier>        ::= [a-zA-Z_][a-zA-Z0-9_]*
```

---

## 5. Transformation Summary Table

| Rule | Problem | Transformation | Result |
|------|---------|------------------|--------|
| `<function_list>` | Left recursion | Replace `A ::= A α \| β` with `A ::= β A'; A' ::= α A' \| ε` | Right-recursive, parseable |
| `<param_list>` | Left recursion | Same transformation | Right-recursive, parseable |
| `<statement_list>` | Left recursion | Same transformation | Right-recursive, parseable |
| `<arg_list>` | Left recursion | Same transformation | Right-recursive, parseable |
| `<expr>` | Left recursion | Use precedence climbing | Right-recursive, maintains precedence |
| `<term>` | Left recursion | Use precedence climbing | Right-recursive, maintains precedence |
| `<if_stmt>` | Left factoring | Extract common prefix, make else optional | Unambiguous |
| `<return_stmt>` | Left factoring | Extract "return", make expression optional | Unambiguous |

---

## 6. Why This Grammar Works for Top-Down Parsing

### Test 1: No Left Recursion

```
✓ No rule has LHS appearing at start of RHS
✓ All recursion is RIGHT recursion (safe for top-down)
✓ Parser won't infinite loop
```

### Test 2: No Left Factoring Ambiguity

```
✓ Every position has unique lookahead to distinguish rules
✓ Parser can always make right choice with 1-token lookahead (LL(1))
✓ No backtracking needed
```

### Test 3: Preserves Operator Precedence

```
✓ Expression hierarchy: expr' (+ -) > term' (* / %) > factor (literals)
✓ Result: * and / always evaluated before + and -
✓ Correct mathematical semantics
```

### Test 4: Preserves Operator Associativity

```
✓ Right recursion in prime rules maintains left-to-right associativity
✓ Example: a + b - c parses as (a + b) - c (not a + (b - c))
✓ Correct mathematical semantics
```

---

## 7. Proof: LL(1) Grammar

An LL(1) grammar requires:

1. **No left recursion** ✓ (we removed it all)
2. **No left factoring conflicts** ✓ (we resolved them all)
3. **Unique lookahead** ✓ (one token determines which rule)

Our corrected grammar satisfies all three!

---

## Next Steps

See file `03_top_down_vs_bottom_up.md` for discussion of parser approaches!
