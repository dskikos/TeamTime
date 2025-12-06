import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QInputDialog, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import QTimer
from ui.components import ProgressBarWidget, ActivityDisplay, StatsPanel
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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.progress_widget = ProgressBarWidget()
        layout.addWidget(self.progress_widget)

        self.activity_display = ActivityDisplay()
        layout.addWidget(self.activity_display)

        self.stats_panel = StatsPanel()
        layout.addWidget(self.stats_panel)

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Tracking")
        self.start_button.clicked.connect(self.start_tracking)
        self.start_button.setStyleSheet("padding: 10px; font-size: 14px; background-color: #27ae60; color: white; border-radius: 5px;")

        self.stop_button = QPushButton("Stop Tracking")
        self.stop_button.clicked.connect(self.stop_tracking)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("padding: 10px; font-size: 14px; background-color: #e74c3c; color: white; border-radius: 5px;")

        self.goal_button = QPushButton("Set Goal")
        self.goal_button.clicked.connect(self.set_goal)
        self.goal_button.setStyleSheet("padding: 10px; font-size: 14px; background-color: #3498db; color: white; border-radius: 5px;")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.goal_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def setup_timer(self):
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)

    def check_goal(self):
        goal = self.goal_manager.get_daily_goal()
        if not goal:
            self.set_goal(show_message=False)

    def start_tracking(self):
        self.activity_tracker.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_tracking(self):
        self.activity_tracker.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def set_goal(self, show_message=True):
        current_goal = self.goal_manager.get_daily_goal()
        default_value = current_goal.target_minutes if current_goal else Config.DEFAULT_GOAL_MINUTES

        minutes, ok = QInputDialog.getInt(
            self,
            "Set Daily Goal",
            "Enter your daily productivity goal (minutes):",
            default_value,
            1,
            1440
        )

        if ok:
            self.goal_manager.set_daily_goal(minutes)
            if show_message:
                QMessageBox.information(self, "Goal Set", f"Daily goal set to {minutes} minutes!")

    def update_display(self):
        progress_data = self.progress_calculator.get_summary()

        self.progress_widget.update_progress(
            progress_data['percentage'],
            progress_data['effective_minutes'],
            progress_data['target_minutes']
        )

        self.stats_panel.update_stats(
            progress_data['productive_minutes'],
            progress_data['neutral_minutes'],
            progress_data['distracting_minutes']
        )

        current_activity = self.activity_tracker.get_current_activity()
        if current_activity:
            self.activity_display.update_activity(
                current_activity['app_name'],
                current_activity['window_title'],
                current_activity['category']
            )

    def closeEvent(self, event):
        self.activity_tracker.stop()
        event.accept()
