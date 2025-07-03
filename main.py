import yaml
import openai
import re
import json
from memory import Memory
from tools import handle_action

# === LOAD CONFIGURATION ===
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

api_key = config["openai"]["api_key"]
model = config["openai"].get("model", "gpt-3.5-turbo")
system_prompt_path = config["agent"]["system_prompt_path"]
memory_limit = config["agent"].get("memory_limit", 50)

# === LOAD SYSTEM PROMPT ===
with open(system_prompt_path, "r", encoding="utf-8") as f:
    system_prompt_text = f.read()

# === SETUP OPENAI CLIENT ===
client = openai.OpenAI(api_key=api_key)

# === INITIALIZE MEMORY MODULE ===
memory = Memory(limit=memory_limit)


# === FORMAT PARSING ===
def parse_reasoning_block(text):
    result = {"thought": None, "action": None, "observation": None, "final_answer": None}
    for key in result.keys():
        match = re.search(rf"{key.replace('_', ' ').capitalize()}: ?(.*)", text, re.IGNORECASE)
        if match:
            result[key] = match.group(1).strip()
    return result


# === AGENT CONTROLLER ===
def call_agent(user_input):
    memory.append("user", user_input)
    messages = memory.get_messages(system_prompt_text)

    # Step 1: Get initial reasoning + action
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    content = response.choices[0].message.content
    parsed = parse_reasoning_block(content)

    # Step 2: Save reasoning block (initial)
    reasoning_block = {
        "thought": parsed.get("thought"),
        "action": parsed.get("action"),
        "observation": parsed.get("observation"),
    }
    memory.append("assistant", reasoning_block, type="reasoning")

    # Step 3: Execute tool if action is provided
    if parsed["action"] and parsed["action"].lower() != "none":
        result = handle_action(parsed["action"])

        if result.get("error"):
            parsed["observation"] = f"Tool execution failed: {result['error']}"
        else:
            parsed["observation"] = result["result"]

        # Update reasoning with new observation
        memory.append("assistant", {
            "thought": parsed.get("thought"),
            "action": parsed.get("action"),
            "observation": parsed.get("observation"),
        }, type="reasoning")

        # Step 4: Follow-up message with observation
        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": f"Observation: {parsed['observation']}"})

        follow_up = client.chat.completions.create(
            model=model,
            messages=messages
        )
        content = follow_up.choices[0].message.content
        parsed = parse_reasoning_block(content)

    # Step 5: Fallback strategy for Final Answer
    final = parsed.get("final_answer")
    if not final and parsed.get("action", "").lower() == "none":
        if "Final Answer:" in content:
            final = content.split("Final Answer:")[-1].strip()
        else:
            final = content.strip()

    final_output = {"final_answer": final or "⚠️ No final answer provided."}
    memory.append("assistant", final_output, type="final")
    return final_output["final_answer"]


# === INTERFACE LAYER ===
if __name__ == "__main__":
    print("Type 'exit' or 'reset' to end or restart the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "reset":
            memory.reset()
            print("🔄 Memory reset.\n")
            continue

        response = call_agent(user_input)
        print("Agent:", response + "\n")