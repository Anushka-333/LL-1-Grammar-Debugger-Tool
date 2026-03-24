"""Parse Tree generation module - FIXED"""

class ParseTreeNode:
    """Node in parse tree"""
    def __init__(self, value):
        self.value = value
        self.children = []
        self.parent = None
        self.production = None
        
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        
    def is_leaf(self):
        return len(self.children) == 0
    
    def is_non_terminal(self):
        return self.value and self.value[0].isupper() if self.value else False
    
    def __str__(self):
        return self.value


class ParseTree:
    """Parse Tree for LL(1) parsing"""
    
    def __init__(self, root_symbol):
        self.root = ParseTreeNode(root_symbol)
        self.root.production = [root_symbol]
        self.current_node = self.root
        
    def expand_node(self, node, production):
        """Expand a node with its production"""
        if node and production:
            node.production = production
            for symbol in production:
                if symbol != 'ε':  # Don't add epsilon as child
                    child = ParseTreeNode(symbol)
                    node.add_child(child)
        
    def find_next_unexpanded_nonterminal(self):
        """Find the next unexpanded non-terminal in leftmost order"""
        from collections import deque
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            if node.is_non_terminal() and node.is_leaf():
                return node
            for child in node.children:
                queue.append(child)
        return None
    
    def get_tree_representation(self, node=None, prefix="", is_last=True, is_root=True):
        """Get string representation of parse tree"""
        if node is None:
            node = self.root
            
        result = ""
        
        # Add current node with proper formatting
        if is_root:
            result = "Parse Tree:\n" + "="*50 + "\n"
            result += f"└── {node.value}"
            if node.production and len(node.production) > 0:
                prod_str = ' '.join(node.production)
                result += f" → {prod_str}"
            result += "\n"
            
            # Process children
            for i, child in enumerate(node.children):
                is_last_child = (i == len(node.children) - 1)
                result += self.get_tree_representation(child, "    ", is_last_child, False)
        else:
            # Add connector
            connector = "└── " if is_last else "├── "
            result += f"{prefix}{connector}{node.value}"
            
            # Add production for non-terminals
            if node.is_non_terminal() and node.production and len(node.production) > 0:
                prod_str = ' '.join(node.production)
                result += f" → {prod_str}"
            result += "\n"
            
            # Process children
            for i, child in enumerate(node.children):
                is_last_child = (i == len(node.children) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                result += self.get_tree_representation(child, new_prefix, is_last_child, False)
        
        return result
    
    def to_ascii(self):
        """Convert tree to ASCII art"""
        return self.get_tree_representation()


class EarleyState:
    """A single Earley parser state"""

    __slots__ = ('lhs', 'rhs', 'dot', 'origin')

    def __init__(self, lhs, rhs, dot, origin):
        self.lhs = lhs
        self.rhs = tuple(rhs)
        self.dot = dot
        self.origin = origin

    def is_complete(self):
        return self.dot >= len(self.rhs)

    def next_symbol(self):
        if self.dot < len(self.rhs):
            return self.rhs[self.dot]
        return None

    def advance(self):
        return EarleyState(self.lhs, self.rhs, self.dot + 1, self.origin)

    def __hash__(self):
        return hash((self.lhs, self.rhs, self.dot, self.origin))

    def __eq__(self, other):
        return isinstance(other, EarleyState) and (self.lhs, self.rhs, self.dot, self.origin) == (other.lhs, other.rhs, other.dot, other.origin)

    def __repr__(self):
        rhs_display = ' '.join(self.rhs) if self.rhs else 'ε'
        return f"[{self.lhs} → {rhs_display[:self.dot]} · {rhs_display[self.dot:]}, {self.origin}]"


class EarleyParser:
    """General CFG parser using Earley algorithm"""

    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, input_tokens, start_symbol):
        chart = [set() for _ in range(len(input_tokens) + 1)]
        start = EarleyState('γ', [start_symbol], 0, 0)
        chart[0].add(start)
        steps = [f"Earley parsing start: {start_symbol}"]

        for i in range(len(chart)):
            added = True
            while added:
                added = False
                for state in list(chart[i]):
                    if not state.is_complete():
                        symbol = state.next_symbol()
                        if symbol in self.grammar:  # Predictor for non-terminal
                            for production in self.grammar[symbol]:
                                new_state = EarleyState(symbol, production, 0, i)
                                if new_state not in chart[i]:
                                    chart[i].add(new_state)
                                    steps.append(f"Predict {new_state} at chart[{i}]")
                                    added = True

                            # Handle epsilon production immediately
                            for production in self.grammar[symbol]:
                                if production == ['ε']:
                                    completed = EarleyState(symbol, production, 1, i)
                                    if completed not in chart[i]:
                                        chart[i].add(completed)
                                        steps.append(f"Complete epsilon {completed} at chart[{i}]")
                                        added = True

                        elif i < len(input_tokens) and symbol == input_tokens[i]:  # Scanner
                            next_state = state.advance()
                            if next_state not in chart[i + 1]:
                                chart[i + 1].add(next_state)
                                steps.append(f"Scan '{symbol}' at chart[{i}] → chart[{i+1}]")
                                added = True
                    else:
                        # Completer
                        for prev_state in list(chart[state.origin]):
                            if not prev_state.is_complete() and prev_state.next_symbol() == state.lhs:
                                advanced = prev_state.advance()
                                if advanced not in chart[i]:
                                    chart[i].add(advanced)
                                    steps.append(f"Complete {state.lhs}: advance {advanced} at chart[{i}]")
                                    added = True

        accepted = any(s.lhs == 'γ' and s.is_complete() and s.origin == 0 for s in chart[len(input_tokens)])
        steps.append("Input accepted" if accepted else "Input rejected")

        return accepted, steps


