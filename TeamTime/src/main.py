import sys
import os

# Add parent directory to path to fix imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from database import initialize_database
from ui import Dashboard
from ui.splash_screen import CircularSplashScreen
from core import Config

def main():
    app = QApplication(sys.argv)

    # Show splash screen
    splash = CircularSplashScreen()

    # Initialize in background
    def initialize():
        Config.ensure_directories()
        initialize_database()

    # Run initialization
    initialize()

    # Create dashboard
    dashboard = Dashboard()

    # Close splash and show dashboard after 2 seconds
    QTimer.singleShot(2000, lambda: splash.finish_animation(dashboard))

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
