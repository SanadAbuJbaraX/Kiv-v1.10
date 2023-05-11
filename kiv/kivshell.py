from kivLexer import Lexer
from kivParser import Parser
from kivInterpreter import Interpreter
from kivContext import Context
from kivSymbolTable import SymbolTable
from kivNumber import *
from kivBool import Bool
from kivFunction import  BuiltInFunction
import os

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
global_symbol_table.set("open", BuiltInFunction.open)
global_symbol_table.set("is_in", BuiltInFunction.is_in)
global_symbol_table.set("round", BuiltInFunction.round)

def run_shell(fn, text,symbol_table):
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
        context.symbol_table = symbol_table
        interpretor = Interpreter()
        result = interpretor.visit(ast.node,context)
        return result.value,result.error
    else:
        return "",None
# shell loop
while True:
    try:
        text = input('kiv> ') # get input
        if text.strip():
            result,error = run_shell('<stdin>', text,global_symbol_table) # run input
            if error:
                print(error.as_string())
            elif result:
                if len(result.elements) == 1:
                    print(repr(result.elements[0]))
                else:
                    print(repr(result))
    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        print("KeyboardInterrupt")
        break
        
   