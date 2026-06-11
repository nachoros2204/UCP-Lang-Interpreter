from minilang.lexer import tokenize
from minilang.tokens import (
    TT_NUMBER,
    TT_ID,
    TT_START,
    TT_IF,
    TT_WHILE,
    TT_PLUS,
    TT_EQ,
    TT_EQEQ
)


def test_reconoce_numero():
    tokens = tokenize("123")

    assert tokens[0].type == TT_NUMBER
    assert tokens[0].value == 123


def test_reconoce_identificador():
    tokens = tokenize("variable")

    assert tokens[0].type == TT_ID
    assert tokens[0].value == "variable"


def test_reconoce_inicio():
    tokens = tokenize("inicio")

    assert tokens[0].type == TT_START
    assert tokens[0].value == "inicio"


def test_reconoce_if():
    tokens = tokenize("si")

    assert tokens[0].type == TT_IF
    assert tokens[0].value == "si"


def test_reconoce_while():
    tokens = tokenize("mientras")

    assert tokens[0].type == TT_WHILE
    assert tokens[0].value == "mientras"


def test_reconoce_suma():
    tokens = tokenize("+")

    assert tokens[0].type == TT_PLUS
    assert tokens[0].value == "+"


def test_reconoce_asignacion():
    tokens = tokenize("=")

    assert tokens[0].type == TT_EQ
    assert tokens[0].value == "="


def test_reconoce_igualdad():
    tokens = tokenize("==")

    assert tokens[0].type == TT_EQEQ
    assert tokens[0].value == "=="


def test_ignora_comentarios():
    tokens = tokenize("# comentario")

    # Solo debería quedar el EOF
    assert len(tokens) == 1


def test_tokeniza_declaracion():
    tokens = tokenize("entero x = 10")

    valores = [t.value for t in tokens[:-1]]

    assert valores == ["entero", "x", "=", 10]