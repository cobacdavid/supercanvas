from supercanvas import *
from tkinter import *

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
#qw = beginMagicTk()
dim = 800
f = Frame(w)
c = supercanvas(f, width=dim, height=dim, bg='black',
                axes=False, ticks=False,
                xlabel=False, ylabel=False,
                grid=False, zero=False,
                follow=False)

l = Label(f, text="", bg="black", fg="white")

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

def montre_premiers_avec(x, y):
    position = x * 100 + y
    texte = "Nombres premiers avec " + str(position)
    l.configure(text=texte)
    print(position)
    c.delete("all")
    for col in range(1, 100):
        for row in range(1, 100):
            nombre = col * 100 + row
            if nombre < position:
                reste = position % nombre
                couleur = hsv_to_rgb(nombre / position, 1, 1)
            else:
                reste = nombre % position
                couleur = hsv_to_rgb(position / nombre, 1, 1)
            ## 
            # h = nombre / position
            # if h > 1:
            #     h = position/nombreq
            if reste == 1:
                c.drawPoint(col, row, width=4,
                            fill=couleur, outline=couleur,
                            style="rectangle")
                # c.drawLine([(0, row), (100, row)], fill=couleur, width=1)
                # c.drawLine([(col, 0), (col, 100)], fill=couleur, width=1)

def evt(event):
    x, y = event.x, event.y
    x, y = c.__coordsCan2Cal__(x, y)
    x, y = round(x), round(y)
    print(x, y)
    montre_premiers_avec(x, y)


c.bind("<3>", evt)

# for nombre in range(200,300):
#     for col in range(100):
#         for row in range(100):
#             position = col * 100 + row
#             couleur = "green"
#             if pgcd(position, nombre) == 1:
#                 couleur = "white"
#                 c.drawPoint(col, row, width=4, fill=couleur, outline=couleur)
#                 # c.drawLine([(0, row), (100, row)], fill=couleur, width=1)
#                 # c.drawLine([(col, 0), (col, 100)], fill=couleur, width=1)
#     c.update()
#     c.after(100)
#     # c.export()
#     c.delete("all")

w.bind("q", quit)
w.mainloop()
