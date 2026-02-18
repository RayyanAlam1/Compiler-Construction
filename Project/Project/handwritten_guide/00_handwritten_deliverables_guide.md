# NumPat Compiler Project - Handwritten Deliverables Summary

## All Markdown Files for Your Team to Copy

Your teammates can copy from these markdown files directly for handwritten work!

---

## 📋 Complete File List

### 1. **01_language_specification.md** ✅
**Content:** Complete NumPat language definition
- Keywords, tokens, operators
- Formal grammar in BNF
- Lexical, syntactic, semantic specifications
- Symbol table structure
- Code examples
- Error handling

**Your teammates should use for:** Understanding language design, referencing grammar rules

---

### 2. **02_grammar_with_problems.md** ✅
**Content:** Original grammar WITH issues
- Shows left recursion problems
- Shows left factoring issues
- Explains why top-down parsing fails
- Lists problematic rules
- Examples of infinite recursion

**Your teammates should use for:** Showing the "before" state of grammar

---

### 3. **02_grammar_without_problems.md** ✅
**Content:** Corrected grammar WITHOUT issues
- Step-by-step transformations for each rule
- Left recursion removal algorithm
- Left factoring resolution algorithm
- Complete corrected grammar (LL(1) compatible)
- Transformation summary table
- Proof that grammar is now LL(1)

**Your teammates should use for:** Showing the "after" state of grammar and transformations

---

### 4. **03_top_down_vs_bottom_up.md** ✅
**Content:** Comprehensive parser comparison
- Parser taxonomy (LL, LR, etc.)
- Top-down algorithm explanation
- Bottom-up algorithm explanation
- Detailed comparison table
- Decision matrix
- Justification for choosing top-down
- What would be needed for bottom-up
- When to use each approach

**Your teammates should use for:** Explaining parser choice in viva

---

### 4. **04_parse_trees_guide.md** ✅
**Content:** How to draw parse trees with examples
- Step-by-step guide for drawing trees
- 7 complete examples:
  1. Simple variable declaration
  2. Simple function call
  3. Binary operation (precedence)
  4. Conditional statement
  5. Recursive function call
  6. Assignment
  7. Nested function calls
- How to verify trees are correct
- Practice exercises

**Your teammates should use for:** Creating handwritten parse tree examples

---

## 🎯 How to Use These Files

### For Person 2 (Grammar & Parser Analysis)

**Use these files:**
- `02_grammar_with_problems.md` - Original grammar
- `02_grammar_without_problems.md` - Transformed grammar with steps
- `03_top_down_vs_bottom_up.md` - Parser justification

**Create handwritten documentation:**
1. Write original grammar (or copy from markdown)
2. Show removal of left recursion (use step-by-step guide from markdown)
3. Show left factoring removal (use step-by-step guide)
4. Create comparison table for TOP-DOWN vs BOTTOM-UP
5. Write justification for why NumPat uses TOP-DOWN

**Handwritten output:**
- 4-6 pages of grammar transformations
- 2-3 pages of parser comparison
- 1-2 pages of justification

---

### For Person 3 (Artifacts & Examples)

**Use these files:**
- `01_language_specification.md` - For understanding structure
- `04_parse_trees_guide.md` - How to draw trees with examples

**Create handwritten artifacts:**
1. **DFA Diagram** (Finite Automaton for Lexer)
   - Draw states for token recognition
   - Show transitions between states
   - Label edges with input characters
   - Reference: Section 1.4 in language spec

2. **Parse Trees** (5-6 examples)
   - Use the 7 examples in parse trees guide
   - Draw clearly on paper
   - Label all nodes with rule names
   - Reference: `04_parse_trees_guide.md`

3. **Symbol Table** (with scoping)
   - Global scope (functions + variables)
   - Local scopes (per function)
   - Show parameter and local variable bindings
   - Reference: Section 3 in language spec

4. **One Complete Example**
   - Choose one test case (e.g., test_case_04: Fibonacci)
   - Show lexical tokens
   - Show parse tree
   - Show symbol table
   - Show execution trace

**Handwritten output:**
- 2-3 pages of DFA diagrams
- 4-6 pages of parse trees
- 1-2 pages of symbol table
- 2-3 pages of complete example

---

## 📝 Content Summary by Document

### Language Specification (01)

| Section | Content | For Handwritten |
|---------|---------|---|
| 1. Lexical | Keywords, tokens, operators | DFA diagram |
| 2. Syntax | Grammar in BNF | Grammar section |
| 3. Semantic | Type system, scoping, functions | Symbol table |
| 4. Examples | Code snippets | Reference |
| 5-11. Reference | Details on all aspects | Support material |

---

### Grammar Documents (02 BEFORE, 02 AFTER)

| Section | Before Document | After Document |
|---------|---|---|
| Left Recursion | Shows 6+ left recursive rules | Transformation steps |
| Left Factoring | Shows 2 factoring issues | Resolution steps |
| Problems | Why it fails | Why it works |
| Proof | Infinite recursion examples | LL(1) proof |

---

### Parser Comparison (03)

| Section | Content | For Handwritten |
|---------|---------|---|
| 1. Taxonomy | Types of parsers | Knowledge base |
| 2. Top-down | Algorithm + example | Explanation |
| 3. Bottom-up | Algorithm + example | Comparison |
| 4. Comparison | Detailed table | Copy to handwritten |
| 5-8. Analysis | Decision matrix + proof | Justification |
| 9-10. Reference | Quick reference + summary | Support |

---

### Parse Tree Guide (04)

