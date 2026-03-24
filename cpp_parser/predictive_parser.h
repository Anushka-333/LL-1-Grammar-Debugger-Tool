#ifndef PREDICTIVE_PARSER_H
#define PREDICTIVE_PARSER_H

#include <iostream>
#include <vector>
#include <map>
#include <stack>
#include <string>
#include <sstream>
#include <iomanip>

class PredictiveParser {
private:
    std::map<std::string, std::vector<std::vector<std::string>>> grammar;
    std::map<std::pair<std::string, std::string>, std::vector<std::string>> parsingTable;
    std::stack<std::string> parseStack;
    std::vector<std::string> input;
    std::vector<std::string> steps;
    std::map<std::string, std::string> symbolTable;
    
    void printStack();
    void printInput(int index);
    void addStep(const std::string& step);
    
public:
    PredictiveParser();
    void setGrammar(const std::map<std::string, std::vector<std::vector<std::string>>>& g);
    void setParsingTable(const std::map<std::pair<std::string, std::string>, std::vector<std::string>>& pt);
    bool parse(const std::string& inputString);
    void printSteps();
    void addSymbol(const std::string& name, const std::string& type);
    void printSymbolTable();
    void clear();
};

#endif