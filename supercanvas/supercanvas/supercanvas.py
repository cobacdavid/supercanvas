# auteur : david cobac
# Début 27/12/2018

import tkinter
from tkinter import filedialog

import time
import os

############################################################################
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
############################################################################


def tuple2rgb(*t):
    return "#" + "".join(["{:02x}".format(i) for i in t])


def beginMagicTk():
    import tkinter
    r = tkinter.Tk()
    r.bind("<q>", quit)
    return r

def endMagicTk(root):
    for w in root.winfo_children():
        w.pack(expand=True)
    tkinter.mainloop()

class supercanvas(tkinter.Canvas):
    def __init__(self, master, **options):
        #########################
        # traitement des options
        # valeurs par défaut
        self.axes   = True
        self.ticks  = True
        self.tticks = True
        self.grid   = True
        self.zero   = True
        self.follow = True
        # parsing de ce qui a été passé à l'appel
        aSupprimer = []
        for k, v in options.items():
            if k=="axes":
                self.axes = v
                aSupprimer.append("axes")
            elif k=="ticks":
                self.ticks = v
                aSupprimer.append("ticks")
            elif k=="tticks":
                self.tticks = v
                aSupprimer.append("tticks")
            elif k=="grid":
                self.grid = v
                aSupprimer.append("grid")
            elif k=="zero":
                self.zero = v
                aSupprimer.append("zero")
            elif k=="follow":
                self.follow = v
                aSupprimer.append("follow")
        # suppression des options particulières
        # pour permettre de passer le reste au canvas pur
        for option in aSupprimer:
            del options[option]
        #########################
        tkinter.Canvas.__init__(self, master, **options)
        #########################
        self.width, self.height  = map(int, self.getDim())
        self.x_origin = self.width / 2
        self.y_origin = self.height / 2
        self.x_unit   = 100
        self.y_unit   = 100
        self.dx_ticks = 1
        self.dy_ticks = 1
        self.step     = .1
        ########################
        # tableau des coordonnées passées en arg. de tous
        # les objets créés (sauf axes)
        self.coordsInit = {}
        ########################
        # comme le canvas reçoit l'appel <Configure> au départ
        # ce qui suit est dispenasable
        self.drawAxes()
        self.drawTicks()
        self.drawTTicks()
        self.drawGrid()
        self.drawZero()
        ########################
        self.event_add("<<Suivi>>", "<Motion>")
        self.event_add("<<Partir>>", "<Leave>")
        #
        self.bind('<Configure>', self.__refresh)
        self.bind('<<Suivi>>', self.__followCursor)
        self.bind('<<Partir>>', self.__partir)
        # self.bind('<<Export>>', self.__export)
        self.bind('<1>', self.__savePosition)
        self.bind('<B1-Motion>', self.__translation)
        self.bind('<ButtonRelease-1>', self.__landing)

    def setOrigin(self, x, y):
        self.x_origin_sv = self.x_origin
        self.y_origin_sv = self.y_origin
        self.x_origin = x
        self.y_origin = y
        self.__refresh()

    def getOrigin(self):
        return [self.x_origin, self.y_origin]

    def setViewX(self, x1, x2):
        x1, x2 = min(x1, x2), max(x1, x2)
        self.x_unit = self.width / (x2 - x1)
        self.x_origin = - self.x_unit * x1
        self.__refresh()

    def setViewY(self, y1, y2):
        y1, y2 = min(y1, y2), max(y1, y2)
        self.y_unit = self.height / (y2 - y1)
        self.y_origin = self.y_unit * y2
        self.__refresh()

    def getView(self):
        x1, y2 = self.__coordsCan2Cal__(0, 0)
        x2, y1 = self.__coordsCan2Cal__(self.width, self.height)
        return [(x1,x2), (y1,y2)]

    def setUnit(self, x, y):
        self.x_unit_sv = self.x_unit
        self.y_unit_sv = self.y_unit
        self.x_unit = x
        self.y_unit = y
        self.__refresh()

    def getUnit(self):
        return [self.x_unit, self.y_unit]

    def setTicks(self, dx, dy):
        self.dx_ticks = dx
        self.dy_ticks = dy
        self.__refresh()

    def getTicks(self):
        return [self.dx_ticks, self.dy_ticks]

    def setDim(self, x, y):
        self.configure(width=x, height=y)
        self.__refresh()

    def getDim(self):
        return [self.cget("width"), self.cget("height")]

    ############################################
    ############################################

    def __refresh(self, *args):
        self.width, self.height = map(int, self.getDim())
        ### traitement des axes
        s = self.itemconfigure("axes")
        options = {}
        for k, v in s.items():
            options[v[0]] = v[4]
        self.drawAxes(**options)
        ### traitement des ticks
        s = self.itemconfigure("ticks")
        options = {}
        for k, v in s.items():
            options[v[0]] = v[4]
        self.drawTicks(**options)
        ### traitement des tticks
        s = self.itemconfigure("tticks")
        options = {}
        for k, v in s.items():
            options[v[0]] = v[4]
        self.drawTTicks(**options)
        ### traitement de grid
        s = self.itemconfigure("grid")
        options = {}
        for k, v in s.items():
            options[v[0]] = v[4]
        self.drawGrid(**options)
        #
        self.drawZero()
        # on cherche TOUS le objets
        for objet in self.find_all():
            # tout ce qui dépend des axes fait l'objet
            # d'un traitement à part (déjà fait juste au-dessus !)
            # en effet, le repère va évoluer mais pas les autres objets
            # qu'il suffit de translater.
            if "axes" not in self.gettags(objet) \
               and "suivi" not in self.gettags(objet) \
               and "ticks" not in self.gettags(objet) \
               and "tticks" not in self.gettags(objet) \
               and "grid" not in self.gettags(objet):
                typeObjet = self.type(objet)
                if typeObjet == "oval":
                    x1, y1, x2, y2 = self.coordsInit[objet]
                    x1, y1 = self.__coordsCal2Can__(x1, y1)
                    x2, y2 = self.__coordsCal2Can__(x2, y2)
                    self.coords(objet, x1, y1, x2, y2)
                elif typeObjet == "line":
                    liste = []
                    it = iter(self.coordsInit[objet])
                    for x in it:
                        x, y = self.__coordsCal2Can__(x, next(it))
                        liste.append(x)
                        liste.append(y)
                    self.coords(objet, liste)
                else:
                    pass
        self.lower("axes")
        self.lower("ticks")
        self.lower("tticks")
        self.lower("grid")

    #############################################
    #############################################

    # https://stackoverflow.com/questions/8131942/how-to-pass-a-default-argument-value-of-an-instance-member-to-a-method
    
    def __coordsCan2Cal__(self, x, y,
                          xo=None, yo=None,
                          xu=None, yu=None):
        xo = xo if xo is not None else self.x_origin
        yo = yo if yo is not None else self.y_origin
        xu = xu if xu is not None else self.x_unit
        yu = yu if yu is not None else self.y_unit
        #        
        x = (x - xo) / xu
        y = (yo - y) / yu
        return [x, y]

    def __coordsCal2Can__(self, x, y,
                          xo=None, yo=None,
                          xu=None, yu=None):
        xo = xo if xo is not None else self.x_origin
        yo = yo if yo is not None else self.y_origin
        xu = xu if xu is not None else self.x_unit
        yu = yu if yu is not None else self.y_unit
        #        
        x = x * xu + xo
        y = - y * yu + yo
        return [x, y]

    #############################################
    #############################################

    def __followCursor(self, event):
        self.delete("suivi")
        if not self.follow: return
        x, y = event.x, event.y
        self.create_line(0, y, self.width, y, tags="suivi", dash=(2, 5))
        self.create_line(x, 0, x, self.height, tags="suivi", dash=(2,5))
        xc, yc = self.__coordsCan2Cal__(x, y)
        self.create_text(x, y, anchor='sw',
                         text="({:<0.2f};{:<0.2f})".format(xc, yc), tags="suivi")

    def __partir(self, event):
        self.delete("suivi")

    def __export(self, event):
        fh = tkinter.filedialog.asksaveasfile(defaultextension=".eps",
                                             filetypes=[("EPS file", "*.eps")],
                                             title="Choose postscript file name")
        if fh is not None:
            try:
                ps = self.postscript(file=fh.name, colormode='color')
            except:
                print("No save... a problem appeared while saving")
        # im = Image.open(io.BytesIO(ps.encode('utf-8')))
        # im.save('export.jpg')

    def __savePosition(self, event):
        # init va servir à savoir comment globalement
        # on a bougé une fois qu'on a relâché
        self.initx, self.inity = event.x, event.y
        # pos pour la __translation petit à petit
        self.posx, self.posy = event.x, event.y

    def __translation(self, event):
        x, y = event.x, event.y
        self.move('all', x - self.posx, y - self.posy)
        self.posx, self.posy = x, y

    def __landing(self, event):
        x, y = event.x, event.y
        xo, yo = self.getOrigin()
        self.setOrigin(xo + x - self.initx, yo + y - self.inity)
        self.__refresh()

    #############################################
    #############################################

    def export(self):
        color = self.cget("bg")
        dimX, dimY = map(int, self.getDim())
        offset = 1
        id = self.create_rectangle(-offset, -offset,
                                   dimX + offset, dimY + offset,
                                   fill = color)
        self.lower(id)
        #
        f = str(int(round(time.time(), 1) * 10))
        try:
            dir = "exportImages"
            if not os.path.exists(dir):
                os.makedirs(dir)
            self.postscript(file= dir+'/'+f+'.eps', colormode='color')
            self.delete(id)
            return f
        except:
            print("eps printing problem...\nhave you correct rights on the current directory?")
            return 0

    #############################################
    #############################################
    # AXES
    #############################################
    #############################################
    
    def __createAxes__(self):
        listeCoords = [0, self.y_origin, self.width, self.y_origin]
        id = self.create_line(*listeCoords,
                              tags="axes", arrow=tkinter.LAST,
                              width=2)
        ##
        listeCoords = [self.x_origin, self.height, self.x_origin, 0]
        id = self.create_line(*listeCoords,
                              tags="axes", arrow=tkinter.LAST,
                              width=2)

    def __refreshAxes__(self, **options):
        self.delete("axes")
        listeCoords = [0, self.y_origin, self.width, self.y_origin]
        id = self.create_line(*listeCoords, **options)
        self.addtag_withtag("axes", id)
        ##
        listeCoords = [self.x_origin, self.height, self.x_origin, 0]
        id = self.create_line(*listeCoords, **options)
        self.addtag_withtag("axes", id)
            
    def drawAxes(self, **options):
        #
        ### on dessine une première fois les axes avec des options par défaut
        ### en utilisant la fenêtre d'affichage -> on n'a pas besoin des coords
        ### calculs ! puisque la modification se fait ici et non dans refresh
        #
        if self.axes:
            if self.find_withtag("axes") == ():
                # CRÉATION AVEC LES OPTIONS PAR DÉFAUT
                self.__createAxes__()
            else:
                # MODIFICATION AVEC (possiblement) LES OPTIONS UTILISATEUR
                self.__refreshAxes__(**options)
        else:
            self.delete("axes")

    #############################################
    #############################################
    # ZERO
    #############################################
    #############################################

    def drawZero(self, **options):
        self.delete("zero")
        if self.zero:
                xo, yo = self.__coordsCal2Can__(0, 0)
                self.create_text(xo, yo, text="O",
                                 anchor="ne", tags="zero", **options)
    
    #############################################
    #############################################
    # TTICKS
    #############################################
    #############################################

    def drawTTicks(self, **options):
        self.delete("tticks")
        if self.tticks:
            #
            dx, dy = self.getTicks()
            #
            # pour gérer les arrondis (horribles) des tticks
            arrondiX, arrondiY = 1, 1
            xpV, ypV = str(dx).find("."), str(dy).find(".")
            if xpV != -1:
                    ldX = len(str(dx))
                    arrondiX = ldX - xpV - 1
            if ypV != -1:
                    ldY = len(str(dy))
                    arrondiY = ldY - ypV - 1
            #
            #
            Teloignement = 6
            #
            # absc. positives
            i = 1
            o1 = self.y_origin + Teloignement
            while self.x_unit * i * dx <= self.width - self.x_origin:
                a = self.x_origin + self.x_unit * i * dx
                self.create_text(a, o1,
                                 text="{:>2}".format(round(dx * i, arrondiX)),
                                 anchor="n",
                                 tags="tticks")
                i += 1

            # abs. negatives
            i = 1
            while self.x_unit * i * dx <= self.x_origin:
                a = self.x_origin - self.x_unit * i * dx
                self.create_text(a, o1,
                                 text="{:>2}".format(round(- dx * i, arrondiX)),
                                 anchor="n",
                                 tags="tticks")
                i += 1

            # ord. positives
            i = 1
            a1 = self.x_origin - Teloignement
            while self.y_unit * i * dy <= self.y_origin:
                o = self.y_origin - self.y_unit * i * dy
                self.create_text(a1, o,
                                 text="{:>2}".format(round(dy * i, arrondiY)),
                                 anchor="e",
                                 tags="tticks")
                i += 1

            # ord. negatives
            i = 1
            while self.y_unit * i * dy <= self.height - self.y_origin:
                o = self.y_origin + self.y_unit * i * dy
                self.create_text(a1, o,
                                 text="{:>2}".format(round(- dy * i, arrondiY)),
                                 anchor="e",
                                 tags="tticks")
                i += 1

    #############################################
    #############################################
    # TICKS
    #############################################
    #############################################

    def __createTicks__(self):
        dx, dy = self.getTicks()
        #
        eloignement  = 2
        #
        # absc. positives
        i = 1
        o1 = self.y_origin + eloignement
        o2 = self.y_origin - eloignement
        while self.x_unit * i * dx <= self.width - self.x_origin:
            a = self.x_origin + self.x_unit * i * dx
            self.create_line(a, o1, a, o2, tags="ticks", width=2)
            i += 1

        # abs. negatives
        i = 1
        while self.x_unit * i * dx <= self.x_origin:
            a = self.x_origin - self.x_unit * i * dx
            self.create_line(a, o1, a, o2, tags="ticks", width=2)
            i += 1

        # ord. positives
        i = 1
        a1 = self.x_origin + eloignement
        a2 = self.x_origin - eloignement
        while self.y_unit * i * dy <= self.y_origin:
            o = self.y_origin - self.y_unit * i * dy
            self.create_line(a1, o, a2, o, tags="ticks", width=2)
            i += 1

        # ord. negatives
        i = 1
        while self.y_unit * i * dy <= self.height - self.y_origin:
            o = self.y_origin + self.y_unit * i * dy
            self.create_line(a1, o, a2, o, tags="ticks", width=2)
            i += 1


    def __refreshTicks__(self, **options):
        #
        self.delete("ticks")
        #
        dx, dy = self.getTicks()
        #
        eloignement  = 2
        #
        # absc. positives
        i = 1
        o1 = self.y_origin + eloignement
        o2 = self.y_origin - eloignement
        while self.x_unit * i * dx <= self.width - self.x_origin:
            a = self.x_origin + self.x_unit * i * dx
            id = self.create_line(a, o1, a, o2, **options)
            self.addtag_withtag(id, "ticks")
            i += 1

        # abs. negatives
        i = 1
        while self.x_unit * i * dx <= self.x_origin:
            a = self.x_origin - self.x_unit * i * dx
            id = self.create_line(a, o1, a, o2, **options)
            self.addtag_withtag(id, "ticks")
            i += 1

        # ord. positives
        i = 1
        a1 = self.x_origin + eloignement
        a2 = self.x_origin - eloignement
        while self.y_unit * i * dy <= self.y_origin:
            o = self.y_origin - self.y_unit * i * dy
            id = self.create_line(a1, o, a2, o, **options)
            self.addtag_withtag(id, "ticks")
            i += 1

        # ord. negatives
        i = 1
        while self.y_unit * i * dy <= self.height - self.y_origin:
            o = self.y_origin + self.y_unit * i * dy
            id = self.create_line(a1, o, a2, o, **options)
            self.addtag_withtag(id, "ticks")
            i += 1

            
    def drawTicks(self, **options):

        if self.ticks:
            if self.find_withtag("ticks") == ():
                # CRÉATION AVEC LES OPTIONS PAR DÉFAUT
                self.__createTicks__()
            else:
                # MODIFICATION AVEC (possiblement) LES OPTIONS UTILISATEUR
                self.__refreshTicks__(**options)
        else:
            self.delete("ticks")

    #############################################
    #############################################
    # GRID
    #############################################
    #############################################

    def __createGrid__(self):
        dx, dy = self.getTicks()
        #
        # absc. positives
        i = 1
        while self.x_unit * i * dx <= self.width - self.x_origin:
            a = self.x_origin + self.x_unit * i * dx
            self.create_line(a, 0, a, self.height, tags="grid")
            i += 1

        # abs. negatives
        i = 1
        while self.x_unit * i * dx <= self.x_origin:
            a = self.x_origin - self.x_unit * i * dx
            self.create_line(a, 0, a, self.height, tags="grid")
            i += 1

        # ord. positives
        i = 1
        while self.y_unit * i * dy <= self.y_origin:
            o = self.y_origin - self.y_unit * i * dy
            self.create_line(0, o, self.width, o, tags="grid")
            i += 1

        # ord. negatives
        i = 1
        while self.y_unit * i * dy <= self.height - self.y_origin:
            o = self.y_origin + self.y_unit * i * dy
            self.create_line(0, o, self.width, o, tags="grid")
            i += 1


    def __refreshGrid__(self, **options):
        #
        self.delete("grid")
        #
        dx, dy = self.getTicks()
        #
        # absc. positives
        i = 1
        while self.x_unit * i * dx <= self.width - self.x_origin:
            a = self.x_origin + self.x_unit * i * dx
            id = self.create_line(a, 0, a, self.height, **options)
            self.addtag_withtag(id, "grid")
            i += 1

        # abs. negatives
        i = 1
        while self.x_unit * i * dx <= self.x_origin:
            a = self.x_origin - self.x_unit * i * dx
            id = self.create_line(a, 0, a, self.height, **options)
            self.addtag_withtag(id, "grid")
            i += 1

        # ord. positives
        i = 1
        while self.y_unit * i * dy <= self.y_origin:
            o = self.y_origin - self.y_unit * i * dy
            id = self.create_line(0, o, self.width, o, **options)
            self.addtag_withtag(id, "grid")
            i += 1

        # ord. negatives
        i = 1
        while self.y_unit * i * dy <= self.height - self.y_origin:
            o = self.y_origin + self.y_unit * i * dy
            id = self.create_line(0, o, self.width, o, **options)
            self.addtag_withtag(id, "grid")
            i += 1

    def drawGrid(self, **options):
        if self.grid:
            if self.find_withtag("grid") == ():
                # CRÉATION AVEC LES OPTIONS PAR DÉFAUT
                self.__createGrid__()
            else:
                # MODIFICATION AVEC (possiblement) LES OPTIONS UTILISATEUR
                self.__refreshGrid__(**options)
        else:
            self.delete("grid")

    #############################################
    #############################################
    # ITEMS CANVAS
    #############################################
    #############################################

    def drawPoint(self, x, y, **options):
        # pb avec oval : outline vs fill et le width !!
        # l'export eps fonctionne supermal si on gère l'épaisseur
        # via le width normal avec une taille de 1
        # du coup récup de l'option width utilisée comme
        # épaisseur.
        epaisseur = 1
        for k, v in options.items():
                if k == "width":
                     epaisseur = v
                     del(options["width"])
                     break
        xcan, ycan = self.__coordsCal2Can__(x, y)
        id = self.create_oval(xcan - epaisseur, ycan - epaisseur,
                         xcan + epaisseur, ycan + epaisseur,
                         tags="point", **options)
        x1cal, y1cal = self.__coordsCan2Cal__(xcan - epaisseur, ycan - epaisseur)
        x2cal, y2cal = self.__coordsCan2Cal__(xcan + epaisseur, ycan + epaisseur)       
        self.coordsInit[id] = [x1cal, y1cal, x2cal, y2cal]
        return id

    def drawLine(self, listeXY, **options):
        # si la liste est un composée de tuples,
        # on l'aplatit
        if type(listeXY[0])==tuple:
            l = []
            for x, y in listeXY:
                l.append(x)
                l.append(y)
            listeXY = l
        if len(listeXY) % 2 != 0:
            print("Please check coords list in drawLine method!")
        else:
            # liste est la liste finale à construire
            liste = []
            # il arrive qu'au départ d'une construction (pour une
            # animation par exemple), on appelle uniquement avec 1
            # point ce qui fait planter !
            # on duplique donc le 1er point
            if len(listeXY)==2:
                listeXY = listeXY*2
            # itérer deux valeurs sur une liste 
            # https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
            it = iter(listeXY)
            for x in it:
                x, y = self.__coordsCal2Can__(x, next(it)) 
                liste.append(x)
                liste.append(y)
            id = self.create_line(*liste,
                                  tags="line",
                                  **options)
            self.coordsInit[id] = listeXY
        return id

    def drawFunction(self, function, a, b, **options):
        listePoints = []
        x = a
        for i in range(round(1 + (b - a) / self.step)):
            listePoints += (x, function(x))
            x += self.step
        return self.drawLine(listePoints, **options)

    def drawParam(self, function, gunction, a, b, **options):
        listePoints = []
        x = a
        for i in range(round(1 + (b - a) / self.step)):
            listePoints += (function(x), gunction(x))
            x += self.step
        return self.drawLine(listePoints, **options)

    def drawSeq(self, function, a, n, **options):
        seq = [a]
        for i in range(n):
            a = function(a)
            seq += [a]
        #
        line = [(seq[0], 0)]
        for i in range(1, n+1):
            line += [(seq[i-1], seq[i])] + [(seq[i], seq[i])]
        #
        return self.drawLine(line, **options)
