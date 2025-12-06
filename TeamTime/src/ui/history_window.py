from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QLabel,
                             QHBoxLayout, QScrollArea, QWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
from datetime import datetime, timedelta
from collections import defaultdict


class HistoryWindow(QDialog):
    def __init__(self, activities, parent=None):
        super().__init__(parent)
        self.activities = activities
        self.setWindowTitle("📊 Activity History")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("background-color: #f8f9fa;")

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Activity History")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Charts section
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)

        # Pie chart
        pie_container = self.create_chart_container("Time Distribution")
        self.pie_label = QLabel()
        self.create_pie_chart()
        pie_layout = QVBoxLayout()
        pie_layout.addWidget(self.pie_label, alignment=Qt.AlignCenter)
        pie_container.layout().addLayout(pie_layout)
        charts_layout.addWidget(pie_container)

        # Timeline chart
        timeline_container = self.create_chart_container("Minute-by-Minute Timeline")
        self.timeline_label = QLabel()
        self.create_timeline_chart()
        timeline_layout = QVBoxLayout()
        timeline_layout.addWidget(self.timeline_label, alignment=Qt.AlignCenter)
        timeline_container.layout().addLayout(timeline_layout)
        charts_layout.addWidget(timeline_container)

        main_layout.addLayout(charts_layout)

        # Activity log section
        log_container = self.create_chart_container("Activity Log")
        self.create_activity_log(log_container)
        main_layout.addWidget(log_container)

        # Close button
        close_button = QPushButton("✕ Close")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #e53e3e;
                color: white;
                border: none;
                padding: 12px 40px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #c53030;
            }
        """)
        close_button.setMaximumWidth(200)
        main_layout.addWidget(close_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def create_chart_container(self, title):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #4a5568;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        container.setLayout(layout)
        return container

    def create_pie_chart(self):
        productive_mins = 0
        distracting_mins = 0
        neutral_mins = 0

        for act in self.activities:
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
        colors = ['#a8e6cf', '#ffb3ba', '#e0e0e0']

        fig, ax = plt.subplots(figsize=(6, 6), facecolor='white')
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                            autopct='%1.1f%%', startangle=90,
                                            textprops={'fontsize': 12, 'weight': 'bold'})

        for autotext in autotexts:
            autotext.set_color('#2d3748')
            autotext.set_fontsize(11)

        for text in texts:
            text.set_color('#4a5568')
            text.set_fontsize(11)

        ax.axis('equal')

        buf = BytesIO()
        plt.savefig(buf, format='png', facecolor='white', bbox_inches='tight', dpi=100)
        buf.seek(0)
        plt.close()

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.pie_label.setPixmap(pixmap)

    def create_timeline_chart(self):
        if not self.activities:
            return

        # Group activities by minute
        minute_data = defaultdict(lambda: {'productive': 0, 'distracting': 0, 'neutral': 0})

        for act in self.activities:
            # Round to nearest minute
            timestamp = act.timestamp.replace(second=0, microsecond=0)
            duration_mins = act.duration_seconds / 60

            if act.category == "productive":
                minute_data[timestamp]['productive'] += duration_mins
            elif act.category == "distracting":
                minute_data[timestamp]['distracting'] += duration_mins
            elif act.category == "neutral":
                minute_data[timestamp]['neutral'] += duration_mins

        if not minute_data:
            return

        # Sort by time
        sorted_times = sorted(minute_data.keys())

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 4), facecolor='white')

        # Prepare data for stacked bar chart
        productive = [minute_data[t]['productive'] for t in sorted_times]
        distracting = [minute_data[t]['distracting'] for t in sorted_times]
        neutral = [minute_data[t]['neutral'] for t in sorted_times]

        # Plot stacked bars
        bar_width = 0.8
        ax.bar(sorted_times, productive, bar_width, label='Productive',
               color='#a8e6cf', edgecolor='none')
        ax.bar(sorted_times, distracting, bar_width, bottom=productive,
               label='Distracting', color='#ffb3ba', edgecolor='none')

        bottom = [p + d for p, d in zip(productive, distracting)]
        ax.bar(sorted_times, neutral, bar_width, bottom=bottom,
               label='Neutral', color='#e0e0e0', edgecolor='none')

        # Format x-axis with smarter tick spacing
        num_ticks = min(20, len(sorted_times))
        if len(sorted_times) > 0:
            interval = max(1, len(sorted_times) // num_ticks)
            # Use AutoDateLocator for better tick placement
            ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=num_ticks))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.xticks(rotation=45, ha='right')

        # Style
        ax.set_ylabel('Minutes', fontsize=11, color='#4a5568', fontweight='bold')
        ax.set_xlabel('Time', fontsize=11, color='#4a5568', fontweight='bold')
        ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
        ax.set_facecolor('#f8f9fa')

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cbd5e0')
        ax.spines['bottom'].set_color('#cbd5e0')

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png', facecolor='white', bbox_inches='tight', dpi=100)
        buf.seek(0)
        plt.close()

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.timeline_label.setPixmap(pixmap)

    def create_activity_log(self, container):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(8)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        # Group activities by minute
        activity_groups = defaultdict(list)
        for act in self.activities:
            minute_key = act.timestamp.replace(second=0, microsecond=0)
            activity_groups[minute_key].append(act)

        # Sort by time (most recent first)
        sorted_times = sorted(activity_groups.keys(), reverse=True)

        for time_key in sorted_times[:100]:  # Show last 100 minutes
            acts = activity_groups[time_key]

            # Create time block
            time_block = QFrame()
            time_block.setStyleSheet("""
                QFrame {
                    background-color: #f7fafc;
                    border-left: 4px solid #cbd5e0;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)

            block_layout = QHBoxLayout()
            block_layout.setSpacing(15)

            # Time label
            time_label = QLabel(time_key.strftime('%H:%M'))
            time_label.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
                color: #4a5568;
                min-width: 60px;
            """)
            block_layout.addWidget(time_label)

            # Activities for this minute
            activities_layout = QVBoxLayout()
            activities_layout.setSpacing(5)

            for act in acts:
                category_colors = {
                    'productive': '#a8e6cf',
                    'distracting': '#ffb3ba',
                    'neutral': '#e0e0e0'
                }
                category_text_colors = {
                    'productive': '#2d5f47',
                    'distracting': '#8b2e2e',
                    'neutral': '#4a5568'
                }

                color = category_colors.get(act.category, '#e0e0e0')
                text_color = category_text_colors.get(act.category, '#4a5568')

                activity_label = QLabel(f"<b>{act.app_name}</b> - {act.window_title[:60]}{'...' if len(act.window_title) > 60 else ''}")
                activity_label.setStyleSheet(f"""
                    background-color: {color};
                    color: {text_color};
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 12px;
                """)
                activity_label.setWordWrap(True)
                activities_layout.addWidget(activity_label)

            block_layout.addLayout(activities_layout, stretch=1)
            time_block.setLayout(block_layout)
            scroll_layout.addWidget(time_block)

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        scroll.setMaximumHeight(300)

        container.layout().addWidget(scroll)
