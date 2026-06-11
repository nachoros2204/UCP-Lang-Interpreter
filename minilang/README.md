MiniLang — Intérprete educativo
================================

Estructura del proyecto:

minilang/
├── lexer.py
├── parser.py
├── interpreter.py
├── tokens.py
├── main.py
├── ejemplos/
└── README.md


Descripción breve
-----------------
MiniLang es un lenguaje educativo mínimo para la materia de Teoría de la Computación.
Este intérprete implementa las fases clásicas: Análisis Léxico (lexer), Análisis Sintáctico
(parser) y Ejecución Semántica/Intérprete. Todo está implementado en Python sin
usar `exec()` ni traducir MiniLang a Python.


Gramática (informal)
--------------------
Programa -> inicio Stmts fin
Stmts -> { Sentencia }
Sentencia -> "entero" ID "=" Expr    (declaración)
           | ID "=" Expr              (asignación)
           | "mostrar" Expr          (impresión)

Expr -> Term { ("+" | "-") Term }
Term -> Factor { ("*" | "/") Factor }
Factor -> NUMBER | ID | "(" Expr ")" | "-" Factor


Características implementadas
-----------------------------
- Lexer basado en expresiones regulares.
- Parser recursivo-descendente que construye un AST.
- Intérprete con tabla de símbolos para variables enteras.
- Manejo básico de errores léxicos, sintácticos y semánticos.


Cómo ejecutar
-------------
Desde la carpeta que contiene `minilang/` ejecutar:

```bash
python -m minilang.main minilang/ejemplos/valid.minilang
```

Salida esperada para `valid.minilang`:

```
30
```


Ejemplos
--------
- `ejemplos/valid.minilang`: programa válido que imprime `30`.
- `ejemplos/invalid_syntax.minilang`: ejemplo con error sintáctico.
- `ejemplos/invalid_lex.minilang`: ejemplo con error léxico.
