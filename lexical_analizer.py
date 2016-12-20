from tables import CONSTANTS, DELIMITERS, IDENTIFICATORS, KEYWORDS, WHITESPACES, SPECIFIC_SYMBOLS
from error import Error

class LA(object):
    def __init__(self, text):
        self.text = text
        self.curr_index = -1
        self.curr_lexem = ""
        self.state = "S"
        self.length_file = len(text)
        self.code_row = []
        self.current_x_pos = -1;
        self.current_y_pos = 0;
        self.open_bracket = False

    def _next(self):
        self.curr_index += 1
        return self.text[self.curr_index] if self.curr_index != self.length_file else None

    def _add_constant(self):
        consts = CONSTANTS.values()
        consts.sort()
        if len(consts):
            last = consts[-1]
            next = int(last) + 1
        else:
            next = '501'
        CONSTANTS[self.curr_lexem] = str(next)
        return str(next)

    def _get_code_lexem(self, state):
        if (state == "IDN" or state == "WS" or state == "DEL") and self.curr_lexem in KEYWORDS:
            return KEYWORDS[self.curr_lexem]
        if (state== "IDN") and self.curr_lexem in IDENTIFICATORS:
            return IDENTIFICATORS[self.curr_lexem]
        if (state == "IDN" or state == "NUM"):
            if not self.curr_lexem in CONSTANTS:
                return self._add_constant()
            else:
                return CONSTANTS[self.curr_lexem]
        if state == "DEL" and self.curr_lexem in DELIMITERS:
            return DELIMITERS[self.curr_lexem]
        return Error('Lexem is not find', self.curr_index, '')

    def _add_to_row(self, code, lexem):
        if code:
            self.code_row.append({
                'lexem': lexem,
                'pos': self.curr_index,
                'code': code,
            })

    def _identificators(self, ch):
        while True:
            self.curr_lexem += ch
            ch = self._next()
            if not ch or not (ch.isalpha() or ch.isdigit()):
                code = self._get_code_lexem('IDN')
                lexem = self.curr_lexem
                self.curr_lexem = ""
                self._add_to_row(code, lexem)
                break
        return ch

    def _numers(self, ch):
        self.curr_lexem = ch
        ch = self._next()
        if ch.isdigit():
            return Error('Only digits', self.curr_index, self.curr_lexem)
        else:
            code = self._get_code_lexem('NUM')
            lexem = self.curr_lexem
            self.curr_lexem = ""
            self._add_to_row(code, lexem)
        return ch

    def _delimiters(self, ch):
        self.curr_lexem = ch

        ch = self._next()
        if ch in DELIMITERS and ch != "*":
            return Error('Only delimiters with length 1', self.curr_index, self.curr_lexem)
        elif ch == "*":
            return self._comments(ch)
        else:
            code = self._get_code_lexem('DEL')
            lexem = self.curr_lexem
            self.curr_lexem = ""
            self._add_to_row(code, lexem)
        return ch

    def _whitespaces(self, ch):
        while True:
            if ch == '\n':
                self.current_y_pos += 1
                self.current_x_pos = -1

            ch = self._next()

            if not ch or not ch in WHITESPACES:
                break
        return ch

    def _comments(self, ch):
        self.curr_lexem = ch
        if ch != "*":
            ch = self._next()
        if ch == "*":
            while True:
                ch = self._next()
                if ch == "*" and self._next() == ")":
                    ch = self._next()
                    self.curr_lexem = ""
                    break
                elif ch == None:
                    return Error('Comment not closed', self.curr_index)
        return ch

    def run(self):
        ch = self._next()
        while True:
            self.current_x_pos += 1
            if ch == None:
                if self.open_bracket:
                    raise Error('Bracket doesn\'t close', self.curr_index)
                return self.code_row

            if isinstance(ch, Error):
                return ch

            if ch.isalpha():
                ch = self._identificators(ch)
            elif ch.isdigit():
                ch = self._numers(ch)
            elif ch in DELIMITERS:
                ch = self._delimiters(ch)
            elif ch in WHITESPACES:
                ch = self._whitespaces(ch)
            elif ch in SPECIFIC_SYMBOLS:
                if ch == "(":
                    ch = self._next()
                    if ch == "*":
                        ch = self._comments(ch)
                    else:
                        self._add_to_row(SPECIFIC_SYMBOLS['('], '(')
                elif ch == ")":
                    self._add_to_row(SPECIFIC_SYMBOLS[')'], ch)
                    ch = self._next();
            else:
                raise Error('Symbol doesn\'t allow')
