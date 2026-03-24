"""LL(1) Parsing Table generation module - FIXED"""

class ParsingTable:
    def __init__(self, grammar, first, follow):
        self.grammar = grammar
        self.first = first
        self.follow = follow
        self.non_terminals = list(grammar.keys())
        self.terminals = self._extract_terminals()
        self.table = {}
        self.conflicts = []
        
    def _extract_terminals(self):
        """Extract terminals from grammar"""
        terminals = set()
        for productions in self.grammar.values():
            for production in productions:
                for symbol in production:
                    if symbol != 'ε' and not (symbol[0].isupper() if symbol else False):
                        terminals.add(symbol)
        terminals.add('$')
        return sorted(terminals)
    
    def generate_table(self):
        """Generate LL(1) parsing table"""
        self.table = {}
        self.conflicts = []
        
        for nt in self.non_terminals:
            for production in self.grammar[nt]:
                # Get First set of the production
                first_prod = self._first_of_string(production)
                
                # For each terminal in First(production), add entry
                for terminal in first_prod:
                    if terminal != 'ε':
                        self._add_entry(nt, terminal, production)
                
                # If ε in First(production), add entries for terminals in Follow(nt)
                if 'ε' in first_prod:
                    for terminal in self.follow[nt]:
                        self._add_entry(nt, terminal, production)
        
        return self.table, self.conflicts
    
    def _first_of_string(self, string):
        """Compute First set of a string of symbols"""
        if not string or string == ['ε']:
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
    
    def _add_entry(self, nt, terminal, production):
        """Add entry to parsing table and detect conflicts"""
        key = (nt, terminal)
        
        # Format production for display
        prod_display = ' '.join(production) if production != ['ε'] else 'ε'
        
        if key not in self.table:
            self.table[key] = production
        else:
            # Check if it's a real conflict or just duplicate entry
            existing_prod = self.table[key]
            if existing_prod != production:
                # Real conflict detected
                conflict_info = {
                    'cell': key,
                    'existing': existing_prod,
                    'new': production,
                    'type': 'Multiple entries'
                }
                self.conflicts.append(conflict_info)
                # Store both for conflict display
                self.table[key] = [existing_prod, production]
    
    def is_ll1(self):
        """Check if grammar is LL(1)"""
        return len(self.conflicts) == 0
    
    def format_table(self):
        """Format parsing table for display"""
        if not self.table:
            return "Table not generated yet."
        
        result = "LL(1) PARSING TABLE:\n" + "="*80 + "\n"
        
        # Create header
        header = "Non-Terminal | " + " | ".join(f"{t:^10}" for t in self.terminals)
        result += header + "\n"
        result += "-" * len(header) + "\n"
        
        # Add rows
        for nt in self.non_terminals:
            row = f"{nt:^12} | "
            for term in self.terminals:
                key = (nt, term)
                if key in self.table:
                    entry = self.table[key]
                    if isinstance(entry, list):
                        # Conflict
                        row += f"{'CONFLICT':^10} | "
                    else:
                        prod_str = ' '.join(entry) if entry != ['ε'] else 'ε'
                        row += f"{prod_str:^10} | "
                else:
                    row += f"{'':^10} | "
            result += row + "\n"
        
        if self.conflicts:
            result += "\nCONFLICTS DETECTED:\n" + "="*50 + "\n"
            for i, conflict in enumerate(self.conflicts, 1):
                nt, term = conflict['cell']
                result += f"{i}. Cell [{nt}, {term}]:\n"
                result += f"   Existing: {' '.join(conflict['existing'])}\n"
                result += f"   New: {' '.join(conflict['new'])}\n"
        
        return result