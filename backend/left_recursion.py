"""Left recursion detection and elimination module - FIXED"""

class LeftRecursionEliminator:
    def __init__(self, grammar):
        self.original_grammar = grammar.copy()
        self.grammar = grammar.copy()
        self.steps = []
        self.non_terminals = list(grammar.keys())
        
    def detect_left_recursion(self):
        """Detect immediate and indirect left recursion"""
        immediate = {}
        indirect = {}
        
        for non_terminal in self.grammar:
            immediate_recursions = []
            for production in self.grammar[non_terminal]:
                if production and production[0] == non_terminal:
                    immediate_recursions.append(production)
            
            if immediate_recursions:
                immediate[non_terminal] = immediate_recursions
        
        # Detect indirect left recursion (simplified)
        for nt in self.grammar:
            for production in self.grammar[nt]:
                if production and production[0] in self.grammar:
                    first_symbol = production[0]
                    if first_symbol != nt:
                        # Check if first_symbol can derive nt
                        if self._derives_to(first_symbol, nt, [nt]):
                            if nt not in indirect:
                                indirect[nt] = []
                            indirect[nt].append(production)
        
        return immediate, indirect
    
    def _derives_to(self, start, target, visited):
        """Check if start can derive target"""
        if start == target:
            return True
        
        if start not in self.grammar:
            return False
            
        for production in self.grammar[start]:
            if production and production[0] in self.grammar:
                if production[0] not in visited:
                    if self._derives_to(production[0], target, visited + [production[0]]):
                        return True
        return False
    
    def eliminate_left_recursion(self):
        """Eliminate left recursion from grammar"""
        self.steps = []
        self.steps.append("Starting left recursion elimination...")
        
        # First, handle immediate left recursion for each non-terminal
        for nt in self.non_terminals:
            self._eliminate_immediate_left_recursion(nt)
        
        # Then handle indirect left recursion by ordering non-terminals
        self._eliminate_indirect_left_recursion()
        
        return self.grammar, self.steps
    
    def _eliminate_immediate_left_recursion(self, non_terminal):
        """Eliminate immediate left recursion for a non-terminal"""
        if non_terminal not in self.grammar:
            return
            
        alpha = []  # Productions with left recursion (A → Aα)
        beta = []   # Productions without left recursion (A → β)
        
        for production in self.grammar[non_terminal]:
            if production and production[0] == non_terminal:
                # This is left recursive: A → Aα
                alpha.append(production[1:])  # Remove the first A
            else:
                # This is not left recursive: A → β
                beta.append(production)
        
        if alpha:
            # Create new non-terminal
            new_nt = non_terminal + "'"
            
            # Create new productions for original non-terminal: A → βA'
            self.grammar[non_terminal] = []
            for b in beta:
                if b == ['ε']:
                    self.grammar[non_terminal].append([new_nt])
                else:
                    self.grammar[non_terminal].append(b + [new_nt])
            
            # Create productions for new non-terminal: A' → αA' | ε
            self.grammar[new_nt] = []
            for a in alpha:
                self.grammar[new_nt].append(a + [new_nt])
            self.grammar[new_nt].append(['ε'])  # Epsilon production
            
            # Add steps
            self.steps.append(f"\nEliminating left recursion for {non_terminal}:")
            self.steps.append(f"  Left recursive productions: {non_terminal} → {' | '.join([non_terminal + ' ' + ' '.join(a) for a in alpha])}")
            self.steps.append(f"  Non-left recursive productions: {non_terminal} → {' | '.join([' '.join(b) for b in beta])}")
            self.steps.append(f"  Created new non-terminal: {new_nt}")
            self.steps.append(f"  New productions:")
            self.steps.append(f"    {non_terminal} → {' | '.join([' '.join(p) for p in self.grammar[non_terminal]])}")
            self.steps.append(f"    {new_nt} → {' | '.join([' '.join(p) for p in self.grammar[new_nt]])}")
    
    def _eliminate_indirect_left_recursion(self):
        """Eliminate indirect left recursion by ordering non-terminals"""
        # Reorder non-terminals to break indirect recursion
        n = len(self.non_terminals)
        
        for i in range(n):
            for j in range(i):
                nt_i = self.non_terminals[i]
                nt_j = self.non_terminals[j]
                
                if nt_i in self.grammar and nt_j in self.grammar:
                    new_productions = []
                    changed = False
                    
                    for production in self.grammar[nt_i]:
                        if production and production[0] == nt_j:
                            # Replace A_i → A_j γ with A_i → δγ for all A_j → δ
                            changed = True
                            for prod_j in self.grammar[nt_j]:
                                new_prod = prod_j + production[1:]
                                new_productions.append(new_prod)
                                self.steps.append(f"  Replaced {nt_i} → {' '.join(production)} with {nt_i} → {' '.join(new_prod)}")
                        else:
                            new_productions.append(production)
                    
                    if changed:
                        self.grammar[nt_i] = new_productions
                        
                        # Check for new immediate left recursion
                        self._eliminate_immediate_left_recursion(nt_i)