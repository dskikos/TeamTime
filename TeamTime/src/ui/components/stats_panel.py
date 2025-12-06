from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt

class StatsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        self.title_label = QLabel("📈 Today's Statistics")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin: 8px;
            color: #ffffff;
        """)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        self.productive_widget = self.create_stat_widget("✨ Productive", "0 min", "#1a1a1a", "#ffffff")
        self.neutral_widget = self.create_stat_widget("⚪ Neutral", "0 min", "#1a1a1a", "#888888")
        self.distracting_widget = self.create_stat_widget("⚠️ Distracting", "0 min", "#1a1a1a", "#ffffff")

        stats_layout.addWidget(self.productive_widget)
        stats_layout.addWidget(self.neutral_widget)
        stats_layout.addWidget(self.distracting_widget)

        layout.addWidget(self.title_label)
        layout.addLayout(stats_layout)

        self.setLayout(layout)

    def create_stat_widget(self, title, value, bg_color, text_color):
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid #333333;
                border-radius: 20px;
                padding: 18px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 600;
            color: {text_color};
        """)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {text_color};
        """)
        # Extract just the word for the object name (remove emoji)
        clean_title = ''.join(c for c in title if c.isalnum() or c.isspace()).strip().lower()
        value_label.setObjectName(f"{clean_title}_value")

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
