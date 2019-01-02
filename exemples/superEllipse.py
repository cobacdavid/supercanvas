from supercanvas import *

w = beginMagicTk()
c = supercanvas(w, bg="white")

c.setViewX(-2, 2)
c.setViewY(-2, 2)

import math

c.step=.1
c.pack(expand=True)
c.update()
p = .1
maxi = int(1 + (10-0)/p)
var = p
for i in range(maxi):
    f = lambda x: math.cos(x) ** (2/var)
    g = lambda x: math.sin(x) ** (2/var)
    id = c.drawParam(f, g, p, math.pi/2, width=5, fill="red")
    c.update()
    c.after(100)
    c.delete(id)
    var += p

endMagicTk(w)
