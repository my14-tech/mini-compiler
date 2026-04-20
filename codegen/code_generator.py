class CodeGenerator:
    def generate(self, icg_code):
        assembly = []

        for line in icg_code:
            parts = line.split()

            if len(parts) == 3:  # a = b
                assembly.append(f"MOV {parts[0]}, {parts[2]}")

            elif len(parts) == 5:  # t1 = a + b
                dest = parts[0]
                op1 = parts[2]
                operator = parts[3]
                op2 = parts[4]

                if operator == '+':
                    assembly.append(f"ADD {dest}, {op1}, {op2}")
                elif operator == '-':
                    assembly.append(f"SUB {dest}, {op1}, {op2}")
                elif operator == '*':
                    assembly.append(f"MUL {dest}, {op1}, {op2}")
                elif operator == '/':
                    assembly.append(f"DIV {dest}, {op1}, {op2}")

            else:
                assembly.append(f"# {line}")

        return assembly