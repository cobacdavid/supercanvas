from supercanvas import *
from tkinter import *
import math
from tkinter import font

##########################################################
# This is a SO code at this adress:
# https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v *= 255
        return  tuple2rgb(v, v, v)
    i = int(h * 6.) # XXX assume int() truncates!
    f = (h * 6.) - i
    p, q, t = int(255*(v*(1.-s))),\
        int(255*(v*(1.-s*f))),\
        int(255*(v*(1.-s*(1-f))))
    v *= 255
    i %= 6
    # if i == 0: return (v, t, p)
    # if i == 1: return (q, v, p)
    # if i == 2: return (p, v, t)
    # if i == 3: return (p, q, v)
    # if i == 4: return (t, p, v)
    # if i == 5: return (v, p, q)
    if i == 0: return tuple2rgb(v, t, p)
    if i == 1: return tuple2rgb(q, v, p)
    if i == 2: return tuple2rgb(p, v, t)
    if i == 3: return tuple2rgb(p, q, v)
    if i == 4: return tuple2rgb(t, p, v)
    if i == 5: return tuple2rgb(v, p, q)
############################################################


def tuple2rgb(*t):
    return "#" + "".join(["{:02x}".format(i) for i in t])


w=tkinter.Tk()
w.configure(background='white')
mafont = font.Font(family='Roboto Heavy', weight='bold', size=18)

dim = 800
f = Frame(w)
c = supercanvas(f, width=dim, height=dim, bg='black',
                axes=False, ticks=False,
                xlabel=False, ylabel=False,
                grid=False, zero=False,
                follow=False)

l = Label(f, text="", bg="black", fg="red", font=mafont)

intervalle = (-1, 100)
c.setView(*intervalle, *intervalle)
c.pack()
l.pack(fill=X)
f.pack()

def pgcd(a,b):
    if b > a:
        a, b = b, a
    if b == 0:
        return a
    return pgcd(b, a % b)

primes = [2]
def liste_premiers(limite):
    for nombre in range(primes[0] + 1, limite + 1):
        compose = 0
        for j in primes:
            if j <= math.sqrt(nombre):
                if nombre % j == 0:
                    compose = 1
                    break
        if not compose:
            primes.append(nombre)

liste_premiers(10_000)
## print(primes, len(primes))
## quit()

def montre_premiers(x, y):
    # position = x * 100 + y
    texte = "Nombres premiers ≤ 9 999"
    l.configure(text=texte)
    # print(position)
    c.delete("all")
    for col in range(100):
        for row in range(100):
            nombre = col * 100 + row
            if nombre in primes:
                couleur = "red"
                c.drawPoint(col, row, width=4,
                            fill=couleur, outline=couleur,
                            style="rectangle")


def evt(event):
    c.export()
    return True
    x, y = event.x, event.y
    x, y = c.__coordsCan2Cal__(x, y)
    x, y = round(x), round(y)
    print(x, y)
    montre_premiers(x, y)

montre_premiers(0, 0)
c.bind("<3>", evt)


w.bind("q", quit)
c.bind("q", quit)
w.mainloop()
