from supercanvas import *
from tkinter import *

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
    for col in range(100):
        for row in range(100):
            nombre = col * 100 + row
            couleur = "green"
            if pgcd(position, nombre) == 1:
                couleur = "white"   
                c.drawPoint(col, row, width=4,
                            fill=couleur, outline=couleur,
                            style='rectangle')
                # c.drawLine([(0, row), (100, row)], fill=couleur, width=1)
                # c.drawLine([(col, 0), (col, 100)], fill=couleur, width=1)


def evt(event):
    x, y = event.x, event.y
    x, y = c.__coordsCan2Cal__(x, y)
    x, y = round(x), round(y)
    montre_premiers_avec(x, y)

c.bind("<3>", evt)

for nombre in range(1,300):
    x = int(nombre / 100)
    y = nombre % 100
    montre_premiers_avec(x, y)
    c.update()
    c.after(500)
    
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
    
