import sys
import os

module_path = os.path.join(os.path.dirname(__file__), '../module')
sys.path.append(module_path)

import re

def solve_math_expression(expression):
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return f"The result is: {result}"
    except Exception as e:
        return f"Could not calculate the expression: {e}"

def is_math_expression(question):
    math_pattern = re.compile(r'^[\d+\-*/().\s]+$')
    return bool(math_pattern.match(question))