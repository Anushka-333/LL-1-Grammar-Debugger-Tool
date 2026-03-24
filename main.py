#!/usr/bin/env python3
"""Main entry point for LL(1) Grammar Debugger"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from gui.main_window import MainWindow


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()