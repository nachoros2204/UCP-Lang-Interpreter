"""
Analizador semántico para MiniLang.

Recorre el AST ANTES de la ejecución y detecta errores semánticos
que el parser no puede encontrar por ser análisis de contexto:
  - Variable usada sin declarar
  - Variable declarada más de una vez
  - División por cero con divisor literal

Lanza `SemanticError` al encontrar el primer error.
"""

from .parser import Program, VarDecl, Assign, Show, BinOp, Number, VarRef, Compare
from .tokens import TT_DIV


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        # Conjunto de nombres de variables ya declaradas
        self.declared = set()

    def analyze(self, program: Program):
        for stmt in program.statements:
            self._check_statement(stmt)

    def _check_statement(self, stmt):
        if isinstance(stmt, VarDecl):
            if stmt.name in self.declared:
                raise SemanticError(
                    f"Variable '{stmt.name}' ya fue declarada (línea {stmt.line})"
                )
            self._check_expr(stmt.expr, stmt.line)
            self.declared.add(stmt.name)

        elif isinstance(stmt, Assign):
            if stmt.name not in self.declared:
                raise SemanticError(
                    f"Variable '{stmt.name}' usada sin declarar (línea {stmt.line})"
                )
            self._check_expr(stmt.expr, stmt.line)

        elif isinstance(stmt, Show):
            self._check_expr(stmt.expr, stmt.line)

    def _check_expr(self, expr, line):
        if isinstance(expr, Number):
            return

        elif isinstance(expr, VarRef):
            if expr.name not in self.declared:
                raise SemanticError(
                    f"Variable '{expr.name}' usada sin declarar (línea {line})"
                )

        elif isinstance(expr, BinOp):
            self._check_expr(expr.left, line)
            self._check_expr(expr.right, line)
            if expr.op == TT_DIV and isinstance(expr.right, Number) and expr.right.value == 0:
                raise SemanticError(f"División por cero detectada (línea {line})")

        elif isinstance(expr, Compare):
            self._check_expr(expr.left, line)
            self._check_expr(expr.right, line)


def analyze(program_ast):
    analyzer = SemanticAnalyzer()
    analyzer.analyze(program_ast)
