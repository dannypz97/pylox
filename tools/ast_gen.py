import sys

DEFAULT_OUTPUT_DIR = "../nodes"


def define_ast(output_dir, base_name, type_meta):
    path = f"{output_dir}/{base_name.lower()}.py"

    with open(path, 'w') as f:
        f.write("from dataclasses import dataclass\n")
        f.write("\n")
        f.write("from lox_token import Token\n")
        f.write("\n\n")
        f.write(f"class {base_name}:\n")
        f.write(f"    def accept(self, visitor):\n")
        f.write("        raise Exception('Not Implemented')")
        f.write("\n\n")

        for class_name, fields_descs in type_meta.items():
            f.write("\n")
            f.write(f"@dataclass\n")
            f.write(f"class {class_name}({base_name}):\n")

            for desc in fields_descs:
                f.write(f"    {desc}\n")

            f.write("\n")

            f.write("    def accept(self, visitor):\n")
            f.write(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)")
            f.write("\n\n")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("Usage: generate_ast [<output directory>]")
        sys.exit(1)

    if len(sys.argv) == 2:
        op_dir = sys.argv[1]
    else:
        op_dir = DEFAULT_OUTPUT_DIR

    define_ast(op_dir, "Expr", {
        "Binary": ["left: Expr", "operator: Token", "right: Expr"],
        "Grouping": ["expression: Expr"],
        "Literal": ["value: object"],
        "Unary": ["operator: Token", "right: Expr"]
    })
