"""
Programa principal para ejecutar MiniLang.

Uso:
    python -m minilang.main archivo.ml

El flujo es: tokenizar -> parsear -> interpretar.
"""

import sys
from .lexer import tokenize, LexerError
from .parser import parse_tokens, ParseError
from .interpreter import run, RuntimeErrorML


def run_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    try:
        tokens = tokenize(src)
    except LexerError as e:
        print(f"Error léxico: {e}")
        return
    try:
        ast = parse_tokens(tokens)
    except ParseError as e:
        print(f"Error sintáctico: {e}")
        return
    try:
        run(ast)
    except RuntimeErrorML as e:
        print(f"Error en tiempo de ejecución: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python -m minilang.main ejemplos/archivo.ml")
        sys.exit(1)
    run_file(sys.argv[1])
