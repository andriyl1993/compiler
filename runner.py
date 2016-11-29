import file

from datetime import datetime
from lexical_analizer import LA

d1 = datetime.now()
data = file.read('program.txt')
la = LA(data)
la.run()
print la.code_row

print "Time = ", datetime.now()- d1
