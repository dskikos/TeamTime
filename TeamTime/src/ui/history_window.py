from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO

class HistoryWindow(QDialog):
    def __init__(self, activities, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Activity History")
        self.setGeometry(200, 200, 900, 600)
        self.setStyleSheet("background-color: #1a1a1a; color: #ffffff;")

        layout = QHBoxLayout()

        # Left side - pie chart
        chart_layout = QVBoxLayout()
        self.chart_label = QLabel()
        self.create_pie_chart(activities)
        chart_layout.addWidget(self.chart_label)
        chart_layout.addStretch()

        # Right side - activity table
        right_layout = QVBoxLayout()

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

        right_layout.addWidget(self.text_display)
        right_layout.addWidget(close_button)

        layout.addLayout(chart_layout)
        layout.addLayout(right_layout)
        self.setLayout(layout)

    def create_pie_chart(self, activities):
        productive_mins = 0
        distracting_mins = 0
        neutral_mins = 0

        for act in activities:
            duration = act.duration_seconds / 60
            if act.category == "productive":
                productive_mins += duration
            elif act.category == "distracting":
                distracting_mins += duration
            elif act.category == "neutral":
                neutral_mins += duration

        total = productive_mins + distracting_mins + neutral_mins
        if total == 0:
            return

        sizes = [productive_mins, distracting_mins, neutral_mins]
        labels = [f'Productive\n{productive_mins:.1f} min',
                  f'Distracting\n{distracting_mins:.1f} min',
                  f'Neutral\n{neutral_mins:.1f} min']
        colors = ['#27ae60', '#e74c3c', '#95a5a6']

        fig, ax = plt.subplots(figsize=(5, 5), facecolor='#1a1a1a')
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'color': 'white', 'fontsize': 11})
        ax.axis('equal')
        plt.title('Time Distribution', color='white', fontsize=14, pad=20)

        buf = BytesIO()
        plt.savefig(buf, format='png', facecolor='#1a1a1a', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.chart_label.setPixmap(pixmap)
