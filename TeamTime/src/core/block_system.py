import platform
import subprocess
from datetime import datetime, timedelta
from database import BlockRecord, db

class BlockSystem:
    """Manages website/app blocking with firewall integration"""

    def __init__(self, xp_system):
        self.xp_system = xp_system
        self.blocked_sites = []
        self.block_limit_minutes = 120  # Block after 2 hours of distracting time
        self.is_blocked = False

    def check_and_activate_block(self, distracting_minutes):
        """Check if block should be activated based on distracting time"""
        if distracting_minutes >= self.block_limit_minutes and not self.is_blocked:
            self.activate_block()
            return True
        return False

    def activate_block(self):
        """Activate blocking (firewall rules)"""
        self.is_blocked = True
        self.blocked_sites = [
            'instagram.com',
            'facebook.com',
            'twitter.com',
            'tiktok.com',
            'youtube.com',
            'reddit.com',
            'twitch.tv'
        ]

        # Apply firewall rules (Windows only for now)
        if platform.system() == 'Windows':
            self._block_sites_windows()

        self._save_block_record("activate", "limit_reached")

    def deactivate_block(self):
        """Deactivate blocking"""
        if self.is_blocked:
            if platform.system() == 'Windows':
                self._unblock_sites_windows()

            self.is_blocked = False
            self.blocked_sites = []
            self._save_block_record("deactivate", "manual")

    def emergency_unlock(self):
        """Emergency unlock with XP penalty"""
        if self.is_blocked:
            xp_lost = self.xp_system.lose_xp_emergency_unlock()
            self.deactivate_block()
            self._save_block_record("emergency_unlock", f"xp_penalty_{xp_lost}")
            return xp_lost
        return 0

    def _block_sites_windows(self):
        """Add firewall rules to block sites on Windows"""
        for site in self.blocked_sites:
            try:
                # Block outbound traffic to the site
                cmd = f'netsh advfirewall firewall add rule name="TeamTime_Block_{site}" dir=out action=block remoteip={site}'
                subprocess.run(cmd, shell=True, capture_output=True, check=False)
            except Exception as e:
                print(f"Failed to block {site}: {e}")

    def _unblock_sites_windows(self):
        """Remove firewall rules on Windows"""
        for site in self.blocked_sites:
            try:
                cmd = f'netsh advfirewall firewall delete rule name="TeamTime_Block_{site}"'
                subprocess.run(cmd, shell=True, capture_output=True, check=False)
            except Exception as e:
                print(f"Failed to unblock {site}: {e}")

    def _save_block_record(self, action, reason):
        """Save block action to database"""
        with db.atomic():
            try:
                BlockRecord.create(
                    action=action,
                    reason=reason,
                    blocked_sites=','.join(self.blocked_sites),
                    timestamp=datetime.now()
                )
            except:
                pass

    def get_status(self):
        """Get current block status"""
        return {
            'is_blocked': self.is_blocked,
            'blocked_sites': self.blocked_sites,
            'limit_minutes': self.block_limit_minutes
        }
