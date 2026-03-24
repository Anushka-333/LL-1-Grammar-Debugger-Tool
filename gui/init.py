"""GUI package for the LL(1) Grammar Debugger"""
from gui.main_window import MainWindow
from gui.styles import Colors, get_dark_palette, get_stylesheet
from gui.widgets import (
    GrammarInputWidget,
    FirstFollowWidget,
    ParsingTableWidget,
    ParseTraceWidget,
    SymbolTableWidget,
    ParseTreeWidget
)

__all__ = [
    'MainWindow',
    'Colors',
    'get_dark_palette',
    'get_stylesheet',
    'GrammarInputWidget',
    'FirstFollowWidget',
    'ParsingTableWidget',
    'ParseTraceWidget',
    'SymbolTableWidget',
    'ParseTreeWidget'
]