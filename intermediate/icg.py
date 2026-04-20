class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, ast_list):
        self.code = []

        for node in ast_list:
            self.visit(node)

        return self.code

    def visit(self, node):
        if node is None:
            return None

        # Assignment
        if node.value == "=":
            left = node.children[0].value
            right = self.visit(node.children[1])
            self.code.append(f"{left} = {right}")
            return left

        # Operators
        elif node.value in ['+', '-', '*', '/']:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])

            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node.value} {right}")
            return temp

        # Control structures
        elif node.value == "IF":
            self.code.append("IF CONDITION")
            for child in node.children:
                self.visit(child)

        elif node.value == "WHILE":
            self.code.append("WHILE LOOP")
            for child in node.children:
                self.visit(child)

        # Leaf node
        else:
            return node.value