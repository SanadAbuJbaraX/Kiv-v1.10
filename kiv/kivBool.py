from kivType import KivType

class Bool(KivType):
    def __init__(self,int_value):
        super().__init__()
        self.int_value = int_value
        self.value = None
        self.get_value()
       
   
    def is_true(self):
        return self.value == 'true'
    def set_context(self,context=None):
        self.context = context
        return self
    def get_comparison_eq(self, other):
        if isinstance(other,Bool):
            return Bool(self.value == other.value),None
        return Bool(0),None

    def get_comparison_ne(self, other):
        if isinstance(other,Bool):
            return Bool(self.value != other.value),None
        return Bool(0),None
    def get_value(self):
        if self.int_value == 1:
            self.value = 'true'
        else:
            self.value = 'false'
        return self
    def notted(self):   
        return Bool(not self.int_value).get_value(),None
    def anded_by(self,other):
        if isinstance(other, Bool):
            return Bool(int(bool(self.int_value and other.int_value))).set_context(self.context), None
    def ored_by(self,other):
        if isinstance(other,Bool):
             return Bool(int(bool(self.int_value or other.int_value))).set_context(self.context), None
    def copy(self):
        copy = Bool(self.int_value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def __repr__(self):
        return str(self.value)
    
Bool.false = Bool(0)
Bool.true = Bool(1)
