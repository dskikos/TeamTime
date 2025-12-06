from datetime import date
from database import DatabaseManager

class ProgressCalculator:
    def __init__(self, penalty_factor=0.5):
        self.db_manager = DatabaseManager()
        self.penalty_factor = penalty_factor

    def calculate_progress(self, target_date=None):
        if target_date is None:
            target_date = date.today()

        progress = self.db_manager.get_progress(target_date)
        goal = self.db_manager.get_goal(target_date)

        if not goal:
            return {
                'percentage': 0,
                'productive_minutes': 0,
                'distracting_minutes': 0,
                'neutral_minutes': 0,
                'target_minutes': 0,
                'effective_minutes': 0
            }

        productive_mins = progress.productive_minutes if progress else 0
        distracting_mins = progress.distracting_minutes if progress else 0
        neutral_mins = progress.neutral_minutes if progress else 0

        effective_minutes = productive_mins - (distracting_mins * self.penalty_factor)
        effective_minutes = max(0, effective_minutes)

        percentage = (effective_minutes / goal.target_minutes) * 100
        percentage = max(0, min(100, percentage))

        return {
            'percentage': round(percentage, 2),
            'productive_minutes': round(productive_mins, 2),
            'distracting_minutes': round(distracting_mins, 2),
            'neutral_minutes': round(neutral_mins, 2),
            'target_minutes': goal.target_minutes,
            'effective_minutes': round(effective_minutes, 2)
        }

    def get_time_remaining(self, target_date=None):
        if target_date is None:
            target_date = date.today()

        progress_data = self.calculate_progress(target_date)
        remaining = progress_data['target_minutes'] - progress_data['effective_minutes']
        return max(0, remaining)

    def get_summary(self, target_date=None):
        if target_date is None:
            target_date = date.today()

        progress_data = self.calculate_progress(target_date)
        time_remaining = self.get_time_remaining(target_date)

        return {
            **progress_data,
            'time_remaining': round(time_remaining, 2),
            'is_complete': progress_data['percentage'] >= 100
        }
