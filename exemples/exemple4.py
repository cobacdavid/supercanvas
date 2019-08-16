from supercanvas import *

w = beginMagicTk()

dim = 600
c = supercanvas(w, bg="white",
                width=dim,
                height=dim,
                grid=False)

c.setOrigin(100, 300)
c.setUnit(200, 200)

x = lambda t: 2 * (1 - t ** 2) / (1 + t ** 2) ** 2
y = lambda t: 4 * t / (1 + t ** 2) ** 2

c.step=.01
c.drawParam(x, y, -10, 10, width=3,
            fill="green",
            dash=(5,2))

endMagicTk(w)
