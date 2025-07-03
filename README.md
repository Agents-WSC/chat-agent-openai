# 🧠 Chat Agent with OpenAI

A minimal yet extensible OpenAI-powered reasoning agent built in pure Python. This project demonstrates how to structure an LLM-based agent that reasons step-by-step, optionally uses tools, and stores its reasoning trace and final outputs in memory.

---

## 📂 Project Structure

```
reasoning-agent/
├── main.py               # Main CLI loop
├── memory.py             # Memory management module
├── tools.py              # Tool definitions and tool dispatch logic
├── config.yaml           # Configuration file (API keys, model settings, etc.)
├── system_prompt.txt     # Base system instructions for the agent
├── memory.json           # Conversation history and reasoning traces (auto-saved)
└── README.md             # Documentation
```

---

## 🤖 What It Does

- Accepts user queries in natural language.
- Follows a strict reasoning format (Thought → Action → Observation → Final Answer).
- Uses basic tools (e.g., calculator) as needed.
- Logs everything to a persistent memory file.
- Returns only the final answer in the interface, while storing full reasoning in background.

---

## 🛠 Features

| Feature         | Description |
|----------------|-------------|
| 🧠 Reasoning Trace | Logs structured reasoning steps (thoughts, actions, observations). |
| 🛠 Tool Usage     | Dynamically calls Python functions (e.g. calculator) via pattern parsing. |
| 💾 Persistent Memory | Stores the entire conversation and reasoning in a local JSON file. |
| 🧹 Resettable | Use `reset` command in CLI to clear memory. |

---

## 🧭 Prompt Format (ReAct Style)

The system prompt instructs the agent to reason step-by-step, decide whether to take an action, then output the final answer.

Example:
```
Thought: I need to calculate a simple math expression.
Action: calculator(3 + 3)
Observation: 6
Final Answer: The result is 6.
```

---

## 🔧 Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/reasoning-agent
   cd reasoning-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `config.yaml`:
   ```yaml
   openai:
     api_key: "sk-..."
     model: "gpt-4o"
   agent:
     system_prompt_path: system_prompt.txt
     memory_limit: 100
   ```

4. Run the agent:
   ```bash
   python main.py
   ```

---

## ⚠️ Why We Didn't Use LangChain

While LangChain offers powerful abstractions for LLM applications, this project intentionally avoids it for the following reasons:

- 🧱 **Transparency & Pedagogy**: We wanted full visibility into every part of the agent’s logic—memory, parsing, tool dispatching.
- 🪶 **Lightweight**: For simple ReAct-style agents, LangChain adds unnecessary complexity and overhead.
- 🔧 **Customization**: We needed complete control over the memory structure (e.g., storing reasoning and answers separately).

LangChain is a fantastic tool for production-grade pipelines and multi-agent orchestration—but this project focuses on learning, minimalism, and hackability.

---

## ✅ Future Improvements

- ✨ Add support for more tools
- 🧠 Replace keyword-based tool invocation with structured function calling
- 📚 Integrate vector memory or retrieval augmentation (RAG)

---

## 🧑‍💻 License

MIT License.