from supercanvas import *
import  math, cmath

w = beginMagicTk()

dim = 600
c = supercanvas(w, bg="purple", width=dim, height=dim)
id = c.create_rectangle(-5, -5, dim+5, dim+5, fill="purple")

I = (-4.5, 4.5)
c.setViewX(*I)
c.setViewY(*I)

c.itemconfigure("grid", fill="white", width=1)
c.itemconfigure("axes", fill="green", width=3)
c.itemconfigure("tticks", fill="green")
c.itemconfigure("ticks", fill="green")
c.pack(expand=True)
p = .05

a, b = -math.pi/4, math.pi/4
t = a
for i in range(int(1 + (b - a) / p)):
    z1 = 1 + math.tan(t)*1j
    z2 = 2 * z1
    z = z1 * z2
    c.drawPoint(z.real, z.imag, width=5, fill="green", outline=None)
    t += p
    c.update()
    c.lower(id)
    c.after(100)
    c.export()
    
endMagicTk(w)
