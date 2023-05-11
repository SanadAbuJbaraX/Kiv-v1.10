import sys
import os

from kivLexer import Lexer
from kivParser import Parser
from kivInterpreter import Interpreter
from kivContext import Context
from kivSymbolTable import SymbolTable
from kivNumber import *
from kivBool import Bool
from kivFunction import  BuiltInFunction
from kivString import String
from kivList import List

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Int(0))
global_symbol_table.set("false", Bool.false)
global_symbol_table.set("true", Bool.true)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("cls", BuiltInFunction.cls)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("index", BuiltInFunction.index)
global_symbol_table.set("type", BuiltInFunction.type)
global_symbol_table.set("toInt", BuiltInFunction.toInt)
global_symbol_table.set("toFloat", BuiltInFunction.toFloat)
global_symbol_table.set("toString", BuiltInFunction.toString)
global_symbol_table.set("range", BuiltInFunction.range)
global_symbol_table.set("is_in", BuiltInFunction.is_in)
global_symbol_table.set("open", BuiltInFunction.open)
global_symbol_table.set("round", BuiltInFunction.round)


def run_file(fn : str, text,symbol_table: SymbolTable):
    
    # Generate tokens
    lexer = Lexer(fn, text) #
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    
    # Generate AST'
    if len(tokens) > 1:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error:
            return None,ast.error
        context = Context('<program>')
        symbol_table.set("FILENAME", String(fn.replace("\\","/").split("/")[-1]))
        rep = []
        for key,value in symbol_table.symbols.items():
            rep.append(String(str(key + ":" + repr(value))))
        GLOBALS = List(rep)
        symbol_table.set("GLOBALS", GLOBALS)
        context.symbol_table = symbol_table
        interpretor = Interpreter()
        result = interpretor.visit(ast.node,context)
        return result.value,result.error
    else:
        return "",None
def run_import(text):
    lexer = Lexer("f", text) #
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    
    # Generate AST'
    if len(tokens) > 1:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error:
            return None,ast.error
        context = Context('<program>')
        context.symbol_table = global_symbol_table
        interpretor = Interpreter()
        result = interpretor.visit(ast.node,context)
        return result.value,result.error,context.symbol_table.symbols
    else:
        return "",None,None
def run():
    try:
        file = open(sys.argv[1])
    except Exception:
        if len(sys.argv) == 1:
            print("Expected file name")
            return
        else:
            print("File Not Found")
            return
    try:
        _,err = run_file(file.name,' '.join(file.readlines()),global_symbol_table)
        if err:
            print( f"Failed to finish executing script \"{file.name}\"\n" +
            err.as_string(),)
    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        print("KeyboardInterrupt: Operation has been dismissed")
run()
        