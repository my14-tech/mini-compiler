import re

# -------- TOKEN DEFINITIONS --------
KEYWORDS = {'int', 'if', 'while', 'return'}
OPERATORS = {'+', '-', '*', '/', '=', '>', '<', '(', ')', '{', '}', ',', ';'}

# -------- LEXER FUNCTION --------
def lexer(code):
    tokens = []

    token_specification = [
        ('NUMBER',   r'\d+'),
        ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('OP',       r'[+\-*/=<>]'),
        ('SYMBOL',   r'[(){},;]'),
        ('SKIP',     r'[ \t\n]+'),
        ('MISMATCH', r'.'),
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NUMBER':
            tokens.append(('NUMBER', value))

        elif kind == 'ID':
            if value in KEYWORDS:
                tokens.append(('KEYWORD', value))
            else:
                tokens.append(('IDENTIFIER', value))

        elif kind == 'OP':
            tokens.append(('OPERATOR', value))

        elif kind == 'SYMBOL':
            if value == ';':
                tokens.append(('SEPARATOR', value))
            else:
                tokens.append(('OPERATOR', value))

        elif kind == 'SKIP':
            continue

        elif kind == 'MISMATCH':
            tokens.append(('ERROR', value))

    return tokens