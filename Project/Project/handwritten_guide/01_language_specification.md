# NumPat Language Specification

## Overview

**NumPat** is a simple imperative programming language designed for educational purposes to demonstrate compiler construction concepts. It supports function definitions with parameters, recursion, local scoping, and basic control flow structures.

### Language Name
**NumPat** - Numerical Pattern (for number pattern generation)

### Target
Educational compiler course project

---

## 1. Lexical Specification

### 1.1 Keywords

Reserved words (cannot be used as identifiers):

```
let      - Variable declaration
print    - Output statement
if       - Conditional statement
else     - Alternative branch
while    - Loop statement
int      - Integer return type
void     - No return type
return   - Return from function
```

### 1.2 Tokens

| Token Type | Pattern | Examples |
|-----------|---------|----------|
| NUMBER | Sequence of digits | `0`, `42`, `3628800` |
| IDENTIFIER | Letter/underscore followed by alphanumerics | `n`, `result`, `factorial`, `_temp` |
| PLUS | `+` | Addition operator |
| MINUS | `-` | Subtraction operator |
| MUL | `*` | Multiplication operator |
| DIV | `/` | Integer division operator |
| MOD | `%` | Modulo operator |
| ASSIGN | `=` | Assignment operator |
| LT | `<` | Less than |
| GT | `>` | Greater than |
| EQ | `==` | Equal to |
| NEQ | `!=` | Not equal to |
| LTE | `<=` | Less than or equal |
| GTE | `>=` | Greater than or equal |
| LPAREN | `(` | Left parenthesis |
| RPAREN | `)` | Right parenthesis |
| LBRACE | `{` | Left brace |
| RBRACE | `}` | Right brace |
| COMMA | `,` | Parameter/argument separator |
| EOF | End of file | Special marker |

### 1.3 Comments

Lines starting with `#` are comments and are ignored:

```
# This is a comment
let x = 5  # This is also a comment
```

### 1.4 Ignored Tokens

- Whitespace (spaces, tabs, newlines)
- Comments (lines starting with `#`)

---

## 2. Syntax Specification (Formal Grammar - BNF)

### 2.1 Program Structure

```bnf
<program>        ::= <function_list> <statement_list>

<function_list>  ::= ε 
                   | <function_def> <function_list>

<statement_list> ::= ε 
                   | <statement> <statement_list>
```

### 2.2 Function Definition

```bnf
<function_def>   ::= <return_type> <identifier> "(" <param_list> ")" "{" <statement_list> "}"

<return_type>    ::= "int" | "void"

<param_list>     ::= ε 
                   | <param_list_non_empty>

<param_list_non_empty> ::= <identifier> 
                         | <identifier> "," <param_list_non_empty>
```

### 2.3 Statements

```bnf
<statement>      ::= <declaration>
                   | <reassignment>
                   | <print_stmt>
                   | <if_stmt>
                   | <while_stmt>
                   | <return_stmt>
                   | <function_call>

<declaration>    ::= "let" <identifier> "=" <expr>

<reassignment>   ::= <identifier> "=" <expr>

<print_stmt>     ::= "print" <expr>

<return_stmt>    ::= "return" <expr>
                   | "return"

<function_call>  ::= <identifier> "(" <arg_list> ")"

<arg_list>       ::= ε 
                   | <arg_list_non_empty>

<arg_list_non_empty> ::= <expr> 
                       | <expr> "," <arg_list_non_empty>
```

### 2.4 Control Flow

```bnf
<if_stmt>        ::= "if" <condition> "{" <statement_list> "}"
                   | "if" <condition> "{" <statement_list> "}" "else" "{" <statement_list> "}"

<while_stmt>     ::= "while" <condition> "{" <statement_list> "}"

<condition>      ::= <expr> <comp_op> <expr>

<comp_op>        ::= "<" | ">" | "==" | "!=" | "<=" | ">="
```

### 2.5 Expressions

```bnf
<expr>           ::= <additive>

<additive>       ::= <multiplicative> 
                   | <additive> "+" <multiplicative>
                   | <additive> "-" <multiplicative>

<multiplicative> ::= <primary> 
                   | <multiplicative> "*" <primary>
                   | <multiplicative> "/" <primary>
                   | <multiplicative> "%" <primary>

<primary>        ::= <number>
                   | <identifier>
                   | <function_call>
                   | "(" <expr> ")"

<number>         ::= [0-9]+

<identifier>     ::= [a-zA-Z_][a-zA-Z0-9_]*
```

---

## 3. Semantic Specification

### 3.1 Type System

**Data Types:**
- `int` - 32-bit signed integer
- `void` - No value (only for function return type)

**No implicit type conversions**

