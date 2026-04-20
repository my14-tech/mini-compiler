class ASTNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        if node:
            self.children.append(node)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # -------- CURRENT TOKEN --------
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # -------- EAT --------
    def eat(self, token_type, value=None):
        token = self.current_token()
        if token and token[0] == token_type and (value is None or token[1] == value):
            self.pos += 1
            return token
        else:
            raise Exception(f"Syntax Error: Expected {token_type} {value}, got {token}")

    # -------- FACTOR --------
    def parse_factor(self):
        token = self.current_token()

        if not token:
            raise Exception("Unexpected end of input")

        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ASTNode(token[1])

        elif token[0] == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return ASTNode(token[1])

        elif token[1] == '(':
            self.eat('OPERATOR', '(')
            node = self.parse_expression()
            self.eat('OPERATOR', ')')
            return node

        else:
            raise Exception(f"Unexpected token: {token}")

    # -------- TERM (*, /) --------
    def parse_term(self):
        node = self.parse_factor()

        while self.current_token() and self.current_token()[1] in ('*', '/'):
            op = self.eat('OPERATOR')
            right = self.parse_factor()

            new_node = ASTNode(op[1])
            new_node.add_child(node)
            new_node.add_child(right)

            node = new_node

        return node

    # -------- ADDITIVE (+, -) --------
    def parse_additive(self):
        node = self.parse_term()

        while self.current_token() and self.current_token()[1] in ('+', '-'):
            op = self.eat('OPERATOR')
            right = self.parse_term()

            new_node = ASTNode(op[1])
            new_node.add_child(node)
            new_node.add_child(right)

            node = new_node

        return node

    # -------- COMPARISON --------
    def parse_comparison(self):
        node = self.parse_additive()

        while self.current_token() and self.current_token()[1] in ('>', '<'):
            op = self.eat('OPERATOR')
            right = self.parse_additive()

            new_node = ASTNode(op[1])
            new_node.add_child(node)
            new_node.add_child(right)

            node = new_node

        return node

    # -------- EXPRESSION --------
    def parse_expression(self):
        node = self.parse_comparison()

        # assignment: a = b + c
        if self.current_token() and self.current_token()[1] == '=':
            self.eat('OPERATOR', '=')
            right = self.parse_expression()

            assign_node = ASTNode("=")
            assign_node.add_child(node)
            assign_node.add_child(right)

            return assign_node

        return node

    # -------- DECLARATION --------
    def parse_declaration(self):
        self.eat('KEYWORD', 'int')

        identifier = self.eat('IDENTIFIER')

        node = ASTNode("DECLARATION")
        node.add_child(ASTNode(identifier[1]))

        if self.current_token() and self.current_token()[1] == '=':
            self.eat('OPERATOR', '=')
            expr = self.parse_expression()

            assign_node = ASTNode("=")
            assign_node.add_child(ASTNode(identifier[1]))
            assign_node.add_child(expr)

            node.add_child(assign_node)

        return node

    # -------- RETURN --------
    def parse_return(self):
        self.eat('KEYWORD', 'return')

        node = ASTNode("RETURN")

        if self.current_token() and self.current_token()[0] != 'SEPARATOR':
            expr = self.parse_expression()
            node.add_child(expr)

        return node

    # -------- IF --------
    def parse_if(self):
        self.eat('KEYWORD', 'if')
        self.eat('OPERATOR', '(')

        condition = self.parse_expression()

        self.eat('OPERATOR', ')')
        self.eat('OPERATOR', '{')

        body = ASTNode("BLOCK")

        while self.current_token() and self.current_token()[1] != '}':
            stmt = self.parse_statement()
            body.add_child(stmt)

            if self.current_token() and self.current_token()[0] == 'SEPARATOR':
                self.eat('SEPARATOR')

        self.eat('OPERATOR', '}')

        node = ASTNode("IF")
        node.add_child(condition)
        node.add_child(body)

        return node

    # -------- WHILE --------
    def parse_while(self):
        self.eat('KEYWORD', 'while')
        self.eat('OPERATOR', '(')

        condition = self.parse_expression()

        self.eat('OPERATOR', ')')
        self.eat('OPERATOR', '{')

        body = ASTNode("BLOCK")

        while self.current_token() and self.current_token()[1] != '}':
            stmt = self.parse_statement()
            body.add_child(stmt)

            if self.current_token() and self.current_token()[0] == 'SEPARATOR':
                self.eat('SEPARATOR')

        self.eat('OPERATOR', '}')

        node = ASTNode("WHILE")
        node.add_child(condition)
        node.add_child(body)

        return node

    # -------- STATEMENT --------
    def parse_statement(self):
        token = self.current_token()

        if not token:
            return None

        if token[0] == 'KEYWORD' and token[1] == 'int':
            return self.parse_declaration()

        elif token[0] == 'KEYWORD' and token[1] == 'if':
            return self.parse_if()

        elif token[0] == 'KEYWORD' and token[1] == 'while':
            return self.parse_while()

        elif token[0] == 'KEYWORD' and token[1] == 'return':
            return self.parse_return()

        else:
            return self.parse_expression()

    # -------- MAIN PARSER --------
    def parse(self):
        try:
            trees = []

            while self.current_token() is not None:
                stmt = self.parse_statement()
                trees.append(stmt)

                if self.current_token() and self.current_token()[0] == 'SEPARATOR':
                    self.eat('SEPARATOR')

            return trees

        except Exception as e:
            return str(e)