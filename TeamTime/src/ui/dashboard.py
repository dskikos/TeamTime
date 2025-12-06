from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QInputDialog, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import QTimer
from ui.components import ActivityDisplay, StatsPanel, XPDisplay
from ui.history_window import HistoryWindow
from ui.custom_categories_window import CustomCategoriesWindow
from monitor import ActivityTracker
from core import GoalManager, ProgressCalculator, Config, XPSystem


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.activity_tracker = ActivityTracker(
            interval=Config.TRACKING_INTERVAL)
        self.goal_manager = GoalManager()
        self.progress_calculator = ProgressCalculator()
        self.xp_system = XPSystem()

        self.previous_productive_mins = 0
        self.previous_distracting_mins = 0

        # Unproductive warning tracking
        self.last_productive_time = None
        self.unproductive_warning_shown = False
        self.UNPRODUCTIVE_THRESHOLD_MINUTES = 15

        self.init_ui()
        self.setup_timer()

        self.check_goal()

    def init_ui(self):
        self.setWindowTitle("TeamTime - Productivity Tracker")
        # Bigger default size and minimum size for better fullscreen experience
        self.setGeometry(50, 50, 950, 1050)
        self.setMinimumSize(750, 850)

        # Set dark minimalist background
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a0a;
            }
            QWidget {
                background-color: #0a0a0a;
                color: #ffffff;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # XP Display
        self.xp_display = XPDisplay()
        layout.addWidget(self.xp_display)

        self.activity_display = ActivityDisplay()
        self.activity_display.category_changed.connect(self.on_category_changed)
        layout.addWidget(self.activity_display)

        self.stats_panel = StatsPanel()
        layout.addWidget(self.stats_panel)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.track_button = QPushButton("▶ Start Tracking")
        self.track_button.clicked.connect(self.toggle_tracking)
        self.track_button.setStyleSheet("""
            QPushButton {
                padding: 14px 28px;
                font-size: 16px;
                font-weight: 600;
                background-color: #ffffff;
                color: #0a0a0a;
                border: 2px solid #333333;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 2px solid #555555;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

        self.history_button = QPushButton("📜 View History")
        self.history_button.clicked.connect(self.show_history)
        self.history_button.setStyleSheet("""
            QPushButton {
                padding: 14px 28px;
                font-size: 16px;
                font-weight: 600;
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border: 2px solid #555555;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """)

        self.goal_button = QPushButton("🎯 Set Goal")
        self.goal_button.clicked.connect(self.set_goal)
        self.goal_button.setStyleSheet("""
            QPushButton {
                padding: 14px 28px;
                font-size: 16px;
                font-weight: 600;
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border: 2px solid #555555;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """)

        self.categories_button = QPushButton("📝 My Categories")
        self.categories_button.clicked.connect(self.show_custom_categories)
        self.categories_button.setStyleSheet("""
            QPushButton {
                padding: 14px 28px;
                font-size: 16px;
                font-weight: 600;
                background-color: #fffacd;
                color: #6b5b00;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #fff8b3;
            }
            QPushButton:pressed {
                background-color: #fff69a;
            }
        """)

        button_layout.addWidget(self.track_button)
        button_layout.addWidget(self.history_button)
        button_layout.addWidget(self.goal_button)
        button_layout.addWidget(self.categories_button)

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

    def toggle_tracking(self):
        if self.activity_tracker.running:
            self.activity_tracker.stop()
            self.track_button.setText("▶ Start Tracking")
            self.track_button.setStyleSheet("""
                QPushButton {
                    padding: 14px 28px;
                    font-size: 16px;
                    font-weight: 600;
                    background-color: #ffffff;
                    color: #0a0a0a;
                    border: 2px solid #333333;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                    border: 2px solid #555555;
                }
                QPushButton:pressed {
                    background-color: #e0e0e0;
                }
            """)
        else:
            self.activity_tracker.start()
            self.track_button.setText("⏹ Stop Tracking")
            self.track_button.setStyleSheet("""
                QPushButton {
                    padding: 14px 28px;
                    font-size: 16px;
                    font-weight: 600;
                    background-color: #0a0a0a;
                    color: #ffffff;
                    border: 2px solid #ffffff;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #1a1a1a;
                    border: 2px solid #f0f0f0;
                }
                QPushButton:pressed {
                    background-color: #2a2a2a;
                }
            """)

    def show_history(self):
        from database import DatabaseManager
        db = DatabaseManager()
        activities = db.get_activities_by_date()

        history_window = HistoryWindow(activities, self)
        history_window.exec_()

    def show_custom_categories(self):
        categories_window = CustomCategoriesWindow(self.activity_tracker.categorizer, self)
        categories_window.exec_()

    def on_category_changed(self, app_name, window_title, new_category):
        # Add the app name to the appropriate category in categories.json
        # Use the actual app_name, not lowercase, so it displays properly in My Categories
        self.activity_tracker.categorizer.add_rule(new_category, app_name)
        QMessageBox.information(
            self,
            "Category Learned!",
            f"'{app_name}' will now be categorized as '{new_category}' in the future!"
        )

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

        self.stats_panel.update_stats(
            progress_data['productive_minutes'],
            progress_data['neutral_minutes'],
            progress_data['distracting_minutes']
        )

        # Update XP based on time changes
        productive_mins = progress_data['productive_minutes']
        distracting_mins = progress_data['distracting_minutes']

        if productive_mins > self.previous_productive_mins:
            gained = productive_mins - self.previous_productive_mins
            self.xp_system.gain_xp(gained)

        if distracting_mins > self.previous_distracting_mins:
            lost = distracting_mins - self.previous_distracting_mins
            self.xp_system.lose_xp_distraction(lost)

        self.previous_productive_mins = productive_mins
        self.previous_distracting_mins = distracting_mins

        # Update XP Display
        xp_stats = self.xp_system.get_stats()
        self.xp_display.update_xp(
            xp_stats['current_xp'],
            xp_stats['level'],
            xp_stats['xp_to_next_level']
        )

        if self.activity_tracker.running:
            current_activity = self.activity_tracker.get_current_activity()
            if current_activity:
                self.activity_display.update_activity(
                    current_activity['app_name'],
                    current_activity['window_title'],
                    current_activity['category']
                )

                # Check for unproductive warning
                self.check_unproductive_warning(current_activity)

    def check_unproductive_warning(self, current_activity):
        from datetime import datetime

        if current_activity['category'] == 'productive':
            self.last_productive_time = datetime.now()
            self.unproductive_warning_shown = False
        elif current_activity['category'] in ['distracting', 'neutral']:
            if self.last_productive_time is None:
                self.last_productive_time = datetime.now()
            else:
                time_unproductive = (
                    datetime.now() - self.last_productive_time
                ).total_seconds() / 60

                if (time_unproductive >= self.UNPRODUCTIVE_THRESHOLD_MINUTES
                        and not self.unproductive_warning_shown):
                    self.unproductive_warning_shown = True
                    QMessageBox.warning(
                        self,
                        "⚠️ Productivity Alert",
                        f"You've been unproductive for "
                        f"{int(time_unproductive)} minutes!\n\n"
                        f"Time to get back on track! 💪\n\n"
                        f"Focus on your goals and stay productive."
                    )

    def closeEvent(self, event):
        # Stop the update timer first
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()

        # Stop activity tracking
        if self.activity_tracker.running:
            self.activity_tracker.stop()

        event.accept()
