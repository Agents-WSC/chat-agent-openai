import json
import os

class Memory:
    def __init__(self, filename="memory.json", limit=50):
        self.filename = filename
        self.limit = limit
        self.history = self._load()

    # === LOADING & SAVING ===

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def _trim(self):
        if len(self.history) > self.limit:
            self.history = self.history[-self.limit:]

    # === PUBLIC API ===

    def append(self, role: str, content, type: str = "message"):
        """
        Append a new entry to the memory.

        Args:
            role (str): 'user' or 'assistant'
            content (str or dict): plain text or structured block
            type (str): 'message', 'reasoning', or 'final'
        """
        self.history.append({
            "role": role,
            "type": type,
            "content": content
        })
        self._trim()
        self._save()

    def get_messages(self, system_prompt: str):
        """
        Build the list of messages to send to the LLM.

        Args:
            system_prompt (str): initial system instruction

        Returns:
            list[dict]: formatted message history for LLM input
        """
        messages = [{"role": "system", "content": system_prompt}]
        for item in self.history:
            if item["type"] in ["message", "final"]:
                content = item["content"]
                if isinstance(content, dict):
                    content = content.get("final_answer", "")
                messages.append({
                    "role": item["role"],
                    "content": content
                })
        return messages

    def reset(self):
        """
        Clear the memory history and save an empty state.
        """
        self.history = []
        self._save()