### 3.2 Variable Declaration

- Must use `let` keyword for first declaration
- Can reassign without `let` after declaration
- All variables initialized to 0 by default
- Scope: Global or local to function

### 3.3 Function Definition

**Syntax:**
```
return_type function_name(param1, param2, ...) {
    statements
}
```

**Rules:**
- Functions can have 0 to N integer parameters
- Return type must be `int` or `void`
- Function body contains statements
- Parameters are local variables within function
- If return type is `int`, function must return value (with `return expr`)
- If return type is `void`, function cannot return value (use `return` or no return)

### 3.4 Function Calls

- Must be declared before use
- Arguments must match parameter count exactly
- All arguments are integers
- Returns integer (for `int` functions) or nothing (for `void` functions)
- Supports recursion

### 3.5 Operator Precedence (High to Low)

1. `( )` - Parentheses (highest)
2. `*`, `/`, `%` - Multiplication, division, modulo
3. `+`, `-` - Addition, subtraction
4. `<`, `>`, `==`, `!=`, `<=`, `>=` - Comparisons (lowest)

### 3.6 Scope Rules

**Global Scope:**
- All function definitions
- Variables declared outside functions
- Accessible everywhere

**Local Scope (per function):**
- Function parameters (act as local variables)
- Variables declared with `let` inside function
- Not accessible outside function
- Shadows global variables with same name

### 3.7 Semantic Constraints

1. **First Use Rule**: Every variable must be declared before use
2. **Function Declaration Rule**: Functions must be defined before called
3. **Return Type Consistency**: 
   - `int` functions must return integer values
   - `void` functions cannot return values
4. **Parameter Count**: Function calls must have exact number of arguments
5. **No Undefined Identifiers**: All identifiers must be declared

---

## 4. Syntactic Analysis

### 4.1 Parser Type

**Top-Down Recursive Descent Parser**

Each grammar rule implements as recursive function:

```
<expr> ::= <additive>
    ↓
def parse_expression():
    return parse_additive()

<additive> ::= <multiplicative> ("+" | "-" <multiplicative>)*
    ↓
def parse_additive():
    left = parse_multiplicative()
    while current_token in [PLUS, MINUS]:
        op = consume_operator()
        right = parse_multiplicative()
        left = BinOp(left, op, right)
    return left
```

### 4.2 Precedence Implementation

Precedence encoded in function hierarchy:

```
parse_expression()      (lowest precedence, top level)
    ↓
parse_additive()        (+ and -)
    ↓
parse_multiplicative()  (* / %)
    ↓
parse_primary()         (literals, identifiers, parentheses) (highest precedence)
```

---

## 5. Symbol Table

### 5.1 Global Symbol Table

```
Entry Type    | Name           | Type/Signature       | Scope
--------------|----------------|----------------------|---------
Function      | fib            | int(int) → int       | global
Function      | add            | int(int, int) → int  | global
Variable      | result         | int                  | global
Variable      | count          | int                  | global
```

### 5.2 Local Symbol Tables (Per Function)

```
Function: fib
Entry Type    | Name           | Type                 | Kind
--------------|----------------|----------------------|---------
Parameter     | n              | int                  | parameter
Variable      | temp           | int                  | local

Function: add
Entry Type    | Name           | Type                 | Kind
--------------|----------------|----------------------|---------
Parameter     | a              | int                  | parameter
Parameter     | b              | int                  | parameter
```

---

## 6. Code Examples

### 6.1 Simple Function (No Parameters)

```
int getNumber() {
    return 42
}

let x = getNumber()
print x
```

**Output:** `42`

### 6.2 Function with Parameters

```
int add(a, b) {
    return a + b
}

print add(3, 4)
```

**Output:** `7`

### 6.3 Recursive Function

```
int fib(n) {
    if n < 2 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

print fib(10)
```

**Output:** `55`

### 6.4 Function with Loop

```
int factorial(n) {
    let result = 1
    let i = 1
    
    while i <= n {
        result = result * i
        i = i + 1
    }
    
    return result
}

print factorial(5)
```

**Output:** `120`

### 6.5 Void Function

```
void printMultiples(n, count) {
    let i = 1
    
    while i <= count {
        print n * i
        i = i + 1
    }
}

printMultiples(5, 3)
```

**Output:**
```
5
10
15
```

---

## 7. Lexical Analysis

### 7.1 Token Recognition

| Input | Token Type | Value |
|-------|-----------|-------|
| `42` | NUMBER | 42 |
| `result` | IDENTIFIER | "result" |
| `int` | INT | "int" |
| `+` | PLUS | "+" |
| `==` | EQ | "==" |

### 7.2 State Machine (Finite Automaton)

