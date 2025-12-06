from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt

class ActivityDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.title_label = QLabel("💻 Current Activity")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin: 8px;
            color: #4a5568;
        """)

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 20px;
                padding: 18px;
            }
        """)

        frame_layout = QVBoxLayout()
        frame_layout.setSpacing(8)

        self.app_label = QLabel("App: -")
        self.app_label.setStyleSheet("""
            font-size: 16px;
            margin: 5px;
            color: #4a5568;
            font-weight: 500;
        """)

        self.window_label = QLabel("Window: -")
        self.window_label.setStyleSheet("""
            font-size: 14px;
            margin: 5px;
            color: #718096;
        """)
        self.window_label.setWordWrap(True)

        self.category_label = QLabel("Category: -")
        self.category_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            margin: 5px;
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
            'productive': '#a8e6cf',
            'distracting': '#ffb3ba',
            'neutral': '#d4d4d4'
        }

        category_text_colors = {
            'productive': '#2d5f47',
            'distracting': '#8b2e2e',
            'neutral': '#4a5568'
        }

        bg_color = category_colors.get(category, '#d4d4d4')
        text_color = category_text_colors.get(category, '#4a5568')
        self.category_label.setText(f"Category: {category.upper()}")
        self.category_label.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 600;
            margin: 5px;
            color: {text_color};
            background-color: {bg_color};
            padding: 8px 16px;
            border-radius: 12px;
        """)
