from supercanvas import *

w = beginMagicTk()

dim = 600
rapport = 16 / 9
c = supercanvas(w, bg="white",
                width=rapport * dim,
                height=dim)

c.setViewX(-.5, 4)
c.setViewY(-.5, 2.5)


c.itemconfigure("grid", dash=(20, 2))

f = lambda x: x ** .5

c.step = 1
c.drawFunction(f, 0, 8, width=2,
               fill="green")

c.step = .1 # it's the default's value
c.drawFunction(f, 0, 8, width=3,
               fill="blue")

c.step = .01
c.drawFunction(f, 0, 8, width=1,
               fill="red")

endMagicTk(w)
