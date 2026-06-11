"""
Programa principal para ejecutar MiniLang.

Uso:
    python -m minilang.main archivo.minilang
    python -m minilang.main archivo.minilang --codigo   (muestra TAC generado)

El flujo es: tokenizar -> parsear -> analizar -> generar código -> interpretar.
"""

import sys
from .lexer import tokenize, LexerError
from .parser import parse_tokens, ParseError
from .semantic_analyzer import analyze, SemanticError
from .codegen import generate
from .interpreter import run, RuntimeErrorML


def run_file(path, mostrar_codigo=False):
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
        analyze(ast)
    except SemanticError as e:
        print(f"Error semántico: {e}")
        return

    instrucciones = generate(ast)

    if mostrar_codigo:
        print("=== Código de tres direcciones generado ===")
        for instr in instrucciones:
            print(f"  {instr}")
        print("===========================================")

    try:
        run(ast)
    except RuntimeErrorML as e:
        print(f"Error en tiempo de ejecución: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python -m minilang.main ejemplos/archivo.minilang [--codigo]")
        sys.exit(1)
    mostrar = '--codigo' in sys.argv
    run_file(sys.argv[1], mostrar_codigo=mostrar)