```
START
  ├─ [digit] → NUMBER
  ├─ [letter/_] → IDENTIFIER/KEYWORD
  ├─ '+' → PLUS
  ├─ '-' → MINUS
  ├─ '*' → MUL
  ├─ '/' → DIV
  ├─ '%' → MOD
  ├─ '(' → LPAREN
  ├─ ')' → RPAREN
  ├─ '{' → LBRACE
  ├─ '}' → RBRACE
  ├─ ',' → COMMA
  ├─ '=' → ASSIGN or EQ (if followed by '=')
  ├─ '<' → LT or LTE (if followed by '=')
  ├─ '>' → GT or GTE (if followed by '=')
  ├─ '!' → NEQ (must be followed by '=')
  └─ [space/newline] → (skip)
```

---

## 8. Language Characteristics

### 8.1 What Is Supported ✅

- Function definitions with multiple parameters
- Function calls (including recursive)
- Integer variables with global and local scope
- Arithmetic expressions with correct precedence
- Comparison operators
- Control flow (if/else, while)
- Return statements
- Comments

### 8.2 What Is NOT Supported ❌

- String type or string literals
- Arrays or lists
- Floating-point numbers
- Boolean type (comparisons return 0 or 1)
- Nested functions
- Function pointers
- Multiple assignment (`x = y = 5`)
- For loops (use while instead)
- Do-while loops
- Switch statements
- Enums or structures
- Include/import statements

---

## 9. Error Handling

### 9.1 Lexical Errors

```
[LEXER ERROR] Line 2, Col 5: Unexpected character '@'
```

### 9.2 Syntax Errors

```
[PARSER ERROR] Line 3, Col 10: Expected ')', got EOF
```

### 9.3 Semantic Errors

```
[SEMANTIC ERROR] Variable 'x' not declared before use
[SEMANTIC ERROR] Function 'foo' expects 2 arguments, got 1
[SEMANTIC ERROR] Void function cannot return a value
```

### 9.4 Runtime Errors

```
[RUNTIME ERROR] Division by zero
[RUNTIME ERROR] Function 'undefined' not found
```

---

## 10. Complete Grammar Summary

**Simplified BNF (without left recursion):**

```bnf
Program          → FunctionList StatementList

FunctionList     → ε | FunctionDef FunctionList

FunctionDef      → ReturnType IDENTIFIER "(" ParamList ")" "{" StatementList "}"

ReturnType       → "int" | "void"

ParamList        → ε | Identifier ParamListRest

ParamListRest    → ε | "," Identifier ParamListRest

StatementList    → ε | Statement StatementList

Statement        → Declaration | Assignment | PrintStmt | IfStmt | WhileStmt | ReturnStmt | FunctionCall

Declaration      → "let" IDENTIFIER "=" Expression

Assignment       → IDENTIFIER "=" Expression

PrintStmt        → "print" Expression

IfStmt           → "if" Condition "{" StatementList "}" (ElseBlock)?

ElseBlock        → "else" "{" StatementList "}"

WhileStmt        → "while" Condition "{" StatementList "}"

ReturnStmt       → "return" (Expression)?

FunctionCall     → IDENTIFIER "(" ArgList ")"

Condition        → Expression CompOp Expression

CompOp           → "<" | ">" | "==" | "!=" | "<=" | ">="

Expression       → AddExpr

AddExpr          → MulExpr (AddOp MulExpr)*

AddOp            → "+" | "-"

MulExpr          → PrimaryExpr (MulOp PrimaryExpr)*

MulOp            → "*" | "/" | "%"

PrimaryExpr      → NUMBER | IDENTIFIER | FunctionCall | "(" Expression ")"

ArgList          → ε | Expression ArgListRest

ArgListRest      → ε | "," Expression ArgListRest
```

---

## 11. Language Design Decisions

### Why Integer-Only?

Simplicity for educational purposes. Demonstrates core compiler concepts without complexity of multiple types.

### Why No Arrays?

Would require additional semantic analysis and memory management concepts beyond scope.

### Why Recursive Descent Parser?

- Grammar is naturally LL(1) compatible
- Easy to implement by hand
- Each rule maps clearly to parser function
- Good for teaching compiler fundamentals

### Why Direct AST Interpretation?

- Simpler than generating intermediate code
- Easier to understand and debug
- Sufficient for educational language

---

## 12. Reference Implementation

The reference NumPat compiler implements:

1. **Lexical Analysis** - Tokenizes source into tokens
2. **Syntax Analysis** - Recursive descent parser builds AST
3. **Semantic Analysis** - Validates types, scopes, function signatures
4. **Interpretation** - Direct AST tree walking execution

All phases in ~900 lines of Python code.

