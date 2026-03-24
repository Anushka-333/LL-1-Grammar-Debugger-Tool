"""Symbol Table management module"""

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scopes = [{}]
        
    def enter_scope(self):
        """Enter a new scope"""
        self.scopes.append({})
        
    def exit_scope(self):
        """Exit current scope"""
        if len(self.scopes) > 1:
            self.scopes.pop()
            
    def add_symbol(self, name, symbol_type, value=None, line_no=None):
        """Add symbol to current scope"""
        symbol = {
            'name': name,
            'type': symbol_type,
            'value': value,
            'line': line_no,
            'scope_level': len(self.scopes) - 1
        }
        
        # Add to current scope
        self.scopes[-1][name] = symbol
        
        # Also add to global symbol dictionary
        key = f"{name}_{len(self.scopes)-1}"
        self.symbols[key] = symbol
        
        return symbol
    
    def lookup(self, name, current_scope_only=False):
        """Look up symbol in symbol table"""
        if current_scope_only:
            return self.scopes[-1].get(name)
        
        # Search from innermost to outermost scope
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        
        return None
    
    def update_symbol(self, name, **kwargs):
        """Update symbol attributes"""
        symbol = self.lookup(name)
        if symbol:
            for key, value in kwargs.items():
                if key in symbol:
                    symbol[key] = value
            return True
        return False
    
    def get_all_symbols(self):
        """Get all symbols in table"""
        all_symbols = []
        for scope_level, scope in enumerate(self.scopes):
            for name, symbol in scope.items():
                symbol['scope_level'] = scope_level
                all_symbols.append(symbol)
        return all_symbols
    
    def format_table(self):
        """Format symbol table for display"""
        if not self.symbols and not any(self.scopes):
            return "Symbol table is empty."
        
        result = "SYMBOL TABLE:\n" + "="*80 + "\n"
        result += f"{'Name':<15} {'Type':<15} {'Value':<15} {'Line':<10} {'Scope':<10}\n"
        result += "-"*80 + "\n"
        
        for symbol in self.get_all_symbols():
            result += f"{symbol['name']:<15} {symbol['type']:<15} "
            result += f"{str(symbol['value']):<15} {str(symbol['line']):<10} "
            result += f"{symbol['scope_level']:<10}\n"
        
        return result