class ParseTreeGenerator:
    """Generate parse tree from parsing steps"""

    def __init__(self, grammar, parsing_table, is_ll1=True):
        self.grammar = grammar
        self.parsing_table = parsing_table
        self.is_ll1 = is_ll1
        self.parse_tree = None
        self.steps = []

    def parse_with_tree(self, input_string, start_symbol):
        """Parse input string using Earley algorithm for general CFGs"""
        return self._parse_earley_with_tree(input_string, start_symbol)

    def _parse_ll1_with_tree(self, input_string, start_symbol):
        # Tokenize input
        tokens = input_string.split()
        tokens.append('$')

        # Initialize parse tree
        self.parse_tree = ParseTree(start_symbol)

        # Initialize stack for parsing
        stack = ['$', start_symbol]

        # For tracking which node to expand
        node_stack = [self.parse_tree.root]

        index = 0
        steps = []

        steps.append("Starting LL(1) parse with tree generation...")
        steps.append(f"Stack: {' '.join(reversed(stack))}")
        steps.append(f"Input: {' '.join(tokens)}")
        steps.append("-" * 60)

        step_count = 1

        while stack:
            top = stack.pop()
            current_token = tokens[index]

            step_info = f"Step {step_count}: "
            step_info += f"Stack top: {top}, Current input: {current_token} | "

            if top == current_token:
                if top == '$':
                    steps.append(step_info + "Accept! String parsed successfully.")
                    break

                steps.append(step_info + f"Match {top}")
                index += 1

                if node_stack and node_stack[0].value == top:
                    node_stack.pop(0)

            elif top[0].isupper():
                key = (top, current_token)
                if key in self.parsing_table:
                    production = self.parsing_table[key]

                    if isinstance(production, list) and len(production) > 0 and isinstance(production[0], list):
                        production = production[0]

                    if node_stack:
                        current_node = node_stack.pop(0)
                        self.parse_tree.expand_node(current_node, production)

                        new_nodes = []
                        for sym in production:
                            if sym != 'ε' and sym[0].isupper():
                                for child in current_node.children:
                                    if child.value == sym:
                                        new_nodes.append(child)
                                        break

                        node_stack = new_nodes + node_stack

                    if production != ['ε']:
                        for sym in reversed(production):
                            stack.append(sym)

                    prod_str = ' '.join(production) if production != ['ε'] else 'ε'
                    steps.append(step_info + f"Apply {top} → {prod_str}")
                else:
                    steps.append(step_info + f"Error: No rule for ({top}, {current_token})")
                    break
            else:
                steps.append(step_info + f"Error: Expected {top}, found {current_token}")
                break

            step_count += 1

        self.steps = steps
        return steps, self.parse_tree

    def _parse_earley_with_tree(self, input_string, start_symbol):
        tokens = [t for t in input_string.split() if t != 'ε']
        parser = EarleyParser(self.grammar)
        accepted, steps = parser.parse(tokens, start_symbol)

        self.steps = ["Starting generalized Earley parse..."] + steps

        if accepted:
            # Create a more detailed parse tree by simulating the derivation
            self.parse_tree = ParseTree(start_symbol)
            # For now, add all tokens as children of root (approximate)
            for token in tokens:
                if token != 'ε':
                    child = ParseTreeNode(token)
                    self.parse_tree.root.add_child(child)
            self.steps.append("Parse tree constructed from accepted token sequence")
            return self.steps, self.parse_tree

        return self.steps, None

    def get_tree_string(self):
        """Get string representation of parse tree"""
        if self.parse_tree:
            return self.parse_tree.to_ascii()
        return "No parse tree generated."
    
    def get_tree_string(self):
        """Get string representation of parse tree"""
        if self.parse_tree:
            return self.parse_tree.to_ascii()
        return "No parse tree generated."