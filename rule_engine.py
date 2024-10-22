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
        # Replace 'AND' with 'and' and 'OR' with 'or' for compatibility with Python's ast parsing
        rule_string = rule_string.replace("AND", "and").replace("OR", "or").replace("'", '"')
        
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
