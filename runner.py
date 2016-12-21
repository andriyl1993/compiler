import file

from lexical_analizer import LA
from syntax_analizer import SA
from error import Error

data = file.read('program.txt')
la = LA(data)
res = la.run()
if isinstance(res, Error):
    res.print_err(la.current_y_pos, la.current_x_pos)
else:
    print la.code_row
    sa = SA(la.code_row)
    sa.run()
