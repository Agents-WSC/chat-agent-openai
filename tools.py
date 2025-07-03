import re

# === TOOL FUNCTIONS ===

def calculator(expression: str) -> str:
    """Evaluate basic math expressions like 2 * (3 + 4)."""
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {str(e)}"

# === TOOL REGISTRY ===

TOOLS = {
    "calculator": calculator,
}

# === ACTION HANDLER ===

def handle_action(action_str: str) -> str:
    """
    Extract the tool name and argument from the action string
    and execute the corresponding function.
    Example: action_str = "calculator(2 * (3 + 4))"
    """
    for name, func in TOOLS.items():
        if action_str.startswith(f"{name}("):
            match = re.search(rf'{name}\((.*)\)', action_str)
            if match:
                argument = match.group(1)
                return func(argument)
    return "Tool not implemented."
    