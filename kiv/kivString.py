from kivType import KivType
from kivErrors import TypeError
from kivNumber import Int
from kivBool import Bool
class String(KivType):
	def __init__(self,value):
		super().__init__()
		self.value = value
	def added_to(self,other):
		if isinstance(other,String):
			return String(self.value + other.value).set_context(self.context).set_pos(self.pos_start,other.pos_end),None
		return None, TypeError(
			self.pos_start,
			self.pos_end,
			f' Can only add string with string but got {type(other).__name__}\nFor example: "hello" + "hello" -> "hellohello"\nbut "hello" + 3 -> TypeError'
		)
	def multed_by(self, other):
		if isinstance(other,Int):
			return String(self.value*other.value).set_context(self.context),None
		return None, TypeError(
			self.pos_start,
			self.pos_end,
			f' Can only multiply string with int but got {type(other).__name__}\nFor example: "hello" * 3 -> "hellohellohello"\nbut "hello" * "hello " -> TypeError'
	)   
	def copy(self):
		copy = String(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return self
	def get_comparison_eq(self,other):
		if isinstance(other,String):
			return Bool(int(str(self.value) == str(other.value))).set_context(self.context),None
		return Bool(0),None
	def get_comparison_ne(self,other):
		if isinstance(other,String):
			return Bool(int(self.value != other.value)).set_context(self.context),None
		return Bool(0),None
	def is_true(self):
		return len(self.value) != 0
	def __repr__(self):
		return f"{self.value}"