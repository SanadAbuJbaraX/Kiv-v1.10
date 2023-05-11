from kivErrors import RuntimeError,TypeError
from kivBool import Bool
from kivType import KivType
class Number(KivType):
    def __init__(self,value):
        super().__init__()
        self.value = value
    def is_true(self):
        return self.value != 0
    def added_to(self,other):
        if isinstance(other,Int):
            return Int(self.value + other.value).set_context(self.context),None
    def subbed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Number(self.value - other.value).set_context(self.context),None
    def multed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Number(self.value * other.value).set_context(self.context),None
    
    def dived_by(self,other):
        if isinstance(other,(Int,Float)):
            if other.value == 0:
                return None,RuntimeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Division by 0',
                    self.context
                )
            else:
                return Int(self.value / other.value).set_context(self.context)
    def powed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Number(self.value ** other.value).set_context(self.context),None
    def get_comparison_eq(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value == other.value)).set_context(self.context),None
    def get_comparison_ne(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value != other.value)).set_context(self.context),None
    def get_comparison_gt(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value > other.value)).set_context(self.context),None
    def get_comparison_gte(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value >= other.value)).set_context(self.context),None
    def get_comparison_lt(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value < other.value)).set_context(self.context),None
    def get_comparison_lte(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value <= other.value)).set_context(self.context),None
    
    
   
    
    def __repr__(self):
        return str(self.value)
    
class Int(Number):
    def copy(self):
        copy = Int(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def added_to(self,other):
        if isinstance(other,(Float,Int)):
            return Int(int(self.value + other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot add int to ' + type(other).__name__,
                    self.context
                )
    def subbed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Int(int(self.value - other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot minus int to ' + type(other).__name__,
                    self.context
                )
    def multed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Int(int(self.value * other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot multiply int to ' + type(other).__name__,
                    self.context
                )
    def dived_by(self,other):
        if isinstance(other,(Int,Float)):
            if other.value == 0:
                return None,RuntimeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Division by 0',
                    self.context
                )
            else:
                return Int(int(self.value / other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot divide int to ' + type(other).__name__,
                    self.context
                )
    def powed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Int(int(self.value ** other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot power int with ' + type(other).__name__,
                    self.context
                )
    def get_comparison_eq(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value == other.value)).set_context(self.context),None
        return Bool(0),None
    def get_comparison_ne(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value != other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare int with' + type(other).__name__,
                    self.context
                )
    def notted(self):
        return Bool(1 if self.value == 0 else 0).set_context(self.context), None
    def get_comparison_gt(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value > other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare int with' + type(other).__name__,
                    self.context
                )
    def get_comparison_gte(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value >= other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare int with' + type(other).__name__,
                    self.context
                )
    def get_comparison_lt(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value < other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare int with' + type(other).__name__,
                    self.context
                )
    def get_comparison_lte(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value <= other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare int with' + type(other).__name__,
                    self.context
                )
class Float(Number):
    def added_to(self,other):
        if isinstance(other,Int):
            return Float(float(self.value + other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot add float to ' + type(other).__name__,
                    self.context
                )
    def subbed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Float(float(self.value - other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot minus float to ' + type(other).__name__,
                    self.context
                )
    def multed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Float(float(self.value * other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot multiply float to ' + type(other).__name__,
                    self.context
                )
    def dived_by(self,other):
        if isinstance(other,(Int,Float)):
            if other.value == 0:
                return None,RuntimeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Division by 0',
                    self.context
                )
            else:
                return Float(float(self.value / other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot divide float to ' + type(other).__name__,
                    self.context
                )
    def powed_by(self,other):
        if isinstance(other,(Int,Float)):
            return Float(float(self.value ** other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot power float with ' + type(other).__name__,
                    self.context
                )
    def get_comparison_eq(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value == other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare int with' + type(other).__name__,
                    self.context
                )
    def get_comparison_ne(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value != other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare float with' + type(other).__name__,
                    self.context
                )
    def get_comparison_gt(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value > other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare float with' + type(other).__name__,
                    self.context
                )
    
    def get_comparison_gte(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value >= other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare float with' + type(other).__name__,
                    self.context
                )
    def get_comparison_lt(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value < other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare float with' + type(other).__name__,
                    self.context
                )
    def get_comparison_lte(self,other):
        if isinstance(other,(Int,Float)):
            return Bool(int(self.value <= other.value)).set_context(self.context),None
        return None,TypeError(
                    other.pos_start, 
                    other.pos_end,
                    ' Cannot compare float with' + type(other).__name__,
                    self.context
                )
    def notted(self):
        return Bool(1 if self.value == 0 else 0).set_context(self.context), None
    def copy(self):
        copy = Float(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy