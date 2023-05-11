from kivRuntimeResult import RuntimeResult
from kivType import KivType
from kivErrors import RuntimeError
from kivSymbolTable import SymbolTable
from kivContext import Context
from kivBool import Bool
from kivNumber import *
from kivList import List
from kivString import String
import os
import time 
class BaseFunction(KivType):
  def __init__(self, name):
    super().__init__()
    self.name = name or "lambda"

  def generate_new_context(self):
    new_context = Context(self.name, self.context, self.pos_start)
    new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
    return new_context

  def check_args(self, arg_names, args):
    res = RuntimeResult()

    if len(args) > len(arg_names):
      return res.failure(RuntimeError(
        self.pos_start, self.pos_end,
        f" too many args passed into {self} Expected {len(arg_names)} but got {len(args) - len(arg_names)}",
        self.context
      ))
    
    if len(args) < len(arg_names):
      return res.failure(RuntimeError(
        self.pos_start, self.pos_end,
         f" too few args passed into {self} Expected {len(arg_names)} but got {len(args) - len(arg_names)}",
        self.context
      ))

    return res.success(None)

  def populate_args(self, arg_names, args, exec_ctx):
    for i in range(len(args)):
      arg_name = arg_names[i]
      arg_value = args[i]
      arg_value.set_context(exec_ctx)
      exec_ctx.symbol_table.set(arg_name, arg_value)

  def check_and_populate_args(self, arg_names, args, exec_ctx):
    res = RuntimeResult()
    res.register(self.check_args(arg_names, args))
    if res.should_return(): return res
    self.populate_args(arg_names, args, exec_ctx)
    return res.success(None)



class Function(BaseFunction):
  def __init__(self, name, body_node, arg_names,should_auto_return):
    super().__init__(name)
    self.body_node = body_node
    self.arg_names = arg_names
    self.should_auto_return = should_auto_return

  def execute(self, args):
    res = RuntimeResult()
    from kivInterpreter import Interpreter
    interpreter = Interpreter()
    exec_ctx = self.generate_new_context()

    res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
    if res.should_return(): return res

    value = res.register(interpreter.visit(self.body_node, exec_ctx))
    if res.should_return() and res.func_return_value == None: return res
    ret_value = (value if self.should_auto_return else None) or res.func_return_value or Int(0)
    return res.success(ret_value)

  def copy(self):
    copy = Function(self.name, self.body_node, self.arg_names,self.should_auto_return)
    copy.set_context(self.context)
    copy.set_pos(self.pos_start, self.pos_end)
    return copy

  def __repr__(self):
    return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
  def __init__(self, name):
    super().__init__(name)

  def execute(self, args):
    res = RuntimeResult()
    exec_ctx = self.generate_new_context()

    method_name = f'execute_{self.name}'
    method = getattr(self, method_name, self.no_visit_method)

    res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
    if res.should_return(): return res

    return_value = res.register(method(exec_ctx))
    if res.should_return(): return res
    return res.success(return_value)
  
  def no_visit_method(self, node, context):
    raise Exception(f'No execute_{self.name} method defined')

  def copy(self):
    copy = BuiltInFunction(self.name)
    copy.set_context(self.context)
    copy.set_pos(self.pos_start, self.pos_end)
    return copy

  def __repr__(self):
    return f"<built-in function {self.name}>"

  #####################################

  def execute_print(self, exec_ctx):
    print(str(exec_ctx.symbol_table.get('value')))
    return RuntimeResult().success(Int(0))
  execute_print.arg_names = ['value']
  def execute_input(self, exec_ctx):
    text = input(str(exec_ctx.symbol_table.get('value')))
    return RuntimeResult().success(String(text))
  execute_input.arg_names = ['value']
  def execute_type(self,exec_ctx):
    obj = exec_ctx.symbol_table.get('object')
    return RuntimeResult().success(String(type(obj).__name__))
  execute_type.arg_names = ['object']
  def execute_cls(self, exec_ctx):
    os.system('cls' if os.name == 'nt' else 'cls') 
    return RuntimeResult().success(Int(0))
  execute_cls.arg_names = []
  def execute_exit(self, exec_ctx):
    exit()
  execute_exit.arg_names = []
  def execute_len(self,exec_ctx):
      object = exec_ctx.symbol_table.get("object")

      if not isinstance(object, List):
        return RuntimeResult().success(Int(len(String(object.value).value)))

      return RuntimeResult().success(Int(len(object.elements)))
  execute_len.arg_names = ["object"]
  def execute_open(self,exec_ctx):
      filename = exec_ctx.symbol_table.get("filename")

      if not isinstance(filename,String):
        return RuntimeResult().failure(TypeError(
          self.pos_start,
          self.pos_end,
          "File Name must be a string"
        ))
      try:
        file = open(filename.value)
        return RuntimeResult().success(String(file.read()))

      except FileNotFoundError:
        return RuntimeResult().failure(TypeError(
          self.pos_start,
          self.pos_end,
          "File Not Found"
        ))
  execute_open.arg_names = ["filename"]
  def execute_index(self,exec_ctx):
      object = exec_ctx.symbol_table.get("object")
      index = exec_ctx.symbol_table.get("index")
      if not isinstance(object, (String,List)):
        return RuntimeResult().failure(RuntimeError(
          self.pos_start,
          self.pos_end, 
          "index() can only be used with a string or a list"
        ))
      if isinstance(object,List):
        if isinstance(object.elements[index.value],Int):
          return RuntimeResult().success(Int(object.elements[index.value].value))
        elif isinstance(object.elements[index.value],String):
          return RuntimeResult().success(String(object.elements[index.value].value))
        elif isinstance(object.elements[index.value],List):
          return RuntimeResult().success(List(object.elements[index.value].elements))
        else:
          return RuntimeResult().success(Bool(0))
      if isinstance(object,Int):
          return RuntimeResult().success(Int(int(str(object.value)[index.value])))
      elif isinstance(object,String):
          return RuntimeResult().success(String(str(object.value[index.value])))
      elif isinstance(object,Float):
          return RuntimeResult().success(Float(float(str(object.value)[index.value])))
      return RuntimeResult().failure(
        TypeError(
        self.pos_start,
        self.pos_end,
        "Unsuported Type: somehow " + type(object).__name__
      ))
  execute_index.arg_names = ["object","index"]
  def execute_toInt(self,exec_ctx):
    object = exec_ctx.symbol_table.get("object")
    if not isinstance(object,(String,Int,Float)):
      return RuntimeResult().failure(RuntimeError(
          self.pos_start,
          self.pos_end,
          "toInt can only be used with a string or float and converts it to a number"
        ))
    return RuntimeResult().success(Int(int(object.value)))
  execute_toInt.arg_names = ["object"]
  def execute_round(self,exec_ctx):
    object = exec_ctx.symbol_table.get("num")
    digits = exec_ctx.symbol_table.get("digits")
    if not isinstance(object,(Int,Float)):
      return RuntimeResult().failure(RuntimeError(
          self.pos_start,
          self.pos_end,
          "round can only be used with a int or float and converts it to a number"
        ))
    return RuntimeResult().success(Int(round(object.value,digits.value)))
  execute_round.arg_names = ["num","digits"]
  def execute_toFloat(self,exec_ctx):
    object = exec_ctx.symbol_table.get("object")
    if not isinstance(object,(String,Int,Float)):
      return RuntimeResult().failure(RuntimeError(
          self.pos_start,
          self.pos_end,
          "toFloat can only be used with a string or int and converts it to a number"
        ))
    return RuntimeResult().success(Float(float(object.value)))
  execute_toFloat.arg_names = ["object"]
  def execute_toString(self,exec_ctx):
    object = exec_ctx.symbol_table.get("object")
    if not isinstance(object,(String,Int,Float)):
      return RuntimeResult().failure(RuntimeError(
          self.pos_start,
          self.pos_end,
          "toString can only be used with a float, int and converts it to a string"
        ))
    return RuntimeResult().success(String(str(object.value)))
  execute_toString.arg_names = ["object"]
  def execute_is_in(self,exec_ctx):
    object = exec_ctx.symbol_table.get("object")
    elem = exec_ctx.symbol_table.get("elem")
    if not isinstance(object,(String,List)):
      return RuntimeResult().failure(RuntimeError(
          self.pos_start,
          self.pos_end,
          "is_in() can only be used with a list or string"
        ))
    if isinstance(object,List):
      for x in object.elements:
        if elem.value == x.value:
          return  RuntimeResult().success(Bool(1))
      return RuntimeResult().success(Bool(0))
    
    return RuntimeResult().success(Bool(int(str(elem.value) in str(object.value))))
  execute_is_in.arg_names = ["object","elem"]
  def execute_range(self,exec_ctx):
    n1 = exec_ctx.symbol_table.get("n1")  
    n2 = exec_ctx.symbol_table.get("n2")

    if not isinstance(n1,Int) and not isinstance(n2,Int) :
      return RuntimeResult().failure(RuntimeError(
          self.pos_start,
          self.pos_end,
          "range can only be used with an int\nFor example: range(0,5) -> [0,1,2,3,4]"
        ))
    return RuntimeResult().success(List(list(range(n1.value,n2.value))))
  execute_range.arg_names = ["n1","n2"]

