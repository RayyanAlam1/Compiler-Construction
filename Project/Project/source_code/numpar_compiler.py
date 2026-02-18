# NumPat Compiler with Enhanced Visualizations
# Includes: Lexical tokens, Parse tree summary, Symbol Table Manager, and execution flow
# TOP-DOWN Recursive Descent Parser with Function Support

import re
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union

# ============================================================================
# PHASE 1: LEXICAL ANALYSIS
# ============================================================================

class TokenType(Enum):
    # Keywords
    LET = "LET"
    PRINT = "PRINT"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FUNC = "FUNC"
    RETURN = "RETURN"
    INT = "INT"
    VOID = "VOID"
    
    # Literals
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    ASSIGN = "ASSIGN"
    
    # Comparisons
    LT = "LT"
    GT = "GT"
    EQ = "EQ"
    NEQ = "NEQ"
    LTE = "LTE"
    GTE = "GTE"
    
    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    
    # Special
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class Lexer:
    KEYWORDS = {
        'let': TokenType.LET,
        'print': TokenType.PRINT,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'func': TokenType.FUNC,
        'return': TokenType.RETURN,
        'int': TokenType.INT,
        'void': TokenType.VOID,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
        print(f"[LEXER ERROR] Line {self.line}, Col {self.column}: {msg}")
        sys.exit(1)
    
    def peek(self, offset=0) -> str:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return '\0'
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace_and_comments(self):
        while self.peek() in ' \t\n':
            self.advance()
        
        if self.peek() == '#':
            while self.peek() != '\n' and self.peek() != '\0':
                self.advance()
            self.skip_whitespace_and_comments()
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.column
        num_str = ''
        while self.peek().isdigit():
            num_str += self.peek()
            self.advance()
        return Token(TokenType.NUMBER, int(num_str), start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.column
        ident = ''
        while self.peek().isalnum() or self.peek() == '_':
            ident += self.peek()
            self.advance()
        
        if ident in self.KEYWORDS:
            token_type = self.KEYWORDS[ident]
            return Token(token_type, ident, start_line, start_col)
        else:
            return Token(TokenType.IDENTIFIER, ident, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace_and_comments()
            
            if self.pos >= len(self.source):
                break
            
            ch = self.peek()
            line, col = self.line, self.column
            
            if ch.isdigit():
                self.tokens.append(self.read_number())
            elif ch.isalpha() or ch == '_':
                self.tokens.append(self.read_identifier())
            elif ch == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', line, col))
                self.advance()
            elif ch == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', line, col))
                self.advance()
            elif ch == '*':
                self.tokens.append(Token(TokenType.MUL, '*', line, col))
                self.advance()
            elif ch == '/':
                self.tokens.append(Token(TokenType.DIV, '/', line, col))
                self.advance()
            elif ch == '%':
                self.tokens.append(Token(TokenType.MOD, '%', line, col))
                self.advance()
            elif ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', line, col))
                self.advance()
            elif ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', line, col))
                self.advance()
            elif ch == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', line, col))
                self.advance()
            elif ch == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', line, col))
                self.advance()
            elif ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', line, col))
                self.advance()
            elif ch == '=':
                self.advance()
                if self.peek() == '=':
                    self.tokens.append(Token(TokenType.EQ, '==', line, col))
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', line, col))
            elif ch == '!':
                self.advance()
                if self.peek() == '=':
                    self.tokens.append(Token(TokenType.NEQ, '!=', line, col))
                    self.advance()
                else:
                    self.error(f"Unexpected character '!'")
            elif ch == '<':
                self.advance()
                if self.peek() == '=':
                    self.tokens.append(Token(TokenType.LTE, '<=', line, col))
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.LT, '<', line, col))
            elif ch == '>':
                self.advance()
                if self.peek() == '=':
                    self.tokens.append(Token(TokenType.GTE, '>=', line, col))
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.GT, '>', line, col))
            else:
                self.error(f"Unexpected character '{ch}'")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


# ============================================================================
# PHASE 2: SYNTAX ANALYSIS (Parsing)
# ============================================================================

@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    functions: List['FunctionDef']
    statements: List['ASTNode']

@dataclass
class FunctionDef(ASTNode):
    return_type: str
    name: str
    params: List[str]
    body: List['ASTNode']

@dataclass
class Declaration(ASTNode):
    identifier: str
    value: 'ASTNode'

@dataclass
class Assignment(ASTNode):
    identifier: str
    value: 'ASTNode'

