"""Custom widgets for the GUI - COMPLETE FIXED VERSION"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QTableWidget,
                             QTableWidgetItem, QHeaderView, QSplitter, QFrame,
                             QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QScrollArea, QGraphicsLineItem)
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QPointF
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QPainter, QPen, QBrush, QFontMetrics
from utils.helpers import get_parser_suggestions_for_non_ll1
import math


class GrammarInputWidget(QWidget):
    """Widget for grammar input and display"""
    
    grammar_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Input section
        input_group = QGroupBox("Grammar Input")
        input_group.setStyleSheet("""
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        input_layout = QVBoxLayout()
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "Enter any Context-Free Grammar (supports ->, ::=, →)\n\n"
            "Examples:\n"
            "  E -> E + T | T     or     S ::= a S b | ε\n"
            "  T -> T * F | F            A := id | num | ( A )\n"
            "  F -> ( E ) | id"
        )
        self.input_text.textChanged.connect(self.on_text_changed)
        self.input_text.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 2px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QTextEdit:focus {
                border-color: #2196F3;
            }
        """)
        
        # Example buttons
        example_btn = QPushButton("📋 LL(1) Example")
        example_btn.clicked.connect(self.load_ll1_example)
        example_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        non_ll1_btn = QPushButton("📋 Non-LL(1) Example")
        non_ll1_btn.clicked.connect(self.load_non_ll1_example)
        non_ll1_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        
        example_layout = QHBoxLayout()
        example_layout.addWidget(example_btn)
        example_layout.addWidget(non_ll1_btn)
        example_layout.addStretch()
        
        input_layout.addWidget(self.input_text)
        input_layout.addLayout(example_layout)
        input_group.setLayout(input_layout)
        
        # Display section
        display_group = QGroupBox("Processed Grammar")
        display_group.setStyleSheet("""
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        display_layout = QVBoxLayout()
        
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.display_text.setFont(QFont("Consolas", 10))
        self.display_text.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #FFB74D;
                border: 2px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
            }
        """)
        
        display_layout.addWidget(self.display_text)
        display_group.setLayout(display_layout)
        
        layout.addWidget(input_group)
        layout.addWidget(display_group)
        self.setLayout(layout)
        
    def on_text_changed(self):
        self.grammar_changed.emit(self.input_text.toPlainText())
        
    def load_ll1_example(self):
        """Load an LL(1) compatible grammar (expression grammar)"""
        example = """E -> E + T | T
T -> T * F | F
F -> ( E ) | id"""
        self.input_text.setText(example)
    
    def load_non_ll1_example(self):
        """Load a non-LL(1) grammar to see alternative parser suggestions"""
        example = """S -> A a | b
A -> a | ε"""
        self.input_text.setText(example)
        
    def set_display(self, text, color=None):
        self.display_text.clear()
        if color:
            self.display_text.setTextColor(QColor(color))
        self.display_text.append(text)


class FirstFollowWidget(QWidget):
    """Widget for displaying First and Follow sets"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        
        # First sets
        first_group = QGroupBox("FIRST Sets")
        first_group.setStyleSheet("""
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        first_layout = QVBoxLayout()
        self.first_text = QTextEdit()
        self.first_text.setReadOnly(True)
        self.first_text.setFont(QFont("Consolas", 10))
        self.first_text.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #64B5F6;
                border: 2px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
            }
        """)
        first_layout.addWidget(self.first_text)
        first_group.setLayout(first_layout)
        
        # Follow sets
        follow_group = QGroupBox("FOLLOW Sets")
        follow_group.setStyleSheet("""
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        follow_layout = QVBoxLayout()
        self.follow_text = QTextEdit()
        self.follow_text.setReadOnly(True)
        self.follow_text.setFont(QFont("Consolas", 10))
        self.follow_text.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #81C784;
                border: 2px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
            }
        """)
        follow_layout.addWidget(self.follow_text)
        follow_group.setLayout(follow_layout)
        
        layout.addWidget(first_group)
        layout.addWidget(follow_group)
        self.setLayout(layout)
        
    def update_sets(self, first, follow):
        self.first_text.clear()
        self.first_text.append("FIRST SETS:\n" + "="*40)
        for nt, f_set in first.items():
            self.first_text.append(f"FIRST({nt}) = {{ {', '.join(sorted(f_set))} }}")
            
        self.follow_text.clear()
        self.follow_text.append("FOLLOW SETS:\n" + "="*40)
        for nt, f_set in follow.items():
            self.follow_text.append(f"FOLLOW({nt}) = {{ {', '.join(sorted(f_set))} }}")


