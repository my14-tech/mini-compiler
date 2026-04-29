📘 Mini Compiler with GUI
A Mini Compiler built in Python that demonstrates the complete compilation pipeline — from lexical analysis to target code generation — with an interactive GUI interface.

🚀 Overview
This project simulates how a real compiler works internally by breaking down the process into multiple phases:
Lexical Analysis (Tokenization)
Syntax Analysis (Parsing)
Abstract Syntax Tree (AST) Generation
Semantic Analysis (Scope & Error Checking)
Intermediate Code Generation (ICG)
Target Code Generation (Assembly-like)

The compiler is designed using a modular and pipeline-based architecture, where each phase works independently and passes its output to the next phase.

🖥️ GUI Features
📝 Code Editor for writing input programs
📊 Token Table for lexical output
🌳 AST Display for structural visualization
⚠️ Error Highlighting (Syntax & Semantic)

⚙️ Full Compilation (ICG + Target Code)

🧠 Compiler Phases Explained
🔹 1. Lexical Analysis
Breaks input code into tokens like:
Keywords (int, if, while)
Identifiers (a, sum)
Operators (+, -, =)
Numbers (5, 10)

🔹 2. Syntax Analysis
Uses a Recursive Descent Parser (LL parser)
Validates grammar rules
Generates an Abstract Syntax Tree (AST)

🌳 3. Abstract Syntax Tree (AST)
Tree representation of the program
Each node represents operations or constructs
Helps simplify further phases

🔹 4. Semantic Analysis
Detects:
Undeclared variables
Redeclarations
Scope errors
Uses a stack-based symbol table

🔹 5. Intermediate Code Generation
Converts AST into three-address code
Example:
t1 = a + bsum = t1

🔹 6. Target Code Generation
Converts intermediate code into assembly-like instructions
Example:
ADD t1, a, bMOV sum, t1

🏗️ Project Structure
compiler-project/│├── lexer/│   └── lexical_analyzer.py│├── myparser/│   └── parser.py│├── semantic/│   └── semantic_analyzer.py│├── intermediate/│   └── icg.py│├── codegen/│   └── code_generator.py│├── gui/│   └── gui.py│└── main.py

⚙️ Technologies Used
Python 🐍
Tkinter (GUI)
Regular Expressions (Lexical Analysis)
Recursive Descent Parsing

▶️ How to Run

Clone the repository:
git clone https://github.com/my14-teach/mini-compiler.git

Navigate to project:
cd mini-compiler

Run the project:
python main.py

🧪 Sample Input
int a = 5;
int b = 10;
int sum = a + b;
if (sum > 10) {    
    int result = sum * 2;
}
while (a < b) {
  a = a + 1;
}
return sum;

⚡ Key Features
Modular Compiler Design
Interactive GUI
AST Visualization
Scope-Based Semantic Analysis
Intermediate & Target Code Generation

⚠️ Limitations
Supports a simplified language (subset of C)
No optimization phase yet
Limited data types

🚀 Future Enhancements
Code optimization phase
Support for more data types
Function call handling
Better assembly generation
Error line tracking

📌 Learning Outcomes
Understanding compiler design concepts
Implementation of parsing techniques
Handling scope using symbol tables
Building GUI-based tools

👩‍💻 Author
Nimisha Chawla
B.Tech (Computer Science)
