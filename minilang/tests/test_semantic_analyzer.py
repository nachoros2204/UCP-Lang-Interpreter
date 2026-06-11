from minilang.lexer import tokenize
from minilang.parser import parse_tokens
from minilang.semantic_analyzer import analyze, SemanticError

import pytest


def test_programa_valido():
    codigo = """
inicio
entero x = 10
x = 20
mostrar x
fin
"""

    ast = parse_tokens(tokenize(codigo))

    # No debería lanzar excepción
    analyze(ast)


def test_variable_sin_declarar():
    codigo = """
inicio
mostrar x
fin
"""

    ast = parse_tokens(tokenize(codigo))

    with pytest.raises(SemanticError):
        analyze(ast)


def test_redeclaracion_variable():
    codigo = """
inicio
entero x = 10
entero x = 20
fin
"""

    ast = parse_tokens(tokenize(codigo))

    with pytest.raises(SemanticError):
        analyze(ast)


def test_asignacion_variable_no_declarada():
    codigo = """
inicio
x = 10
fin
"""

    ast = parse_tokens(tokenize(codigo))

    with pytest.raises(SemanticError):
        analyze(ast)


def test_division_por_cero_literal():
    codigo = """
inicio
entero x = 10 / 0
fin
"""

    ast = parse_tokens(tokenize(codigo))

    with pytest.raises(SemanticError):
        analyze(ast)


def test_uso_variable_declarada_en_expresion():
    codigo = """
inicio
entero x = 10
entero y = x + 5
mostrar y
fin
"""

    ast = parse_tokens(tokenize(codigo))

    # No debería lanzar excepción
    analyze(ast)