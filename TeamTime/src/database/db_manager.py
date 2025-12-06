from datetime import datetime, date
from .models import db, Activity, Goal, Progress

class DatabaseManager:
    def __init__(self):
        self.db = db

    def connect(self):
        if self.db.is_closed():
            self.db.connect()

    def close(self):
        if not self.db.is_closed():
            self.db.close()

    def add_activity(self, app_name, window_title, category=None, duration_seconds=0):
        self.connect()
        activity = Activity.create(
            app_name=app_name,
            window_title=window_title,
            category=category,
            duration_seconds=duration_seconds
        )
        self.close()
        return activity

    def get_activities_by_date(self, target_date=None):
        if target_date is None:
            target_date = date.today()

        self.connect()
        activities = Activity.select().where(
            Activity.timestamp >= datetime.combine(target_date, datetime.min.time()),
            Activity.timestamp < datetime.combine(target_date, datetime.max.time())
        )
        result = list(activities)
        self.close()
        return result

    def set_goal(self, target_minutes, target_date=None):
        if target_date is None:
            target_date = date.today()

        self.connect()
        goal, created = Goal.get_or_create(
            date=target_date,
            defaults={'target_minutes': target_minutes}
        )
        if not created:
            goal.target_minutes = target_minutes
            goal.save()
        self.close()
        return goal

    def get_goal(self, target_date=None):
        if target_date is None:
            target_date = date.today()

        self.connect()
        try:
            goal = Goal.get(Goal.date == target_date)
        except Goal.DoesNotExist:
            goal = None
        self.close()
        return goal

    def update_progress(self, productive_mins=0, distracting_mins=0, neutral_mins=0, target_date=None):
        if target_date is None:
            target_date = date.today()

        self.connect()
        progress, created = Progress.get_or_create(
            date=target_date,
            defaults={
                'productive_minutes': productive_mins,
                'distracting_minutes': distracting_mins,
                'neutral_minutes': neutral_mins
            }
        )
        if not created:
            progress.productive_minutes += productive_mins
            progress.distracting_minutes += distracting_mins
            progress.neutral_minutes += neutral_mins
            progress.save()
        self.close()
        return progress

    def get_progress(self, target_date=None):
        if target_date is None:
            target_date = date.today()

        self.connect()
        try:
            progress = Progress.get(Progress.date == target_date)
        except Progress.DoesNotExist:
            progress = Progress.create(date=target_date)
        self.close()
        return progress
