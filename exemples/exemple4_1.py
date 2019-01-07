from supercanvas import *

import math

w = beginMagicTk()

dim = 600
c = supercanvas(w, bg="black",
                width=dim,
                height=dim,
                grid=False,
                axes=False,
                xlabel=False,
                ticks=False,
                ylabel=False,
                zero=False)

c.setOrigin(300, 300)
c.setUnit(200, 200)

c.pack(expand=True)

x = lambda t: 2 * (1 - t ** 2) / (1 + t ** 2) ** 2
y = lambda t: 4 * t / (1 + t ** 2) ** 2

x = lambda t: math.cos(t)
y = lambda t: math.sin(t)


c.step=.01

p = .05
a, b = -10, 10
frames = int(1 + (b - a) / p)
t = a

listeSeg = []

for f in range(frames):
    ide = c.drawParam(x, y, t - 10*p, t, width=10,
                      fill="#ffcc00", smooth=1, capstyle="round")

    s = c.drawLine([0, 0, x(t), y(t)], fill="#ffcc80", width= 4)
    c.lower(s)
    listeSeg += [s]
    
    t += p
    c.update()
    c.after(10)
    # c.export()
    for s in range(f-9):
        c.delete(listeSeg[s])
    c.delete(ide)

endMagicTk(w)
