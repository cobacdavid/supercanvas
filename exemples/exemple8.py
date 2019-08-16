from supercanvas import *

import math

w = beginMagicTk()

dim = 800
rapport = 1
c = supercanvas(w, width=dim * rapport, height=dim,
                bg="black", xlabel=False, ylabel=False,
                grid=False, axes=False, zero=False)
c.pack(expand=True)

c.setView(-10, 10, -10, 10)

tour = 4 * math.pi
pas = .1

frames = int(1+tour/pas)

# xpas = abs(X1) / (frames / 2) 

R1 = 10
R2 = 5

t = 0
listeS = []
for f in range(frames//2):

    xg = R1 * math.cos(t)
    yg = R1 * math.sin(t)

    xp = R2 + R2 * math.cos(t)
    yp = R2 * math.sin(t)

    id = c.drawLine([xg, yg, xp, yp], fill="white", width=5)
    listeS += [id]
    c.update()
    c.after(100)
    c.export()
    t += pas

for s in listeS:
    c.itemconfigure(s, fill="black")
    c.update()
    c.after(100)
    c.export()

    
endMagicTk(w)
