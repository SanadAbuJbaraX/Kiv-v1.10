from kivLexer import Lexer
from kivParser import Parser
from kivInterpreter import Interpreter
from kivContext import Context
from kivSymbolTable import SymbolTable
from kivNumber import *
from kivBool import Bool
from kivFunction import  BuiltInFunction
from kivString import String
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


def run_import(fn,text):
    lexer = Lexer(fn, text) #
    tokens, error = lexer.make_tokens()
    if error:
        return None, error, None
    
    # Generate AST'
    if len(tokens) > 1:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error:
            print(ast.error.as_string())
            return None,ast.error,{}
        context = Context('<program>')
        context.symbol_table = global_symbol_table
        interpretor = Interpreter()
        result = interpretor.visit(ast.node,context)
        return result.value,result.error,context.symbol_table.symbols
    else:
        return None,None,{}