BuiltInFunction.type = BuiltInFunction("type")
BuiltInFunction.toInt = BuiltInFunction("toInt")
BuiltInFunction.toFloat = BuiltInFunction("toFloat")
BuiltInFunction.toString = BuiltInFunction("toString")
BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.cls = BuiltInFunction("cls")
BuiltInFunction.exit = BuiltInFunction("exit")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.index = BuiltInFunction("index")
BuiltInFunction.range = BuiltInFunction("range")
BuiltInFunction.open = BuiltInFunction("open")
BuiltInFunction.is_in = BuiltInFunction("is_in")
BuiltInFunction.round = BuiltInFunction("round")

class ModuleTime(BaseFunction):
  def __init__(self, name):
    super().__init__(name)
  def execute(self, args):
    res = RuntimeResult()
    exec_ctx = self.generate_new_context()

    method_name = f'execute_{self.name}'
    method = getattr(self, method_name, self.no_visit_method)
    res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
    if res.should_return(): return res

    return_value = res.register(method(exec_ctx))
    if res.should_return(): return res
    return res.success(return_value)
  
  def no_visit_method(self, node, context):
    raise Exception(f'No execute_{self.name} method defined')

  def copy(self):
    copy = ModuleTime(self.name)
    copy.set_context(self.context)
    copy.set_pos(self.pos_start, self.pos_end)
    return copy

  def __repr__(self):
    return f"<module-graphics function {self.name}>"
  def execute_counter(self,exec_ctx):
    return RuntimeResult().success(Float(time.perf_counter())) 
  execute_counter.arg_names = []
  def execute_sleep(self,exec_ctx):
    res = RuntimeResult()
    secs = exec_ctx.symbol_table.get("secs")
    if type(secs) not in (Int,Float):
      return res.failure(
        TypeError(
        self.pos_start,
        self.pos_end,
        "Seconds must be an Int or Float"
        )
      )
    time.sleep(secs.value)
    return res.success(Int(0))
  execute_sleep.arg_names = ["secs"]
ModuleTime.symbols = {"counter":ModuleTime("counter"),"sleep":ModuleTime("sleep")}