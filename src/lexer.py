from enum import Enum
import sys

class Lexer:
    def __init__(self, source):
        self.source = source + '\n'
        self.cur_pos = -1
        self.cur_char = '\0'
        self.next_char()
    def peek(self):
        if self.cur_pos+1 >= len(self.source):
            return '\0'
        return self.source[self.cur_pos+1]
    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0'
        else:
            self.cur_char = self.source[self.cur_pos]
    def abort(self, message):
        sys.exit(f"Lexer exiting with message:{message}")
    def remove_whitespaces(self):
        while self.cur_char == ' 'or self.cur_char == '\t' or self.cur_char == '\r':
            self.next_char()
    def remove_comments(self):
        if self.cur_char == '#':
            while self.cur_char != '\n':
                self.next_char()
    def get_token(self):
        self.remove_whitespaces()
        self.remove_comments()
        token = Token(None, TokenType.NONE)
        if self.cur_char == '+':
            token = Token(self.cur_char, TokenType.PLUS)
        elif self.cur_char == '-':
            token = Token(self.cur_char, TokenType.MINUS)
        elif self.cur_char == '*':
            token = Token(self.cur_char, TokenType.ASTERISK)
        elif self.cur_char == '/':
            token = Token(self.cur_char, TokenType.SLASH)
        elif self.cur_char == '\n':
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == '\0':
            token = Token(self.cur_char, TokenType.EOF)
        elif self.cur_char == '=':
            # We need to check weather the token is a = or ==
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, TokenType.EQEQ)
            else:
                token = Token(self.cur_char, TokenType.EQ)
        elif self.cur_char == '>':
            # We need to check weather the token is a > or >=
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, TokenType.GTEQ)
            else:
                token = Token(self.cur_char, TokenType.GT)
        elif self.cur_char == '<':
            # We need to check weather the token is a < or <=
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, TokenType.LTEQ)
            else:
                token = Token(self.cur_char, TokenType.LT)
        elif self.cur_char == '!':
            # We need to check weather the token is != and ! alone is not allowed
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, TokenType.NOTEQ)
            else:
                self.abort("Found ! instead of !=")
        #Return a string capability
        elif self.cur_char == '"':
            self.next_char()
            start_pos = self.cur_pos
            while self.cur_char != '"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                #We can't do this as we are using C's `printf` statement, once we move to rustpython
                #This wont be an issue
                if self.cur_char == '\r' or self.cur_char == '\n' or self.cur_char == '\t' or self.cur_char == '\\' or self.cur_char == '%':
                    self.abort(f"Illegal charecter used {self.cur_char}")
                self.next_char()
            token = Token(self.source[start_pos: self.cur_pos], TokenType.STRING)
        elif self.cur_char.isdigit():
            #The leading charecter has to be a digit .9 is not allowed 0.9 is alloweda
            #Get all consecutive numbers
            start_pos = self.cur_pos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == '.':
                self.next_char()
                if not self.peek().isdigit():
                    self.abort(f"Charecter after decimal is not digit: {self.peek()}")
                while self.peek().isdigit():
                    self.next_char()
            token = Token(self.source[start_pos:self.cur_pos+1], TokenType.NUMBER)
        #Get all the keywords
        elif self.cur_char.isalpha():
            #First charecter in keyword should be a letter and not Numeric
            #After that it allows alphanumeric
            start_pos = self.cur_pos
            while self.peek().isalnum():
                self.next_char()
            #Check if the Token is a keyword
            tokentext = self.source[start_pos: self.cur_pos+1]
            keyword = Token.check_keyword(tokentext)
            if keyword == None:
                token = Token(tokentext, TokenType.IDENT)
            else:
                token = Token(tokentext, keyword)
        else:
            self.abort(f"Unknown token {self.cur_char}")
        self.next_char()
        return token

class Token:
    def __init__(self, text, kind):
        self.text = text
        self.kind = kind
    @staticmethod
    def check_keyword(keyword):
        for kind in TokenType:
            if kind.name == keyword and kind.value == None:
                return kind
            elif kind.name == keyword and kind.value >= 100 and kind.value < 200: 
                return kind
        return None

class TokenType(Enum):
    NONE = None #This is native NoneType, its enum like rust but uses Py default
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211

'''
# TODO:
    -[ ] Create a funtion to identify None
'''
