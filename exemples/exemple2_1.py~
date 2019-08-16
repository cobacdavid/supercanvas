from supercanvas import *
import random

w = beginMagicTk()

dim = 800
c = supercanvas(w, bg="white", width=dim, height=dim)

aleaList = [(random.normalvariate(0, 1),
             random.normalvariate(0, 1)) for i in range(100)]

for p in aleaList:
    c.drawPoint(*p, width=5, fill="red", outline="red")

endMagicTk(w)
