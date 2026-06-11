from minilang.lexer import tokenize
from minilang.parser import parse_tokens
from minilang.codegen import generate


def test_generacion_declaracion():
    codigo = """
inicio
entero x = 10
fin
"""

    instrucciones = generate(parse_tokens(tokenize(codigo)))

    assert "t1 = 10" in instrucciones
    assert "x = t1" in instrucciones


def test_generacion_suma():
    codigo = """
inicio
entero x = 5 + 3
fin
"""

    instrucciones = generate(parse_tokens(tokenize(codigo)))

    assert any("+" in instr for instr in instrucciones)


def test_generacion_mostrar():
    codigo = """
inicio
mostrar 10
fin
"""

    instrucciones = generate(parse_tokens(tokenize(codigo)))

    assert instrucciones[-1].startswith("mostrar")


def test_generacion_if():
    codigo = """
inicio
si 1 == 1
mostrar 1
fin_si
fin
"""

    instrucciones = generate(parse_tokens(tokenize(codigo)))

    assert any("if_false" in instr for instr in instrucciones)


def test_generacion_while():
    codigo = """
inicio
mientras 1 < 5
mostrar 1
fin_mientras
fin
"""

    instrucciones = generate(parse_tokens(tokenize(codigo)))

    assert any(instr.startswith("L") for instr in instrucciones)
    assert any("goto" in instr for instr in instrucciones)