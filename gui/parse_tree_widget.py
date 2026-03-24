"""Parse Tree Widget for GUI - NEW"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QScrollArea,
                             QGraphicsView, QGraphicsScene, QGraphicsItem)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainter, QFontMetrics
import math


class ParseTreeGraphicsView(QGraphicsView):
    """Graphics view for displaying parse tree"""
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
    def wheelEvent(self, event):
        """Zoom in/out with mouse wheel"""
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1/zoom_factor, 1/zoom_factor)


class TreeNodeItem(QGraphicsItem):
    """Graphics item for tree node"""
    
    def __init__(self, value, x, y, parent=None):
        super().__init__(parent)
        self.value = value
        self.x = x
        self.y = y
        self.setPos(x, y)
        
        # Calculate size based on text
        font = QFont("Consolas", 10)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(value) + 20
        text_height = fm.height() + 10
        self.rect = QRectF(-text_width/2, -text_height/2, text_width, text_height)
        
    def boundingRect(self):
        return self.rect
    
    def paint(self, painter, option, widget):
        # Draw circle/rectangle
        painter.setPen(QPen(QColor("#2196F3"), 2))
        
        # Different colors for terminals and non-terminals
        if self.value[0].isupper():
            painter.setBrush(QBrush(QColor("#64B5F6")))  # Non-terminal
        else:
            painter.setBrush(QBrush(QColor("#81C784")))  # Terminal
            
        painter.drawRoundedRect(self.rect, 5, 5)
        
        # Draw text
        painter.setPen(QPen(QColor("#FFFFFF"), 1))
        painter.setFont(QFont("Consolas", 10))
        painter.drawText(self.rect, Qt.AlignCenter, self.value)


class ParseTreeWidget(QWidget):
    """Widget for displaying parse tree"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.zoom_in_btn = QPushButton("🔍+ Zoom In")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        
        self.zoom_out_btn = QPushButton("🔍- Zoom Out")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        
        self.fit_btn = QPushButton("↔ Fit to Window")
        self.fit_btn.clicked.connect(self.fit_to_view)
        
        control_layout.addWidget(self.zoom_in_btn)
        control_layout.addWidget(self.zoom_out_btn)
        control_layout.addWidget(self.fit_btn)
        control_layout.addStretch()
        
        # Tree display area
        self.graphics_view = ParseTreeGraphicsView()
        
        # Text representation as backup
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Consolas", 10))
        self.text_display.setMaximumHeight(200)
        self.text_display.hide()
        
        # Toggle button
        self.toggle_view_btn = QPushButton("Show Text View")
        self.toggle_view_btn.clicked.connect(self.toggle_view)
        
        layout.addLayout(control_layout)
        layout.addWidget(self.graphics_view)
        layout.addWidget(self.text_display)
        layout.addWidget(self.toggle_view_btn)
        
        self.setLayout(layout)
        
        self.show_graphics = True
        
    def set_tree(self, tree_string):
        """Set and display parse tree"""
        # Clear previous scene
        self.graphics_view.scene.clear()
        
        # Parse tree string and create graphical representation
        self.create_graphical_tree(tree_string)
        
        # Set text representation
        self.text_display.clear()
        self.text_display.append(tree_string)
        
        # Fit to view
        self.fit_to_view()
        
    def create_graphical_tree(self, tree_string):
        """Create graphical tree from string representation"""
        lines = tree_string.split('\n')
        if len(lines) < 2:
            return
            
        # Simple parser for tree structure
        # This is a simplified version - you might want to enhance this
        root_text = lines[1].strip()
        if '→' in root_text:
            root_value = root_text.split('→')[0].strip().replace('└──', '').strip()
        else:
            root_value = root_text.replace('└──', '').strip()
            
        # Create root node at center top
        root_item = TreeNodeItem(root_value, 400, 50)
        self.graphics_view.scene.addItem(root_item)
        
        # Add some example children for demonstration
        # In real implementation, you would parse the actual tree structure
        self.add_sample_children(root_item)
        
    def add_sample_children(self, parent_item):
        """Add sample children for demonstration"""
        # This is just for demonstration - you'll need to implement proper tree layout
        child_positions = [(350, 150), (450, 150)]
        child_values = ["T", "E'"]
        
        for i, (x, y) in enumerate(child_positions):
            child = TreeNodeItem(child_values[i], x, y)
            self.graphics_view.scene.addItem(child)
            
            # Draw line from parent to child
            line = self.graphics_view.scene.addLine(
                parent_item.x, parent_item.y + 20,
                x, y - 20,
                QPen(QColor("#888888"), 1, Qt.DashLine)
            )
        
    def zoom_in(self):
        self.graphics_view.scale(1.2, 1.2)
        
    def zoom_out(self):
        self.graphics_view.scale(1/1.2, 1/1.2)
        
    def fit_to_view(self):
        self.graphics_view.fitInView(self.graphics_view.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        
    def toggle_view(self):
        """Toggle between graphics and text view"""
        self.show_graphics = not self.show_graphics
        if self.show_graphics:
            self.graphics_view.show()
            self.text_display.hide()
            self.toggle_view_btn.setText("Show Text View")
        else:
            self.graphics_view.hide()
            self.text_display.show()
            self.toggle_view_btn.setText("Show Graphics View")