from datetime import date
from database import DatabaseManager

class GoalManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def set_daily_goal(self, target_minutes, target_date=None):
        if target_date is None:
            target_date = date.today()
        return self.db_manager.set_goal(target_minutes, target_date)

    def get_daily_goal(self, target_date=None):
        if target_date is None:
            target_date = date.today()
        return self.db_manager.get_goal(target_date)

    def is_goal_met(self, target_date=None):
        if target_date is None:
            target_date = date.today()

        goal = self.db_manager.get_goal(target_date)
        if not goal:
            return False

        progress = self.db_manager.get_progress(target_date)
        if not progress:
            return False

        return progress.productive_minutes >= goal.target_minutes

    def mark_goal_completed(self, target_date=None):
        if target_date is None:
            target_date = date.today()

        goal = self.db_manager.get_goal(target_date)
        if goal:
            self.db_manager.connect()
            goal.completed = True
            goal.save()
            self.db_manager.close()
