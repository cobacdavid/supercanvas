from supercanvas import *

import math

w = beginMagicTk()

dim = 800
c = supercanvas(w, bg="black",
                width=dim,
                height=dim)

c.itemconfigure("repere", fill="white")
c.itemconfigure("axes", fill="white")
c.itemconfigure("zero", fill="white")
c.pack(expand=True)

c.create_text(dim / 2 ,dim / 2, anchor='ne', text="O", fill="white")
maxi =math.pi
f = lambda x : math.sin(x)

debut = 1
objectif = maxi
c.setView(-debut, debut, -debut, debut)

p = .025
frames = round((objectif - debut) / p)

offset = 10
txmax = c.width - offset
txmin = offset
c.step=.001
xmin, xmax, ymin, ymax = c.getView()
while xmax  <= maxi + 2 * p:
    xmin, xmax, ymin, ymax = c.getView()
    c.setView(xmin - p, xmax + p, ymin - p, ymax + p)
    x1, y = c.__coordsCan2Cal__(txmin, 0)
    x2, y = c.__coordsCan2Cal__(txmax, 0)
    if xmax - 2 * p  >= 1:
        c.drawFunction(lambda x: ( xmax - 2 * p) * f(x),
                       x1, x2,
                       fill="red", width=6, capstyle="round")
    c.drawFunction(lambda x: f(x),
                   x1, x2,
                   fill="red", width=6, capstyle="round")
    c.update()
    c.export()
    c.after(10)
    c.delete("supercanvas")




debut = maxi
objectif = 1
p = .06

frames = round((objectif - debut) / p)
for g in range(-frames):
    xmin, xmax, ymin, ymax = c.getView()
    c.setView(xmin + p, xmax - p, ymin + p, ymax - p)
    x1, y = c.__coordsCan2Cal__(txmin, 0)
    x2, y = c.__coordsCan2Cal__(txmax, 0)
    if xmax - 2 * p > 1:
        c.drawFunction(lambda x: (xmax - 2 * p) * f(x),
                       x1, x2,
                       fill="red", width=6, capstyle="round")
    c.drawFunction(lambda x: f(x),
                   x1, x2,
                   fill="red", width=6, capstyle="round")
    c.update()
    c.export()
    c.after(10)
    c.delete("supercanvas")

w.bind("<e>", c.export)

endMagicTk(w)
