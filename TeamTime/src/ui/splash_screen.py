from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QRegion
import math


class CircularSplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        size = 300
        self.setFixedSize(size, size)

        # Make window circular
        region = QRegion(0, 0, size, size, QRegion.Ellipse)
        self.setMask(region)

        # Center on screen
        screen = self.screen().geometry()
        self.move(
            (screen.width() - size) // 2,
            (screen.height() - size) // 2
        )

        self.angle = 0

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dark background circle
        painter.setBrush(QBrush(QColor('#0a0a0a')))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 300, 300)

        # Draw outer ring
        painter.setPen(QPen(QColor('#1a1a1a'), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(10, 10, 280, 280)

        # Draw progress arc
        center = 150
        radius = 120

        # Animated arc
        painter.setPen(QPen(QColor('#ffffff'), 3))
        start_angle = -90 * 16  # Start at top
        span_angle = int(self.angle * 16)
        painter.drawArc(30, 30, 240, 240, start_angle, span_angle)

        # Draw rotating dot
        rad = math.radians(self.angle - 90)
        dot_x = center + radius * math.cos(rad)
        dot_y = center + radius * math.sin(rad)

        painter.setBrush(QBrush(QColor('#ffffff')))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(dot_x - 6), int(dot_y - 6), 12, 12)

        # Title
        painter.setPen(QColor('#ffffff'))
        painter.setFont(painter.font())
        font = painter.font()
        font.setPointSize(24)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(0, 120, 300, 40, Qt.AlignCenter, "TeamTime")

        # Subtitle
        font.setPointSize(10)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QColor('#888888'))
        painter.drawText(0, 160, 300, 20, Qt.AlignCenter, "Loading...")

    def update_animation(self):
        self.angle = (self.angle + 3) % 360
        self.update()

    def finish_animation(self, main_window):
        self.timer.stop()
        self.close()
        main_window.show()
