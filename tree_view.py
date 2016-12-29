
def show_tree(fn_name):
    def wrapper(fn):
        def wrapper_wrappper(self):
            self.print_tree_elem(METHOD_NAMES[fn_name], fn_name, self.curr_code, self.curr_codes_elem.get('lexem'), add=True)
            res = fn(self)
            self.print_tree_elem(METHOD_NAMES[fn_name], fn_name, self.curr_code, self.curr_codes_elem.get('lexem'), add=False)
            return res
        return wrapper_wrappper
    return wrapper


METHOD_NAMES = {
    'signal_program':1,
    'program': 2,
    'block': 3,
    'statements_list': 4,
    'paramenters_list': 5,
    'declarations_list': 6,
    'declaration': 7,
    'identifiers_list': 8,
    'attributes_list': 9,
    'attribute': 10,
    'procedure_identifier': 11,
    'variable_identifier': 12,
}