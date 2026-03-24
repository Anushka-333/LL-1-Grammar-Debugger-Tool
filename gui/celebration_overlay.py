"""Celebration overlay with flying balloons when string is accepted"""

import random
import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygonF, QPainterPath


class Balloon:
    """Single balloon with position and animation state"""
    def __init__(self, x, y, color, radius=25):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.drift = random.uniform(-1.5, 1.5)  # Horizontal drift speed
        self.float_speed = random.uniform(2, 4)  # Upward speed
        self.wobble = random.uniform(0, 6.28)  # Phase for slight wobble


class CelebrationOverlay(QWidget):
    """Overlay widget showing celebration with flying balloons when parse is accepted"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.balloons = []
        self.timer = None
        self.duration_ms = 3000
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # Capture clicks to dismiss
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.hide()
        
        # Balloon colors - festive and vibrant
        self.balloon_colors = [
            QColor(255, 99, 71),   # Tomato
            QColor(255, 165, 0),   # Orange
            QColor(50, 205, 50),   # Lime green
            QColor(30, 144, 255),  # Dodger blue
            QColor(255, 105, 180), # Hot pink
            QColor(255, 215, 0),   # Gold
            QColor(147, 112, 219), # Medium purple
            QColor(0, 206, 209),   # Dark turquoise
        ]
        
        # Success message label
        self.message_label = QLabel("✓ String Accepted!")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }
        """)
        self.message_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(self.message_label)
        layout.addStretch()
        # Subtle dark overlay so balloons stand out
        self.setStyleSheet("background-color: rgba(0, 0, 0, 35);")
        
    def show_celebration(self):
        """Start the celebration animation"""
        if self.parent() is None:
            return
            
        # Resize to cover parent
        self.setGeometry(self.parent().rect())
        self.raise_()
        
        # Create balloons at bottom, spread across width
        self.balloons = []
        width = self.width()
        height = self.height()
        
        num_balloons = 12
        for i in range(num_balloons):
            x = random.randint(50, max(100, width - 50))
            y = height + random.randint(0, 100)
            color = random.choice(self.balloon_colors)
            radius = random.randint(20, 35)
            self.balloons.append(Balloon(x, y, color, radius))
        
        self.show()
        
        # Start animation timer
        if self.timer:
            self.timer.stop()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(50)
        
        # Auto-hide after duration
        QTimer.singleShot(self.duration_ms, self._stop_celebration)
        
    def _animate(self):
        """Update balloon positions - float upward with drift"""
        width = self.width()
        
        for b in self.balloons:
            b.y -= b.float_speed
            b.x += b.drift
            b.wobble += 0.1
            b.x += math.sin(b.wobble) * 0.5  # Slight wobble
            
            # Wrap horizontally if needed
            if b.x < -50:
                b.x = width + 50
            elif b.x > width + 50:
                b.x = -50
                
        self.update()
        
    def _stop_celebration(self):
        """Stop animation and hide"""
        if self.timer:
            self.timer.stop()
            self.timer = None
        self.balloons = []
        self.hide()
        self.update()
        
    def mousePressEvent(self, event):
        """Dismiss celebration on click"""
        self._stop_celebration()
        
    def paintEvent(self, event):
        """Draw balloons over the overlay"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        for b in self.balloons:
            self._draw_balloon(painter, b)
            
    def _draw_balloon(self, painter, b):
        """Draw a single balloon with string"""
        # Balloon body (ellipse)
        painter.setPen(QPen(b.color.darker(120), 2))
        painter.setBrush(QBrush(b.color))
        rect = QRectF(b.x - b.radius, b.y - b.radius * 1.2, 
                      b.radius * 2, b.radius * 2.4)
        painter.drawEllipse(rect)
        
        # Balloon knot (small triangle at bottom)
        knot_points = [
            QPointF(b.x, b.y + b.radius * 1.1),
            QPointF(b.x - 5, b.y + b.radius * 0.8),
            QPointF(b.x + 5, b.y + b.radius * 0.8),
        ]
        painter.setBrush(QBrush(b.color.darker(150)))
        painter.drawPolygon(QPolygonF(knot_points))
        
        # String (curved line)
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        path = QPainterPath()
        path.moveTo(b.x, b.y + b.radius * 1.2)
        # Simple curved string
        ctrl_y = b.y + b.radius * 2.5
        path.quadTo(b.x + 10, ctrl_y, b.x + 5, b.y + b.radius * 4)
        painter.drawPath(path)
