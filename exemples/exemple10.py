import random, math
from supercanvas import *
from tkinter import font

# x et y en coords maths
def est_dans_disque(x, y):
    return x ** 2 + y ** 2 <= 1

w = beginMagicTk()
mafont = font.Font(family='Roboto Heavy', weight='bold', size=18)

dim = 800
c = supercanvas(w, width=dim, height=dim, bg="white")
c.pack(expand=True)

offset = .1
intervalle = (-offset, 1+offset)
c.setView(*intervalle, *intervalle)
c.update()
qC=c.create_arc(*c.__coordsCal2Can__(-1, 1),
             *c.__coordsCal2Can__(1, -1),
             width=0, fill="#FFAAAA", outline="#FFAAAA")
nb_points = 10_000
compteur = 0
for i in range(nb_points):
    x, y = random.random(), random.random()
    b = est_dans_disque(x, y)
    compteur += b
    couleur = ["black", "white"][b]
    c.drawPoint(x, y, fill=couleur, outline=couleur, width=1)
    frq = compteur / (i + 1)
    part = frq * 100
    approx_pi = 4 * frq
    texte = "{:04d} points dont {:4.2f}% dans \
le quart de cercle : π ≈ {:4.3}".format(i + 1, frq * 100, 4 * frq)
    ide = c.create_text(dim // 6, dim - 50, text=texte,
                        anchor=tkinter.W,
                        font=mafont)
    if i <= nb_points - 1:
        c.update()
        c.tag_lower(qC)
        w.after(10)
        # c.export()
        c.delete(ide)

endMagicTk(w)
