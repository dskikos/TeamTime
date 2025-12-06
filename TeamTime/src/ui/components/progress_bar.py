from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt

class ProgressBarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.label = QLabel("📊 Today's Progress")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            margin: 10px;
            color: #4a5568;
        """)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 25px;
                text-align: center;
                height: 50px;
                font-size: 18px;
                font-weight: bold;
                background-color: #e2e8f0;
                color: #2d3748;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #bae1ff, stop:1 #a8e6cf);
                border-radius: 25px;
            }
        """)

        self.stats_label = QLabel("0 / 0 minutes")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("""
            font-size: 18px;
            margin: 8px;
            color: #718096;
            font-weight: 500;
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def update_progress(self, percentage, effective_mins, target_mins):
        self.progress_bar.setValue(int(percentage))

        if percentage >= 100:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 25px;
                    text-align: center;
                    height: 50px;
                    font-size: 18px;
                    font-weight: bold;
                    background-color: #e2e8f0;
                    color: #2d3748;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #a8e6cf, stop:1 #dcedc8);
                    border-radius: 25px;
                }
            """)
        else:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 25px;
                    text-align: center;
                    height: 50px;
                    font-size: 18px;
                    font-weight: bold;
                    background-color: #e2e8f0;
                    color: #2d3748;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #bae1ff, stop:1 #a8e6cf);
                    border-radius: 25px;
                }
            """)

        self.stats_label.setText(f"{int(effective_mins)} / {int(target_mins)} minutes")
