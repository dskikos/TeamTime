from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, QFrame
from PyQt5.QtCore import Qt

class XPDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Header
        header_layout = QHBoxLayout()

        self.title_label = QLabel("⭐ Experience Level")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
        """)

        self.level_label = QLabel("Level 1")
        self.level_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.level_label.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #0a0a0a;
            background-color: #ffffff;
            padding: 10px 24px;
            border-radius: 18px;
        """)

        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.level_label)

        # XP Progress Bar
        self.xp_bar = QProgressBar()
        self.xp_bar.setMinimum(0)
        self.xp_bar.setMaximum(1000)
        self.xp_bar.setValue(0)
        self.xp_bar.setTextVisible(True)
        self.xp_bar.setFormat("%v / %m XP")
        self.xp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #333333;
                border-radius: 22px;
                text-align: center;
                height: 50px;
                font-size: 18px;
                font-weight: bold;
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff, stop:1 #aaaaaa);
                border-radius: 18px;
            }
        """)

        # XP Stats
        self.xp_label = QLabel("0 XP")
        self.xp_label.setAlignment(Qt.AlignCenter)
        self.xp_label.setStyleSheet("""
            font-size: 18px;
            color: #888888;
            font-weight: 500;
        """)

        layout.addLayout(header_layout)
        layout.addWidget(self.xp_bar)
        layout.addWidget(self.xp_label)

        self.setLayout(layout)

    def update_xp(self, current_xp, level, xp_to_next_level):
        self.level_label.setText(f"Level {level}")
        self.xp_label.setText(f"{current_xp} XP")

        # Update progress bar
        self.xp_bar.setMaximum(1000)
        xp_in_current_level = current_xp % 1000
        self.xp_bar.setValue(xp_in_current_level)
        self.xp_bar.setFormat(f"{xp_in_current_level} / 1000 XP")
