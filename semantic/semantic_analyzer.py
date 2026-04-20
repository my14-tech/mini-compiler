class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, ast_list):
        errors = []

        for node in ast_list:
            err = self.visit(node)
            if err:
                errors.append(err)

        return errors if errors else "Semantic Analysis Successful"

    # -------- VISITOR --------
    def visit(self, node):
        if node is None:
            return None

        if node.value == "DECLARATION":
            return self.handle_declaration(node)

        elif node.value == "=":
            return self.handle_assignment(node)

        elif node.value == "IF" or node.value == "WHILE":
            for child in node.children:
                err = self.visit(child)
                if err:
                    return err

        elif node.value == "FUNCTION":
            return self.handle_function(node)

        elif node.value == "RETURN":
            for child in node.children:
                err = self.visit(child)
                if err:
                    return err

        else:
            # Check identifiers usage
            if not node.children:
                if isinstance(node.value, str) and node.value.isalpha():
                    if node.value not in self.symbol_table:
                        return f"Semantic Error: Variable '{node.value}' not declared"

        for child in node.children:
            err = self.visit(child)
            if err:
                return err

        return None

    # -------- DECLARATION --------
    def handle_declaration(self, node):
        var_name = node.children[0].value

        if var_name in self.symbol_table:
            return f"Semantic Error: Variable '{var_name}' already declared"

        self.symbol_table[var_name] = "int"

        # Check assignment if exists
        if len(node.children) > 1:
            return self.visit(node.children[1])

    # -------- ASSIGNMENT --------
    def handle_assignment(self, node):
        var_name = node.children[0].value

        if var_name not in self.symbol_table:
            return f"Semantic Error: Variable '{var_name}' not declared"

        return self.visit(node.children[1])

    # -------- FUNCTION --------
    def handle_function(self, node):
        # Skip function name, params are allowed
        for child in node.children:
            err = self.visit(child)
            if err:
                return err