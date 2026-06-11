"""
Generador de código intermedio para MiniLang.

Traduce el AST a código de tres direcciones (Three-Address Code / TAC).
Cada instrucción tiene la forma:  resultado = operando1 operador operando2

Esta fase convierte el intérprete en un compilador: en vez de ejecutar el
AST directamente, primero lo traduce a una representación intermedia (TAC)
que luego puede ser ejecutada o traducida a otro lenguaje destino.

Ejemplos de instrucciones generadas:
    t1 = 5
    t2 = x
    t3 = t1 + t2
    x = t3
    mostrar t3
    if_false t4 goto L2
    goto L1
    L1:
"""

from .parser import Program, VarDecl, Assign, Show, BinOp, Number, VarRef, Compare, IfStmt, WhileStmt
from .tokens import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_EQEQ, TT_NEQ, TT_LT, TT_GT, TT_LTE, TT_GTE


_OP_SYMBOLS = {
    TT_PLUS:  '+',
    TT_MINUS: '-',
    TT_MUL:   '*',
    TT_DIV:   '/',
    TT_EQEQ:  '==',
    TT_NEQ:   '!=',
    TT_LT:    '<',
    TT_GT:    '>',
    TT_LTE:   '<=',
    TT_GTE:   '>=',
}


class CodeGen:
    def __init__(self):
        self.instructions = []
        self._temp_count = 0
        self._label_count = 0

    def _new_temp(self):
        self._temp_count += 1
        return f"t{self._temp_count}"

    def _new_label(self):
        self._label_count += 1
        return f"L{self._label_count}"

    def _emit(self, instr):
        self.instructions.append(instr)

    # ------------------------------------------------------------------ #
    # Punto de entrada                                                     #
    # ------------------------------------------------------------------ #

    def generate(self, program: Program):
        for stmt in program.statements:
            self._gen_stmt(stmt)
        return self.instructions

    # ------------------------------------------------------------------ #
    # Sentencias                                                           #
    # ------------------------------------------------------------------ #

    def _gen_stmt(self, stmt):
        if isinstance(stmt, (VarDecl, Assign)):
            temp = self._gen_expr(stmt.expr)
            self._emit(f"{stmt.name} = {temp}")

        elif isinstance(stmt, Show):
            temp = self._gen_expr(stmt.expr)
            self._emit(f"mostrar {temp}")

        elif isinstance(stmt, IfStmt):
            temp = self._gen_expr(stmt.condition)
            else_label = self._new_label()
            end_label  = self._new_label()

            self._emit(f"if_false {temp} goto {else_label}")
            for s in stmt.then_body:
                self._gen_stmt(s)

            if stmt.else_body:
                self._emit(f"goto {end_label}")
                self._emit(f"{else_label}:")
                for s in stmt.else_body:
                    self._gen_stmt(s)
                self._emit(f"{end_label}:")
            else:
                self._emit(f"{else_label}:")

        elif isinstance(stmt, WhileStmt):
            start_label = self._new_label()
            end_label   = self._new_label()

            self._emit(f"{start_label}:")
            temp = self._gen_expr(stmt.condition)
            self._emit(f"if_false {temp} goto {end_label}")
            for s in stmt.body:
                self._gen_stmt(s)
            self._emit(f"goto {start_label}")
            self._emit(f"{end_label}:")

    # ------------------------------------------------------------------ #
    # Expresiones — devuelven el nombre del temporal que guarda el valor  #
    # ------------------------------------------------------------------ #

    def _gen_expr(self, expr):
        if isinstance(expr, Number):
            temp = self._new_temp()
            self._emit(f"{temp} = {expr.value}")
            return temp

        elif isinstance(expr, VarRef):
            temp = self._new_temp()
            self._emit(f"{temp} = {expr.name}")
            return temp

        elif isinstance(expr, (BinOp, Compare)):
            left  = self._gen_expr(expr.left)
            right = self._gen_expr(expr.right)
            temp  = self._new_temp()
            self._emit(f"{temp} = {left} {_OP_SYMBOLS[expr.op]} {right}")
            return temp


def generate(program_ast):
    cg = CodeGen()
    return cg.generate(program_ast)
