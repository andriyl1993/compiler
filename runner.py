import file

from lexical_analizer import LA
from syntax_analizer import SA

data = file.read('program.txt')
la = LA(data)
la.run()
print la.code_row

sa = SA(la.code_row)
sa.run()
