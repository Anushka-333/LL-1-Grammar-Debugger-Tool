# LL(1) Grammar Debugger & Parser

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive, interactive tool for analyzing, debugging, and parsing LL(1) grammars. Built with Python and PyQt5, this application provides a complete environment for compiler construction education and language processing tasks.

## 🎯 Overview

This tool bridges the gap between theoretical compiler design concepts and practical implementation. Whether you're a student learning about formal languages, a developer building parsers, or an educator teaching compiler construction, the LL(1) Grammar Debugger offers an intuitive interface to explore the intricacies of LL(1) parsing.

## ✨ Key Features

### 📝 Grammar Analysis & Validation
- **Interactive Grammar Input**: Enter grammars using standard BNF notation
- **Real-time Validation**: Automatic syntax checking and error highlighting
- **Built-in Examples**: Pre-loaded grammars for quick experimentation
- **Grammar Formatting**: Automatic cleanup and standardization

### 🔄 Left Recursion Handling
- **Detection Algorithms**: Identifies both immediate and indirect left recursion
- **Step-by-Step Elimination**: Visual walkthrough of the transformation process
- **Corrected Grammar Generation**: Automatic production of LL(1)-compatible grammars

### 📊 Set Computation Engine
- **FIRST Sets**: Automatic computation for all non-terminals and productions
- **FOLLOW Sets**: Complete follow set generation with dependency tracking
- **Interactive Display**: Color-coded, structured visualization of sets

### 📋 LL(1) Parsing Table
- **Conflict Detection**: Identifies and highlights parsing table conflicts
- **Resolution Suggestions**: Provides actionable advice for conflict resolution
- **Table Visualization**: Clear, organized display of parsing actions

### ⚡ Predictive Parser
- **Step-by-Step Execution**: Watch the parser work through input strings
- **Stack Visualization**: Real-time display of parser stack operations
- **Parse Tree Generation**: Automatic derivation tree construction
- **Error Recovery**: Intelligent handling of syntax errors

### 🏷️ Symbol Table Management
- **Scope Tracking**: Hierarchical symbol table with scope management
- **Attribute Storage**: Flexible storage for symbol properties
- **Lookup Operations**: Efficient symbol resolution and retrieval

### 🎨 Modern GUI
- **PyQt5 Interface**: Professional, responsive desktop application
- **Dark/Light Themes**: Customizable appearance
- **Tabbed Interface**: Organized workflow with multiple analysis views
- **Export Capabilities**: Save results and visualizations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anushka-333/LL-1-Grammar-Debugger-Tool.git
   cd LL-1-Grammar-Debugger-Tool
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 📖 Usage Examples

### Basic Grammar Analysis
1. Launch the application
2. Enter a grammar in the input panel:
   ```
   E → E + T | T
   T → T * F | F
   F → ( E ) | id
   ```
3. Click "Analyze Grammar" to validate and process
4. View FIRST/FOLLOW sets in the respective tabs

### Left Recursion Elimination
1. Input a left-recursive grammar
2. Navigate to the "Left Recursion" tab
3. Click "Detect & Eliminate" to see the transformation
4. Review the step-by-step process and corrected grammar

### Parsing Input Strings
1. After generating a valid parsing table
2. Go to the "Parser" tab
3. Enter an input string (e.g., `id + id * id`)
4. Click "Parse" to see the step-by-step derivation

## 🏗️ Architecture

```
LL(1) Grammar Debugger/
├── main.py                 # Application entry point
├── backend/                # Core parsing algorithms
│   ├── grammar_analyzer.py # Grammar validation & processing
│   ├── first_follow.py     # Set computation engine
│   ├── left_recursion.py   # Recursion elimination
│   ├── parsing_table.py    # LL(1) table generation
│   ├── parse_tree.py       # Parse tree construction
│   └── symbol_table.py     # Symbol management
├── gui/                    # User interface components
│   ├── main_window.py      # Main application window
│   ├── widgets.py          # Custom UI widgets
│   ├── parse_tree_widget.py# Tree visualization
│   └── styles.py           # Theme and styling
├── cpp_parser/             # C++ implementation (bonus)
│   ├── predictive_parser.h
│   ├── predictive_parser.cpp
│   └── main.cpp
└── utils/                  # Utility functions
    └── helpers.py          # Common utilities
```

## 🎓 Educational Value

This tool serves as an excellent companion for:
- **CS Students**: Visual learning of compiler theory concepts
- **Instructors**: Demonstration tool for classroom teaching
- **Developers**: Rapid prototyping of language parsers
- **Researchers**: Testing grammar transformations and algorithms

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PyQt5](https://pypi.org/project/PyQt5/) for the GUI framework
- Inspired by classic compiler construction textbooks
- Thanks to the open-source community for algorithm implementations

## 📞 Support

If you encounter issues or have questions:
- Open an [issue](https://github.com/Anushka-333/LL-1-Grammar-Debugger-Tool/issues) on GitHub
- Check the [Wiki](https://github.com/Anushka-333/LL-1-Grammar-Debugger-Tool/wiki) for documentation
- Review the code comments for implementation details

---

**Happy Parsing! 🚀**