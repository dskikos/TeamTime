from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt


class ActivityDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.title_label = QLabel("💻 Current Activity")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #ffffff;
        """)

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border: 2px solid #333333;
                border-radius: 20px;
                padding: 20px;
            }
        """)

        frame_layout = QVBoxLayout()
        frame_layout.setSpacing(10)

        self.app_label = QLabel("App: -")
        self.app_label.setStyleSheet("""
            font-size: 17px;
            color: #ffffff;
            font-weight: 600;
        """)

        self.window_label = QLabel("Window: -")
        self.window_label.setStyleSheet("""
            font-size: 14px;
            color: #888888;
        """)
        self.window_label.setWordWrap(True)

        self.category_label = QLabel("Category: -")
        self.category_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
        """)

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
            'productive': '#ffffff',
            'distracting': '#888888',
            'neutral': '#444444'
        }

        category_text_colors = {
            'productive': '#0a0a0a',
            'distracting': '#0a0a0a',
            'neutral': '#ffffff'
        }

        bg_color = category_colors.get(category, '#444444')
        text_color = category_text_colors.get(category, '#ffffff')
        self.category_label.setText(f"Category: {category.upper()}")
        self.category_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {text_color};
            background-color: {bg_color};
            padding: 10px 18px;
            border-radius: 12px;
        """)
