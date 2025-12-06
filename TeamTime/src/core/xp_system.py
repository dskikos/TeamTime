from datetime import datetime
from database import XPRecord, db

class XPSystem:
    """Manages XP gaining and losing mechanics"""

    XP_PER_PRODUCTIVE_MINUTE = 20
    XP_LOSS_PER_DISTRACTING_MINUTE = 3

    def __init__(self):
        self.current_xp = self.load_current_xp()
        self.level = self.calculate_level(self.current_xp)

    def load_current_xp(self):
        """Load current XP from database"""
        with db.atomic():
            try:
                latest_record = XPRecord.select().order_by(XPRecord.timestamp.desc()).first()
                return latest_record.total_xp if latest_record else 0
            except:
                return 0

    def gain_xp(self, productive_minutes):
        """Gain XP for productive time"""
        xp_gained = int(productive_minutes * self.XP_PER_PRODUCTIVE_MINUTE)
        self.current_xp += xp_gained
        self.level = self.calculate_level(self.current_xp)
        self._save_xp_record(xp_gained, "productive_time")
        return xp_gained

    def lose_xp_distraction(self, distracting_minutes):
        """Lose XP for distracting time"""
        xp_lost = int(distracting_minutes * self.XP_LOSS_PER_DISTRACTING_MINUTE)
        self.current_xp = max(0, self.current_xp - xp_lost)
        self.level = self.calculate_level(self.current_xp)
        self._save_xp_record(-xp_lost, "distraction")
        return xp_lost

    def calculate_level(self, xp):
        """Calculate level based on XP (every 500 XP = 1 level)"""
        return max(1, xp // 500 + 1)

    def get_xp_for_next_level(self):
        """Get XP needed for next level"""
        next_level_xp = self.level * 500
        return next_level_xp - self.current_xp

    def _save_xp_record(self, xp_change, reason):
        """Save XP change to database"""
        with db.atomic():
            try:
                XPRecord.create(
                    xp_change=xp_change,
                    total_xp=self.current_xp,
                    reason=reason,
                    timestamp=datetime.now()
                )
            except:
                pass

    def get_stats(self):
        """Get XP stats"""
        return {
            'current_xp': self.current_xp,
            'level': self.level,
            'xp_to_next_level': self.get_xp_for_next_level()
        }
