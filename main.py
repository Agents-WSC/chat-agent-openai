# === openai-basic-conversational-agent ===
# A basic LLM-powered conversational agent using OpenAI's GPT API.
# Now configured to load settings from config.yaml

import openai
import yaml

# === LOAD CONFIGURATION ===
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

api_key = config["openai"]["api_key"]
model = config["openai"].get("model", "gpt-4")
system_prompt_text = config["agent"]["system_prompt"]
memory_limit = config["agent"].get("memory_limit", 50)

# === MEMORY MODULE ===
# Holds the conversation history and trims it when needed
conversation_history = []

# === AGENT CONTROLLER ===
# Manages interaction flow and message construction
def call_agent(user_input):
    global conversation_history

    openai.api_key = api_key
    conversation_history.append({"role": "user", "content": user_input})

    # Trim memory if it exceeds the defined limit
    if len(conversation_history) > memory_limit:
        conversation_history = conversation_history[-memory_limit:]

    system_prompt = {"role": "system", "content": system_prompt_text}
    messages = [system_prompt] + conversation_history

    # === REASONING CORE ===
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    content = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": content})
    return content

# === INTERFACE LAYER ===
# Simple CLI interface for chatting
if __name__ == "__main__":
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = call_agent(user_input)
        print("Agent:", response)
