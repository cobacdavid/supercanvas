from supercanvas import *

import math

w = beginMagicTk()

dim = 600
rapport = 1
c = supercanvas(w, width=dim * rapport, height=dim,
                bg="black", xlabel=False, ylabel=False,
                grid=False, axes=False, zero=False)
c.pack(expand=True)


R1 = 5
R2 = 3

c.setView(-5, 13, -10, 8)

tour = 4 * math.pi
pas = .2q

frames = int(1+tour/pas)

# xpas = abs(X1) / (frames / 2) 

for s in range(0,10):
    t = 0
    listeS = []
    for f in range(frames):

        coef = 1.01**(s*f/frames)
        
        xg = R1 * math.cos(t)
        yg = R1 * math.sin(t)

        xp = R1 +  R2 + R1 * math.cos(coef*t)
        yp = R1 * math.sin(coef*t)

        id = c.drawLine([xg, yg, xp, yp], fill="white", width=3,\
                        capstyle="round")
        listeS += [id]
        c.update()
        c.after(100)
        #c.delete(id)
        #c.export()
        t += pas

# for s in listeS:
#     c.itemconfigure(s, fill="black")
#     c.update()
#     c.after(100)
#     c.export()

    
endMagicTk(w)
