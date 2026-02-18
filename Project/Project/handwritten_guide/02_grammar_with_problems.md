# NumPat Grammar - WITH Left Recursion and Left Factoring Issues

## This document shows the ORIGINAL grammar WITH problems

---

## 1. Original Grammar WITH Left Recursion

This is what we started with - **PROBLEMATIC** for top-down parsing:

### Full Grammar

```bnf
<program>         ::= <function_list> <statement_list>

<function_list>   ::= <function_def> <function_list>        [LEFT RECURSIVE!]
                    | ε

<function_def>    ::= <return_type> <identifier> "(" <param_list> ")" "{" <statement_list> "}"

<return_type>     ::= "int" | "void"

<param_list>      ::= <identifier> <param_list>             [LEFT RECURSIVE!]
                    | ε

<statement_list>  ::= <statement> <statement_list>          [LEFT RECURSIVE!]
                    | ε

<statement>       ::= <declaration>
                    | <reassignment>
                    | <print_stmt>
                    | <if_stmt>
                    | <while_stmt>
                    | <return_stmt>
                    | <function_call>

<declaration>     ::= "let" <identifier> "=" <expr>

<reassignment>    ::= <identifier> "=" <expr>

<print_stmt>      ::= "print" <expr>

<if_stmt>         ::= "if" <condition> "{" <statement_list> "}" <else_part>    [LEFT FACTOR!]
                    | "if" <condition> "{" <statement_list> "}"

<else_part>       ::= "else" "{" <statement_list> "}"

<while_stmt>      ::= "while" <condition> "{" <statement_list> "}"

<return_stmt>     ::= "return" <expr>                         [LEFT FACTOR!]
                    | "return"

<function_call>   ::= <identifier> "(" <arg_list> ")"

<arg_list>        ::= <expr> <arg_list>                      [LEFT RECURSIVE!]
                    | ε

<expr>            ::= <expr> "+" <term>                      [LEFT RECURSIVE!]
                    | <expr> "-" <term>                      [LEFT RECURSIVE!]
                    | <term>

<term>            ::= <term> "*" <factor>                    [LEFT RECURSIVE!]
                    | <term> "/" <factor>                    [LEFT RECURSIVE!]
                    | <term> "%" <factor>                    [LEFT RECURSIVE!]
                    | <factor>

<factor>          ::= <number>
                    | <identifier>
                    | <function_call>
                    | "(" <expr> ")"

<condition>       ::= <expr> <comp_op> <expr>

<comp_op>         ::= "<" | ">" | "==" | "!=" | "<=" | ">="

<number>          ::= [0-9]+

<identifier>      ::= [a-zA-Z_][a-zA-Z0-9_]*
```

---

## 2. LEFT RECURSION Issues Identified

### 2.1 Direct Left Recursion

An immediate left-recursive rule has the non-terminal appearing as the first symbol on the right side:

#### Problem 1: `<function_list>`

```bnf
<function_list>   ::= <function_def> <function_list>
                    | ε
```

**Issue:** Top-down parser would try:
```
parse_function_list() calls parse_function_list()
  → parse_function_list() calls parse_function_list()
    → ... infinite recursion!
```

#### Problem 2: `<param_list>`

```bnf
<param_list>      ::= <identifier> <param_list>
                    | ε
```

**Same issue** - Left recursive

#### Problem 3: `<statement_list>`

```bnf
<statement_list>  ::= <statement> <statement_list>
                    | ε
```

**Same issue** - Left recursive

#### Problem 4-6: Expression Recursion

```bnf
<expr>            ::= <expr> "+" <term>
                    | <expr> "-" <term>
                    | <term>

<term>            ::= <term> "*" <factor>
                    | <term> "/" <factor>
                    | <term> "%" <factor>
                    | <factor>

<arg_list>        ::= <expr> <arg_list>
                    | ε
```

**All are left recursive**

---

## 3. LEFT FACTORING Issues Identified

### 3.1 Common Prefix Problem

A left factoring issue occurs when multiple alternatives start with the same prefix:

#### Problem 1: `<if_stmt>`

```bnf
<if_stmt>   ::= "if" <condition> "{" <statement_list> "}" "else" "{" <statement_list> "}"
              | "if" <condition> "{" <statement_list> "}"
```

**Common prefix:** `"if" <condition> "{" <statement_list> "}"`

**Top-down parser issue:**
```
Sees: "if"
Starts parsing if_stmt
After parsing condition and statements, sees either "else" or something else
But already committed to parsing without knowing which branch!
```

#### Problem 2: `<return_stmt>`

```bnf
<return_stmt>   ::= "return" <expr>
                  | "return"
```

**Common prefix:** `"return"`

**Top-down parser issue:**
```
Sees: "return"
Starts parsing return_stmt
Next token is either an expression or something else (like "}")
Parser doesn't know which rule to use until lookahead!
```

---

## 4. Why This Grammar Doesn't Work for Top-Down Parsing

### Top-Down Parsing Algorithm

```
1. Start with start symbol
2. Examine input token
3. Choose which production rule to expand based on current token
4. Recursively parse chosen rule
```

### Problem with Left Recursion

```
Parsing <expr>:
  Rule: <expr> ::= <expr> "+" <term>
  
  parse_expr():
    Try to parse <expr> first
    But that calls parse_expr() again!
    → Infinite recursion, never consumes input
```

### Problem with Left Factoring

```
Parsing <if_stmt>:
  See "if" token
  Two rules both start with "if"
  Which to choose?
  
  If we choose first: then we MUST see "else"
  If we choose second: we MUST NOT see "else"
  
  But we don't know until we parse the block!
```

---

## 5. Summary of Problems

| Rule | Problem Type | Why Problematic |
|------|--------------|-----------------|
| `<function_list>` | Left Recursion | Infinite recursion in parser |
| `<param_list>` | Left Recursion | Infinite recursion in parser |
| `<statement_list>` | Left Recursion | Infinite recursion in parser |
| `<expr>` | Left Recursion | Infinite recursion in parser |
| `<term>` | Left Recursion | Infinite recursion in parser |
| `<arg_list>` | Left Recursion | Infinite recursion in parser |
| `<if_stmt>` | Left Factoring | Parser can't decide which rule |
| `<return_stmt>` | Left Factoring | Parser can't decide which rule |

---

## 6. What Happens When We Try to Parse

### Example: Parsing `if n < 2 { return n }`

```
parse_if_stmt() called

Look at: <if_stmt> ::= "if" <condition> "{" <statement_list> "}" ("else" ...)?
                     | "if" <condition> "{" <statement_list> "}"

Both rules start with "if" and the same prefix!

After parsing "{" <statement_list> "}", we see:
  - Either "else" (need to use first rule)
  - Or something else (need to use second rule)

We've already committed! Can't backtrack in top-down without LL(2) or more lookahead.
```

### Example: Parsing `fib(n)`

```
parse_function_list()

Rule: <function_list> ::= <function_def> <function_list>

Call parse_function_def()
  Successfully parses: int fib(n) { ... }

Call parse_function_list() again  [LEFT RECURSION!]
  Rule: <function_list> ::= <function_def> <function_list>
  
  Call parse_function_def() again
    Now at: let result = fib(10)  [This is a statement, not a function!]
    ERROR!

OR: Infinite loop trying to call parse_function_list() 
    repeatedly without consuming input
```

---

## Next Steps

See file `02_grammar_without_left_recursion.md` for how these problems are FIXED!

This file shows the **problem grammar**. The next file shows the **corrected grammar** with all transformations.
