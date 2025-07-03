import yaml
import openai
import re
from memory import Memory
from tools import handle_action  # 👈 Ahora importamos herramientas externas

# === LOAD CONFIGURATION ===
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

api_key = config["openai"]["api_key"]
model = config["openai"].get("model", "gpt-3.5-turbo")
system_prompt_text = config["agent"]["system_prompt"]
memory_limit = config["agent"].get("memory_limit", 50)

# === SETUP OPENAI CLIENT ===
client = openai.OpenAI(api_key=api_key)

# === INITIALIZE MEMORY MODULE ===
memory = Memory(limit=memory_limit)

# === AGENT CONTROLLER ===
def call_agent(user_input):
    memory.append("user", user_input, type="message")
    messages = memory.get_messages(system_prompt_text)

    # Step 1: Get initial response with reasoning
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    content = response.choices[0].message.content

    # Step 2: Detect if there is an Action
    match = re.search(r'Action:\s*(.*)', content)
    observation = "none"

    if match:
        action = match.group(1).strip()
        if action.lower() != "none":
            observation = handle_action(action)

            # Step 3: Build second message with observation
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": f"Observation: {observation}"})

            # Save the reasoning step separately
            memory.append("assistant", content, type="reasoning")

            follow_up = client.chat.completions.create(
                model=model,
                messages=messages
            )
            content = follow_up.choices[0].message.content

    # Save final answer
    memory.append("assistant", content, type="final")
    return content

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
        print("Agent:\n" + response + "\n")