import json
import os
from pathlib import Path

class Categorizer:
    def __init__(self, config_path=None):
        if config_path is None:
            # Get the correct path relative to the project root
            base_dir = Path(__file__).resolve().parent.parent.parent
            config_path = base_dir / 'config' / 'categories.json'
        self.config_path = str(config_path)
        self.categories = self.load_categories()

    def load_categories(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                # Ensure manually_changed exists
                if "manually_changed" not in data:
                    data["manually_changed"] = []
                return data
        else:
            return {
                "productive": [],
                "distracting": [],
                "neutral": [],
                "manually_changed": []
            }

    def categorize(self, app_name, window_title=""):
        app_lower = app_name.lower() if app_name else ""
        title_lower = window_title.lower() if window_title else ""

        # FIRST: Check if this app was manually categorized - these have highest priority!
        manually_changed = self.categories.get("manually_changed", [])
        for manual_app in manually_changed:
            if manual_app.lower() == app_lower:
                # Find which category this manually changed app is in
                for category in ['productive', 'distracting', 'neutral']:
                    if manual_app in self.categories.get(category, []):
                        return category

        # Check if it's a browser
        is_browser = False
        for browser in self.categories.get("distracting_browsers", []):
            if browser.lower() in app_lower:
                is_browser = True
                break

        # If it's a browser, analyze the active tab (window title)
        if is_browser:
            # Extract domain/site from window title
            # Browser titles are usually: "Page Title - Site Name" or "Tab Title | Domain - Browser"
            # Examples:
            # "ChatGPT - Mozilla Firefox" -> need to check for "chatgpt" keyword
            # "Instagram - Brave" -> "instagram" is clear
            # "Pull Requests · user/repo - Mozilla Firefox" -> check for github patterns

            # Check for productive sites/apps in window title
            productive_sites = [
                'stackoverflow', 'github', 'gitlab', 'bitbucket',
                'docs', 'documentation', 'tutorial', 'learn',
                'developer', 'api', 'programming', 'code',
                'leetcode', 'hackerrank', 'codewars', 'geeksforgeeks',
                'mdn', 'w3schools', 'freecodecamp',
                'coursera', 'udemy', 'edx', 'khan academy', 'pluralsight',
                'chatgpt', 'claude', 'gemini', 'copilot',  # AI assistants for coding
                'jupyter', 'colab', 'kaggle', 'huggingface',
                'arxiv', 'scholar', 'researchgate', 'pubmed',  # Research
                'overleaf', 'latex',
                'jira', 'confluence', 'linear'  # Project management
            ]

            # Check for productive keywords/patterns
            productive_patterns = [
                'pull request', 'merge request', 'commit', 'issue',  # Git terms
                'documentation', 'api reference', 'tutorial',
                'stackoverflow.com', 'github.com', 'gitlab.com'
            ]

            for site in productive_sites:
                if site in title_lower:
                    return "productive"

            for pattern in productive_patterns:
                if pattern in title_lower:
                    return "productive"

            # Check for distracting sites in the window title (active tab)
            distracting_sites = [
                'instagram', 'facebook', 'twitter', 'x.com', 'tiktok',
                'reddit', 'youtube', 'twitch', 'netflix',
                'hulu', 'primevideo', 'disney', 'snapchat',
                'whatsapp', 'messenger', 'telegram',
                'pinterest', 'tumblr', '9gag', 'imgur',
                'spotify web', 'soundcloud',  # Music streaming in browser
                'amazon', 'ebay', 'shopping'  # Shopping sites
            ]

            # Distracting patterns
            distracting_patterns = [
                'watch', 'stream', 'gaming', 'meme',
                'feed', 'trending', 'for you'
            ]

            for site in distracting_sites:
                if site in title_lower:
                    return "distracting"

            for pattern in distracting_patterns:
                if pattern in title_lower:
                    return "distracting"

            # Check for neutral sites
            neutral_sites = [
                'gmail', 'outlook', 'mail', 'protonmail',
                'calendar', 'drive', 'dropbox', 'onedrive',
                'zoom', 'teams', 'slack', 'discord',
                'notion', 'trello', 'asana', 'monday',
                'wikipedia', 'news'
            ]

            for site in neutral_sites:
                if site in title_lower:
                    return "neutral"

            # Check browser name at the end to determine default
            # If the window title ends with browser name and nothing else useful detected,
            # it's probably a new tab or homepage -> neutral
            browser_names = ['firefox', 'chrome', 'safari', 'edge', 'brave', 'opera']
            for browser in browser_names:
                # If title is basically just "New Tab - Firefox" or similar
                if title_lower.startswith('new tab') or title_lower.startswith('start page'):
                    return "neutral"

            # If no specific site detected, default to neutral for browsers
            # (changed from distracting to be less aggressive)
            return "neutral"

        # Check productive apps/keywords
        for keyword in self.categories.get("productive", []):
            if keyword.lower() in app_lower or keyword.lower() in title_lower:
                return "productive"

        # Check distracting keywords
        for keyword in self.categories.get("distracting", []):
            if keyword.lower() in app_lower or keyword.lower() in title_lower:
                return "distracting"

        # Check neutral keywords
        for keyword in self.categories.get("neutral", []):
            if keyword.lower() in app_lower or keyword.lower() in title_lower:
                return "neutral"

        # Default to neutral for unknown applications
        return "neutral"

    def add_rule(self, category, keyword):
        if category in self.categories:
            # Remove keyword from ALL other categories first
            for cat in ['productive', 'distracting', 'neutral']:
                if cat != category and keyword in self.categories.get(cat, []):
                    self.categories[cat].remove(keyword)

            # Add to the new category
            if keyword not in self.categories[category]:
                self.categories[category].append(keyword)

            # Track that this was manually changed
            if "manually_changed" not in self.categories:
                self.categories["manually_changed"] = []
            if keyword not in self.categories["manually_changed"]:
                self.categories["manually_changed"].append(keyword)

            self.save_categories()
            self.reload_categories()

    def remove_rule(self, category, keyword):
        if category in self.categories:
            if keyword in self.categories[category]:
                self.categories[category].remove(keyword)
                self.save_categories()
                self.reload_categories()

    def save_categories(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.categories, f, indent=2)

    def reload_categories(self):
        self.categories = self.load_categories()
