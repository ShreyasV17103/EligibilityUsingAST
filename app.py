from flask import Flask, render_template, request, jsonify
import ast
import json

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    rule_string = request.form['rule']
    try:
        engine = RuleEngine()
        rule_ast = engine.create_rule(rule_string)

        # Load JSON data
        with open('sampledata.json', 'r') as f:
            data_list = json.load(f)
        
        results = []
        for data in data_list:
            result = evaluate_rule(rule_ast, data)
            results.append({'data': data, 'result': result})
        
        return jsonify({'status': 'success', 'results': results})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
