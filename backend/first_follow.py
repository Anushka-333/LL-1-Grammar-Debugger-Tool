"""First and Follow set computation module - FIXED"""

class FirstFollow:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = {}
        self.follow = {}
        self.non_terminals = list(grammar.keys())
        self.terminals = self._extract_terminals()
        
    def _extract_terminals(self):
        """Extract terminals from grammar"""
        terminals = set()
        for productions in self.grammar.values():
            for production in productions:
                for symbol in production:
                    if symbol != 'ε' and not (symbol[0].isupper() if symbol else False):
                        terminals.add(symbol)
        return sorted(terminals)
    
    def compute_first(self):
        """Compute First sets for all non-terminals"""
        # Initialize First sets
        for nt in self.non_terminals:
            self.first[nt] = set()
        
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for production in self.grammar[nt]:
                    # Case 1: Production is epsilon
                    if production == ['ε']:
                        if 'ε' not in self.first[nt]:
                            self.first[nt].add('ε')
                            changed = True
                        continue
                    
                    # Case 2: Production starts with terminal
                    if production[0] in self.terminals:
                        if production[0] not in self.first[nt]:
                            self.first[nt].add(production[0])
                            changed = True
                        continue
                    
                    # Case 3: Production starts with non-terminal
                    all_have_epsilon = True
                    for symbol in production:
                        if symbol in self.terminals:
                            if symbol not in self.first[nt]:
                                self.first[nt].add(symbol)
                            all_have_epsilon = False
                            break
                        else:  # Non-terminal
                            # Add First of symbol except epsilon
                            before_size = len(self.first[nt])
                            self.first[nt] |= (self.first[symbol] - {'ε'})
                            if len(self.first[nt]) > before_size:
                                changed = True
                            
                            # If this symbol doesn't have epsilon, stop
                            if 'ε' not in self.first[symbol]:
                                all_have_epsilon = False
                                break
                    
                    # If all symbols can derive epsilon, add epsilon
                    if all_have_epsilon and 'ε' not in self.first[nt]:
                        self.first[nt].add('ε')
                        changed = True
        
        return self.first
    
    def compute_follow(self):
        """Compute Follow sets for all non-terminals"""
        # Initialize Follow sets
        for nt in self.non_terminals:
            self.follow[nt] = set()
        
        # Add $ to follow of start symbol
        if self.non_terminals:
            start_symbol = self.non_terminals[0]
            self.follow[start_symbol].add('$')
        
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for production in self.grammar[nt]:
                    for i, symbol in enumerate(production):
                        if symbol in self.non_terminals:
                            # Case: A → αBβ
                            if i < len(production) - 1:
                                beta = production[i+1:]
                                first_beta = self._first_of_string(beta)
                                
                                # Add First(β) - {ε} to Follow(B)
                                before_size = len(self.follow[symbol])
                                self.follow[symbol] |= (first_beta - {'ε'})
                                if len(self.follow[symbol]) > before_size:
                                    changed = True
                                
                                # If ε in First(β), add Follow(A) to Follow(B)
                                if 'ε' in first_beta:
                                    before_size = len(self.follow[symbol])
                                    self.follow[symbol] |= self.follow[nt]
                                    if len(self.follow[symbol]) > before_size:
                                        changed = True
                            
                            # Case: A → αB (β is empty)
                            else:
                                before_size = len(self.follow[symbol])
                                self.follow[symbol] |= self.follow[nt]
                                if len(self.follow[symbol]) > before_size:
                                    changed = True
        
        return self.follow
    
    def _first_of_string(self, string):
        """Compute First set of a string of symbols"""
        if not string:
            return {'ε'}
        
        result = set()
        all_have_epsilon = True
        
        for symbol in string:
            if symbol in self.terminals:
                result.add(symbol)
                all_have_epsilon = False
                break
            else:  # Non-terminal
                result |= (self.first[symbol] - {'ε'})
                if 'ε' not in self.first[symbol]:
                    all_have_epsilon = False
                    break
        
        if all_have_epsilon:
            result.add('ε')
        
        return result
    
    def format_sets(self):
        """Format First and Follow sets for display"""
        result = "FIRST SETS:\n" + "="*50 + "\n"
        for nt in self.non_terminals:
            first_set = ', '.join(sorted(self.first[nt]))
            result += f"FIRST({nt}) = {{ {first_set} }}\n"
        
        result += "\nFOLLOW SETS:\n" + "="*50 + "\n"
        for nt in self.non_terminals:
            follow_set = ', '.join(sorted(self.follow[nt]))
            result += f"FOLLOW({nt}) = {{ {follow_set} }}\n"
        
        return result