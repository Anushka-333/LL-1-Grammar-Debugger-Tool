"""Helper functions and utilities - FIXED"""

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def format_grammar(grammar):
    """Format grammar for display"""
    formatted = []
    for lhs, rhs in grammar.items():
        productions = ' | '.join([' '.join(p) if isinstance(p, list) else p for p in rhs])
        formatted.append(f"{lhs} → {productions}")
    return '\n'.join(formatted)


def _normalize_production_symbol(prod):
    """Parse a production string into list of symbols. Supports any CFG format."""
    prod = prod.strip()
    if not prod:
        return []
    
    # Epsilon handling - multiple notations
    if prod.lower() in ('ε', 'epsilon', 'e', 'eps', 'null', 'lambda', 'λ'):
        return ['ε']
    
    symbols = []
    current = ""
    in_single_quote = False
    in_double_quote = False
    
    # Special characters that form single-symbol terminals (operators, punctuation)
    SPECIAL_CHARS = set('+ * ( ) - / = < > [ ] { } ; : , . & | ! ? @ # $ % ^ ~ `')
    
    for i, char in enumerate(prod):
        if in_double_quote:
            if char == '"':
                if current:
                    symbols.append(current)
                    current = ""
                in_double_quote = False
            else:
                current += char
            continue
        if in_single_quote:
            if char == "'":
                if current:
                    symbols.append(current)
                    current = ""
                in_single_quote = False
            else:
                current += char
            continue
        if char == '"':
            if current:
                symbols.append(current)
                current = ""
            in_double_quote = True
            continue
        if char == "'":
            if current:
                symbols.append(current)
                current = ""
            in_single_quote = True
            continue
        if char == ' ':
            if current:
                symbols.append(current)
                current = ""
            continue
        if char in SPECIAL_CHARS:
            if current:
                symbols.append(current)
                current = ""
            symbols.append(char)
            continue
        current += char
    
    if current:
        symbols.append(current)
    
    return [s for s in symbols if s]


def validate_grammar_input(grammar_text):
    """
    Validate and parse grammar input. Supports multiple CFG formats:
    - Arrows: ->, ::=, →, :=
    - Epsilon: ε, epsilon, e, eps, λ
    - Terminals: +, *, (, ), -, /, =, ; etc. or quoted "id" 'num'
    - Non-terminals: Start with uppercase (e.g., E, Expr, STMT)
    """
    lines = grammar_text.strip().split('\n')
    grammar = {}
    
    # Support multiple arrow notations (order matters: longer patterns first)
    ARROW_PATTERNS = ['::=', '->', '→', ':=']
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Find which arrow is used
        arrow = None
        arrow_pos = -1
        for ap in ARROW_PATTERNS:
            if ap in line:
                arrow_pos = line.find(ap)
                arrow = ap
                break
        
        if arrow is None:
            raise ValueError(f"Line {line_num}: Missing production arrow (use -> or ::=)")
        
        lhs = line[:arrow_pos].strip()
        rhs = line[arrow_pos + len(arrow):].strip()
        
        if not lhs:
            raise ValueError(f"Line {line_num}: Empty left-hand side")
        
        # Non-terminal: uppercase first letter (supports multi-char like Expr, STMT)
        if not lhs[0].isupper():
            raise ValueError(f"Line {line_num}: Non-terminal must start with uppercase: {lhs}")
        
        if not rhs:
            raise ValueError(f"Line {line_num}: No productions after arrow")
        
        productions = []
        for prod in rhs.split('|'):
            symbols = _normalize_production_symbol(prod)
            if symbols:
                productions.append(symbols)
        
        if not productions:
            raise ValueError(f"Line {line_num}: No valid productions found")
        
        grammar[lhs] = productions
        
    if not grammar:
        raise ValueError("No valid grammar productions found")
    
    return grammar


def get_parser_suggestions_for_non_ll1():
    """Return professional parser recommendations for non-LL(1) grammars."""
    return [
        {
            "name": "SLR(1)",
            "type": "Bottom-up (LR family)",
            "best_for": "Many practical programming-language grammars",
            "tradeoff": "Simpler tables than LR(1), but less powerful than CLR(1)",
        },
        {
            "name": "LALR(1)",
            "type": "Bottom-up (LR family)",
            "best_for": "Production compilers and parser generators (Yacc/Bison style)",
            "tradeoff": "Good balance of power and table size",
        },
        {
            "name": "CLR(1) / Canonical LR(1)",
            "type": "Bottom-up (LR family)",
            "best_for": "Complex grammars requiring full LR(1) power",
            "tradeoff": "Most powerful, but larger parsing tables",
        },
        {
            "name": "General Bottom-up Shift-Reduce",
            "type": "Bottom-up",
            "best_for": "Cases where predictive LL parsing is unsuitable",
            "tradeoff": "Typically more implementation complexity than LL(1)",
        },
        {
            "name": "Earley",
            "type": "General CFG parser",
            "best_for": "Any context-free grammar (including ambiguous and non-LL/LR)",
            "tradeoff": "Slower (O(n^3) worst-case) but guarantees recognition for CFG",
        },
    ]