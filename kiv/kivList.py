from kivType import KivType
from kivErrors import *
from kivNumber import *
class List(KivType):
    def __init__(self,elements):
        super().__init__()
        self.elements = elements
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list,None
    def is_true(self):
        return Bool(int(len(self.elements) != 0)),None
    def multed_by(self, other):
        if isinstance(other,List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list,None
        return None,TypeError(other.pos_start,other.pos_end,f'Unable to concat {other.value} with {self}\nconcat should be maken only with a list and not a {type(other).__name__}')
    def subbed_by(self, other):
        if isinstance(other,Int):
            new_list  = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list,None
            except:
                return None,RuntimeError(
                    other.pos_start,
                    other.pos_end,
                    f"Couldn't remove item because index is out of bound {other.value}"
                )
        else:
            return None,TypeError(
                other.pos_start,
                other.pos_end,
                f"When removing items from list index (number) must be provided\nbut got {type(other).__name__}:{other.value} "
            )
    def dived_by(self, other):
        if isinstance(other,Int):
            try:
                return self.elements[other],None
            except:
                return None,RuntimeError(
                    other.pos_start,
                    other.pos_end,
                    f"Couldn't get item because index is out of bounds {other.value}"
                )
        else:
            return None,TypeError(
                other.pos_start,
                other.pos_end,
                f"When getting items from list index (number) must be provided\nbut got {type(other).__name__}:{other.value} "
            )
    def get_comparison_eq(self, other):
        if isinstance(other,List):
            return Bool(int(self.elements == other.elements)),None
        return Bool(0),None
    def get_comparison_ne(self, other):
        if isinstance(other,List):
            return Bool(int(self.elements != other.elements)),None
        return Bool(0),None
    def notted(self):
        return Bool(int(not len(self.elements) != 0)),None
    def copy(self):
        copy = List(list(self.elements[:]))
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    def __repr__(self):
        return f"[{', '.join([str(x) for x in self.elements])}]"