from minilang.lexer import tokenize
from minilang.parser import (
    parse_tokens,
    Program,
    VarDecl,
    Assign,
    Show,
    IfStmt,
    WhileStmt
)


def test_parse_programa_vacio():
    codigo = """
inicio
fin
"""
    ast = parse_tokens(tokenize(codigo))

    assert isinstance(ast, Program)
    assert len(ast.statements) == 0


def test_parse_declaracion_variable():
    codigo = """
inicio
entero x = 10
fin
"""
    ast = parse_tokens(tokenize(codigo))

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], VarDecl)
    assert ast.statements[0].name == "x"


def test_parse_asignacion():
    codigo = """
inicio
x = 20
fin
"""
    ast = parse_tokens(tokenize(codigo))

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], Assign)
    assert ast.statements[0].name == "x"


def test_parse_mostrar():
    codigo = """
inicio
mostrar 10
fin
"""
    ast = parse_tokens(tokenize(codigo))

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], Show)


def test_parse_if():
    codigo = """
inicio
si 1 == 1
mostrar 1
fin_si
fin
"""
    ast = parse_tokens(tokenize(codigo))

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], IfStmt)


def test_parse_if_else():
    codigo = """
inicio
si 1 == 1
mostrar 1
sino
mostrar 0
fin_si
fin
"""
    ast = parse_tokens(tokenize(codigo))

    nodo = ast.statements[0]

    assert isinstance(nodo, IfStmt)
    assert len(nodo.then_body) == 1
    assert len(nodo.else_body) == 1


def test_parse_while():
    codigo = """
inicio
mientras 1 < 5
mostrar 1
fin_mientras
fin
"""
    ast = parse_tokens(tokenize(codigo))

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], WhileStmt)


def test_parse_varias_sentencias():
    codigo = """
inicio
entero x = 10
x = 20
mostrar x
fin
"""
    ast = parse_tokens(tokenize(codigo))

    assert len(ast.statements) == 3