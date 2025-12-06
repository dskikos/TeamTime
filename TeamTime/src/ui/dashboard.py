import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QInputDialog, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import QTimer
from ui.components import ProgressBarWidget, ActivityDisplay, StatsPanel
from ui.history_window import HistoryWindow
from monitor import ActivityTracker
from core import GoalManager, ProgressCalculator, Config

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.activity_tracker = ActivityTracker(interval=Config.TRACKING_INTERVAL)
        self.goal_manager = GoalManager()
        self.progress_calculator = ProgressCalculator()

        self.init_ui()
        self.setup_timer()

        self.check_goal()

    def init_ui(self):
        self.setWindowTitle("TeamTime - Productivity Tracker")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #0d0d0d; color: #ffffff;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.activity_display = ActivityDisplay()
        layout.addWidget(self.activity_display)

        self.stats_panel = StatsPanel()
        layout.addWidget(self.stats_panel)

        button_layout = QHBoxLayout()

        self.track_button = QPushButton("Start Tracking")
        self.track_button.clicked.connect(self.toggle_tracking)
        self.track_button.setStyleSheet("padding: 15px; font-size: 16px; background-color: #ffffff; color: #000000; border: 2px solid #333333; border-radius: 5px; font-weight: bold;")

        self.history_button = QPushButton("View History")
        self.history_button.clicked.connect(self.show_history)
        self.history_button.setStyleSheet("padding: 15px; font-size: 16px; background-color: #1a1a1a; color: #ffffff; border: 2px solid #333333; border-radius: 5px; font-weight: bold;")

        button_layout.addWidget(self.track_button)
        button_layout.addWidget(self.history_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def setup_timer(self):
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)

    def check_goal(self):
        goal = self.goal_manager.get_daily_goal()
        if not goal:
            self.goal_manager.set_daily_goal(99999)

    def toggle_tracking(self):
        if self.activity_tracker.running:
            self.activity_tracker.stop()
            self.track_button.setText("Start Tracking")
            self.track_button.setStyleSheet("padding: 15px; font-size: 16px; background-color: #ffffff; color: #000000; border: 2px solid #333333; border-radius: 5px; font-weight: bold;")
        else:
            self.activity_tracker.start()
            self.track_button.setText("Stop Tracking")
            self.track_button.setStyleSheet("padding: 15px; font-size: 16px; background-color: #000000; color: #ffffff; border: 2px solid #ffffff; border-radius: 5px; font-weight: bold;")

    def show_history(self):
        from database import DatabaseManager
        db = DatabaseManager()
        activities = db.get_activities_by_date()

        history_window = HistoryWindow(activities, self)
        history_window.exec_()

    def update_display(self):
        progress_data = self.progress_calculator.get_summary()

        self.stats_panel.update_stats(
            progress_data['productive_minutes'],
            progress_data['neutral_minutes'],
            progress_data['distracting_minutes']
        )

        if self.activity_tracker.running:
            current_activity = self.activity_tracker.get_current_activity()
            if current_activity:
                self.activity_display.update_activity(
                    current_activity['app_name'],
                    current_activity['window_title'],
                    current_activity['category']
                )

    def closeEvent(self, event):
        # Stop the update timer first
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()

        # Stop activity tracking
        if self.activity_tracker.running:
            self.activity_tracker.stop()

        event.accept()
