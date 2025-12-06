import json
import os

class Categorizer:
    def __init__(self, config_path='config/categories.json'):
        self.config_path = config_path
        self.categories = self.load_categories()

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