@dataclass
class PrintStmt(ASTNode):
    value: 'ASTNode'

@dataclass
class IfStmt(ASTNode):
    condition: 'ASTNode'
    then_block: List['ASTNode']
    else_block: Optional[List['ASTNode']]

@dataclass
class WhileStmt(ASTNode):
    condition: 'ASTNode'
    body: List['ASTNode']

@dataclass
class ReturnStmt(ASTNode):
    value: Optional['ASTNode']

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List['ASTNode']

@dataclass
class BinOp(ASTNode):
    left: 'ASTNode'
    op: str
    right: 'ASTNode'

@dataclass
class Number(ASTNode):
    value: int

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class Comparison(ASTNode):
    left: 'ASTNode'
    op: str
    right: 'ASTNode'

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current_token()
        print(f"[PARSER ERROR] Line {token.line}, Col {token.column}: {msg}")
        sys.exit(1)
    
    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]
    
    def peek_token(self, offset=1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def consume(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type}")
        self.pos += 1
        return token
    
    def advance(self):
        self.pos += 1
    
    def parse(self) -> Program:
        functions = []
        statements = []
        
        while self.current_token().type != TokenType.EOF:
            if self.current_token().type in [TokenType.INT, TokenType.VOID]:
                if self.peek_token(1).type == TokenType.IDENTIFIER and \
                   self.peek_token(2).type == TokenType.LPAREN:
                    functions.append(self.parse_function_def())
                else:
                    self.error("Expected function definition")
            else:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
        
        return Program(functions, statements)
    
    def parse_function_def(self) -> FunctionDef:
        return_type_token = self.current_token()
        if return_type_token.type == TokenType.INT:
            return_type = 'int'
        elif return_type_token.type == TokenType.VOID:
            return_type = 'void'
        else:
            self.error("Expected 'int' or 'void'")
        self.advance()
        
        name_token = self.consume(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.consume(TokenType.LPAREN)
        params = self.parse_param_list()
        self.consume(TokenType.RPAREN)
        
        self.consume(TokenType.LBRACE)
        body = self.parse_block()
        self.consume(TokenType.RBRACE)
        
        return FunctionDef(return_type, name, params, body)
    
    def parse_param_list(self) -> List[str]:
        params = []
        
        if self.current_token().type == TokenType.RPAREN:
            return params
        
        params.append(self.consume(TokenType.IDENTIFIER).value)
        
        while self.current_token().type == TokenType.COMMA:
            self.consume(TokenType.COMMA)
            params.append(self.consume(TokenType.IDENTIFIER).value)
        
        return params
    
    def parse_statement(self) -> Optional[ASTNode]:
        token = self.current_token()
        
        if token.type == TokenType.LET:
            return self.parse_declaration()
        elif token.type == TokenType.PRINT:
            return self.parse_print()
        elif token.type == TokenType.IF:
            return self.parse_if()
        elif token.type == TokenType.WHILE:
            return self.parse_while()
        elif token.type == TokenType.RETURN:
            return self.parse_return()
        elif token.type == TokenType.IDENTIFIER:
            if self.peek_token(1).type == TokenType.ASSIGN:
                return self.parse_reassignment()
            elif self.peek_token(1).type == TokenType.LPAREN:
                return self.parse_function_call_stmt()
            else:
                self.error(f"Unexpected token sequence starting with {token.type}")
        else:
            self.error(f"Unexpected token: {token.type}")
    
    def parse_declaration(self) -> Declaration:
        self.consume(TokenType.LET)
        ident_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        return Declaration(ident_token.value, value)
    
    def parse_reassignment(self) -> Assignment:
        ident_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        return Assignment(ident_token.value, value)
    
    def parse_print(self) -> PrintStmt:
        self.consume(TokenType.PRINT)
        value = self.parse_expression()
        return PrintStmt(value)
    
    def parse_if(self) -> IfStmt:
        self.consume(TokenType.IF)
        condition = self.parse_condition()
        self.consume(TokenType.LBRACE)
        then_block = self.parse_block()
        self.consume(TokenType.RBRACE)
        
        else_block = None
        if self.current_token().type == TokenType.ELSE:
            self.consume(TokenType.ELSE)
            self.consume(TokenType.LBRACE)
            else_block = self.parse_block()
            self.consume(TokenType.RBRACE)
        
        return IfStmt(condition, then_block, else_block)
    
    def parse_while(self) -> WhileStmt:
        self.consume(TokenType.WHILE)
        condition = self.parse_condition()
        self.consume(TokenType.LBRACE)
        body = self.parse_block()
        self.consume(TokenType.RBRACE)
        return WhileStmt(condition, body)
    
    def parse_return(self) -> ReturnStmt:
        self.consume(TokenType.RETURN)
        
        if self.current_token().type in [TokenType.RBRACE, TokenType.EOF]:
            return ReturnStmt(None)
        
        value = self.parse_expression()
        return ReturnStmt(value)
    
    def parse_function_call_stmt(self) -> FunctionCall:
        return self.parse_function_call()
    
    def parse_function_call(self) -> FunctionCall:
        name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.LPAREN)
        arguments = self.parse_arg_list()
        self.consume(TokenType.RPAREN)
        return FunctionCall(name, arguments)
    
    def parse_arg_list(self) -> List[ASTNode]:
        args = []
        
        if self.current_token().type == TokenType.RPAREN:
            return args
        
        args.append(self.parse_expression())
        
        while self.current_token().type == TokenType.COMMA:
            self.consume(TokenType.COMMA)
            args.append(self.parse_expression())
        
        return args
    
    def parse_block(self) -> List[ASTNode]:
        statements = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements
    
    def parse_condition(self) -> Comparison:
        left = self.parse_expression()
        op_token = self.current_token()
        
        if op_token.type not in [TokenType.LT, TokenType.GT, TokenType.EQ, 
                                  TokenType.NEQ, TokenType.LTE, TokenType.GTE]:
            self.error(f"Expected comparison operator, got {op_token.type}")
        
        self.advance()
        right = self.parse_expression()
        return Comparison(left, op_token.value, right)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_additive()
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.current_token()
            self.advance()
            right = self.parse_multiplicative()
            left = BinOp(left, op_token.value, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_primary()
        
        while self.current_token().type in [TokenType.MUL, TokenType.DIV, TokenType.MOD]:
            op_token = self.current_token()
            self.advance()
            right = self.parse_primary()
            left = BinOp(left, op_token.value, right)
        
        return left
    
    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        elif token.type == TokenType.IDENTIFIER:
            if self.peek_token(1).type == TokenType.LPAREN:
                return self.parse_function_call()
            else:
                self.advance()
                return Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        else:
            self.error(f"Unexpected token: {token.type}")


# ============================================================================
# PHASE 3: SEMANTIC ANALYSIS WITH SYMBOL TABLE MANAGER
# ============================================================================

@dataclass
class FunctionSignature:
    return_type: str
    param_count: int
    param_names: List[str]

class SymbolTable:
    """Symbol Table Manager for tracking variables and functions"""
    def __init__(self, parent=None, name="global"):
        self.symbols: Dict[str, Dict[str, Any]] = {}
        self.functions: Dict[str, FunctionSignature] = {}
        self.parent = parent
        self.name = name
    
    def declare_var(self, name: str, value: int = 0):
        if name in self.symbols:
            print(f"[SEMANTIC ERROR] Variable '{name}' already declared in scope '{self.name}'")
            sys.exit(1)
        self.symbols[name] = {'type': 'int', 'value': value}
    
    def declare_function(self, name: str, return_type: str, params: List[str]):
        if name in self.functions:
            print(f"[SEMANTIC ERROR] Function '{name}' already declared")
            sys.exit(1)
        self.functions[name] = FunctionSignature(return_type, len(params), params)
    
    def lookup_var(self, name: str) -> Optional[Dict[str, Any]]:
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup_var(name)
        return None
    
    def lookup_function(self, name: str) -> Optional[FunctionSignature]:
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.lookup_function(name)
        return None
    
    def set_value(self, name: str, value: int):
        if name in self.symbols:
            self.symbols[name]['value'] = value
        elif self.parent:
            self.parent.set_value(name, value)
        else:
            print(f"[SEMANTIC ERROR] Variable '{name}' not declared")
            sys.exit(1)
    
    def get_all_symbols(self) -> Dict[str, Dict[str, Any]]:
        """Get all symbols including parent scopes"""
        all_symbols = {}
        if self.parent:
            all_symbols.update(self.parent.get_all_symbols())
        all_symbols.update(self.symbols)
        return all_symbols

class SemanticAnalyzer:
    def __init__(self, ast: Program):
        self.ast = ast
        self.global_scope = SymbolTable(name="global")
        self.current_scope = self.global_scope
        self.current_function_return_type: Optional[str] = None
        self.all_scopes: List[SymbolTable] = [self.global_scope]
    
    def analyze(self):
        for func in self.ast.functions:
            self.global_scope.declare_function(func.name, func.return_type, func.params)
        
        for func in self.ast.functions:
            self.check_function(func)
        
        for stmt in self.ast.statements:
            self.check_statement(stmt)
    
    def check_function(self, func: FunctionDef):
        func_scope = SymbolTable(parent=self.global_scope, name=f"function_{func.name}")
        self.all_scopes.append(func_scope)
        
        for param in func.params:
            func_scope.declare_var(param)
        
        old_scope = self.current_scope
        old_return_type = self.current_function_return_type
        
        self.current_scope = func_scope
        self.current_function_return_type = func.return_type
        
        has_return = False
        for stmt in func.body:
            self.check_statement(stmt)
            if isinstance(stmt, ReturnStmt):
                has_return = True
        
        if func.return_type == 'int' and not has_return:
            print(f"[SEMANTIC WARNING] Function '{func.name}' with return type 'int' may not return a value")
        
        self.current_scope = old_scope
        self.current_function_return_type = old_return_type
    
    def check_statement(self, stmt: ASTNode):
        if isinstance(stmt, (Declaration, Assignment)):
            self.check_expression(stmt.value)
            if stmt.identifier not in self.current_scope.symbols:
                self.current_scope.declare_var(stmt.identifier)
        elif isinstance(stmt, PrintStmt):
            self.check_expression(stmt.value)
        elif isinstance(stmt, IfStmt):
            self.check_expression(stmt.condition)
            for s in stmt.then_block:
                self.check_statement(s)
            if stmt.else_block:
                for s in stmt.else_block:
                    self.check_statement(s)
        elif isinstance(stmt, WhileStmt):
            self.check_expression(stmt.condition)
            for s in stmt.body:
                self.check_statement(s)
        elif isinstance(stmt, ReturnStmt):
            if self.current_function_return_type is None:
                print("[SEMANTIC ERROR] Return statement outside of function")
                sys.exit(1)
            
            if stmt.value is None:
                if self.current_function_return_type != 'void':
                    print(f"[SEMANTIC ERROR] Function expects '{self.current_function_return_type}' return type, got void")
                    sys.exit(1)
            else:
                if self.current_function_return_type == 'void':
                    print(f"[SEMANTIC ERROR] Void function cannot return a value")
                    sys.exit(1)
                self.check_expression(stmt.value)
        elif isinstance(stmt, FunctionCall):
            self.check_function_call(stmt)
    
    def check_expression(self, expr: ASTNode):
        if isinstance(expr, BinOp):
            self.check_expression(expr.left)
            self.check_expression(expr.right)
        elif isinstance(expr, Identifier):
            if self.current_scope.lookup_var(expr.name) is None:
                print(f"[SEMANTIC ERROR] Variable '{expr.name}' not declared")
                sys.exit(1)
        elif isinstance(expr, Comparison):
            self.check_expression(expr.left)
            self.check_expression(expr.right)
        elif isinstance(expr, FunctionCall):
            self.check_function_call(expr)
    
    def check_function_call(self, call: FunctionCall):
        func_sig = self.current_scope.lookup_function(call.name)
        
        if func_sig is None:
            print(f"[SEMANTIC ERROR] Function '{call.name}' not declared")
            sys.exit(1)
        
        if len(call.arguments) != func_sig.param_count:
            print(f"[SEMANTIC ERROR] Function '{call.name}' expects {func_sig.param_count} arguments, got {len(call.arguments)}")
            sys.exit(1)
        
        for arg in call.arguments:
            self.check_expression(arg)


# ============================================================================
# PHASE 4-6: DIRECT INTERPRETATION
# ============================================================================

class SimpleInterpreter:
    """Direct AST interpreter - simpler and more reliable than 3-address code"""
    
    def __init__(self, ast: Program):
        self.ast = ast
        self.global_vars: Dict[str, int] = {}
        self.functions: Dict[str, FunctionDef] = {}
    
    def run(self):
        # Register all functions
        for func in self.ast.functions:
            self.functions[func.name] = func
        
        # Execute main statements
        for stmt in self.ast.statements:
            self.execute_stmt(stmt, self.global_vars)
    
    def execute_stmt(self, stmt: ASTNode, scope: Dict[str, int]) -> Optional[int]:
        """Execute statement, return value if it's a return statement"""
        if isinstance(stmt, Declaration):
            value = self.eval_expr(stmt.value, scope)
            scope[stmt.identifier] = value
            return None
        
        elif isinstance(stmt, Assignment):
            value = self.eval_expr(stmt.value, scope)
            scope[stmt.identifier] = value
            return None
        
        elif isinstance(stmt, PrintStmt):
            value = self.eval_expr(stmt.value, scope)
            print(value)
            return None
        
        elif isinstance(stmt, ReturnStmt):
            if stmt.value:
                return self.eval_expr(stmt.value, scope)
            return 0
        
        elif isinstance(stmt, IfStmt):
            cond = self.eval_expr(stmt.condition, scope)
            if cond:
                for s in stmt.then_block:
                    ret = self.execute_stmt(s, scope)
                    if ret is not None:
                        return ret
            elif stmt.else_block:
                for s in stmt.else_block:
                    ret = self.execute_stmt(s, scope)
                    if ret is not None:
                        return ret
            return None
        
        elif isinstance(stmt, WhileStmt):
            while self.eval_expr(stmt.condition, scope):
                for s in stmt.body:
                    ret = self.execute_stmt(s, scope)
                    if ret is not None:
                        return ret
            return None
        
        elif isinstance(stmt, FunctionCall):
            self.call_function(stmt.name, stmt.arguments, scope)
            return None
        
        return None
    
    def eval_expr(self, expr: ASTNode, scope: Dict[str, int]) -> int:
        if isinstance(expr, Number):
            return expr.value
        
        elif isinstance(expr, Identifier):
            if expr.name in scope:
                return scope[expr.name]
            elif expr.name in self.global_vars:
                return self.global_vars[expr.name]
            else:
                print(f"[RUNTIME ERROR] Variable '{expr.name}' not found")
                sys.exit(1)
        
        elif isinstance(expr, BinOp):
            left = self.eval_expr(expr.left, scope)
            right = self.eval_expr(expr.right, scope)
            
            if expr.op == '+':
                return left + right
            elif expr.op == '-':
                return left - right
            elif expr.op == '*':
                return left * right
            elif expr.op == '/':
                return left // right if right != 0 else 0
            elif expr.op == '%':
                return left % right if right != 0 else 0
            
            return 0
        
        elif isinstance(expr, Comparison):
            left = self.eval_expr(expr.left, scope)
            right = self.eval_expr(expr.right, scope)
            
            if expr.op == '<':
                return 1 if left < right else 0
            elif expr.op == '>':
                return 1 if left > right else 0
            elif expr.op == '==':
                return 1 if left == right else 0
            elif expr.op == '!=':
                return 1 if left != right else 0
            elif expr.op == '<=':
                return 1 if left <= right else 0
            elif expr.op == '>=':
                return 1 if left >= right else 0
            
            return 0
        
        elif isinstance(expr, FunctionCall):
            return self.call_function(expr.name, expr.arguments, scope)
        
        return 0
    
    def call_function(self, name: str, arguments: List[ASTNode], caller_scope: Dict[str, int]) -> int:
        if name not in self.functions:
            print(f"[RUNTIME ERROR] Function '{name}' not found")
            sys.exit(1)
        
        func = self.functions[name]
        
        # Create new scope for function
        func_scope = {}
        
        # Evaluate and bind arguments to parameters
        for i, param_name in enumerate(func.params):
            arg_value = self.eval_expr(arguments[i], caller_scope)
            func_scope[param_name] = arg_value
        
        # Execute function body
        for stmt in func.body:
            ret_val = self.execute_stmt(stmt, func_scope)
            if ret_val is not None:  # Return statement
                return ret_val
        
        return 0  # Default return value


# ============================================================================
# MAIN COMPILER WITH VISUALIZATIONS
# ============================================================================

class NumPatCompiler:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.ast = None
        self.semantic_analyzer = None
    
    def compile(self):
        print("="*70)
        print("[PHASE 1] LEXICAL ANALYSIS")
        print("="*70)
        lexer = Lexer(self.source)
        self.tokens = lexer.tokenize()
        self.print_tokens()
        
        print("\n" + "="*70)
        print("[PHASE 2] SYNTAX ANALYSIS (Top-Down Recursive Descent)")
        print("="*70)
        parser = Parser(self.tokens)
        self.ast = parser.parse()
        print("✓ Parse successful!")
        print(f"  • Functions defined: {len(self.ast.functions)}")
        for func in self.ast.functions:
            params_str = ', '.join(func.params) if func.params else 'none'
            print(f"    - {func.return_type} {func.name}({params_str})")
        print(f"  • Main statements: {len(self.ast.statements)}")
        self.print_parse_tree_summary()
        
        print("\n" + "="*70)
        print("[PHASE 3] SEMANTIC ANALYSIS & SYMBOL TABLE MANAGER")
        print("="*70)
        self.semantic_analyzer = SemanticAnalyzer(self.ast)
        self.semantic_analyzer.analyze()
        print("✓ Semantic analysis successful!")
        self.print_symbol_table()
        
        print("\n" + "="*70)
        print("[PHASE 4-6] INTERPRETATION & EXECUTION")
        print("="*70)
        print("Output:")
        print("-" * 70)
        interpreter = SimpleInterpreter(self.ast)
        interpreter.run()
        print("-" * 70)
    
    def print_tokens(self):
        print(f"\n{'Lexeme':<15} {'Token Type':<15} {'Line':<5} {'Column':<5}")
        print("-" * 50)
        display_count = min(30, len(self.tokens))
        for token in self.tokens[:display_count]:
            if token.type != TokenType.EOF:
                print(f"{str(token.value):<15} {token.type.value:<15} {token.line:<5} {token.column:<5}")
        if len(self.tokens) > display_count:
            print(f"... ({len(self.tokens) - display_count} more tokens)")
        print(f"\n✓ Total tokens: {len(self.tokens)}")
    
    def print_parse_tree_summary(self):
        print("\nParse Tree Structure:")
        print("-" * 50)
        print("Program")
        
        if self.ast.functions:
            print("├── Functions")
            for i, func in enumerate(self.ast.functions):
                is_last_func = (i == len(self.ast.functions) - 1) and len(self.ast.statements) == 0
                prefix = "└──" if is_last_func else "├──"
                print(f"│   {prefix} {func.return_type} {func.name}(...) [{len(func.body)} statements in body]")
        
        if self.ast.statements:
            print("└── Main Statements")
            for i, stmt in enumerate(self.ast.statements):
                is_last = i == len(self.ast.statements) - 1
                prefix = "└──" if is_last else "├──"
                stmt_type = type(stmt).__name__
                print(f"    {prefix} {stmt_type}")
    
    def print_symbol_table(self):
        print("\nSymbol Table Manager (STM) Visualization:")
        print("=" * 70)
        
        # Global scope
        global_scope = self.semantic_analyzer.global_scope
        print("\n[GLOBAL SCOPE]")
        print("-" * 70)
        
        # Functions table
        if global_scope.functions:
            print("\nFunctions:")
            print(f"{'Name':<20} {'Return Type':<15} {'Parameters':<30}")
            print("-" * 70)
            for name, sig in global_scope.functions.items():
                params_str = ', '.join(sig.param_names) if sig.param_names else '(none)'
                print(f"{name:<20} {sig.return_type:<15} {params_str:<30}")
        
        # Global variables
        if global_scope.symbols:
            print("\nGlobal Variables:")
            print(f"{'Name':<20} {'Type':<15} {'Initial Value':<15}")
            print("-" * 70)
            for name, info in global_scope.symbols.items():
                print(f"{name:<20} {info['type']:<15} {info['value']:<15}")
        
        # Local scopes (function scopes)
        for scope in self.semantic_analyzer.all_scopes:
            if scope.name != "global":
                print(f"\n[{scope.name.upper()}]")
                print("-" * 70)
                if scope.symbols:
                    print(f"{'Name':<20} {'Type':<15} {'Scope':<15}")
                    print("-" * 70)
                    for name, info in scope.symbols.items():
                        scope_type = "parameter" if scope.parent == global_scope else "local"
                        print(f"{name:<20} {info['type']:<15} {scope_type:<15}")
                else:
                    print("(No local variables)")
        
        print("\n" + "=" * 70)
        print(f"✓ Total scopes: {len(self.semantic_analyzer.all_scopes)}")
        print(f"✓ Total functions: {len(global_scope.functions)}")
        total_vars = sum(len(scope.symbols) for scope in self.semantic_analyzer.all_scopes)
        print(f"✓ Total variables: {total_vars}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 numpar_compiler.py <source_file>")
        sys.exit(1)
    
    try:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found")
        sys.exit(1)
    
    compiler = NumPatCompiler(source)
    compiler.compile()


if __name__ == "__main__":
    main()
