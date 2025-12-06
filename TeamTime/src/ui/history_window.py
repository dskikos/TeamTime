from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt

class HistoryWindow(QDialog):
    def __init__(self, activities, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Activity History")
        self.setGeometry(200, 200, 700, 500)
        self.setStyleSheet("background-color: #1a1a1a; color: #ffffff;")

        layout = QVBoxLayout()

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("""
            QTextEdit {
                background-color: #0d0d0d;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New';
                font-size: 12px;
            }
        """)

        history_html = "<table width='100%' style='border-collapse: collapse;'>"
        history_html += "<tr style='background-color: #2a2a2a; font-weight: bold;'>"
        history_html += "<td style='padding: 10px; border: 1px solid #333;'>Time</td>"
        history_html += "<td style='padding: 10px; border: 1px solid #333;'>App</td>"
        history_html += "<td style='padding: 10px; border: 1px solid #333;'>Category</td>"
        history_html += "</tr>"

        for act in activities[-100:]:
            color = "#27ae60" if act.category == "productive" else "#e74c3c" if act.category == "distracting" else "#95a5a6"
            history_html += f"<tr style='border: 1px solid #333;'>"
            history_html += f"<td style='padding: 8px; border: 1px solid #333;'>{act.timestamp.strftime('%H:%M:%S')}</td>"
            history_html += f"<td style='padding: 8px; border: 1px solid #333;'>{act.app_name}</td>"
            history_html += f"<td style='padding: 8px; border: 1px solid #333; color: {color}; font-weight: bold;'>{act.category.upper()}</td>"
            history_html += "</tr>"

        history_html += "</table>"
        self.text_display.setHtml(history_html)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)

        layout.addWidget(self.text_display)
        layout.addWidget(close_button)
        self.setLayout(layout)
