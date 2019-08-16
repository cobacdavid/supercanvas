from supercanvas import *
from tkinter import *

w = tkinter.Tk()
dim = 800
f = Frame(w)
c = supercanvas(f, width=dim, height=dim, bg='white',
                axes=True, ticks=True,
                xlabel=True, ylabel=True,
                grid=True, zero=True,
                follow=False)


c.pack()
f.pack()


intervalleX = (-10, 35)
intervalleY = (-1.05, 1.05)
c.setView(*intervalleX, *intervalleY)
c.setTicks(5, .2)


c.step = .1


def decaleRepere(can=c, pasX=.1):
    minX, maxX, *_ = can.getView()
    can.setViewX(minX + pasX, maxX + pasX)
#    can.update()


# def suitCourbe(fonction, Xdepart, Xfin, can=c, canVisu=d, nb_etapes=100):
#     pas = (Xfin - Xdepart) / nb_etapes
#     x = Xdepart
#     for i in range(nb_etapes):
#         x1, x2, y1, y2 = can.getView()
#         demi_largeur = (x2 - x1) / 2
#         demi_hauteur = (y2 - y1) / 2
#         x1 = x - demi_largeur
#         x2 = x + demi_largeur
#         y1 = fonction(x) - demi_hauteur
#         y2 = fonction(x) + demi_hauteur
#         can.setView(x1, x2, y1, y2)
#         X1, Y2 = canVisu.__coordsCal2Can__(x1, y2)
#         X2, Y1 = canVisu.__coordsCal2Can__(x2, y1)
#         try:
#             canVisu.delete(visu)
#         except:
#             pass
#         visu = canVisu.create_rectangle(X1, Y2, X2, Y1, fill="white")
#         x += pas
#         canVisu.update
#         can.after(100)


import math
inverse = lambda x: 1 / x
def sinc(x):
    limite = 4.5 * math.pi
    g = lambda x: math.sin(x) / x
    if x == 0:
        return 1
    elif x < limite:
        return g(x)
    else:
        d = x - limite
        return g(limite - d)


def sinusC(x):
    global param
    limite = 4.5 * math.pi
    g = lambda x: math.sin(x) / ((1 - param) * x + param)
    if x < limite:
        try:
            return g(x)
        except:
            return 1
    else:
        d = x - limite
        return sinusC(limite - d)


for i in range(100+1):
    try:
        c.delete(courbe)
    except:
        pass
    param = i / 100
    courbe = c.drawFunction(sinusC, 0, 9 * math.pi,
                            fill="red",
                            width=5,
                            capstyle="round",
                            joinstyle="round")
    c.update()
    c.after(100)

# for i in range(100):
#     decaleRepere(pasX=.4)
#     c.after(100)

# c.after(5000)

# suitCourbe(fonction, 0, 9 * math.pi, nb_etapes=300)

w.bind("q", quit)
w.mainloop()
