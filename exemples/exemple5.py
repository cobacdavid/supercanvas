from supercanvas import *

w = beginMagicTk()

dim = 600
c = supercanvas(w, bg="white",
                width=dim,
                height=dim,
                grid=False,
                zero=False)

c.setOrigin(100, 300)
c.setUnit(200, 200)

x = lambda t: 2 * (1 - t ** 2) / (1 + t ** 2) ** 2
y = lambda t: 4 * t / (1 + t ** 2) ** 2

p = .05
a, b = -10, 10
maxi = int(1 + (b - a) / p)

t = a
for i in range(maxi):
    X, Y = x(t), y(t)
    c.drawLine([(0, 0), (X, Y)], fill="darkred", width=3)
    t += p

endMagicTk(w)
