from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox
from PyQt5.QtCore import Qt

class BlockDisplay(QWidget):
    def __init__(self, block_system):
        super().__init__()
        self.block_system = block_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Title
        self.title_label = QLabel("🛡️ Site Blocker")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin: 8px;
            color: #4a5568;
        """)

        # Status Frame
        self.status_frame = QFrame()
        self.status_frame.setFrameShape(QFrame.NoFrame)
        self.status_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 20px;
                padding: 18px;
            }
        """)

        status_layout = QVBoxLayout()

        self.status_label = QLabel("Status: Not Active")
        self.status_label.setStyleSheet("""
            font-size: 16px;
            margin: 5px;
            color: #4a5568;
            font-weight: 500;
        """)

        self.limit_label = QLabel("Limit: 120 minutes distracting time")
        self.limit_label.setStyleSheet("""
            font-size: 14px;
            margin: 5px;
            color: #718096;
        """)

        self.sites_label = QLabel("Blocked sites: None")
        self.sites_label.setStyleSheet("""
            font-size: 14px;
            margin: 5px;
            color: #718096;
        """)
        self.sites_label.setWordWrap(True)

        # Emergency Unlock Button
        self.unlock_button = QPushButton("🚨 Emergency Unlock (-100 XP)")
        self.unlock_button.clicked.connect(self.on_emergency_unlock)
        self.unlock_button.setEnabled(False)
        self.unlock_button.setStyleSheet("""
            QPushButton {
                padding: 12px 20px;
                font-size: 15px;
                font-weight: 600;
                background-color: #ff6b6b;
                color: #ffffff;
                border: none;
                border-radius: 15px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
            QPushButton:pressed {
                background-color: #ff3838;
            }
            QPushButton:disabled {
                background-color: #d4d4d4;
                color: #888888;
            }
        """)

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.limit_label)
        status_layout.addWidget(self.sites_label)
        status_layout.addWidget(self.unlock_button)

        self.status_frame.setLayout(status_layout)

        layout.addWidget(self.title_label)
        layout.addWidget(self.status_frame)

        self.setLayout(layout)

    def update_status(self, is_blocked, blocked_sites):
        if is_blocked:
            self.status_label.setText("Status: 🔴 ACTIVE - Sites Blocked")
            self.status_label.setStyleSheet("""
                font-size: 16px;
                margin: 5px;
                color: #ff6b6b;
                font-weight: 600;
            """)
            self.sites_label.setText(f"Blocked sites: {', '.join(blocked_sites)}")
            self.unlock_button.setEnabled(True)
        else:
            self.status_label.setText("Status: 🟢 Not Active")
            self.status_label.setStyleSheet("""
                font-size: 16px;
                margin: 5px;
                color: #a8e6cf;
                font-weight: 600;
            """)
            self.sites_label.setText("Blocked sites: None")
            self.unlock_button.setEnabled(False)

    def on_emergency_unlock(self):
        reply = QMessageBox.question(
            self,
            "Emergency Unlock",
            "Are you sure you want to unlock blocked sites?\n\nThis will cost you 100 XP!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            xp_lost = self.block_system.emergency_unlock()
            QMessageBox.warning(
                self,
                "Sites Unlocked",
                f"Sites have been unlocked.\nYou lost {xp_lost} XP!"
            )
            self.update_status(False, [])
