from supercanvas import *
import random, math


w = beginMagicTk()

dim = 800
c = supercanvas(w, bg="white", width=dim, height=dim)
c.pack(expand=True)




def distance(l):
    x, y = l
    return x ** 2 + y ** 2

aleaList = [(random.normalvariate(0, 1),
             random.normalvariate(0, 1)) for i in range(1000)]

maxi = 0
distances = []
listeObj=[]
cercle = c.drawPoint(0, 0, fill="darkred", outline="darkred")

for p in aleaList:
    ide = c.drawPoint(*p, width=5, fill="green", outline="green")
    d = distance(p)
    if d > maxi:
        for o in listeObj:
            c.itemconfigure(o, fill="green", outline="green")
        c.itemconfigure(ide, fill="red", outline="red")
        x , y = c.getUnit()
        c.itemconfigure(cercle, width=x * 2 * math.sqrt(d))
        listeObj += [ide]
        maxi = d
    c.update()
    c.after(100)

endMagicTk(w)