class ParsingTableWidget(QWidget):
    """Widget for displaying LL(1) parsing table"""
    
    def __init__(self):
        super().__init__()
        self.current_table = {}
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Table
        self.table = QTableWidget()
        self.table.setFont(QFont("Consolas", 9))
        self.table.setStyleSheet("""
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
                font-weight: bold;
            }
        """)
        
        # Conflict info + parser suggestions
        self.conflict_text = QTextEdit()
        self.conflict_text.setReadOnly(True)
        self.conflict_text.setMaximumHeight(280)
        self.conflict_text.setFont(QFont("Consolas", 9))
        self.conflict_text.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                border: 2px solid #404040;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Consolas', monospace;
            }
        """)
        
        layout.addWidget(self.table)
        layout.addWidget(self.conflict_text)
        self.setLayout(layout)
        
    def update_table(self, table, non_terminals, terminals, conflicts):
        self.current_table = table
        
        # Set up table dimensions
        self.table.setRowCount(len(non_terminals))
        self.table.setColumnCount(len(terminals))
        
        # Set headers
        self.table.setVerticalHeaderLabels(non_terminals)
        self.table.setHorizontalHeaderLabels(terminals)
        
        # Fill table
        for i, nt in enumerate(non_terminals):
            for j, term in enumerate(terminals):
                key = (nt, term)
                if key in table:
                    entry = table[key]
                    if isinstance(entry, list) and len(entry) > 0 and isinstance(entry[0], list):
                        # Conflict
                        item = QTableWidgetItem("⚠ CONFLICT")
                        item.setBackground(QColor(244, 67, 54))  # Red
                        item.setForeground(QColor(255, 255, 255))
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setFont(QFont("Consolas", 9, QFont.Bold))
                    else:
                        prod_str = ' '.join(entry) if entry != ['ε'] else 'ε'
                        item = QTableWidgetItem(prod_str)
                        item.setBackground(QColor(69, 69, 69))  # Gray
                        item.setForeground(QColor(255, 255, 255))
                        item.setTextAlignment(Qt.AlignCenter)
                else:
                    item = QTableWidgetItem("")
                    item.setBackground(QColor(45, 45, 45))
                    item.setForeground(QColor(255, 255, 255))
                
                self.table.setItem(i, j, item)
        
        # Resize columns
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Show conflicts and parser suggestions
        if conflicts:
            self.conflict_text.clear()
            self.conflict_text.append("⚠ CONFLICTS DETECTED - Grammar is NOT LL(1)\n" + "="*50)
            def format_prod(prod):
                if prod == ['ε']:
                    return 'ε'
                if isinstance(prod, list):
                    if prod and isinstance(prod[0], list):
                        # conflict stores list of productions
                        return ' | '.join(' '.join(p) if isinstance(p, list) else str(p) for p in prod)
                    return ' '.join(str(x) for x in prod)
                return str(prod)

            for i, conflict in enumerate(conflicts, 1):
                nt, term = conflict['cell']
                self.conflict_text.append(f"\n{i}. Cell [{nt}, {term}]:")
                existing = format_prod(conflict['existing'])
                new = format_prod(conflict['new'])
                self.conflict_text.append(f"   Existing: {existing}")
                self.conflict_text.append(f"   New: {new}")

            suggestions = get_parser_suggestions_for_non_ll1()
            rows = "".join(
                f"""
                <tr>
                    <td style='padding:8px;border:1px solid #555;color:#ffffff;'><b>{item['name']}</b></td>
                    <td style='padding:8px;border:1px solid #555;color:#cccccc;'>{item['type']}</td>
                    <td style='padding:8px;border:1px solid #555;color:#cccccc;'>{item['best_for']}</td>
                    <td style='padding:8px;border:1px solid #555;color:#cccccc;'>{item['tradeoff']}</td>
                </tr>
                """
                for item in suggestions
            )
            panel_html = f"""
            <div style='margin-top:12px;padding:12px;border:1px solid #8b0000;border-radius:6px;background:#2b1f1f;'>
                <div style='color:#ff6b6b;font-size:13px;font-weight:700;margin-bottom:8px;'>
                    Recommended Alternatives for This Grammar
                </div>
                <table style='border-collapse:collapse;width:100%;font-size:11px;'>
                    <thead>
                        <tr style='background:#3a2a2a;'>
                            <th style='padding:8px;border:1px solid #555;color:#ffd1d1;'>Parser</th>
                            <th style='padding:8px;border:1px solid #555;color:#ffd1d1;'>Category</th>
                            <th style='padding:8px;border:1px solid #555;color:#ffd1d1;'>Best Use</th>
                            <th style='padding:8px;border:1px solid #555;color:#ffd1d1;'>Trade-off</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
            """
            self.conflict_text.insertHtml(panel_html)
            self.conflict_text.setStyleSheet("""
                QTextEdit {
                    background-color: #2D2D2D;
                    color: #F44336;
                    border: 2px solid #404040;
                    border-radius: 4px;
                    padding: 5px;
                    font-family: 'Consolas', monospace;
                    font-size: 10px;
                }
            """)
        else:
            self.conflict_text.clear()
            self.conflict_text.append("✓ No conflicts detected. Grammar is LL(1)!")
            self.conflict_text.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 12px;")


class ParseTraceWidget(QWidget):
    """Widget for displaying parse trace"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Input section
        input_group = QGroupBox("Input String")
        input_group.setStyleSheet("""
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        input_layout = QHBoxLayout()
        
        self.input_line = QTextEdit()
        self.input_line.setMaximumHeight(60)
        self.input_line.setPlaceholderText("Enter string to parse... (e.g., id + id * id)")
        self.input_line.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 2px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        
        self.parse_btn = QPushButton("▶ Parse String")
        self.parse_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.parse_btn)
        input_group.setLayout(input_layout)
        
        # Trace display
        trace_group = QGroupBox("Parse Trace")
        trace_group.setStyleSheet("""
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        trace_layout = QVBoxLayout()
        
        self.trace_text = QTextEdit()
        self.trace_text.setReadOnly(True)
        self.trace_text.setFont(QFont("Consolas", 10))
        self.trace_text.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #BA68C8;
                border: 2px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
            }
        """)
        
        trace_layout.addWidget(self.trace_text)
        trace_group.setLayout(trace_layout)
        
        layout.addWidget(input_group)
        layout.addWidget(trace_group)
        self.setLayout(layout)
        
    def set_trace(self, steps):
        self.trace_text.clear()
        for step in steps:
            self.trace_text.append(step)


class SymbolTableWidget(QWidget):
    """Widget for displaying symbol table"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Value", "Line", "Scope"])
        self.table.setStyleSheet("""
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
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
        
    def update_table(self, symbols):
        self.table.setRowCount(len(symbols))
        
        for i, symbol in enumerate(symbols):
            self.table.setItem(i, 0, QTableWidgetItem(symbol['name']))
            self.table.setItem(i, 1, QTableWidgetItem(symbol['type']))
            self.table.setItem(i, 2, QTableWidgetItem(str(symbol['value'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(symbol['line'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(symbol['scope_level'])))
        
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)


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
        self.setBackgroundBrush(QBrush(QColor(45, 45, 45)))
        
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
        self.setPos(x, y)
        self.children = []
        self.parent_node = parent
        
        # Calculate size based on text
        font = QFont("Consolas", 10, QFont.Bold)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(value) + 30
        text_height = fm.height() + 20
        self.rect = QRectF(-text_width/2, -text_height/2, text_width, text_height)
        self.setAcceptHoverEvents(True)
        self.is_hovered = False
        
    def boundingRect(self):
        return self.rect
    
    def paint(self, painter, option, widget):
        # Draw node background
        if self.is_hovered:
            painter.setPen(QPen(QColor("#FF4081"), 3))
        else:
            painter.setPen(QPen(QColor("#2196F3"), 2))
        
        # Different colors for terminals and non-terminals
        if self.value and self.value[0].isupper() if self.value else False:
            painter.setBrush(QBrush(QColor("#64B5F6")))  # Non-terminal
        else:
            painter.setBrush(QBrush(QColor("#81C784")))  # Terminal
            
        painter.drawRoundedRect(self.rect, 10, 10)
        
        # Draw text
        painter.setPen(QPen(QColor("#FFFFFF"), 1))
        painter.setFont(QFont("Consolas", 10, QFont.Bold))
        painter.drawText(self.rect, Qt.AlignCenter, self.value)
        
    def hoverEnterEvent(self, event):
        self.is_hovered = True
        self.update()
        
    def hoverLeaveEvent(self, event):
        self.is_hovered = False
        self.update()
        
    def add_child(self, child_item):
        self.children.append(child_item)


class ParseTreeWidget(QWidget):
    """Widget for displaying parse tree"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_tree_string = ""
        self.current_parse_tree = None
        self.node_items = []
        self.edge_items = []
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Control buttons
        control_group = QGroupBox("Tree Controls")
        control_group.setStyleSheet("""
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        control_layout = QHBoxLayout()
        
        self.zoom_in_btn = QPushButton("🔍+ Zoom In")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_in_btn.setStyleSheet("""
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
        """)
        
        self.zoom_out_btn = QPushButton("🔍- Zoom Out")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.zoom_out_btn.setStyleSheet("""
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
        """)
        
        self.fit_btn = QPushButton("↔ Fit to Window")
        self.fit_btn.clicked.connect(self.fit_to_view)
        self.fit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.refresh_btn = QPushButton("⟳ Refresh")
        self.refresh_btn.clicked.connect(self.refresh_tree)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        control_layout.addWidget(self.zoom_in_btn)
        control_layout.addWidget(self.zoom_out_btn)
        control_layout.addWidget(self.fit_btn)
        control_layout.addWidget(self.refresh_btn)
        control_layout.addStretch()
        control_group.setLayout(control_layout)
        
        # Tree display area
        display_group = QGroupBox("Parse Tree Visualization")
        display_group.setStyleSheet("""
            QGroupBox {
                color: #FFFFFF;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        display_layout = QVBoxLayout()
        
        self.graphics_view = ParseTreeGraphicsView()
        
        # Text representation
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Consolas", 10))
        self.text_display.setMaximumHeight(250)
        self.text_display.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #BA68C8;
                border: 2px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
            }
        """)
        self.text_display.hide()
        
        display_layout.addWidget(self.graphics_view)
        display_layout.addWidget(self.text_display)
        display_group.setLayout(display_layout)
        
        # Toggle button
        self.toggle_view_btn = QPushButton("📝 Show Text View")
        self.toggle_view_btn.clicked.connect(self.toggle_view)
        self.toggle_view_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        
        layout.addWidget(control_group)
        layout.addWidget(display_group)
        layout.addWidget(self.toggle_view_btn)
        
        self.setLayout(layout)
        
        self.show_graphics = True
        
    def set_tree(self, tree_string, parse_tree=None):
        """Set and display parse tree. Use parse_tree object for accurate visual when available."""
        self.current_tree_string = tree_string
        self.current_parse_tree = parse_tree
        
        # Clear previous scene
        self.graphics_view.scene.clear()
        self.node_items = []
        self.edge_items = []
        
        # Build graphical tree from actual structure when available
        if parse_tree and parse_tree.root:
            self.build_tree_from_object(parse_tree.root)
        else:
            self.create_graphical_tree(tree_string)
        
        # Set text representation
        self.text_display.clear()
        self.text_display.append(tree_string)
        
        # Fit to view
        self.fit_to_view()
        
    def _count_leaves(self, node):
        """Count leaf nodes under this node for layout spacing"""
        if not node.children:
            return 1
        return sum(self._count_leaves(child) for child in node.children)
    
    def build_tree_from_object(self, root_node, center_x=400, y=50, x_spacing=120, y_spacing=80):
        """Build graphical tree from ParseTree/ParseTreeNode structure recursively"""
        if root_node is None:
            return None
        
        # Create root graphics item (ensure value is displayable)
        node_value = str(root_node.value) if root_node.value else "ε"
        root_item = TreeNodeItem(node_value, center_x, y)
        self.graphics_view.scene.addItem(root_item)
        self.node_items.append(root_item)
        
        if not root_node.children:
            return root_item
        
        # Calculate total width needed for children
        child_widths = [self._count_leaves(c) for c in root_node.children]
        total_width = sum(child_widths) * x_spacing
        start_x = center_x - total_width / 2 + x_spacing / 2
        
        pen = QPen(QColor("#888888"), 2, Qt.SolidLine)
        
        for i, child_node in enumerate(root_node.children):
            # Position child at center of its subtree's span
            child_span = child_widths[i] * x_spacing
            child_center_x = start_x + child_span / 2
            start_x += child_span
            
            child_y = y + y_spacing
            
            # Recursively build child subtree
            child_item = self._add_tree_node(child_node, child_center_x, child_y, x_spacing, y_spacing)
            if child_item:
                root_item.add_child(child_item)
                # Draw edge from parent to child
                line = self.graphics_view.scene.addLine(
                    center_x, y + 20,
                    child_center_x, child_y - 20,
                    pen
                )
                self.edge_items.append(line)
        
        return root_item
    
    def _add_tree_node(self, node, x, y, x_spacing, y_spacing):
        """Recursively add a tree node and its children"""
        if node is None:
            return None
        
        node_value = str(node.value) if node.value else "ε"
        item = TreeNodeItem(node_value, x, y)
        self.graphics_view.scene.addItem(item)
        self.node_items.append(item)
        
        if not node.children:
            return item
        
        child_widths = [self._count_leaves(c) for c in node.children]
        total_width = sum(child_widths) * x_spacing
        start_x = x - total_width / 2 + x_spacing / 2
        
        pen = QPen(QColor("#888888"), 2, Qt.SolidLine)
        
        for i, child_node in enumerate(node.children):
            child_span = child_widths[i] * x_spacing
            child_center_x = start_x + child_span / 2
            start_x += child_span
            child_y = y + y_spacing
            
            child_item = self._add_tree_node(child_node, child_center_x, child_y, x_spacing, y_spacing)
            if child_item:
                item.add_child(child_item)
                line = self.graphics_view.scene.addLine(
                    x, y + 20,
                    child_center_x, child_y - 20,
                    pen
                )
                self.edge_items.append(line)
        
        return item
    
    def create_graphical_tree(self, tree_string):
        """Create graphical tree from string representation (fallback when no parse tree object)"""
        lines = tree_string.split('\n')
        if len(lines) < 3:
            # Add a sample tree for demonstration
            self.create_sample_tree()
            return
        
        # Find root node
        root_node = None
        root_line = ""
        for line in lines:
            if '└──' in line and '→' in line:
                root_line = line
                break
        
        if root_line:
            # Extract root value
            root_value = root_line.split('→')[0].strip().replace('└──', '').strip()
            if root_value:
                # Create root node at center top
                root_item = TreeNodeItem(root_value, 400, 50)
                self.graphics_view.scene.addItem(root_item)
                self.node_items.append(root_item)
                
                # Parse the rest of the tree
                self._parse_tree_levels(lines, 1, root_item, 400, 50, 150, 80)
        
    def _parse_tree_levels(self, lines, start_idx, parent_item, parent_x, parent_y, x_offset, y_offset):
        """Parse tree levels recursively"""
        level_nodes = []
        current_level = -1
        
        for i in range(start_idx, len(lines)):
            line = lines[i]
            if '├──' in line or '└──' in line:
                # Determine level by indentation
                level = line.count('│') + line.count('   ')
                if current_level == -1:
                    current_level = level
                
                if level == current_level:
                    # Extract node value
                    if '→' in line:
                        node_value = line.split('→')[0].strip().replace('├──', '').replace('└──', '').replace('│', '').strip()
                    else:
                        node_value = line.replace('├──', '').replace('└──', '').replace('│', '').strip()
                    
                    if node_value:
                        level_nodes.append(node_value)
        
        # Create child nodes
        if level_nodes:
            num_children = len(level_nodes)
            start_x = parent_x - (num_children - 1) * x_offset / 2
            
            for i, node_value in enumerate(level_nodes):
                child_x = start_x + i * x_offset
                child_y = parent_y + y_offset
                
                # Create child node
                child_item = TreeNodeItem(node_value, child_x, child_y)
                self.graphics_view.scene.addItem(child_item)
                self.node_items.append(child_item)
                parent_item.add_child(child_item)
                
                # Draw edge from parent to child
                pen = QPen(QColor("#888888"), 2, Qt.SolidLine)
                line = self.graphics_view.scene.addLine(
                    parent_x, parent_y + 20,
                    child_x, child_y - 20,
                    pen
                )
                self.edge_items.append(line)
        
    def create_sample_tree(self):
        """Create a sample tree for demonstration"""
        # Create root
        root = TreeNodeItem("E", 400, 50)
        self.graphics_view.scene.addItem(root)
        self.node_items.append(root)
        
        # Create children
        child1 = TreeNodeItem("T", 300, 150)
        child2 = TreeNodeItem("E'", 500, 150)
        self.graphics_view.scene.addItem(child1)
        self.graphics_view.scene.addItem(child2)
        self.node_items.extend([child1, child2])
        root.add_child(child1)
        root.add_child(child2)
        
        # Draw edges
        pen = QPen(QColor("#888888"), 2, Qt.SolidLine)
        self.graphics_view.scene.addLine(400, 70, 300, 130, pen)
        self.graphics_view.scene.addLine(400, 70, 500, 130, pen)
        
        # Add grandchildren
        child1_1 = TreeNodeItem("F", 250, 250)
        child1_2 = TreeNodeItem("T'", 350, 250)
        self.graphics_view.scene.addItem(child1_1)
        self.graphics_view.scene.addItem(child1_2)
        self.node_items.extend([child1_1, child1_2])
        child1.add_child(child1_1)
        child1.add_child(child1_2)
        
        self.graphics_view.scene.addLine(300, 170, 250, 230, pen)
        self.graphics_view.scene.addLine(300, 170, 350, 230, pen)
        
    def refresh_tree(self):
        """Refresh the tree display"""
        if self.current_tree_string:
            self.set_tree(self.current_tree_string, self.current_parse_tree)
        else:
            self.create_sample_tree()
        
    def zoom_in(self):
        self.graphics_view.scale(1.2, 1.2)
        
    def zoom_out(self):
        self.graphics_view.scale(1/1.2, 1/1.2)
        
    def fit_to_view(self):
        if self.graphics_view.scene.items():
            self.graphics_view.fitInView(self.graphics_view.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        
    def toggle_view(self):
        """Toggle between graphics and text view"""
        self.show_graphics = not self.show_graphics
        if self.show_graphics:
            self.graphics_view.show()
            self.text_display.hide()
            self.toggle_view_btn.setText("📝 Show Text View")
        else:
            self.graphics_view.hide()
            self.text_display.show()
            self.toggle_view_btn.setText("🎨 Show Graphics View")


# Export all widget classes
__all__ = [
    'GrammarInputWidget',
    'FirstFollowWidget', 
    'ParsingTableWidget',
    'ParseTraceWidget',
    'SymbolTableWidget',
    'ParseTreeWidget'
]