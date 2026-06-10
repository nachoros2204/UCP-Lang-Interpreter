"""
Lexer para MiniLang.

Usa expresiones regulares para tokenizar la entrada. Detecta errores léxicos
cuando encuentra lexemas no reconocidos.

Salida: lista de objetos `Token` definidos en `tokens.py`.
"""

import re
from .tokens import *


# Especificación de tokens: nombre de grupo -> regex
TOKEN_SPECIFICATION = [
    ('NEWLINE', r"\n"),
    ('SKIP', r"[ \t]+"),
    ('COMMENT', r"#.*"),
    ('START', r"\binicio\b"),
    ('END', r"\bfin\b"),
    ('INT', r"\bentero\b"),
    ('SHOW', r"\bmostrar\b"),
    ('NUMBER', r"\b\d+\b"),
    ('ID', r"\b[A-Za-z_]\w*\b"),
    ('PLUS', r"\+"),
    ('MINUS', r"-"),
    ('MUL', r"\*"),
    ('DIV', r"/"),
    ('EQ', r"="),
    ('LPAREN', r"\("),
    ('RPAREN', r"\)"),
]


# Compilar regex combinado con grupos nombrados
master_pattern = re.compile('|'.join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECIFICATION))


class LexerError(Exception):
    pass


def tokenize(text):
    """Convierte `text` en una lista de Token.

    Regresa una lista que termina con un token `TT_EOF`.
    Lanza `LexerError` si encuentra un lexema no reconocido.
    """
    tokens = []
    line_num = 1
    line_start = 0
    for mo in master_pattern.finditer(text):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1

        if kind == 'NEWLINE':
            line_num += 1
            line_start = mo.end()
            tokens.append(Token(TT_NEWLINE, '\n', line=line_num - 1, column=column))
            continue
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'ID':
            # Palabras reservadas ya habrán sido capturadas por sus grupos
            tokens.append(Token(TT_ID, value, line=line_num, column=column))
        elif kind == 'NUMBER':
            tokens.append(Token(TT_NUMBER, int(value), line=line_num, column=column))
        elif kind == 'PLUS':
            tokens.append(Token(TT_PLUS, value, line=line_num, column=column))
        elif kind == 'MINUS':
            tokens.append(Token(TT_MINUS, value, line=line_num, column=column))
        elif kind == 'MUL':
            tokens.append(Token(TT_MUL, value, line=line_num, column=column))
        elif kind == 'DIV':
            tokens.append(Token(TT_DIV, value, line=line_num, column=column))
        elif kind == 'EQ':
            tokens.append(Token(TT_EQ, value, line=line_num, column=column))
        elif kind == 'LPAREN':
            tokens.append(Token(TT_LPAREN, value, line=line_num, column=column))
        elif kind == 'RPAREN':
            tokens.append(Token(TT_RPAREN, value, line=line_num, column=column))
        elif kind == 'START':
            tokens.append(Token(TT_START, value, line=line_num, column=column))
        elif kind == 'END':
            tokens.append(Token(TT_END, value, line=line_num, column=column))
        elif kind == 'INT':
            tokens.append(Token(TT_INT, value, line=line_num, column=column))
        elif kind == 'SHOW':
            tokens.append(Token(TT_SHOW, value, line=line_num, column=column))
        else:
            # Si alguna categoría se añade y no se maneja arriba
            raise LexerError(f"Token desconocido {value!r} en línea {line_num}")

    tokens.append(Token(TT_EOF, None, line=line_num))
    return tokens


if __name__ == '__main__':
    # Pequeña prueba manual
    sample = """
inicio

entero x = 10
entero y = 20

mostrar x + y

fin
"""
    for t in tokenize(sample):
        print(t)
