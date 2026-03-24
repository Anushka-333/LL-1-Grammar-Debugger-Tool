"""Main window for the LL(1) Grammar Debugger"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QPushButton, QLabel, QStatusBar,
                             QMessageBox, QFileDialog, QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from gui.widgets import (GrammarInputWidget, FirstFollowWidget, ParsingTableWidget,ParseTraceWidget, SymbolTableWidget, ParseTreeWidget)
import sys
import os

# Fix imports - use absolute imports
from gui.styles import Colors, get_dark_palette, get_stylesheet
from gui.widgets import (GrammarInputWidget, FirstFollowWidget, ParsingTableWidget,
                     ParseTraceWidget, SymbolTableWidget, ParseTreeWidget)
from backend.grammar_analyzer import GrammarAnalyzer
from backend.symbol_table import SymbolTable
from backend.parse_tree import ParseTreeGenerator
from gui.celebration_overlay import CelebrationOverlay


class AnalysisThread(QThread):
    """Thread for running grammar analysis"""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, grammar_text, remove_left_recursion=False):
        super().__init__()
        self.grammar_text = grammar_text
        self.remove_left_recursion = remove_left_recursion
        
    def run(self):
        try:
            analyzer = GrammarAnalyzer(self.grammar_text)
            result = analyzer.analyze(remove_left_recursion=self.remove_left_recursion)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()
        self.current_grammar = None
        self.parsing_table = {}
        self.last_grammar_text = ""
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("LL(1) Grammar Debugger & Parser")
        self.setGeometry(100, 100, 1400, 900)
        
        # Apply dark theme
        self.setPalette(get_dark_palette())
        self.setStyleSheet(get_stylesheet())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Grammar tab
        self.grammar_widget = GrammarInputWidget()
        self.grammar_widget.grammar_changed.connect(self.on_grammar_changed)
        self.tab_widget.addTab(self.grammar_widget, "📝 Grammar")
        
        # First/Follow tab
        self.first_follow_widget = FirstFollowWidget()
        self.tab_widget.addTab(self.first_follow_widget, "📊 First & Follow")
        
        # Parsing Table tab
        self.parsing_table_widget = ParsingTableWidget()
        self.tab_widget.addTab(self.parsing_table_widget, "📋 Parsing Table")
        
        # Parse Trace tab
        self.parse_trace_widget = ParseTraceWidget()
        self.parse_trace_widget.parse_btn.clicked.connect(self.on_parse_with_tree)
        self.tab_widget.addTab(self.parse_trace_widget, "▶️ Parse Trace")
        
        # Parse Tree tab
        self.parse_tree_widget = ParseTreeWidget()
        self.tab_widget.addTab(self.parse_tree_widget, "🌳 Parse Tree")
        
        # Symbol Table tab
        self.symbol_table_widget = SymbolTableWidget()
        self.tab_widget.addTab(self.symbol_table_widget, "📚 Symbol Table")
        
        main_layout.addWidget(self.tab_widget)
        
        # Celebration overlay (for parse success)
        self.celebration_overlay = CelebrationOverlay(central_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton("🔍 Analyze Grammar")
        self.analyze_btn.clicked.connect(self.analyze_grammar)
        self.analyze_btn.setStyleSheet(f"background-color: {Colors.PRIMARY};")
        
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.clicked.connect(self.clear_all)

        self.remove_recursion_btn = QPushButton("♻ Remove Recursion")
        self.remove_recursion_btn.clicked.connect(self.remove_left_recursion)
        self.remove_recursion_btn.setEnabled(False)
        self.remove_recursion_btn.setStyleSheet(f"background-color: {Colors.WARNING}; color: #000000;")
        
        self.save_btn = QPushButton("💾 Save Results")
        self.save_btn.clicked.connect(self.save_results)
        
        button_layout.addWidget(self.analyze_btn)
        button_layout.addWidget(self.remove_recursion_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Initialize analysis thread
        self.analysis_thread = None
        
    def on_grammar_changed(self, text):
        """Handle grammar text changes"""
        self.status_bar.showMessage("Grammar modified - Click 'Analyze' to process")
        
    def analyze_grammar(self):
        """Analyze the grammar"""
        grammar_text = self.grammar_widget.input_text.toPlainText()
        
        if not grammar_text.strip():
            QMessageBox.warning(self, "Warning", "Please enter a grammar first!")
            return
        
        self.last_grammar_text = grammar_text

        # Disable analyze button
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("⏳ Analyzing...")
        self.remove_recursion_btn.setEnabled(False)
        self.status_bar.showMessage("Analyzing grammar...")
        
        # Start analysis in separate thread
        self.analysis_thread = AnalysisThread(grammar_text, remove_left_recursion=False)
        self.analysis_thread.finished.connect(self.on_analysis_finished)
        self.analysis_thread.error.connect(self.on_analysis_error)
        self.analysis_thread.start()

    def remove_left_recursion(self):
        """Analyze grammar with explicit left recursion removal"""
        grammar_text = self.grammar_widget.input_text.toPlainText().strip()
        if not grammar_text:
            QMessageBox.warning(self, "Warning", "Please enter a grammar first!")
            return

        self.analyze_btn.setEnabled(False)
        self.remove_recursion_btn.setEnabled(False)
        self.remove_recursion_btn.setText("⏳ Removing...")
        self.status_bar.showMessage("Removing left recursion and re-analyzing...")

        self.analysis_thread = AnalysisThread(grammar_text, remove_left_recursion=True)
        self.analysis_thread.finished.connect(self.on_analysis_finished)
        self.analysis_thread.error.connect(self.on_analysis_error)
        self.analysis_thread.start()
        
    def on_analysis_finished(self, result):
        """Handle analysis completion"""
        self.current_grammar = result['grammar']
        self.parsing_table = result['parsing_table']
        self.is_ll1 = result.get('is_ll1', False)
        
        # Update grammar display
        grammar_display = "PROCESSED GRAMMAR:\n" + "="*50 + "\n"
        for lhs, rhs in result['grammar'].items():
            productions = ' | '.join([' '.join(p) for p in rhs])
            grammar_display += f"{lhs} → {productions}\n"
        
        if result['left_recursion_removed']:
            grammar_display += "\n✓ Left recursion removed successfully!\n"
            for step in result['left_recursion_steps']:
                grammar_display += f"  {step}\n"
        elif result.get('has_left_recursion'):
            grammar_display += "\n⚠ Left recursion detected (not removed).\n"
            grammar_display += "  Use the 'Remove Recursion' button to transform grammar.\n"
        
        self.grammar_widget.set_display(grammar_display, Colors.GRAMMAR)
        
        # Update First/Follow
        self.first_follow_widget.update_sets(result['first'], result['follow'])
        
        # Update Parsing Table
        self.parsing_table_widget.update_table(
            result['parsing_table'],
            result['non_terminals'],
            result['terminals'],
            result['conflicts']
        )
        
        # Add some symbols to symbol table for demonstration
        self.symbol_table = SymbolTable()
        self.symbol_table.add_symbol("id", "identifier", None, 1)
        self.symbol_table.add_symbol("num", "number", None, 1)
        
        # Update Symbol Table
        self.symbol_table_widget.update_table(self.symbol_table.get_all_symbols())
        
        # Update status
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("🔍 Analyze Grammar")
        self.remove_recursion_btn.setText("♻ Remove Recursion")
        self.remove_recursion_btn.setEnabled(bool(result.get('has_left_recursion')))
        
        if result['is_ll1']:
            self.status_bar.showMessage("✓ Grammar is LL(1)!", 5000)
            self.status_bar.setStyleSheet(f"color: {Colors.SUCCESS};")
        else:
            self.status_bar.showMessage(f"✗ Grammar is not LL(1)! Found {len(result['conflicts'])} conflicts", 5000)
            self.status_bar.setStyleSheet(f"color: {Colors.ERROR};")
        
        # Switch to parsing table tab to show conflicts
        if result['conflicts']:
            self.tab_widget.setCurrentIndex(2)  # Parsing Table tab
            
    def on_analysis_error(self, error_msg):
        """Handle analysis error"""
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("🔍 Analyze Grammar")
        self.remove_recursion_btn.setEnabled(False)
        self.remove_recursion_btn.setText("♻ Remove Recursion")
        self.status_bar.showMessage("Analysis failed!")
        QMessageBox.critical(self, "Error", f"Analysis failed:\n{error_msg}")
        
    def on_parse_with_tree(self):
        """Parse input string and generate parse tree"""
        input_string = self.parse_trace_widget.input_line.toPlainText().strip()
        
        if not input_string:
            QMessageBox.warning(self, "Warning", "Please enter a string to parse!")
            return
        
        if not self.current_grammar:
            QMessageBox.warning(self, "Warning", "Please analyze a grammar first!")
            return
        
        # Get start symbol
        start_symbol = list(self.current_grammar.keys())[0]
        
        # Generate parse tree (LL(1) when possible, Earley for general CFGs)
        tree_gen = ParseTreeGenerator(self.current_grammar, self.parsing_table, getattr(self, 'is_ll1', False))
        steps, parse_tree = tree_gen.parse_with_tree(input_string, start_symbol)
        
        # Update parse trace
        self.parse_trace_widget.set_trace(steps)
        
        # Update parse tree display
        if parse_tree:
            tree_string = tree_gen.get_tree_string()
            self.parse_tree_widget.set_tree(tree_string, parse_tree)
            self.status_bar.showMessage("Parse tree generated!", 3000)
            
            # Show celebration if string was accepted
            if steps and "Accept!" in steps[-1]:
                self.celebration_overlay.setGeometry(self.centralWidget().rect())
                self.celebration_overlay.raise_()
                self.celebration_overlay.show_celebration()
        else:
            self.status_bar.showMessage("Failed to generate parse tree!", 3000)
        
    def clear_all(self):
        """Clear all widgets"""
        self.grammar_widget.input_text.clear()
        self.grammar_widget.display_text.clear()
        self.first_follow_widget.first_text.clear()
        self.first_follow_widget.follow_text.clear()
        self.parsing_table_widget.table.clear()
        self.parsing_table_widget.conflict_text.clear()
        self.parse_trace_widget.input_line.clear()
        self.parse_trace_widget.trace_text.clear()
        self.parse_tree_widget.graphics_view.scene.clear()
        self.parse_tree_widget.text_display.clear()
        self.parse_tree_widget.current_tree_string = ""
        self.parse_tree_widget.current_parse_tree = None
        self.symbol_table_widget.table.clear()
        self.current_grammar = None
        self.last_grammar_text = ""
        self.remove_recursion_btn.setEnabled(False)
        self.remove_recursion_btn.setText("♻ Remove Recursion")
        self.status_bar.showMessage("Cleared all data")
        
    def save_results(self):
        """Save analysis results to file"""
        if not self.current_grammar:
            QMessageBox.warning(self, "Warning", "No results to save!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Results", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("LL(1) GRAMMAR DEBUGGER RESULTS\n")
                    f.write("="*60 + "\n\n")
                    
                    # Grammar
                    f.write("GRAMMAR:\n")
                    f.write("-"*40 + "\n")
                    for lhs, rhs in self.current_grammar.items():
                        productions = ' | '.join([' '.join(p) for p in rhs])
                        f.write(f"{lhs} → {productions}\n")
                    
                self.status_bar.showMessage(f"Results saved to {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")