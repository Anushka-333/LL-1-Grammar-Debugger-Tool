"""Colorful styles for the GUI"""

from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class Colors:
    """Color constants for the application"""
    PRIMARY = "#2196F3"
    SECONDARY = "#FF4081"
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    ERROR = "#F44336"
    INFO = "#00BCD4"
    
    BACKGROUND = "#2D2D2D"
    SURFACE = "#383838"
    TEXT = "#FFFFFF"
    TEXT_SECONDARY = "#B0B0B0"
    
    GRAMMAR = "#FFB74D"
    FIRST_FOLLOW = "#64B5F6"
    TABLE = "#81C784"
    CONFLICT = "#E57373"
    PARSE = "#BA68C8"


def get_dark_palette():
    """Get dark theme palette"""
    palette = QPalette()
    
    # Set colors for different roles
    palette.setColor(QPalette.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(33, 150, 243))
    palette.setColor(QPalette.Highlight, QColor(33, 150, 243))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    
    return palette


def get_stylesheet():
    """Get application stylesheet"""
    return """
        QMainWindow {
            background-color: #2D2D2D;
        }
        
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QTabWidget::pane {
            border: 2px solid #404040;
            border-radius: 5px;
            background-color: #383838;
        }
        
        QTabBar::tab {
            background-color: #404040;
            color: #FFFFFF;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        
        QTabBar::tab:selected {
            background-color: #2196F3;
        }
        
        QTabBar::tab:hover {
            background-color: #555555;
        }
        
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #1976D2;
        }
        
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        
        QPushButton:disabled {
            background-color: #666666;
            color: #999999;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 2px solid #404040;
            border-radius: 4px;
            padding: 5px;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border-color: #2196F3;
        }
        
        QGroupBox {
            border: 2px solid #404040;
            border-radius: 5px;
            margin-top: 10px;
            font-weight: bold;
            color: #FFFFFF;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QTableWidget {
            background-color: #2D2D2D;
            color: #FFFFFF;
            gridline-color: #404040;
            border: none;
        }
        
        QTableWidget::item {
            padding: 5px;
        }
        
        QTableWidget::item:selected {
            background-color: #2196F3;
        }
        
        QHeaderView::section {
            background-color: #404040;
            color: #FFFFFF;
            padding: 5px;
            border: 1px solid #555555;
        }
        
        QListWidget {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 2px solid #404040;
            border-radius: 4px;
        }
        
        QListWidget::item:selected {
            background-color: #2196F3;
        }
        
        QProgressBar {
            border: 2px solid #404040;
            border-radius: 5px;
            text-align: center;
            color: white;
        }
        
        QProgressBar::chunk {
            background-color: #4CAF50;
            border-radius: 3px;
        }
        
        QStatusBar {
            background-color: #404040;
            color: #FFFFFF;
        }
        
        QMenuBar {
            background-color: #404040;
            color: #FFFFFF;
        }
        
        QMenuBar::item:selected {
            background-color: #2196F3;
        }
        
        QMenu {
            background-color: #404040;
            color: #FFFFFF;
            border: 1px solid #555555;
        }
        
        QMenu::item:selected {
            background-color: #2196F3;
        }
        
        QScrollBar:vertical {
            background-color: #404040;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #666666;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #888888;
        }
        
        QScrollBar:horizontal {
            background-color: #404040;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #666666;
            border-radius: 6px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #888888;
        }
        
        QCheckBox {
            color: #FFFFFF;
        }
        
        QCheckBox::indicator {
            width: 15px;
            height: 15px;
        }
        
        QRadioButton {
            color: #FFFFFF;
        }
        
        QComboBox {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 2px solid #404040;
            border-radius: 4px;
            padding: 5px;
        }
        
        QComboBox:hover {
            border-color: #2196F3;
        }
        
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: #404040;
            border-left-style: solid;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 2px solid #404040;
            selection-background-color: #2196F3;
        }
    """