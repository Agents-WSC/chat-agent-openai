import json
import os

class Memory:
    def __init__(self, filename="memory.json", limit=50):
        self.filename = filename
        self.limit = limit
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.filename, "w") as f:
            json.dump(self.history, f, indent=2)

    def _trim(self):
        if len(self.history) > self.limit:
            self.history = self.history[-self.limit:]

    def append(self, role, content, type="message"):
        self.history.append({
            "role": role,
            "type": type,
            "content": content
        })
        self._trim()
        self._save()

    def get_messages(self, system_prompt):
        messages = [{"role": "system", "content": system_prompt}]
        for item in self.history:
            if item["type"] in ["message", "final"]:
                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })
        return messages

    def reset(self):
        self.history = []
        self._save()
