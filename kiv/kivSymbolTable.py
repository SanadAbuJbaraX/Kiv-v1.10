class SymbolTable:
    def __init__(self,parent=None):
        self.symbols = {}
        self.parent = parent
        if parent:
            self.get_parent_symbols()
    def get_parent_symbols(self):
        parent_symbols = self.parent.symbols
        for item in list(parent_symbols.items()):
            self.symbols[item[0]] = item[1]
    def get(self,varname):
        value = self.symbols.get(varname,None)
        if value == None and self.parent:
            return self.parent.get(value)
        return value
    def set(self,varname,value):
        self.symbols[varname] = value
    def remove(self,varname):
        del self.symbols[varname]
    