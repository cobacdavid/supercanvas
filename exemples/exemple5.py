from supercanvas import *

import math

w = beginMagicTk()

dim = 600
c = supercanvas(w, bg="black",
                width=dim,
                height=dim)


c.setUnit(150, 150)
c.setOrigin(300, 300)
c.setTicks(.5, .5)

c.itemconfigure("repere", fill="white")
c.itemconfigure("axes", fill="white")

c.pack(expand=True)

x = lambda t: t
y = lambda t: t ** 3

p = .001
r = 1.25

a, b = -r, r
maxi = int(1 + (b - a) / p)

t = a
for i in range(maxi):
    X, Y = x(t), y(t)
    if X > 0:
        c.drawLine([(X, X), (X, Y)], fill="red", width=1)
    else:
        c.drawLine([(X, -X), (X, Y)], fill="red", width=1)

    t += p

c.update()

w.bind("<e>", c.export)

endMagicTk(w)
