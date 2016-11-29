from tables import CONSTANTS, DELIMITERS, IDENTIFICATORS, KEYWORDS, WHITESPACES
from error import Error

class LA(object):
    def __init__(self, text):
        self.text = text
        self.curr_index = -1
        self.curr_lexem = ""
        self.state = "S"
        self.length_file = len(text)
        self.code_row = []

    def _next(self):
        self.curr_index += 1
        return self.text[self.curr_index] if self.curr_index != self.length_file else None

    def is_next_lexem_state(self):
        if self.state == "S" or self.state == "OUT":
            return True
        else:
            return False

    def _add_constant(self):
        consts = CONSTANTS.values()
        if len(consts):
            last = consts[-1]
            next = int(last) + 1
        else:
            next = '501'
        CONSTANTS[self.curr_lexem] = str(next)
        return str(next)

    def _get_code_lexem(self):
        if (self.state == "IDN" or self.state == "WS" or self.state == "DEL") and self.curr_lexem in KEYWORDS:
            return KEYWORDS[self.curr_lexem]
        if (self.state== "IDN") and self.curr_lexem in IDENTIFICATORS:
            return IDENTIFICATORS[self.curr_lexem]
        if (self.state == "IDN" or self.state == "NUM"):
            if not self.curr_lexem in CONSTANTS:
                return self._add_constant()
            else:
                return CONSTANTS[self.curr_lexem]
        if self.state == "DEL" and self.curr_lexem in DELIMITERS:
            return DELIMITERS[self.curr_lexem]
        return None

    def run(self):
        ch = self._next()
        while self.state != "EXIT":
            if ch == None:
                self.state = "EXIT"
                break

            if ch.isalpha() and self.is_next_lexem_state():
                self.state = "IDN"
                while self.state != "OUT":
                    self.curr_lexem += ch
                    ch = self._next()
                    if not ch or not (ch.isalpha() or ch.isdigit()):
                        code = self._get_code_lexem()
                        self.curr_lexem = ""
                        self.state = "OUT"
            elif ch.isdigit() and self.is_next_lexem_state():
                self.state = "NUM"
                while self.state != "OUT":
                    self.curr_lexem += ch
                    ch = self._next()
                    if not ch or not ch.isdigit():
                        code = self._get_code_lexem()
                        self.curr_lexem = ""
                        self.state = "OUT"
            elif ch in DELIMITERS and self.is_next_lexem_state():
                self.state = "DEL"
                while self.state != "OUT":
                    self.curr_lexem += ch
                    ch = self._next()
                    if not ch or not ch in DELIMITERS:
                        code = self._get_code_lexem()
                        self.curr_lexem = ""
                        self.state = "OUT"
            elif ch in WHITESPACES and self.is_next_lexem_state():
                self.state = "WS"
                while self.state != "OUT":
                    ch = self._next()
                    if not ch or not ch in WHITESPACES:
                        code = None
                        self.state = "OUT"
            elif ch == '(' and self.is_next_lexem_state():
                self.curr_lexem = ch
                ch = self._next()
                if ch == "*":
                    self.state = "COM"
                    while not self.state == "OUT":
                        ch = self._next()
                        if ch == "*" and self._next() == ")":
                            ch = self._next()
                            self.state = "OUT"
                        elif ch == None:
                            self.state = "ERROR"
                            break

            if self.state == "ERROR":
                error = Error('message Error')
                return error.print_mess()

            if code:
                self.code_row.append(code)