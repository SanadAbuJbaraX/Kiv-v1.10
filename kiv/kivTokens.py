import string

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS  = "MINUS"
TT_MUL = "MUL"
TT_DIV  = "DIV"
TT_BANG = "BANG" # !
TT_BOOL = "BOOL"
TT_POW = "POW"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_KEYWORD = "KEYWORD"
TT_IDENTIFIER = "IDENTIFIER"
TT_EQUALS = "EQ" # =
TT_EOF = 'EOF' #end of file
TT_STRING = 'STRING'
TT_LSQUARE = 'LSQUARE'
TT_RSQUARE = 'RSQUARE'
TT_NEWLINE = 'NEWLINE'
TT_EQEQ = "EQEQ" # ==
TT_LT = "LT" # <
TT_GT = "GRT" # >
TT_LTE = "LTE" # <=
TT_GTE  = "GTE" # >=
TT_NE = "NE" # !=
TT_COMMA = 'COMMA'
TT_ARROW = 'ARROW'
DIGITS = '0123456789'
LETTERS = string.ascii_letters + '_'
LETTERS_DIGIT = LETTERS + DIGITS
KEYWORDS = (
    "var",
    'step',
    'not',
    'if',
    'do',
    'elseif',
    'else',
    'for',
    'while',
    'until',
    'function',
    'end',
    'continue',
    'break',
    'return',
    "import",
    '&',
    '|'
)
class Token:
    def __init__(self,_type,_value=None,pos_start=None,pos_end=None):
        self.type = _type
        self.value = _value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy() 
            self.pos_end.advance(_value)
        if pos_end:
            self.pos_end = pos_end.copy()
    def matches(self,_type,_value):
        if self.type == _type and self.value == _value:
            return True
        return False
    
    def __repr__(self):
        if self.value: return f"{self.type}:{self.value}"
        return f"{self.type}"
class Position:
    def __init__(self,idx,ln,col,fn,ftxt):
        self.idx = idx
        self.ln  = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    def advance(self,current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == "\n":
            self.ln += 1
            self.col = 0
        return self
    def copy(self):
        return Position(self.idx,self.ln,self.col,self.fn,self.ftxt)
    