import time
import threading
from datetime import datetime
from monitor.window_tracker import WindowTracker
from monitor.categorizer import Categorizer
from database import DatabaseManager

class ActivityTracker:
    def __init__(self, interval=10):
        self.interval = interval
        self.running = False
        self.thread = None
        self.window_tracker = WindowTracker()
        self.categorizer = Categorizer()
        self.db_manager = DatabaseManager()
        self.last_activity = None
        self.last_timestamp = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._track_loop, daemon=True)
            self.thread.start()
            print("Activity tracking started")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("Activity tracking stopped")

    def _track_loop(self):
        while self.running:
            try:
                self._track_current_activity()
                time.sleep(self.interval)
            except Exception as e:
                print(f"Error in tracking loop: {e}")

    def _track_current_activity(self):
        window_title, app_name = self.window_tracker.get_active_window()

        if not app_name or not window_title:
            return

        category = self.categorizer.categorize(app_name, window_title)

        current_activity = {
            'app_name': app_name,
            'window_title': window_title,
            'category': category
        }

        current_time = datetime.now()

        if self.last_activity and self.last_activity == current_activity:
            duration = (current_time - self.last_timestamp).total_seconds()
            self.db_manager.add_activity(
                app_name=app_name,
                window_title=window_title,
                category=category,
                duration_seconds=int(duration)
            )

            duration_minutes = duration / 60
            if category == "productive":
                self.db_manager.update_progress(productive_mins=duration_minutes)
            elif category == "distracting":
                self.db_manager.update_progress(distracting_mins=duration_minutes)
            elif category == "neutral":
                self.db_manager.update_progress(neutral_mins=duration_minutes)
        else:
            self.db_manager.add_activity(
                app_name=app_name,
                window_title=window_title,
                category=category,
                duration_seconds=0
            )

        self.last_activity = current_activity
        self.last_timestamp = current_time

    def get_current_activity(self):
        window_title, app_name = self.window_tracker.get_active_window()
        if app_name and window_title:
            category = self.categorizer.categorize(app_name, window_title)
            return {
                'app_name': app_name,
                'window_title': window_title,
                'category': category
            }
        return None
