import tkinter as tk
from tkinter import ttk
from lexer.lexical_analyzer import lexer
from myparser.parser import Parser
from semantic.semantic_analyzer import SemanticAnalyzer
from intermediate.icg import IntermediateCodeGenerator
from codegen.code_generator import CodeGenerator


def start_gui():
    root = tk.Tk()
    root.title("Mini Compiler IDE")
    root.geometry("1000x650")
    root.configure(bg="#1e1e1e")

    # -------- STYLE --------
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#2d2d2d",
                    foreground="white",
                    fieldbackground="#2d2d2d",
                    rowheight=25)

    style.configure("Treeview.Heading",
                    background="#444",
                    foreground="white")

    # -------- MAIN FRAME --------
    main_frame = tk.Frame(root, bg="#1e1e1e")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # -------- LEFT: CODE EDITOR --------
    left_frame = tk.Frame(main_frame, bg="#1e1e1e")
    left_frame.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(left_frame, text="Code Editor",
             bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).pack(anchor="w")

    input_text = tk.Text(left_frame, bg="#252526", fg="white",
                         insertbackground="white", font=("Consolas", 11))
    input_text.pack(fill="both", expand=True, pady=5)

    # -------- RIGHT PANEL --------
    right_frame = tk.Frame(main_frame, bg="#1e1e1e")
    right_frame.pack(side="right", fill="both", expand=True, padx=5)

    # -------- TOKEN TABLE --------
    tk.Label(right_frame, text="Tokens",
             bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).pack(anchor="w")

    tree = ttk.Treeview(right_frame, columns=("Type", "Value"), show="headings", height=8)
    tree.heading("Type", text="Token Type")
    tree.heading("Value", text="Token Value")
    tree.pack(fill="x", pady=5)

    # -------- OUTPUT --------
    tk.Label(right_frame, text="Output",
             bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).pack(anchor="w")

    output_text = tk.Text(right_frame, height=12,
                          bg="#1e1e1e", fg="white", font=("Consolas", 10))
    output_text.pack(fill="both", expand=True, pady=5)

    output_text.tag_config("error", foreground="red")
    output_text.tag_config("success", foreground="lightgreen")
    output_text.tag_config("info", foreground="cyan")

    # -------- AST DISPLAY --------
    def display_ast(node, indent=0):
        if node is None:
            return ""

        result = "  " * indent + f"{node.value}\n"

        if hasattr(node, "children"):
            for child in node.children:
                result += display_ast(child, indent + 1)

        return result

    # -------- RUN COMPILER (LEXER + PARSER) --------
    def run_compiler():
        try:
            code = input_text.get("1.0", "end-1c")
            tokens = lexer(code)

            # Clear table
            for row in tree.get_children():
                tree.delete(row)

            # Insert tokens
            for token in tokens:
                tree.insert("", "end", values=token)

            # Parsing
            parser = Parser(tokens)
            result = parser.parse()

            output_text.delete("1.0", tk.END)

            if isinstance(result, str):
                output_text.insert(tk.END, result, "error")
            else:
                output_text.insert(tk.END, "✅ Syntax Analysis Successful\n", "success")

        except Exception as e:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, str(e), "error")

    # -------- SHOW AST --------
    def show_ast():
        try:
            code = input_text.get("1.0", "end-1c")
            tokens = lexer(code)

            parser = Parser(tokens)
            trees = parser.parse()

            output_text.delete("1.0", tk.END)

            if isinstance(trees, str):
                output_text.insert(tk.END, trees, "error")

            elif not trees:
                output_text.insert(tk.END, "⚠️ No AST generated")

            else:
                output_text.insert(tk.END, "🌳 Abstract Syntax Tree:\n\n", "info")

                for t in trees:
                    if t:
                        output_text.insert(tk.END, display_ast(t))
                        output_text.insert(tk.END, "\n")

        except Exception as e:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, str(e), "error")

    # -------- FULL COMPILATION --------
    def full_compile():
        try:
            code = input_text.get("1.0", "end-1c")
            tokens = lexer(code)

            parser = Parser(tokens)
            ast = parser.parse()

            output_text.delete("1.0", tk.END)

            if isinstance(ast, str):
                output_text.insert(tk.END, ast, "error")
                return

            # -------- SEMANTIC --------
            semantic = SemanticAnalyzer()
            sem_result = semantic.analyze(ast)

            if isinstance(sem_result, list):
                output_text.insert(tk.END, "\n".join(sem_result), "error")
                return

            # -------- INTERMEDIATE CODE --------
            icg = IntermediateCodeGenerator()
            icg_code = icg.generate(ast)

            # -------- TARGET CODE --------
            codegen = CodeGenerator()
            assembly = codegen.generate(icg_code)

            # -------- DISPLAY --------
            output_text.insert(tk.END, "✅ Compilation Successful\n\n", "success")

            output_text.insert(tk.END, "🔹 Intermediate Code:\n", "info")
            for line in icg_code:
                output_text.insert(tk.END, line + "\n")

            output_text.insert(tk.END, "\n🔹 Target Code:\n", "info")
            for line in assembly:
                output_text.insert(tk.END, line + "\n")

        except Exception as e:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, str(e), "error")

    # -------- BUTTONS --------
    btn_frame = tk.Frame(root, bg="#1e1e1e")
    btn_frame.pack(fill="x", pady=5)

    def styled_button(text, command):
        return tk.Button(btn_frame, text=text, command=command,
                         bg="#0e639c", fg="white",
                         font=("Arial", 10, "bold"),
                         relief="flat", padx=10, pady=5)

    styled_button("Run Compiler", run_compiler).pack(side="left", padx=5)
    styled_button("Show AST", show_ast).pack(side="left", padx=5)
    styled_button("Full Compile", full_compile).pack(side="left", padx=5)

    root.mainloop()