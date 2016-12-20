KEYWORDS = {
    'PROGRAM': '401',
    'PROCEDURE': '402',
    'BEGIN': '403',
    'END': '404',
}

IDENTIFICATORS = {
    'SIGNAL': '1001',
    'COMPLEX': '1002',
    'INTEGER': '1003',
    'FLOAT': '1004',
    'BLOCKFLOAT': '1005',
    'EXT': '1006',
}

CONSTANTS = {

}

DELIMITERS = {
    ';': ord(';'),
    '.': ord('.'),
    ':': ord(':'),
    ',': ord(','),
    '=': ord('='),
}

SPECIFIC_SYMBOLS = {
    '(': ord('('),
    ')': ord(')'),
}

WHITESPACES = {
    chr(9): '9',
    chr(10): '10',
    chr(11): '11',
    chr(12): '12',
    chr(13): '13',
    chr(32): '32',
}