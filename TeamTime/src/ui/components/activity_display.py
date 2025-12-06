from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt

class ActivityDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Current Activity")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setStyleSheet("background-color: #ecf0f1; border-radius: 5px; padding: 10px;")

        frame_layout = QVBoxLayout()

        self.app_label = QLabel("App: -")
        self.app_label.setStyleSheet("font-size: 12px; margin: 5px;")

        self.window_label = QLabel("Window: -")
        self.window_label.setStyleSheet("font-size: 12px; margin: 5px;")
        self.window_label.setWordWrap(True)

        self.category_label = QLabel("Category: -")
        self.category_label.setStyleSheet("font-size: 12px; font-weight: bold; margin: 5px;")

        frame_layout.addWidget(self.app_label)
        frame_layout.addWidget(self.window_label)
        frame_layout.addWidget(self.category_label)

        self.frame.setLayout(frame_layout)

        layout.addWidget(self.title_label)
        layout.addWidget(self.frame)

        self.setLayout(layout)

    def update_activity(self, app_name, window_title, category):
        self.app_label.setText(f"App: {app_name}")
        self.window_label.setText(f"Window: {window_title[:100]}...")

        category_colors = {
            'productive': '#27ae60',
            'distracting': '#e74c3c',
            'neutral': '#95a5a6'
        }

        color = category_colors.get(category, '#95a5a6')
        self.category_label.setText(f"Category: {category.upper()}")
        self.category_label.setStyleSheet(f"font-size: 12px; font-weight: bold; margin: 5px; color: {color};")
