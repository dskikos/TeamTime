from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

class ActivityDisplay(QWidget):
    category_changed = pyqtSignal(str, str, str)  # app_name, window_title, new_category

    def __init__(self):
        super().__init__()
        self.current_app = None
        self.current_window = None
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

        # Add recategorize buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.productive_btn = QPushButton("✅ Productive")
        self.productive_btn.clicked.connect(lambda: self.recategorize("productive"))
        self.productive_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                background-color: #a8e6cf;
                color: #2d5f47;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #91d9b8;
            }
        """)

        self.neutral_btn = QPushButton("➖ Neutral")
        self.neutral_btn.clicked.connect(lambda: self.recategorize("neutral"))
        self.neutral_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                background-color: #d4d4d4;
                color: #4a5568;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
        """)

        self.distracting_btn = QPushButton("❌ Distracting")
        self.distracting_btn.clicked.connect(lambda: self.recategorize("distracting"))
        self.distracting_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                background-color: #ffb3ba;
                color: #8b2e2e;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ff9ba3;
            }
        """)

        button_layout.addWidget(self.productive_btn)
        button_layout.addWidget(self.neutral_btn)
        button_layout.addWidget(self.distracting_btn)

        frame_layout.addLayout(button_layout)

        self.frame.setLayout(frame_layout)

        layout.addWidget(self.title_label)
        layout.addWidget(self.frame)

        self.setLayout(layout)

    def recategorize(self, new_category):
        if self.current_app and self.current_window:
            self.category_changed.emit(self.current_app, self.current_window, new_category)

    def update_activity(self, app_name, window_title, category):
        self.current_app = app_name
        self.current_window = window_title
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
