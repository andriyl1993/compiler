import file

from lexical_analizer import LA

data = file.read('program.txt')
la = LA(data)
la.run()

print la.code_row

