#include "predictive_parser.h"
#include <iostream>

int main() {
    PredictiveParser parser;
    
    // Example grammar
    std::map<std::string, std::vector<std::vector<std::string>>> grammar;
    grammar["E"] = {{"T", "E'"}};
    grammar["E'"] = {{"+", "T", "E'"}, {"ε"}};
    grammar["T"] = {{"F", "T'"}};
    grammar["T'"] = {{"*", "F", "T'"}, {"ε"}};
    grammar["F"] = {{"(", "E", ")"}, {"id"}};
    
    // Example parsing table
    std::map<std::pair<std::string, std::string>, std::vector<std::string>> parsingTable;
    parsingTable[{ "E", "id" }] = { "T", "E'" };
    parsingTable[{ "E", "(" }] = { "T", "E'" };
    parsingTable[{ "E'", "+" }] = { "+", "T", "E'" };
    parsingTable[{ "E'", ")" }] = { "ε" };
    parsingTable[{ "E'", "$" }] = { "ε" };
    parsingTable[{ "T", "id" }] = { "F", "T'" };
    parsingTable[{ "T", "(" }] = { "F", "T'" };
    parsingTable[{ "T'", "+" }] = { "ε" };
    parsingTable[{ "T'", "*" }] = { "*", "F", "T'" };
    parsingTable[{ "T'", ")" }] = { "ε" };
    parsingTable[{ "T'", "$" }] = { "ε" };
    parsingTable[{ "F", "id" }] = { "id" };
    parsingTable[{ "F", "(" }] = { "(", "E", ")" };
    
    parser.setGrammar(grammar);
    parser.setParsingTable(parsingTable);
    
    std::cout << "LL(1) Parser Test\n";
    std::cout << "=================\n\n";
    
    std::string input = "id + id * id";
    std::cout << "Parsing: " << input << std::endl;
    
    bool result = parser.parse(input);
    
    if (result) {
        std::cout << "\n✓ String accepted!\n";
    } else {
        std::cout << "\n✗ String rejected!\n";
    }
    
    parser.printSteps();
    
    // Test symbol table
    parser.addSymbol("x", "int");
    parser.addSymbol("y", "float");
    parser.addSymbol("z", "char");
    parser.printSymbolTable();
    
    return 0;
}