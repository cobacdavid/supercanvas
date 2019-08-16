# David COBAC
# mi-février 2019

from supercanvas import *
import random, math
from tkinter import font

def point_hasard(x, y, distance):
    theta = 2 * math.pi * random.random()
    x1 = distance * math.cos(theta)
    y1 = distance * math.sin(theta)
    return (x + x1, y + y1)


w = beginMagicTk()
mafont = font.Font(family='Roboto Heavy', weight='bold', size=18)
dim = 800
c = supercanvas(w, width=dim, height=dim,
                bg ="white",
                axes=False, ticks=False,
                xlabel=False, ylabel=False,
                grid=False, zero=False,
                follow=False)

c.pack(expand=True)
offset = .1
intervalle = (-1 - offset, 1 + offset)
c.setView(*intervalle, *intervalle)
c.update()

espacement = 2/3
longueur_aiguilles = espacement

liste = [round(-1 + i * espacement, 6) for i in range(4)]
for v in liste:
    c.drawLine(((v, 1 + offset), (v, -1 - offset)), width=3)

nb_aiguilles = 200
compteur = 0

ide = c.create_text(0, 0, text="")
for i in range(nb_aiguilles):
    c.delete(ide)
    # entre -0.5 et 0.5
    x = random.random() - .5
    y = random.random() - .5
    x1, y1 = point_hasard(x, y, longueur_aiguilles)
    couleur = "gray"
    # tests à revoir pour ne pas hardcoder ces valeurs
    # ça doit pouvoir se faire avec des retour à 0 et
    # un signe de produit
    if (x < -1/3 and x1 > -1/3) or (x < 1/3 and x1 > 1/3) or\
       (x1 < -1/3 and x > -1/3) or (x1 < 1/3 and x > 1/3) or\
       (x1 < -1 and x > -1) or (x1 > 1 and x < 1):
        compteur += 1
        couleur = "red"
    c.drawLine(((x, y), (x1, y1)), width=2 , fill=couleur)
    #
    if compteur>0:
        texte = "{:03}".format(compteur) + " aiguilles sur " +\
            "{:03}".format(i+1) + ":  π ≈ {:1.5}".format((i+1)*2/compteur)
        ide = c.create_text(dim // 6, dim - 50, text=texte,
                        anchor=tkinter.W,
                        font=mafont)
    #
    c.after(50)
    # c.export()
    c.update()


endMagicTk(w)
