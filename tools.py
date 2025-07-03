import re

# === TOOL FUNCTIONS ===

def calculator(expression: str) -> dict:
    """
    Evaluate basic math expressions like 2 * (3 + 4).

    Returns:
        dict: {"result": str, "error": str or None}
    """
    try:
        result = str(eval(expression, {"__builtins__": {}}))
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}

# === TOOL REGISTRY ===

TOOLS = {
    "calculator": calculator,
}

# === ACTION HANDLER ===

def handle_action(action_str: str) -> dict:
    """
    Parse the action string and invoke the appropriate tool.

    Returns:
        dict: {"result": str or None, "error": str or None}
    """
    try:
        if "calculator(" in action_str:
            expr = re.search(r'calculator\((.*)\)', action_str)
            if expr:
                return calculator(expr.group(1))
        return {"result": "Tool not implemented.", "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}
