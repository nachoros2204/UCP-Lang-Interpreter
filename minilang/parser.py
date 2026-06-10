"""
Parser para MiniLang (análisis sintáctico).

Implementa un parser recursivo-descendente que construye un AST simple.
Detecta errores sintácticos básicos y levanta excepciones con línea.
"""

from .tokens import *


class ParseError(Exception):
    pass


# Nodos del AST (simples, orientados a interpretación directa)
class Program:
    def __init__(self, statements):
        self.statements = statements


class VarDecl:
    def __init__(self, name, expr, line):
        self.name = name
        self.expr = expr
        self.line = line


class Assign:
    def __init__(self, name, expr, line):
        self.name = name
        self.expr = expr
        self.line = line


class Show:
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Number:
    def __init__(self, value):
        self.value = value


class VarRef:
    def __init__(self, name):
        self.name = name


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, ttype):
        tok = self.current()
        if tok.type == ttype:
            self.pos += 1
            return tok
        raise ParseError(f"Se esperaba {ttype} pero se encontró {tok.type} en línea {tok.line}")

    def skip_newlines(self):
        while self.current().type == TT_NEWLINE:
            self.pos += 1

    def parse(self):
        # Programa -> 'inicio' Stmts 'fin'
        self.skip_newlines()
        if self.current().type != TT_START:
            raise ParseError(f"Programa debe comenzar con 'inicio' (línea {self.current().line})")
        self.eat(TT_START)
        self.skip_newlines()

        statements = []
        while self.current().type not in (TT_END, TT_EOF):
            if self.current().type == TT_NEWLINE:
                self.skip_newlines()
                continue
            statements.append(self.parse_statement())
            self.skip_newlines()

        if self.current().type != TT_END:
            raise ParseError(f"Falta 'fin' al final del programa (l. {self.current().line})")
        self.eat(TT_END)
        # aceptar posibles NEWLINEs y EOF
        return Program(statements)

    def parse_statement(self):
        tok = self.current()
        if tok.type == TT_INT:
            # declaración: entero id = expr
            self.eat(TT_INT)
            idtok = self.eat(TT_ID)
            self.eat(TT_EQ)
            expr = self.parse_expr()
            return VarDecl(idtok.value, expr, tok.line)
        elif tok.type == TT_SHOW:
            self.eat(TT_SHOW)
            expr = self.parse_expr()
            return Show(expr, tok.line)
        elif tok.type == TT_ID:
            # asignación: id = expr
            idtok = self.eat(TT_ID)
            self.eat(TT_EQ)
            expr = self.parse_expr()
            return Assign(idtok.value, expr, idtok.line)
        else:
            raise ParseError(f"Sentencia inesperada: {tok.type} (línea {tok.line})")

    # Expresiones con precedencia: term ((+|-) term)*
    def parse_expr(self):
        node = self.parse_term()
        while self.current().type in (TT_PLUS, TT_MINUS):
            op = self.current()
            if op.type == TT_PLUS:
                self.eat(TT_PLUS)
            else:
                self.eat(TT_MINUS)
            right = self.parse_term()
            node = BinOp(node, op.type, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current().type in (TT_MUL, TT_DIV):
            op = self.current()
            if op.type == TT_MUL:
                self.eat(TT_MUL)
            else:
                self.eat(TT_DIV)
            right = self.parse_factor()
            node = BinOp(node, op.type, right)
        return node

    def parse_factor(self):
        tok = self.current()
        if tok.type == TT_NUMBER:
            self.eat(TT_NUMBER)
            return Number(tok.value)
        elif tok.type == TT_ID:
            self.eat(TT_ID)
            return VarRef(tok.value)
        elif tok.type == TT_LPAREN:
            self.eat(TT_LPAREN)
            node = self.parse_expr()
            self.eat(TT_RPAREN)
            return node
        elif tok.type == TT_MINUS:
            # soporte de unario: -factor
            self.eat(TT_MINUS)
            factor = self.parse_factor()
            return BinOp(Number(0), TT_MINUS, factor)
        else:
            raise ParseError(f"Factor inesperado {tok.type} en línea {tok.line}")


def parse_tokens(tokens):
    p = Parser(tokens)
    return p.parse()
