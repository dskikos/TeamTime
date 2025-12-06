from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt

class ProgressBarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Today's Progress")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3498db;
                border-radius: 5px;
                text-align: center;
                height: 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)

        self.stats_label = QLabel("0 / 0 minutes")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 12px; margin: 5px;")

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def update_progress(self, percentage, effective_mins, target_mins):
        self.progress_bar.setValue(int(percentage))

        if percentage >= 100:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #27ae60;
                    border-radius: 5px;
                    text-align: center;
                    height: 30px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QProgressBar::chunk {
                    background-color: #27ae60;
                }
            """)
        else:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #3498db;
                    border-radius: 5px;
                    text-align: center;
                    height: 30px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QProgressBar::chunk {
                    background-color: #3498db;
                }
            """)

        self.stats_label.setText(f"{int(effective_mins)} / {int(target_mins)} minutes")
