"""
Intérprete para MiniLang.

Recibe un AST (desde `parser.py`) y lo ejecuta usando una tabla de símbolos simple.
No traduce a Python: evalúa las expresiones manualmente.
"""

from .parser import *


class RuntimeErrorML(Exception):
    pass


class Interpreter:
    def __init__(self):
        # Tabla de símbolos: nombre -> valor entero
        self.symbols = {}

    def interpret(self, program: Program):
        for stmt in program.statements:
            self.exec_statement(stmt)

    def exec_statement(self, stmt):
        if isinstance(stmt, VarDecl):
            if stmt.name in self.symbols:
                raise RuntimeErrorML(f"Variable ya declarada: {stmt.name} (línea {stmt.line})")
            value = self.eval_expr(stmt.expr)
            # tipado simple: sólo enteros
            if not isinstance(value, int):
                raise RuntimeErrorML(f"Solo valores enteros permitidos (línea {stmt.line})")
            self.symbols[stmt.name] = value
        elif isinstance(stmt, Assign):
            if stmt.name not in self.symbols:
                raise RuntimeErrorML(f"Variable no declarada: {stmt.name} (línea {stmt.line})")
            value = self.eval_expr(stmt.expr)
            if not isinstance(value, int):
                raise RuntimeErrorML(f"Solo valores enteros permitidos (línea {stmt.line})")
            self.symbols[stmt.name] = value
        elif isinstance(stmt, Show):
            value = self.eval_expr(stmt.expr)
            print(value)
        else:
            raise RuntimeErrorML(f"Sentencia desconocida: {stmt}")

    def eval_expr(self, expr):
        if isinstance(expr, Number):
            return expr.value
        elif isinstance(expr, VarRef):
            if expr.name not in self.symbols:
                raise RuntimeErrorML(f"Variable no declarada: {expr.name}")
            return self.symbols[expr.name]
        elif isinstance(expr, BinOp):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            op = expr.op
            if op == TT_PLUS:
                return left + right
            elif op == TT_MINUS:
                return left - right
            elif op == TT_MUL:
                return left * right
            elif op == TT_DIV:
                if right == 0:
                    raise RuntimeErrorML("División por cero")
                return left // right
            else:
                raise RuntimeErrorML(f"Operador desconocido: {op}")
        else:
            raise RuntimeErrorML(f"Expresión no manejada: {expr}")


def run(program_ast):
    interp = Interpreter()
    interp.interpret(program_ast)
