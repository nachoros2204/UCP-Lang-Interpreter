from minilang.lexer import tokenize
from minilang.parser import parse_tokens
from minilang.interpreter import Interpreter


def ejecutar(codigo):
    ast = parse_tokens(tokenize(codigo))
    interpreter = Interpreter()
    interpreter.interpret(ast)
    return interpreter


def test_declaracion_variable():
    codigo = """
inicio
entero x = 10
fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 10


def test_asignacion_variable():
    codigo = """
inicio
entero x = 10
x = 20
fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 20


def test_suma():
    codigo = """
inicio
entero x = 10 + 5
fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 15


def test_resta():
    codigo = """
inicio
entero x = 10 - 3
fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 7


def test_multiplicacion():
    codigo = """
inicio
entero x = 4 * 5
fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 20


def test_division_entera():
    codigo = """
inicio
entero x = 10 / 2
fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 5


def test_if_verdadero():
    codigo = """
inicio
entero x = 0

si 1 == 1
x = 10
fin_si

fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 10


def test_if_else_falso():
    codigo = """
inicio
entero x = 0

si 1 == 2
x = 10
sino
x = 20
fin_si

fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 20


def test_while():
    codigo = """
inicio
entero x = 0

mientras x < 5
x = x + 1
fin_mientras

fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 5


def test_comparacion():
    codigo = """
inicio
entero x = 5 < 10
fin
"""

    interp = ejecutar(codigo)

    assert interp.symbols["x"] == 1