from tables import CONSTANTS, DELIMITERS, IDENTIFICATORS, KEYWORDS, WHITESPACES, SPECIFIC_SYMBOLS
from error import Error
from tree_view import show_tree

class SA(object):
    def __init__(self, codes):
        self.curr_code = None
        self.codes = codes
        self.curr_codes_elem = None
        self.curr_index = -1
        self.index = 1
        return super(SA, self).__init__()

    def _next(self):
        self.curr_index += 1
        try:
            self.curr_code = self.codes[self.curr_index]['code']
            self.curr_codes_elem = self.codes[self.curr_index]
            return self.curr_code
        except:
            return None

    def print_tree_elem(self, index, add=True):
        if add:
            print "-" * self.index + " " + str(index)
        self.index = self.index + 1 if add else self.index - 1

    @show_tree('signal_program')
    def _check_signal_program(self):
        if self._check_program():
            return True
        raise Error('signal_program', None, None)

    @show_tree('program')
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
                        self.curr_code = self._next()
                        if self.curr_code == DELIMITERS['.']:
                            return True
        raise Error('program', None, None)

    @show_tree('block')
    def _check_block(self):
        self.curr_code = self._next()
        if KEYWORDS['BEGIN'] == self.curr_code:
            if self._check_statements_list():
                self.curr_code = self._next()
                if KEYWORDS['END'] == self.curr_code:
                    return True
        raise Error('block', None, None)

    @show_tree('statements_list')
    def _check_statements_list(self):
        return True

    @show_tree('paramenters_list')
    def _check_paramenters_list(self):
        self.curr_code = self._next()
        if SPECIFIC_SYMBOLS['('] == self.curr_code:
            if self._check_declarations_list():
                if SPECIFIC_SYMBOLS[')'] == self.curr_code:
                    return True
        else:
            return True
        raise Error('statements_list')

    @show_tree('declarations_list')
    def _check_declarations_list(self):
        if self._check_declaration():
            if self._check_declarations_list():
                return True
        else:
            return True
        raise Error('declarations_list')

    @show_tree('declaration')
    def _check_declaration(self):
        if self._check_variable_identifier():
            if self._check_identifiers_list():
                if DELIMITERS[':'] == self.curr_code:
                    if self._check_attribute():
                        if self._check_attributes_list():
                            if DELIMITERS[';'] == self.curr_code:
                                return True
        else:
            return False
        raise Error('declaration')

    @show_tree('identifiers_list')
    def _check_identifiers_list(self):
        self.curr_code = self._next()
        if DELIMITERS[','] == self.curr_code:
            if self._check_variable_identifier():
                if self._check_identifiers_list():
                    return True
        else:
            return True
        raise Error("identifiers_list")

    @show_tree('attributes_list')
    def _check_attributes_list(self):
        if self._check_attribute():
            if self._check_attributes_list():
                return True
        else:
            return True
        raise Error('attributes_list')

    @show_tree('attribute')
    def _check_attribute(self):
        self.curr_code = self._next()
        if IDENTIFICATORS['SIGNAL'] == self.curr_code or IDENTIFICATORS['COMPLEX'] == self.curr_code or \
                IDENTIFICATORS['INTEGER'] == self.curr_code or IDENTIFICATORS['FLOAT'] == self.curr_code or \
                IDENTIFICATORS['BLOCKFLOAT'] == self.curr_code or IDENTIFICATORS['EXT'] == self.curr_code:
            return True
        else:
            return False

    @show_tree('procedure_identifier')
    def _check_procedure_identifier(self):
        self.curr_code = self._next()
        if self.curr_code in CONSTANTS.values():
            return True
        raise Error('procedure_identifier')

    @show_tree('variable_identifier')
    def _check_variable_identifier(self):
        self.curr_code = self._next()
        if self.curr_code in CONSTANTS.values():
            return True
        else:
            return False

    def run(self):
        self.curr_code = self._next()
        print CONSTANTS
        print DELIMITERS
        print IDENTIFICATORS
        print KEYWORDS
        print WHITESPACES
        print WHITESPACES
        self._check_signal_program()
        self.curr_code = self._next()
        if self.curr_code == None:
            return True
        else:
            raise Error('Error')
