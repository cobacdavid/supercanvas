from .supercanvas import *


if __name__ == '__main__':

    example = 15
    
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 0
    ######################################################
    ######################################################
    ######################################################
    if example==0:
        r = tkinter.Tk()
        c = supercanvas(r, bg="white", width=500, height=500,
                        axes=True,
                        ticks=True,
                        follow=True)
        c.pack(expand=True)
        r.bind("<q>", quit)

        tkinter.mainloop()
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 1
    ######################################################
    ######################################################
    ######################################################
    elif example==1:
        import math
        r = tkinter.Tk()
        c = supercanvas(r, bg="white", width=800, height=600,
                        axes=True,
                        ticks=True,
                        follow=True)

        c.itemconfigure("ylabel", fill="red")
        c.setUnit(100, 100)
        c.setTicks(1, .5)
        #c.setOrigin(100,100)

        f=lambda x: x #(x!=0 and math.cos(x) / x) or 0
        g=lambda x:x>=0 and x**.5 or x<0 and (-x)**.5

        p = .1
        a, b = -5, 5
        x = a
        listePointsF = []
        listePointsG = []
        for i in range(round(1 + (b-a)/p)):
            c.drawPoint(x, f(x), fill="red", outline="red")
            listePointsF += (x, f(x))
            listePointsG += [x] + [g(x)]
            x += p

        c.drawLine(listePointsF, fill="green")
        c.drawLine(listePointsG, fill="blue", width=3)

        h=lambda x:math.sin(x)
        c.step = .01
        c.drawFunction(h, -math.pi, math.pi, fill="#ff00ff", width=1)

        c.itemconfigure("ticks", fill="red")

        c.pack(expand=True)
        # force un refresh
        #c.setOrigin(400,400)

        r.bind("<q>", quit)

        tkinter.mainloop()

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 2
    ######################################################
    ######################################################
    ######################################################

    elif example==2:
        import math
        r = tkinter.Tk()
        
        c = supercanvas(r, bg="#00964a")
        c.setOrigin(30, 150)
        c.setUnit(10, 80)

        f = lambda x: math.sin(x)/x
        c.step=.1
        c.drawFunction(f, c.step, 10*math.pi, width=3, fill="white")

        c.pack()
        r.bind("<q>", quit)
        tkinter.mainloop()
        
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 3
    ######################################################
    ######################################################
    ######################################################

    elif example==3:
        import math
        r = tkinter.Tk()
        
        c = supercanvas(r, bg="red", width=500, height=500)
        c.setOrigin(100, 250)
        c.setUnit(150, 150)

        x = lambda t: 2 * (1 - t ** 2) / (1 + t ** 2) ** 2
        y = lambda t: 4 * t / (1 + t ** 2) ** 2
        c.step=.001
        c.drawParam(x, y, -10, 10, width=3, fill="white")

        c.pack()
        r.bind("<q>", quit)
        tkinter.mainloop()
        
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 4
    ######################################################
    ######################################################
    ######################################################

    elif example==4:
        w = beginMagicTk()

        c = supercanvas(w, bg="white")
        c.setUnit(100, 20)
        c.setTicks(.5, 2)

        f=lambda x: x**3
        c.step=.1
        c.drawFunction(f, -3, 3)

        endMagicTk(w)
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 5
    ######################################################
    ######################################################
    ######################################################

    elif example==5:
        import math
        w = beginMagicTk()

        c = supercanvas(w, bg="white", ticks=False)
        c.setUnit(100, 100)
        
        f=lambda x: math.cos(x)
        g=lambda x: math.sin(2 * x)
        c.step = .01
        c.pack()
        w.update()
        for i in range(1,201):
            id = c.drawParam(f, g, 0, 2 * math.pi * i / 200, width=5, fill="red")
            w.update()
            c.export()
            w.after(100)
            c.delete(id)
        endMagicTk(w)
        
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 6
    ######################################################
    ######################################################
    ######################################################

    elif example==6:
        import math
        w = beginMagicTk()

        dim = 800
        
        c = supercanvas(w, bg="white", width=dim, height=dim, axes=False, ticks=False, grid=False,zero=False,xlabel=False,ylabel=False)
        c.pack(expand=True)
        c.update()
        c.setUnit(dim/2 - 2, dim/2 - 2)
        f=lambda x: math.cos(x)
        g=lambda x: math.sin(3 * x)
        n = 50
        c.step = .005
        for i in range(n + 1):
            #c.step = ( 200 - i != 0 and (200 - i) / 200 ) or .001
            # print(abs(n / 2 - j))
            id = c.drawParam(lambda x: math.cos((abs(n / 2 - i)) * x ),
                             lambda x:math.sin((n / 2 - abs(n / 2 - i)) * x ),
                             0, 2 * math.pi, width=5, fill="black", smooth=1)
            w.update()
            #c.export()
            w.after(10)
            c.delete(id)


        endMagicTk(w)
        
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 7
    ######################################################
    ######################################################
    ######################################################

    elif example==7:
        import math
        w = beginMagicTk()
        # canvas dimension
        dim = 600
        # offset: mid-with of the linewidth
        offset = 25
        #
        c = supercanvas(w, bg="white", width=dim, height=dim,
                        axes=False, ticks=False,
                        grid=False, xlabel=False,
                        ylabel=False, zero=False)
        c.pack(expand=True)
        c.setUnit(dim/2 - offset, dim/2 - offset)

        # steps between entry values
        c.step = .005
        # exploring to 10 with 50 values in-between
        n = 10
        steps = 50
        #
        for i in range(steps * n + 1):
            j = i / steps
            allerRetour = abs(n / 2 - j)
            twoPi = 2 * math.pi
            id = c.drawParam(lambda x: math.cos(allerRetour * x),
                             lambda x:math.sin((n / 2 - allerRetour) * x),
                             0, twoPi,
                             width=50, fill="black", smooth=1,
                             joinstyle="round", capstyle="round")
            # update content
            c.update()
            # export image to directory
            # next line to uncomment to export
            # c.export()
            # wait a little
            w.after(10)
            # delete actual curve from content
            c.delete(id)

        endMagicTk(w)

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 8
    ######################################################
    ######################################################
    ######################################################

    elif example==8:
        import math
        w = beginMagicTk()
        # canvas dimension
        dim = 600
        # offset: mid-with of the linewidth
        offset = 25
        #
        c = supercanvas(w, bg="black", width=dim, height=dim,
                        axes=False, ticks=False,
                        grid=False, xlabel=False,
                        ylabel=False)
        c.pack(expand=True)
        c.setUnit(dim/2 - offset, dim/2 - offset)
        # 
        #
        # steps between entry values
        c.step = .005
        # exploring to 10 with 50 values in-between
        n = 10
        steps = 50
        #
        for i in range(steps * n + 1):
            j = i / steps
            allerRetour = abs(n / 2 - j)
            twoPi = 2 * math.pi
            couleur = hsv_to_rgb( i / (n * steps +1), 1, 1)
            id = c.drawParam(lambda x: math.cos(allerRetour * x),
                             lambda x: math.sin((n / 2 - allerRetour) * x),
                             0, twoPi/4,
                             width=50, fill=couleur, smooth=1,
                             joinstyle="round", capstyle="round")
            # update content
            c.update()
            # export image to directory
            # next line to uncomment to export
            # c.export()
            # wait a little
            w.after(10)
            # delete actual curve from content
            c.delete(id)

        endMagicTk(w)

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 9
    ######################################################
    ######################################################
    ######################################################

    elif example==9:
        import math
        from opensimplex import OpenSimplex
        w = beginMagicTk()
        # canvas dimension
        dim = 600
        # offset: mid-with of the linewidth
        offset = 25
        #
        c = supercanvas(w, bg="black", width=dim, height=dim,
                        axes=False, ticks=False,
                        grid=False, xlabel=False, ylabel=False)
        c.pack(expand=True)
        c.setUnit(dim/3 - offset, dim/3 - offset)
        # 

        # steps between entry values
        c.step = .01
        
        tmp = OpenSimplex(seed=1)
        #
        f = lambda x: .18 * (3 * math.cos(x) - math.cos(3 * x))
        g = lambda x: .18 * (3 * math.sin(x) - math.sin(3 * x))

        #f = lambda x: math.cos(x)
        #g = lambda x: math.sin(x)
        
        #
        tabIndice = {}
        nbFigures = 1000
        for j in range(nbFigures):
            c.delete(id)
            p = .05
            a, b = 0, 2*math.pi
            #
            x = a
            listePoints = []
            for t in range(int(1 + (b - a) / p)):
                X, Y = f(x), g(x)
                r = 1 + .5 * tmp.noise3d(X, Y,  math.cos(2*math.pi*j/50))
                listePoints += [r * f(x)] + [r * g(x)]
                x += p
            x, y = listePoints[0:2]
            listePoints += [x, y]
            #
            it = iter(listePoints)
            tabIndice[j] = []
            for x in it:
                l = c.drawPoint(x, next(it), fill="red")
                tabIndice[j].append(l)
            #
            id = c.drawLine(listePoints, fill="white",
                            width=3, smooth=1,
                            capstyle="round", joinstyle="round")

            for k in range(j-20):
                for ind in tabIndice[k]:
                    c.delete(ind)
            # update content
            c.update()
                # export image to directory
                # next line to uncomment to export
            #c.export()
                # wait a little
            w.after(50)
                # delete actual curve from content


        endMagicTk(w)

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 10
    ######################################################
    ######################################################
    ######################################################

    elif example==10:
        import math
        
        w = beginMagicTk()
        # canvas dimension
        dim = 600
        #
        c = supercanvas(w, bg="black", width=dim, height=dim,
                        axes=False, ticks=False, zero=False,
                        grid=False, xlabel=False, ylabel=False)
        c.pack(expand=True)
        c.setUnit(.95*dim, .95*dim)
        c.setOrigin(.025*dim, .975*dim)
        c.setTicks(.5, .5)
        # 
        # set canvas background to black
        #
        # steps between entry values
        c.step = .01
        pas = .05
        a, b = 0, 5
        puissance = a
        maxi = int(1 + (b - a) / pas)
        maxi = 100

        tabObjet = {}
        for j in range(2 * maxi):
            if j <= maxi:
                if j == 0:
                    continue
                elif j <= maxi/2:
                    puissance = j / (maxi/2)
                else:
                    puissance = ( maxi / 2) / (maxi - j +.1)

                #c.delete(id)
                couleur = hsv_to_rgb( j / (maxi - 1), 1, 1)
                id = c.drawFunction(lambda x: x ** puissance,
                                  0, 1,
                                    width=4, fill=couleur, smooth=1,
                                    capstyle="round")

                tabObjet[j] = id
            else:
                if j == 0:
                    continue
                elif j <= 3 * maxi/2:
                    puissance = j / (2 * maxi)
                else:
                    puissance = ( 2 * maxi) / (2 * maxi - j)

                #c.delete(id)
                couleur = hsv_to_rgb( j / (maxi - 1), 1, 1)
                id = c.drawFunction(lambda x: x ** puissance,
                                  0, 1,
                                    width=4, fill=couleur, smooth=1,
                                    capstyle="round")

                tabObjet[j] = id
                
            if j > 5:
                for k in range(j-5,j):
                    couleur =  hsv_to_rgb( j / (maxi - 1), (k/2)*1/j , 1)
                    c.itemconfigure(tabObjet[k], fill=couleur)
            for k in range(1,j-5):
                c.delete(tabObjet[k])
            # update content
            c.update()
                # export image to directory
                # next line to uncomment to export
            #c.export()
                # wait a little
            w.after(10)
                # delete actual curve from content
        endMagicTk(w)


    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 11
    ######################################################
    ######################################################
    ######################################################

    elif example==11:
        import math
        w = beginMagicTk()
        # canvas dimension
        c = supercanvas(w, bg="white", width=600, height=300)
        c.pack(expand=True)
        #c.setUnit(100, 100)
        a, b = -3.141, 3.141
        c.setViewX(a, b)
        c.setViewY(-1.05, 1.05)
        c.setTicks(1, .1)

        c.step = .05
        c.drawFunction(math.sin, -100, 100,
                       width=3, fill="red",
                       smooth=1, joinstyle="round")
        
        c.pack(expand=True)
        c.update()
        for n in range(50):
            a += -.1
            b += .1
            c.after(10)
            # c.export()
            c.setViewX(a, b)
            c.update()

        for n in range(50):
            a += .5
            b += .5
            c.after(10)
            # c.export()
            c.setViewX(a, b)
            c.update()


        w.mainloop()

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 12
    ######################################################
    ######################################################
    ######################################################

    elif example==12:
        import math
        from opensimplex import OpenSimplex
        w = beginMagicTk()
        c = supercanvas(w, bg="white", width=600, height=600,
                        axes=False, ticks=False, zero=False,
                        grid=False, xlabel=False, ylabel=False)

        #c.create_rectangle(-10, -10, 700, 700, fill="darkred")
        c.update()
        f = lambda x:math.sin(x)

        c.step = .01
        a, b = -math.pi, math.pi

        c.setViewX(a - .2, b )
        c.setViewY(-1.2, 1.2)
        id = c.drawFunction(f, a, b, width=3, fill="red",
                       smooth=1, joinstyle="round",
                       capstyle="round")
        c.delete(id)
        c.pack(expand=True)
        c.update()

        p = .3
        maxi = int(1 + (b - a) / p)
        x = a
        for i in range(maxi):
           
            x += p

        k = 2
        listeId = {}
        for j in range(k):
            listeId[j]=[]
            listePN = []
            x = a
            for i in range(maxi):
                y = f(x)
                tmp = OpenSimplex(seed=j)
                n = tmp.noise3d(.05 * x, .05 * y, .05 * math.cos(2 * math.pi * i / maxi))
                ie = c.drawLine([x, 10, x, f(x)], width=3)
                id = c.drawPoint(x, y, 
                                 outline="",#hsv_to_rgb(abs((1+n)/1), 1, 1),
                                 fill=hsv_to_rgb(abs((1+n)/1), 1, 1),
                                 width=20)
                listeId[j].append(ie)
                listeId[j].append(id)
                x += p
            c.update()
            # c.export()
            c.after(100)
            #for element in listeId[j]:
                #c.delete(element)

        endMagicTk(w)

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 13
    ######################################################
    ######################################################
    ######################################################

    elif example == 13:
        w = beginMagicTk()
        dim = 600
        c = supercanvas(w, bg="white", width=dim, height=dim,
                        axes=True,
                        ticks=True, zero=False,
                        xlabel=True, ylabel=False,
                        grid=True)
        c.setUnit(100, 100)
        c.itemconfigure("axes", fill="red", width=1)
        c.itemconfigure("grid", fill="blue", dash=(5, 2, 1, 2))
        c.itemconfigure("ticks", fill="blue", width=5)
        c.step=.1
        c.drawFunction(lambda x:.5 * x**2, -5, 5,
                       fill="darkgreen", dash=(5, 2), width=4)
        c.update()
        endMagicTk(w)
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 14
    ######################################################
    ######################################################
    ######################################################

    elif example == 14:
        w = beginMagicTk()
        dim = 800
        c = supercanvas(w, bg="white", width=dim, height=dim,
                        axes=True,
                        ticks=True,
                        xlabel=False, ylabel=False,
                        grid=False)
        I = (-.1, 1.1)
        c.setViewX(*I)
        c.setViewY(*I)
        f = lambda x: 1/(1 + x)
        c.drawFunction(lambda x:x, *I)
        c.drawFunction(f, *I, smooth=1, width=2)
        c.drawSeq(f, 1, 3, fill="red", width=3)

        endMagicTk(w)

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 15
    ######################################################
    ######################################################
    ######################################################

    elif example == 15:
        import math
        from opensimplex import OpenSimplex
        from noise import *
        w = beginMagicTk()
        dim = 800
        c = supercanvas(w, bg="black", width=dim, height=dim,
                        axes=False,
                        ticks=False,
                        xlabel=False, ylabel=False,
                        grid=False,
                        zero=False)
        taille = 10
        I = (0, taille)
        c.setViewX(*I)
        c.setViewY(*I)
        c.pack(expand=True)

        frames = 100
        tabPoints = []
        listeN =[]

        functionVar = lambda x:math.cos( 2 * math.pi * x / frames)
        #functionVar = lambda x:(x<.5 and (2*x)**2) or (2 - 2*x)

        
        for f in range(frames):
            #tmp = OpenSimplex(seed=f)
            for id in tabPoints:
                c.delete(id)
            tabPoints = []
            var =  functionVar(f)
            coef = .1
            for i in range(taille + 1):
                for j in range(taille + 1):
                    #n = tmp.noise3d(coef * i, coef * j, .5 * var)
                    n = pnoise3(coef * i, coef * j, 1 * var)
                    # listeN += [n]
                    couleur = hsv_to_rgb((n + 1) / 2, 1, 1)
                    tabPoints += [c.drawPoint(i, j,
                                    fill=couleur, width=dim / (2 * taille), outline=couleur)]
            c.update()
            c.after(50)
            # c.export()
        #print(min(listeN), max(listeN))

        endMagicTk(w)
        
    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 16
    ######################################################
    ######################################################
    ######################################################

    elif example == 16:
        import math
        from noise import *
        from tkinter import font
        
        w = beginMagicTk()
        mafont = font.Font(family='Roboto Heavy', weight='bold')
        dim = 800
        c = supercanvas(w, bg="white", width=dim, height=dim,
                        axes=False,
                        ticks=False,
                        xlabel=False, ylabel=False,
                        grid=False,
                        zero=False)
        #print(font.families())
        #quit()

        taille = 60
        I = (0, taille)
        c.setViewX(*I)
        c.setViewY(*I)
        c.pack(expand=True)

        frames = 100
        tabPoints = []

        functionVar = lambda x:math.cos( 2 * math.pi * x / frames)
        #functionVar = lambda x:(x<.5 and (2*x)**2) or (2 - 2*x)

        tabChar = ['b', 'o', 'n', 'n', 'e', 'a', 'n', 'n', 'e', 'e', '2', '0', '1', '9']
        
        for f in range(frames):
            for id in tabPoints:
                c.delete(id)
            tabPoints = []
            var =  functionVar(f)
            coef = .09
            for i in range(taille + 1):
                for j in range(taille + 1):
                    n = pnoise3(coef * i, coef * j, 1 * var)
                    # listeN += [n]
                    couleur = hsv_to_rgb((n + 1) / 3, 1, 1)
                    # tabPoints += [c.drawPoint(i, j,
                    #                fill=couleur, width=dim / (2 * taille), outline=couleur)]
                    #n = (48 + ((n + 1) / 2) * 10)
                    #char = chr(int(n))
                    n = max(min(int(len(tabChar) * ((n + 1) / 2)) ,13),0)
                    x, y = c.__coordsCal2Can__(i, j)
                    tabPoints += [c.create_text(x, y,
                            text=tabChar[n],
                            fill=couleur,
                            font=mafont,
                            width=dim / (1.5 * taille))]
            c.update()
            c.after(10)
            # c.export()
        endMagicTk(w)

    ######################################################
    ######################################################
    ######################################################
    #######  EXAMPLE 17
    ######################################################
    ######################################################
    ######################################################

    elif example == 17:
        import random, math
        import noise
        from tkinter import font
        
        w = beginMagicTk()
        dim = 800
        c = supercanvas(w, bg="white", width=dim, height=dim,
                        axes=False,
                        ticks=False,
                        xlabel=False, ylabel=False,
                        grid=False,
                        zero=False)
        I=(-1, 50)
        c.setViewX(*I)
        c.setViewY(*I)
        c.pack(expand=True)

        c.update()
        
        frames = 500
        
        r = range(50)
        s = range(50)
        t = list(range(9))
        u = t * 2500
        random.shuffle(u)
        
        tabId = []
        for f in range(frames):
            for o in tabId:
                c.delete(o)
            tabId = []
            k = 0
            coef = .07
            for i in r:
                for j in s:
                    n = noise.snoise3(coef * i, coef * j,
                                math.cos(2 * math.pi * f / frames))
                    n= (n + 1) / 2
                    couleur = hsv_to_rgb(n+.7, 1, 1)
                    x, y = c.__coordsCal2Can__(i, j)
                    #ide = c.create_text(x, y, text=str(u[k]), fill=couleur)
                    ide = c.drawLine([i, j, i+1, j+1],  fill=couleur)
                    tabId += [ide]
                    u[k] = (u[k] + 1) % len(t)
                    k += 1
            c.update()
            c.after(100)

        
        endMagicTk(w)
