from flask import Flask, render_template, request, jsonify
import json
from rule_engine import RuleEngine, evaluate_rule

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    rule_string = data.get('rule')
    user_data = data.get('data')

    engine = RuleEngine()
    try:
        rule_ast = engine.create_rule(rule_string)
        result = evaluate_rule(rule_ast, user_data)
        return jsonify({"status": "success", "result": result})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
