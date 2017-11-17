import math
import sys

###################################################################################
#                                                                                 #
#                                                                                 #
#                                                                                 #
#                                                                                 #
#                           Simple Python interpreter                             #
#                           Developed by: Stralle                                 #
#                                                                                 #
#                                                                                 #
#                                                                                 #
###################################################################################


# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, BRAO, BRAC, FUNC, DOT, COMMA, NOT, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'BRAO', 'BRAC', 'FUNC', 'DOT', 'COMMA', 'NOT', 'EOF'
)

GRTR, LESS, EQU, GREQU, LEQU, ASSIGN, VAR = (
    'GRTR', 'LESS', 'EQU', 'GREQU', 'LEQU', 'ASSIGN', 'VAR'
)

SIN, COS, TAN, CTG, SQRT, POW, LOG = (
    'SIN', 'COS', 'TAN', 'CTG', 'SQRT', 'POW', 'LOG'
)

variables = {}

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, or EOF
        self.type = type
        # token value: non-negative integer value, '+', '-', '*', '/', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            if result == '':
                result = '0'
            result += '.'
            self.advance();
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return float(result)
        else:
            return int(result)

    def texta(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char == '.':
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                string = self.texta()
                if string in (SIN, COS, TAN, CTG, POW, SQRT, LOG):
                    return Token(FUNC, string)
                else:
                    return Token(VAR, string)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(BRAO, '(')
 
            if self.current_char == ')':
                self.advance()
                return Token(BRAC, ')')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LEQU, '<=')
                return Token(LESS, '<')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GREQU, '>=')
                return Token(GRTR, '>')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQU, '==')
                return Token(ASSIGN, '=')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            self.error()

        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()
        self.prev_token = Token("NOT", "!")
        self.mid_token = self.prev_token

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.prev_token = self.mid_token
            self.mid_token = self.current_token
            self.current_token = self.lexer.get_next_token()
            #print(self.prev_token)
            #print(self.current_token)
            #print("--------------------")
        else:
            self.error()

    def isDecimal(self, result):
        if result.is_integer():
            return int(result)
        return result
            
    def countFunc(self, result, token):
        if token=='SIN':
            return math.sin(result)
        if token=='COS':
            return math.cos(result)
        if token=='TAN':
            return math.tan(result)
        if token=='CTG':
            return math.cos(result)/math.sin(result)
        if token=='SQRT':
            return math.sqrt(result)
        if token=='LOG':
            return math.log10(result)
        
        self.error()
        
    def factor(self):
        """factor : INTEGER"""
        token = self.current_token
        global variables

        if token.type == VAR and token.value not in variables:
            self.error()

        if token.type == VAR and token.value in variables:
            self.eat(VAR)
            if self.current_token.type == ASSIGN:
                if self.prev_token.type == PLUS or self.prev_token.type == MINUS or self.prev_token.type == MUL or self.prev_token.type == DIV:         #ERROR
                    self.error()
                self.eat(ASSIGN)
                variables[token.value] = self.assignment()
                return variables[token.value]
            return variables[token.value]

        elif token.type == FUNC:
            self.eat(FUNC)
            self.eat(BRAO)
            
            result = self.logexpr() #LOGEXPR
            power = 1
            
            if token.value == 'POW':
                self.eat(COMMA)
                power = self.logexpr() #LOGEXPR
                
            self.eat(BRAC)

            if self.current_token.type == ASSIGN:           #ERROR
                self.error()
            
            if token.value == 'POW':
                result = math.pow(result, power)
            else:
                result = self.countFunc(result, token.value)
            result = self.isDecimal(result)
            return result
        elif token.type == BRAO:
            self.eat(BRAO)
            result = self.logexpr() #LOGEXPR
            self.eat(BRAC)
            return result
        else:
            self.eat(INTEGER)
            result = token.value
            if self.current_token.type == VAR or self.current_token.type == ASSIGN:             #ERROR
                self.error()
        return result

    def unaryOp(self):
        sign = 1
        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == MINUS:
                sign *= (-1)
                self.eat(MINUS)
            else:
                self.eat(PLUS)
        return sign*self.factor()
        
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.unaryOp()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.unaryOp()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.unaryOp()

        return result

    def expr(self):
        """Arithmetic expression parser / interpreter.

        >  14 + 2 * 3 - 6 / 2`
        17

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

    def logexpr(self):
        """
        logexpr: expr ((< | > | <= | >= | ==)*
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = last = self.expr()
        curr = 0
        flag = False
        fresult = True

        while self.current_token.type in (LESS, GRTR, EQU, LEQU, GREQU):
            flag = True
            
            token = self.current_token
            self.eat(token.type)
            curr = self.expr()
            #print(last)
            #print(token)
            #print(curr)
            
            
            if token.type == LESS:
                if curr <= last:
                    fresult = False
                
            elif token.type == GRTR:
                if curr >= last:
                    fresult = False
                
            elif token.type == EQU:
                if curr != last:
                    fresult = False
                
            elif token.type == LEQU:
                if curr < last:
                    fresult = False
                
            elif token.type == GREQU:
                if curr > last:
                    fresult = False
            last = curr
            
        if flag:
            return fresult
        return result

    def assignment(self):
        global variables
        
        token = self.current_token

        if token.type == VAR and token.value == 'EXIT':
            sys.exit()
        
        if token.type == VAR and token.value not in variables:
            self.eat(VAR)
            if self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                variables[token.value] = self.assignment()
                return variables[token.value]
            else:
                self.error()
        result = self.logexpr()
        #print(result)
        #if isinstance(result, bool):
            #print('yes bool')
         #   if result:
          #      result = 'True'
          #  else:
          #      result = 'False'
        return result
            
def main():
    while True:
        try:
            text = input('RAFMAT >>> ')
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.assignment()
        if not isinstance(result, int):
            #if float(result).is_integer():
            #    print ('{:.0f}'.format(result))
            #else:
            print ('{:.3f}'.format(result))
        else:
            print(result)


if __name__ == '__main__':
    main()
