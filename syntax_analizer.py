from tables import CONSTANTS, DELIMITERS, IDENTIFICATORS, KEYWORDS, WHITESPACES
from error import Error

class SA(object):
    def __init__(self, codes):
        self.curr_code = None
        self.codes = codes
        self.curr_codes_elem = None
        self.curr_index = -1

    def _next(self):
        self.curr_index += 1
        self.curr_code = self.codes[self.curr_index]['code']
        self.curr_codes_elem = self.codes[self.curr_index]
        return self.curr_code

    def _check_signal_program(self):
        if self._check_program():
            return True
        raise Error('signal_program', None, None)

    def _check_program(self):
        if KEYWORDS['PROGRAM'] == self.curr_code :
            if self._check_procedure_identifier():
                self.curr_code = self._next()
                if DELIMITERS[';'] == self.curr_code:
                    if self._check_block():
                        return True
        elif KEYWORDS['PROCEDURE'] == self.curr_code:
            if self._check_procedure_identifier():
                if self._check_paramenters_list():
                    if self._check_block():
                        return True
        raise Error('program', None, None)

    def _check_block(self):
        self.curr_code = self._next()
        if KEYWORDS['BEGIN'] == self.curr_code:
            if self._check_statements_list():
                if KEYWORDS['END'] == self.curr_code:
                    return True
        raise Error('block', None, None)

    def _check_statements_list(self):
        return True

    def _check_paramenters_list(self):
        self.curr_code = self._next()
        if DELIMITERS['('] == self.curr_code:
            if self._check_declarations_list():
                self.curr_code = self._next()
                if DELIMITERS[')'] == self.curr_code:
                    return True
        else:
            return True
        raise Error('statements_list')

    def _check_declarations_list(self):
        if self._check_declaration():
            if self._check_declarations_list():
                return True
        else:
            return True
        raise Error('declarations_list')

    def _check_declaration(self):
        if self._check_variable_identifier():
            if self._check_identifiers_list():
                self.curr_code = self._next()
                if DELIMITERS[':'] == self.curr_code:
                    if self._check_attribute():
                        if self._check_attributes_list():
                            self.curr_code = self._next()
                            if DELIMITERS[';'] == self.curr_code:
                                return True
        raise Error('declaration')


    def _check_identifiers_list(self):
        self.curr_code = self._next()
        if DELIMITERS[','] == self.curr_code:
            if self._check_variable_identifier():
                if self._check_identifiers_list():
                    return True
        else:
            return True
        raise Error("identifiers_list")

    def _check_attributes_list(self):
        if self._check_attribute():
            if self._check_attributes_list():
                return True
        raise Error('attributes_list')

    def _check_attribute(self):
        self.curr_code = self._next()
        if IDENTIFICATORS['SIGNAL'] == self.curr_code or IDENTIFICATORS['COMPLEX'] == self.curr_code or \
                IDENTIFICATORS['INTEGER'] == self.curr_code or IDENTIFICATORS['FLOAT'] == self.curr_code or \
                IDENTIFICATORS['BLOCKFLOAT'] == self.curr_code or IDENTIFICATORS['EXT'] == self.curr_code:
            return True
        raise Error('attribute')

    def _check_procedure_identifier(self):
        self.curr_code = self._next()
        if self.curr_code in CONSTANTS.values():
            return True
        raise Error('procedure_identifier')

    def _check_variable_identifier(self):
        self.curr_code = self._next()
        if self.curr_code in CONSTANTS.values():
            return True
        raise Error('variable_identifier')

    def run(self):
        self.curr_code = self._next()
        print CONSTANTS
        print DELIMITERS
        print IDENTIFICATORS
        print KEYWORDS
        print WHITESPACES
        self._check_signal_program()
