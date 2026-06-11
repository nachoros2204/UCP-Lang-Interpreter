"""
Módulo de definición de tokens para MiniLang.
Contiene la clase Token y constantes de tipos de token.

Este archivo se mantiene deliberadamente simple para uso académico.
"""

from dataclasses import dataclass
from typing import Any


# Tipos de token usados por el lexer y el parser
TT_INT = 'INT'          # palabra reservada 'entero'
TT_START = 'START'      # 'inicio'
TT_END = 'END'          # 'fin'
TT_SHOW = 'SHOW'        # 'mostrar'
TT_ID = 'ID'            # identificador de variable
TT_NUMBER = 'NUMBER'    # literal numérico entero
TT_PLUS = 'PLUS'        # +
TT_MINUS = 'MINUS'      # -
TT_MUL = 'MUL'          # *
TT_DIV = 'DIV'          # /
TT_EQ = 'EQ'            # = asignación
TT_LPAREN = 'LPAREN'    # (
TT_RPAREN = 'RPAREN'    # )
TT_NEWLINE = 'NEWLINE'  # fin de línea (separador de sentencias)
TT_EOF = 'EOF'          # fin de archivo

# Operadores de comparación
TT_EQEQ = 'EQEQ'       # ==
TT_NEQ   = 'NEQ'        # !=
TT_LT    = 'LT'         # <
TT_GT    = 'GT'         # >
TT_LTE   = 'LTE'        # <=
TT_GTE   = 'GTE'        # >=


@dataclass
class Token:
    type: str
    value: Any = None
    line: int = 0 
    column: int = 0

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {self.value}, line={self.line})"
        return f"Token({self.type}, line={self.line})"
