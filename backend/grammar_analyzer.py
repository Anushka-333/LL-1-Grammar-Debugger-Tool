"""Main grammar analyzer that coordinates all components - FIXED"""

from backend.left_recursion import LeftRecursionEliminator
from backend.first_follow import FirstFollow
from backend.parsing_table import ParsingTable
from utils.helpers import validate_grammar_input


class GrammarAnalyzer:
    def __init__(self, grammar_text):
        self.grammar_text = grammar_text
        self.grammar = None
        self.original_grammar = None
        self.non_terminals = []
        self.terminals = []
        self.first = {}
        self.follow = {}
        self.parsing_table = {}
        self.conflicts = []
        self.left_recursion_removed = False
        self.left_recursion_steps = []
        self.is_ll1 = False
        
    def analyze(self, remove_left_recursion=False):
        """Perform complete grammar analysis"""
        try:
            # Parse grammar input
            self.grammar = validate_grammar_input(self.grammar_text)
            self.original_grammar = self.grammar.copy()
            
            # Detect left recursion first
            eliminator = LeftRecursionEliminator(self.grammar)
            immediate, indirect = eliminator.detect_left_recursion()
            has_left_recursion = bool(immediate or indirect)
            
            if has_left_recursion and remove_left_recursion:
                self.grammar, self.left_recursion_steps = eliminator.eliminate_left_recursion()
                self.left_recursion_removed = True
            elif has_left_recursion:
                self.left_recursion_removed = False
                self.left_recursion_steps = [
                    "Left recursion detected. Click 'Remove Recursion' to transform grammar."
                ]
            else:
                self.left_recursion_steps = ["No left recursion detected in the grammar."]
            
            # Get non-terminals
            self.non_terminals = list(self.grammar.keys())
            
            # Compute First and Follow
            ff = FirstFollow(self.grammar)
            self.first = ff.compute_first()
            self.follow = ff.compute_follow()
            self.terminals = ff.terminals
            
            # Generate parsing table
            pt = ParsingTable(self.grammar, self.first, self.follow)
            self.parsing_table, self.conflicts = pt.generate_table()
            self.is_ll1 = pt.is_ll1()
            
            return self.get_results(immediate, indirect, has_left_recursion)
            
        except Exception as e:
            raise Exception(f"Grammar analysis failed: {str(e)}")
        
    def get_results(self, immediate_left_recursion=None, indirect_left_recursion=None, has_left_recursion=False):
        """Get all analysis results"""
        return {
            'original_grammar': self.original_grammar,
            'grammar': self.grammar,
            'non_terminals': self.non_terminals,
            'terminals': self.terminals,
            'first': self.first,
            'follow': self.follow,
            'parsing_table': self.parsing_table,
            'conflicts': self.conflicts,
            'is_ll1': self.is_ll1,
            'left_recursion_removed': self.left_recursion_removed,
            'left_recursion_steps': self.left_recursion_steps,
            'has_left_recursion': has_left_recursion,
            'immediate_left_recursion': immediate_left_recursion or {},
            'indirect_left_recursion': indirect_left_recursion or {},
        }