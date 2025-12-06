import json
import os
from anthropic import Anthropic

class Categorizer:
    def __init__(self, config_path='config/categories.json', use_llm=False):
        self.config_path = config_path
        self.categories = self.load_categories()
        self.use_llm = use_llm
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY")) if use_llm else None
        self.cache = {}

    def load_categories(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "productive": [],
                "distracting": [],
                "neutral": []
            }

    def categorize(self, app_name, window_title=""):
        app_lower = app_name.lower() if app_name else ""
        title_lower = window_title.lower() if window_title else ""

        for keyword in self.categories.get("productive", []):
            if keyword.lower() in app_lower or keyword.lower() in title_lower:
                return "productive"

        for keyword in self.categories.get("distracting", []):
            if keyword.lower() in app_lower or keyword.lower() in title_lower:
                return "distracting"

        for keyword in self.categories.get("neutral", []):
            if keyword.lower() in app_lower or keyword.lower() in title_lower:
                return "neutral"

        if self.use_llm and self.client:
            return self._categorize_with_llm(app_name, window_title)

        return "neutral"

    def _categorize_with_llm(self, app_name, window_title):
        cache_key = f"{app_name}:{window_title[:50]}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=50,
                messages=[{
                    "role": "user",
                    "content": f"Categorize this activity as 'productive', 'distracting', or 'neutral':\nApp: {app_name}\nWindow: {window_title}\n\nRespond with ONLY one word: productive, distracting, or neutral."
                }]
            )

            category = message.content[0].text.strip().lower()
            if category in ['productive', 'distracting', 'neutral']:
                self.cache[cache_key] = category
                return category
        except Exception as e:
            print(f"LLM categorization error: {e}")

        return "neutral"

    def add_rule(self, category, keyword):
        if category in self.categories:
            if keyword not in self.categories[category]:
                self.categories[category].append(keyword)
                self.save_categories()

    def remove_rule(self, category, keyword):
        if category in self.categories:
            if keyword in self.categories[category]:
                self.categories[category].remove(keyword)
                self.save_categories()

    def save_categories(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.categories, f, indent=2)
