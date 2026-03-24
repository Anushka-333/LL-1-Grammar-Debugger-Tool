#include "predictive_parser.h"
#include <algorithm>

PredictiveParser::PredictiveParser() {
    // Constructor
}

void PredictiveParser::setGrammar(const std::map<std::string, std::vector<std::vector<std::string>>>& g) {
    grammar = g;
}

void PredictiveParser::setParsingTable(const std::map<std::pair<std::string, std::string>, std::vector<std::string>>& pt) {
    parsingTable = pt;
}

void PredictiveParser::printStack() {
    std::stack<std::string> temp = parseStack;
    std::vector<std::string> elements;
    
    while (!temp.empty()) {
        elements.push_back(temp.top());
        temp.pop();
    }
    
    std::reverse(elements.begin(), elements.end());
    
    std::cout << "Stack: [";
    for (size_t i = 0; i < elements.size(); ++i) {
        if (i > 0) std::cout << " ";
        std::cout << elements[i];
    }
    std::cout << "]";
}

void PredictiveParser::printInput(int index) {
    std::cout << "Input: [";
    for (size_t i = index; i < input.size(); ++i) {
        if (i > index) std::cout << " ";
        std::cout << input[i];
    }
    std::cout << "]";
}

void PredictiveParser::addStep(const std::string& step) {
    steps.push_back(step);
}

bool PredictiveParser::parse(const std::string& inputString) {
    // Clear previous state
    while (!parseStack.empty()) parseStack.pop();
    steps.clear();
    
    // Tokenize input
    input.clear();
    std::istringstream iss(inputString);
    std::string token;
    while (iss >> token) {
        input.push_back(token);
    }
    input.push_back("$"); // End marker
    
    // Initialize stack
    parseStack.push("$");
    parseStack.push(grammar.begin()->first); // Start symbol
    
    size_t inputIndex = 0;
    bool success = true;
    
    addStep("Starting parse...");
    addStep("Stack: $ " + grammar.begin()->first);
    addStep("Input: " + inputString + " $");
    addStep("----------------------------------------");
    
    while (!parseStack.empty()) {
        std::string top = parseStack.top();
        std::string currentInput = input[inputIndex];
        
        std::stringstream stepStream;
        stepStream << "Step " << steps.size() << ": ";
        printStack();
        stepStream << " | ";
        printInput(inputIndex);
        
        if (top == currentInput) {
            // Match
            if (top == "$") {
                addStep(stepStream.str() + " | Accepted!");
                success = true;
                break;
            }
            
            parseStack.pop();
            inputIndex++;
            addStep(stepStream.str() + " | Match " + top);
        }
        else if (top[0] >= 'A' && top[0] <= 'Z') {
            // Non-terminal
            auto key = std::make_pair(top, currentInput);
            auto it = parsingTable.find(key);
            
            if (it != parsingTable.end()) {
                parseStack.pop();
                const auto& production = it->second;
                
                if (!(production.size() == 1 && production[0] == "ε")) {
                    // Push production in reverse order
                    for (int i = production.size() - 1; i >= 0; --i) {
                        parseStack.push(production[i]);
                    }
                }
                
                std::string prodStr;
                for (const auto& sym : production) {
                    if (!prodStr.empty()) prodStr += " ";
                    prodStr += sym;
                }
                
                addStep(stepStream.str() + " | Output: " + top + " -> " + prodStr);
            }
            else {
                addStep(stepStream.str() + " | Error: No rule for (" + top + ", " + currentInput + ")");
                success = false;
                break;
            }
        }
        else {
            // Terminal mismatch
            addStep(stepStream.str() + " | Error: Expected " + top + ", found " + currentInput);
            success = false;
            break;
        }
    }
    
    return success;
}

void PredictiveParser::printSteps() {
    std::cout << "\n" << std::string(80, '=') << std::endl;
    std::cout << "PARSE STEPS:" << std::endl;
    std::cout << std::string(80, '=') << std::endl;
    
    for (const auto& step : steps) {
        std::cout << step << std::endl;
    }
}

void PredictiveParser::addSymbol(const std::string& name, const std::string& type) {
    symbolTable[name] = type;
}

void PredictiveParser::printSymbolTable() {
    std::cout << "\n" << std::string(80, '=') << std::endl;
    std::cout << "SYMBOL TABLE:" << std::endl;
    std::cout << std::string(80, '=') << std::endl;
    std::cout << std::left << std::setw(20) << "Name" << "Type" << std::endl;
    std::cout << std::string(80, '-') << std::endl;
    
    for (const auto& symbol : symbolTable) {
        std::cout << std::left << std::setw(20) << symbol.first << symbol.second << std::endl;
    }
}

void PredictiveParser::clear() {
    while (!parseStack.empty()) parseStack.pop();
    steps.clear();
    symbolTable.clear();
}