from kivTokens import *
from kivErrors import *
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
		
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
                if self.current_char in ' \t':
                        self.advance()
                elif self.current_char == "/":
                        tok = self.make_comment_or_div()
                        if tok:
                                tokens.append(tok)
                                self.advance()
                elif self.current_char in ';\n':
                       tokens.append(Token(TT_NEWLINE,pos_start=self.pos))
                       self.advance()
                elif self.current_char in DIGITS:
                        tokens.append(self.make_number())
                elif self.current_char == '+':
                        tokens.append(Token(TT_PLUS, pos_start=self.pos))
                        self.advance()
                elif self.current_char == '-':
                        tokens.append(self.make_arrow_or_minus())
                elif self.current_char in ("'",'"'):
                        tokens.append(self.make_string())
                elif self.current_char == '*':
                        tokens.append(Token(TT_MUL, pos_start=self.pos))
                        self.advance()
                elif self.current_char == '^':
                        tokens.append(Token(TT_POW, pos_start=self.pos))
                        self.advance()
                elif self.current_char == '(':
                        tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                        self.advance()
                elif self.current_char == ')':
                        tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                        self.advance()
                elif self.current_char == '[':
                        tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                        self.advance()
                elif self.current_char == ']':
                        tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                        self.advance()
                elif self.current_char == ',':
                        tokens.append(Token(TT_COMMA, pos_start=self.pos))
                        self.advance()
                elif self.current_char == '&':
                       tokens.append(Token(TT_KEYWORD,'&', pos_start=self.pos))
                       self.advance()
                elif self.current_char == '|':
                       tokens.append(Token(TT_KEYWORD,'|' ,pos_start=self.pos))
                       self.advance()
                elif self.current_char == '=':
                        tokens.append(self.make_equals())
                elif self.current_char == '!':
                        tok,err = self.make_not_equals()
                        if err:
                           return [],err
                        tokens.append(tok)
                elif self.current_char == '>':
                        tokens.append(self.make_greater_than())
                elif self.current_char == '<':
                        tokens.append(self.make_less_than())
                elif self.current_char in LETTERS:
                       tokens.append(self.make_identifier())
                else:
                        pos_start = self.pos.copy()
                        char = self.current_char
                        self.advance()
                        return [], IllegalCharacterError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))

        return tokens, None
    def make_comment_or_div(self):
           pos_start = self.pos.copy()
           self.advance()
           if self.current_char == '/':
                  self.skip_comment()
                  return None   
           return Token(TT_DIV,pos_start=pos_start,pos_end=self.pos)
    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
                'n': '\n',
                't': '\t',
                "'" : "\'",
                '"' : "\"",
                "\\":"\\"
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
                if escape_character:
                        string += escape_characters.get(self.current_char, self.current_char)
                        escape_character = False
                else:
                        if self.current_char == '\\':
                                escape_character = True
                        else:
                                string += self.current_char
                self.advance()
        
        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)
    def make_arrow_or_minus(self):
           tok_type = TT_MINUS
           pos_start = self.pos.copy()
           self.advance()
           if self.current_char == '>':
                tok_type = TT_ARROW
                self.advance()
           return Token(tok_type,pos_start=pos_start,pos_end=self.pos)
    
    def make_not_equals(self):
           pos_start = self.pos.copy()
           self.advance()
           if self.current_char == '=':
                  self.advance()
                  return Token(TT_NE,pos_start=pos_start,pos_end=self.pos),None
           self.advance()
           return Token(TT_BANG,pos_start=pos_start,pos_end=self.pos),None
    def make_equals(self):
           pos_start = self.pos.copy()
           tok_type = TT_EQUALS
           self.advance()
           if self.current_char == '=':
                self.advance()
                tok_type = TT_EQEQ
           return Token(tok_type,pos_start=pos_start,pos_end=self.pos)

    def make_less_than(self):
           pos_start = self.pos.copy()
           tok_type = TT_LT
           self.advance()
           if self.current_char == '=':
                self.advance()
                tok_type = TT_LTE
           return Token(tok_type,pos_start=pos_start,pos_end=self.pos)
    def make_greater_than(self):
           pos_start = self.pos.copy()
           tok_type = TT_GT
           self.advance()
           if self.current_char == '=':
                self.advance()
                tok_type = TT_GTE
           return Token(tok_type,pos_start=pos_start,pos_end=self.pos)
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGIT + '_':
                id_str += self.current_char
                self.advance()
        if id_str == "true":
               return Token(TT_BOOL,1,pos_start,self.pos)
        elif id_str == "false":
                return Token(TT_BOOL,0,pos_start,self.pos)
        else:
                tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type,id_str,pos_start,self.pos)        
    def skip_comment(self):
        self.advance()
        while self.current_char != '\n' and self.current_char != None:     
                self.advance()

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
                if self.current_char == '.':
                        if dot_count == 1: break
                        dot_count += 1
                        num_str += '.'
                else:
                        num_str += self.current_char
                self.advance()

        if dot_count == 0:
                return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
                return Token(TT_FLOAT, float(num_str), pos_start, self.pos)