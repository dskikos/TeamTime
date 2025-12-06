from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt

class StatsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Today's Statistics")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")

        stats_layout = QHBoxLayout()

        self.productive_widget = self.create_stat_widget("Productive", "0 min", "#27ae60")
        self.neutral_widget = self.create_stat_widget("Neutral", "0 min", "#95a5a6")
        self.distracting_widget = self.create_stat_widget("Distracting", "0 min", "#e74c3c")

        stats_layout.addWidget(self.productive_widget)
        stats_layout.addWidget(self.neutral_widget)
        stats_layout.addWidget(self.distracting_widget)

        layout.addWidget(self.title_label)
        layout.addLayout(stats_layout)

        self.setLayout(layout)

    def create_stat_widget(self, title, value, color):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet(f"background-color: {color}; border-radius: 5px; padding: 10px;")

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; color: white;")

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        value_label.setObjectName(f"{title.lower()}_value")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        frame.setLayout(layout)

        return frame

    def update_stats(self, productive_mins, neutral_mins, distracting_mins):
        productive_label = self.productive_widget.findChild(QLabel, "productive_value")
        if productive_label:
            mins = int(productive_mins)
            secs = int((productive_mins - mins) * 60)
            productive_label.setText(f"{mins}m {secs}s")

        neutral_label = self.neutral_widget.findChild(QLabel, "neutral_value")
        if neutral_label:
            mins = int(neutral_mins)
            secs = int((neutral_mins - mins) * 60)
            neutral_label.setText(f"{mins}m {secs}s")

        distracting_label = self.distracting_widget.findChild(QLabel, "distracting_value")
        if distracting_label:
            mins = int(distracting_mins)
            secs = int((distracting_mins - mins) * 60)
            distracting_label.setText(f"{mins}m {secs}s")
