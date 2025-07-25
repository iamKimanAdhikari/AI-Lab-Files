from itertools import product

def extract_var(expr):
    keywords = {"and", "or", "not", "True", "False"}
    spaced_symbols = ["(", ")", "⇒", "→", "↔", "<=>"]
    
    for symbol in spaced_symbols:
        expr = expr.replace(symbol, " ")
    tokens = expr.split()
    variables = []

    for token in tokens:
        if token.isalpha() and token not in keywords and token not in variables:
            variables.append(token)
    return sorted(variables)

def process(expr):
    expr = expr.replace("¬", "not ")
    expr = expr.replace("∧", "and")
    expr = expr.replace("∨", "or")
    expr = expr.replace("→", "=>").replace("⇒", "=>")
    expr = expr.replace("↔", "<=>")

    expr = expr.replace("<=>", " <=> ")  
    expr = expr.replace("=>", " => ")

    tokens = expr.split()
    while "=>" in tokens:
        idx = tokens.index("=>")
        left = tokens[idx - 1]
        right = tokens[idx + 1]
        tokens[idx - 1:idx + 2] = [f"(not {left} or {right})"]
    while "<=>" in tokens:
        idx = tokens.index("<=>")
        left = tokens[idx - 1]
        right = tokens[idx + 1]
        tokens[idx - 1:idx + 2] = [f"(({left} and {right}) or (not {left} and not {right}))"]
    return " ".join(tokens)

def evaluate(expr, values):
    for var in values:
        expr = expr.replace(var, str(values[var]))
    try:
        return eval(expr)
    except:
        return "Error"
    
def generate_truth_table(expr):
    original_expr = expr
    processed_expr = process(original_expr)
    variables = extract_var(original_expr)

    if not variables:
        print("No variables found in the expression.")
        try:
            result = eval(processed_expr)
            print(f"Result: {result}")
        except:
            print("Error evaluating expression.")
        return

    col_widths = [max(len(var), 5) for var in variables]
    result_col_width = len("Result")

    header_parts = [f"{var:<{col_widths[i]}}" for i, var in enumerate(variables)]
    header = " | ".join(header_parts) + f" | {'Result':<{result_col_width}}"
    
    separator_parts = ["-" * width for width in col_widths]
    separator = "-|-".join(separator_parts) + f"-|-{'-' * result_col_width}"

    print("\nTruth Table:")
    print(header)
    print(separator)

    for combo in product([False, True], repeat=len(variables)):
        values = dict(zip(variables, combo))
        result = evaluate(processed_expr, values)
        
        row_parts = [f"{str(values[v]):<{col_widths[i]}}" for i, v in enumerate(variables)]
        row = " | ".join(row_parts) + f" | {str(result):<{result_col_width}}"
        print(row)

def main():
    print("Enter a logical expression using: and, or, not, parentheses")
    print("Example: (A and B) or not C\n")

    user_expr = input("Your expression: ")

    generate_truth_table(user_expr)

if __name__== "__main__":
    main()