| Section | Content | Example |
|---------|---------|---|
| How to Draw | Step-by-step algorithm | `let x = 5` |
| Example 1 | Simple declaration | `let result = 42` |
| Example 2 | Function call | `print add(3, 4)` |
| Example 3 | Operator precedence | `let x = a + b * c` |
| Example 4 | Conditional | `if n < 2 { return n }` |
| Example 5 | Recursion | `fib(n-1) + fib(n-2)` |
| Example 6 | Assignment | `result = result * i` |
| Example 7 | Nested calls | `print double(add(3,4))` |

---

## ✍️ Handwritten Artifact Checklist

Person 2 Should Create:

- [ ] Original grammar with left recursion marked
- [ ] Step-by-step left recursion removal (each rule)
- [ ] Step-by-step left factoring resolution
- [ ] Final corrected grammar (LL(1))
- [ ] TOP-DOWN vs BOTTOM-UP comparison table
- [ ] Justification: Why top-down for NumPat
- [ ] Algorithm: How top-down parser works (general)
- [ ] Proof: Why our grammar is LL(1)

Person 3 Should Create:

- [ ] DFA diagram (lexical analysis state machine)
- [ ] Parse tree for simple declaration (`let x = 42`)
- [ ] Parse tree for function call (`print add(3, 4)`)
- [ ] Parse tree with precedence (`a + b * c`)
- [ ] Parse tree with recursion (`fib(n-1)`)
- [ ] Symbol table with global scope
- [ ] Symbol table with function scope (local variables/parameters)
- [ ] One complete example walkthrough (tokens → parse tree → symbol table)

---

## 🎓 How to Present These

### In Viva (Oral Examination)

**Show Person 2's Work:**
- "Here's the original grammar with left recursion..."
- "We removed it using this transformation algorithm..."
- "Our final grammar is LL(1), suitable for top-down parsing..."
- "Top-down was chosen because..." (comparison table)

**Show Person 3's Work:**
- "This is the DFA for lexical analysis..."
- "For test case X, the parse tree looks like..."
- "The symbol table shows function signatures here..."
- "During execution, scopes are created and destroyed..."

---

## 💡 Tips for Your Team

### Grammar Work (Person 2)

1. **Don't just copy** - show the transformation steps
2. **Use color** - highlight what changes during transformation
3. **Number your steps** - makes it clear and traceable
4. **Show examples** - apply transformations to specific rules
5. **Explain why** - each transformation has a reason

### Artifact Work (Person 3)

1. **Use clear notation** - consistent symbols and labels
2. **Test your trees** - read left-to-right should give input
3. **Show multiple examples** - demonstrate understanding
4. **Use hierarchy** - DFA → tokens → parse tree → symbol table
5. **Add annotations** - explain what each part shows

---

## 📚 Cross-References

### If explaining "left recursion removal":
→ See `02_grammar_without_problems.md`, Section 2

### If explaining "top-down parsing":
→ See `03_top_down_vs_bottom_up.md`, Section 2 + Section 6

### If drawing parse trees:
→ See `04_parse_trees_guide.md`, all examples

### If explaining operator precedence:
→ See `04_parse_trees_guide.md`, Example 3

### If explaining function scoping:
→ See `01_language_specification.md`, Section 3.6 + `04_parse_trees_guide.md`

---

## 🔗 Files to Download/Copy

All these markdown files are ready to download. Your teammates should:

1. Download all 4 markdown files
2. Read through relevant sections
3. Use the examples and explanations
4. Create their own handwritten versions
5. Add their own explanations and insights

---

## Final Output Expected

### From These Markdown Files

Your team should produce approximately:

- **Person 1 (Implementation)**: ✅ Already done
  - Working compiler: `numpar_compiler_with_stm.py`
  - 10 test cases
  - All tests pass

- **Person 2 (Grammar & Parser)**:
  - Grammar handwritten document: 6-8 pages
  - Parser analysis document: 3-4 pages
  - Total: ~12 pages

- **Person 3 (Artifacts & Examples)**:
  - DFA diagrams: 2-3 pages
  - Parse trees: 4-6 pages
  - Symbol tables: 2-3 pages
  - Example walkthrough: 2-3 pages
  - Total: ~12 pages

**Overall:** ~24 pages of handwritten work + compiler code

---

## Quality Checklist

Before submitting, verify:

- [ ] All grammar transformations are correct and traceable
- [ ] All parse trees parse the original input correctly
- [ ] All symbol tables are accurate
- [ ] All explanations are clear and educational
- [ ] Parser choice is well-justified
- [ ] Code compiles and all 10 tests pass
- [ ] No plagiarism - all work is original
- [ ] Presentation is neat and professional

---

## Support Resources

### If stuck on grammar transformation:
→ Read the detailed step-by-step in `02_grammar_without_problems.md`

### If stuck on parse tree:
→ Follow the algorithm in `04_parse_trees_guide.md` with examples

### If stuck on parser comparison:
→ Use the decision matrix in `03_top_down_vs_bottom_up.md`

### If stuck on implementation:
→ Run `numpar_compiler_with_stm.py` to see STM visualization

---

## Good Luck! 🎉

All the tools you need are in these markdown files. Your teammates can easily copy, reference, and build upon the explanations and examples provided.

The key is to **understand deeply** - not just copy, but explain why each transformation is needed and how it helps the parser work correctly.

**When you present to the jury:**
- Show the original vs corrected grammar
- Explain the transformation steps
- Justify why top-down parsing was chosen
- Demonstrate parse trees and symbol tables
- Run the compiler on test cases
- Explain how it all fits together