import sys
import os

# Add parent directory to path to fix imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from database import initialize_database
from ui import Dashboard
from core import Config

def main():
    Config.ensure_directories()

    initialize_database()

    app = QApplication(sys.argv)

    dashboard = Dashboard()
    dashboard.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
