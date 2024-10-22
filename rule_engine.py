import ast
import json

class ASTNode:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # 'operator' or 'operand'
        self.value = value  # Value for operand node, e.g. age > 30
        self.left = left  # Left child (another ASTNode)
        self.right = right  # Right child (another ASTNode)

    def __repr__(self):
        if self.type == "operand":
            return f"Operand({self.value})"
        return f"Operator({self.value}) with left={self.left} and right={self.right}"

class RuleEngine:
    VALID_ATTRIBUTES = {"age", "department", "salary", "experience"}
    
    def create_rule(self, rule_string):
        """Parse a rule string and return an ASTNode representing the rule with error handling."""
        try:
            expr = ast.parse(rule_string, mode='eval').body
            return self._build_ast(expr)
        except (SyntaxError, ValueError) as e:
            raise ValueError(f"Invalid rule format: {str(e)}")

    def _build_ast(self, expr):
        """Helper method to recursively build the ASTNode from the parsed expression."""
        if isinstance(expr, ast.BoolOp):  # AND/OR
            operator_type = "AND" if isinstance(expr.op, ast.And) else "OR"
            left = self._build_ast(expr.values[0])
            right = self._build_ast(expr.values[1])
            return ASTNode("operator", operator_type, left, right)

        elif isinstance(expr, ast.Compare):  # Operand (e.g., age > 30)
            if not isinstance(expr.left, ast.Name) or expr.left.id not in self.VALID_ATTRIBUTES:
                raise ValueError(f"Invalid attribute: {expr.left.id}")
            left = expr.left.id
            op = self._get_operator(expr.ops[0])
            right = expr.comparators[0].n if isinstance(expr.comparators[0], ast.Constant) else expr.comparators[0].id
            return ASTNode("operand", f"{left} {op} {right}")
    
    def _get_operator(self, op):
        """Map AST operator types to string representation."""
        if isinstance(op, ast.Gt):
            return ">"
        if isinstance(op, ast.Lt):
            return "<"
        if isinstance(op, ast.Eq):
            return "=="
        raise ValueError("Unsupported operator")

    def modify_rule(self, ast_node, new_operator=None, new_operand_value=None):
        """Modify existing ASTNode, allowing changes to operator or operand value."""
        if ast_node.type == "operand" and new_operand_value:
            attribute, operator, _ = ast_node.value.split()
            ast_node.value = f"{attribute} {operator} {new_operand_value}"
        if ast_node.type == "operator" and new_operator:
            ast_node.value = new_operator
        return ast_node

def combine_rules(rules):
    """Takes a list of rule ASTs and combines them with the most frequent operator (e.g., AND)."""
    if not rules:
        return None
    
    combined_ast = rules[0]
    for rule in rules[1:]:
        combined_ast = ASTNode("operator", "AND", combined_ast, rule)
    
    return combined_ast

def evaluate_rule(node, data):
    """Evaluates the ASTNode against user data to determine eligibility."""
    if node.type == "operand":
        return eval_operand(node.value, data)
    
    if node.type == "operator":
        if node.value == "AND":
            return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
        elif node.value == "OR":
            return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)

def eval_operand(operand, data):
    """Helper function to evaluate a condition operand (e.g., 'age > 30') against user data."""
    attribute, operator, value = operand.split()
    if value.isdigit():
        value = int(value)
    else:
        value = value.strip("'")
    
    if operator == ">":
        return data.get(attribute, 0) > value
    elif operator == "<":
        return data.get(attribute, 0) < value
    elif operator == "==":
        return data.get(attribute, '') == value
    else:
        raise ValueError(f"Unsupported operator in operand: {operator}")

def main():
    engine = RuleEngine()

    # Load the sample data from uploaded JSON file
    file_path = (r'C:\Users\vanam\Desktop\Zeotap\sampledata.json')
    try:
        with open(file_path, 'r') as f:
            data_list = json.load(f)
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return
    except json.JSONDecodeError:
        print("Invalid JSON format. Please check the file content.")
        return

    # Define sample rules
    rule1_string = "(age > 30 and department == 'Sales')"
    rule2_string = "(age < 25 or salary > 50000)"

    # Create ASTs for each rule
    try:
        rule1_ast = engine.create_rule(rule1_string)
        rule2_ast = engine.create_rule(rule2_string)
    except ValueError as e:
        print(e)
        return

    # Modify a rule (example)
    modified_rule1 = engine.modify_rule(rule1_ast, new_operator="OR")

    # Run evaluations on the loaded data
    print("\nTesting Rule 1: age > 30 OR department == 'Sales' (modified)")
    for idx, data in enumerate(data_list):
        result = evaluate_rule(modified_rule1, data)
        print(f"Test Case {idx+1}: {data} -> Result: {result}")

    print("\nTesting Rule 2: age < 25 or salary > 50000")
    for idx, data in enumerate(data_list):
        result = evaluate_rule(rule2_ast, data)
        print(f"Test Case {idx+1}: {data} -> Result: {result}")

if __name__ == "__main__":
    main()
