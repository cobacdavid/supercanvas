from supercanvas import *

import math

w = beginMagicTk()

dim = 800
rapport = 1.5625
c = supercanvas(w, width=dim * rapport, height=dim,
                bg="black", xlabel=False, ylabel=False,
                grid=False, axes=False, zero=False)
c.pack(expand=True)

c.setView(-10.5, 2, -2, 6)

tour = math.pi
pas = .005

frames = int(1+tour/pas)

def rotation(x, y, angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return (c * x - s * y, s * x + c * y)


X1 = -5
X2 = 0

xpas = abs(X1) / (frames / 2) 

a = 0
for f in range(frames):
    c.drawLine([rotation(X1, 0, a), rotation(X2, 0, a)],
               fill="red", width=10, capstyle="round")
    c.update()
    c.after(10)
    c.export()
    a += pas
    X1 += xpas
    X2 += xpas 


c.export()
c.export()
c.export()
c.export()
c.export()
c.export()
c.export()

endMagicTk(w)
