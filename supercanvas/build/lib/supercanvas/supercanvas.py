# auteur : david cobac
# Début 27/12/2018

import tkinter
import math # drawBoxPlot : ceil
from tkinter import filedialog

import time
import os

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

    #### zone de réflexion sur le futur repère
    
    gridDefault = {'activedash': '', 'activefill': '', 'activestipple': '', 'activewidth': '0.0', 'arrow': 'none', 'arrowshape': '8 10 3', 'capstyle': 'butt', 'fill': 'black', 'dash': (5,2), 'dashoffset': '0', 'disableddash': '', 'disabledfill': '', 'disabledstipple': '', 'disabledwidth': '0.0', 'joinstyle': 'round', 'offset': '0,0', 'smooth': '0', 'splinesteps': '12', 'state': '', 'stipple': '', 'tags': 'grid repere', 'width': '1.0'}

    gridUser = gridDefault
    
    ticksDefault = {'activedash': '', 'activefill': '', 'activestipple': '', 'activewidth': '0.0', 'arrow': 'none', 'arrowshape': '8 10 3', 'capstyle': 'butt', 'fill': 'black', 'dash': '', 'dashoffset': '0', 'disableddash': '', 'disabledfill': '', 'disabledstipple': '', 'disabledwidth': '0.0', 'joinstyle': 'round', 'offset': '0,0', 'smooth': '0', 'splinesteps': '12', 'state': '', 'stipple': '', 'tags': 'ticks repere', 'width': '2.0'}

    ticksUser = ticksDefault
    
    xlabelDefault = {'activefill': '', 'activestipple': '', 'anchor': 'ne', 'angle': '0.0', 'disabledfill': '', 'disabledstipple': '', 'fill': 'black', 'font': 'TkDefaultFont', 'justify': 'left', 'offset': '0,0', 'state': '', 'stipple': '', 'tags': 'xlabel repere', 'text': '', 'underline': '-1', 'width': '0'}

    xlabelUser = xlabelDefault
    
    ylabelDefault = {'activefill': '', 'activestipple': '', 'anchor': 'ne', 'angle': '0.0', 'disabledfill': '', 'disabledstipple': '', 'fill': 'black', 'font': 'TkDefaultFont', 'justify': 'left', 'offset': '0,0', 'state': '', 'stipple': '', 'tags': 'ylabel repere', 'text': '', 'underline': '-1', 'width': '0'}
    
    ylabelUser = ylabelDefault
    
    def __init__(self, master, **options):
        #########################
        # traitement des options
        # valeurs par défaut
        self.axes   = True
        self.ticks  = True
        self.xlabel = True
        self.ylabel = True
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
            elif k=="xlabel":
                self.xlabel = v
                aSupprimer.append("xlabel")
            elif k=="ylabel":
                self.ylabel = v
                aSupprimer.append("ylabel")
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
        # ce qui suit est dispensable
        self.drawAxes()
        # self.drawTicks()
        # self.drawTTicks()
        # self.drawGrid()
        self.drawRepere(self.ticksDefault, self.gridDefault,
                        self.xlabelDefault, self.ylabelDefault)
        self.drawZero()
        ########################
        self.__calculZoom = False
        ########################
        self.event_add("<<Suivi>>", "<Motion>")
        self.event_add("<<Partir>>", "<Leave>")
        #
        self.bind('<Configure>', self.__refresh)
        self.bind('<<Suivi>>', self.__followCursor)
        self.bind('<<Partir>>', self.__partir)
        self.bind('<Button-4>', self.__zoom)
        self.bind('<Button-5>', self.__zoom)
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

    def setView(self, x1, x2, y1, y2):
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        self.x_unit = self.width / (x2 - x1)
        self.x_origin = - self.x_unit * x1
        self.y_unit = self.height / (y2 - y1)
        self.y_origin = self.y_unit * y2
        self.__refresh()
        
    def getView(self):
        x1, y2 = self.__coordsCan2Cal__(0, 0)
        x2, y1 = self.__coordsCan2Cal__(self.width, self.height)
        return [x1, x2, y1, y2]

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
        ### AXES
        s = self.itemconfigure("axes")
        optionsAxes = {}
        for k, v in s.items():
            optionsAxes[v[0]] = v[4]
        self.drawAxes(**optionsAxes)
        self.drawZero()
        self.drawRepere(self.ticksUser, self.gridUser,
                        self.xlabelUser, self.ylabelUser)
        # print(optionsTicks, optionsGrid,
        #                optionsXlabel, optionsYlabel)
        #
        for objet in self.find_withtag("supercanvas"):
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
        self.lower("xlabel")
        self.lower("ylabel")
        self.lower("zero")
        self.lower("grid")
        #
        self.update()

    #############################################
    #############################################

    def __coordsCan2Cal__(self, x, y):
        x = (x - self.x_origin) / self.x_unit
        y = (self.y_origin - y) / self.y_unit
        return [x, y]

    def __coordsCal2Can__(self, x, y):
        x = x * self.x_unit + self.x_origin
        y = - y * self.y_unit + self.y_origin
        return [x, y]

    #############################################
    #############################################

    def __followCursor(self, event):
        self.delete("follow")
        if not self.follow: return
        x, y = event.x, event.y
        self.create_line(0, y, self.width, y, tags="follow", dash=(2, 5))
        self.create_line(x, 0, x, self.height, tags="follow", dash=(2,5))
        xc, yc = self.__coordsCan2Cal__(x, y)
        self.create_text(x, y, anchor='sw',
                         text="({:<0.2f};{:<0.2f})".format(xc, yc), tags="follow")

    def __partir(self, event):
        self.delete("follow")

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

    def __zoomIn(self):
        self.__calculZoom = True
        coef = 1.05
        x1, x2, y1, y2 = [coef * c for c in self.getView()]
        self.setViewX(x1, x2)
        self.setViewY(y1, y2)
        self.__calculZoom = False

    def __zoomOut(self):
        self.__calculZoom = True
        coef = 1.05
        x1, x2, y1, y2 = [1 / coef * c for c in self.getView()]
        self.setViewX(x1, x2)
        self.setViewY(y1, y2)
        self.__calculZoom = False

    def __zoom(self, event):
        if event.num == 4 and not self.__calculZoom:
            self.__zoomIn()
        elif event.num == 5 and not self.__calculZoom:
            self.__zoomOut()
        else:
            pass

    #############################################
    #############################################

    def export(self, event=None):
        color = self.cget("bg")
        dimX, dimY = map(int, self.getDim())
        offset = 10
        __lefond = self.create_rectangle(-offset, -offset,
                                   dimX + offset, dimY + offset,
                                   fill = color)
        self.tag_lower(__lefond)
        #
        f = str(int(round(time.time(), 1) * 10))
        try:
            dir = "exportImages"
            if not os.path.exists(dir):
                os.makedirs(dir)
            self.postscript(file= dir+'/'+f+'.eps',
                            colormode='color',
                            width=self.width,
                            height=self.height)
            self.delete(__lefond)
            return f
        except:
            print("eps printing problem...\nhave you correct rights on the current directory?")
            return 0
    
    #############################################
    #############################################
    # REPÈRE : réunion de l'ensemble des éléments
    #          après les avoir séparés...
    #############################################
    #############################################


    # que les éléments liés au repérage numérique
    def drawRepere(self, optionsTicks, optionsGrid,
                          optionsXlabel, optionsYlabel):

        # ### TICKS
        s = self.itemconfigure("ticks")
        if s != "":
            for k, v in s.items():
                optionsTicks[str(v[0])] = v[4]
                self.ticksUser[v[0]] = v[4]
        ### GRID
        s = self.itemconfigure("grid")
        if s != "":
            for k, v in s.items():
                optionsGrid[str(v[0])] = v[4]
                self.gridUser[v[0]] = v[4]
        # ### XLABEL
        s = self.itemconfigure("xlabel")
        if s != "":
            for k, v in s.items():
                optionsXlabel[str(v[0])] = v[4]
                self.xlabelUser[v[0]] = v[4]
         # ### YLABEL
        s = self.itemconfigure("ylabel")
        if s != "":
            for k, v in s.items():
                optionsYlabel[str(v[0])] = v[4]
                self.ylabelUser[v[0]] = v[4]
        ##
        #for tag in ["ticks", "grid", "xlabel", "ylabel"]:
        #    self.delete(tag)
        self.delete("repere")
        #
        dx, dy = self.getTicks()
        #
        # Pour les TTICKS
        #
        arrondiX, arrondiY = 1, 1
        xpV, ypV = str(dx).find("."), str(dy).find(".")
        if xpV != -1:
            ldX = len(str(dx))
            arrondiX = ldX - xpV - 1
        if ypV != -1:
            ldY = len(str(dy))
            arrondiY = ldY - ypV - 1
        #
        Teloignement = 1
        #
        #
        eloignement = 2
        #
        #
        # absc. positives
        o1 = self.y_origin + eloignement
        o2 = self.y_origin - eloignement
        o3 = self.y_origin + Teloignement
        i = 0
        a = self.x_origin
        # gestion de la partie qui ne doit pas s'afficher (entre 0 et le minimum)
        # on rend donc a > 0
        while a <= 0:
            a += self.x_unit * dx
            i += 1
        # on peut commancer à afficher avec la bonne valeur de a
        # du coup recalcul de a à la fin, du coup limite + 1
        while a < self.width:
            if self.ticks and 0 < self.y_origin < self.height:
                ide = self.create_line(a, o1, a, o2, **optionsTicks)
                # self.addtag_withtag(ide, "ticks")
                 #self.addtag_withtag(ide, "repere")
            if self.grid:
                ide = self.create_line(a, 0, a, self.height, **optionsGrid)
                # self.addtag_withtag(ide, "grid")
                # self.addtag_withtag(ide, "repere")
            # on n'affiche pas à l'origine -> i!=0
            # on n'affiche pas si on ne voit pas
            # l'axe des abscisses -> 0 < y_origin < height
            if self.xlabel and i != 0 and 0 < self.y_origin < self.height:
                ide = self.create_text(a, o3, **optionsXlabel)
                self.itemconfigure(ide, text="{:>2}".format(round(dx * i, arrondiX)))
                # self.addtag_withtag(ide, "xlabel")
                # self.addtag_withtag(ide, "repere")
            a += self.x_unit * dx
            i += 1

        # abs. negatives
        i = 0
        a = self.x_origin
        while a >= self.width:
            a -= self.x_unit * dx
            i += 1
        while a > 0:
            if self.ticks and 0 < self.y_origin < self.height:
                ide = self.create_line(a, o1, a, o2, **optionsTicks)
                # self.addtag_withtag(ide, "ticks")
                # self.addtag_withtag(ide, "repere")
            if self.grid:
                ide = self.create_line(a, 0, a, self.height, **optionsGrid)
                # self.addtag_withtag(ide, "grid")
                # self.addtag_withtag(ide, "repere")
            if self.xlabel and i != 0 and  0 < self.y_origin < self.height:
                ide = self.create_text(a, o3, **optionsXlabel)
                self.itemconfigure(ide, text="{:>2}".format(round(- dx * i, arrondiX)))
                # self.addtag_withtag(ide, "xlabel")
                # self.addtag_withtag(ide, "repere")
            a -= self.x_unit * dx
            i += 1

        # ord. positives
        a1 = self.x_origin + eloignement
        a2 = self.x_origin - eloignement
        a3 = self.x_origin - Teloignement
        i = 0
        o = self.y_origin
        while o >= self.height:
            i += 1
            o -= self.y_unit * dy
        while o > 0:
            if self.ticks and 0 < self.x_origin < self.width:
                ide = self.create_line(a1, o, a2, o, **optionsTicks)
                self.addtag_withtag(ide, "ticks")
                self.addtag_withtag(ide, "repere")
            if self.grid:
                ide = self.create_line(0, o, self.width, o, **optionsGrid)
                self.addtag_withtag(ide, "grid")
                self.addtag_withtag(ide, "repere")
            if self.ylabel and i != 0 and 0 < self.x_origin < self.width:
                ide = self.create_text(a3, o, **optionsYlabel)
                self.itemconfigure(ide, text="{:>2}".format(round(dy * i, arrondiY)))
                self.addtag_withtag(ide, "ylabel")
                self.addtag_withtag(ide, "repere")
            o -= self.y_unit * dy
            i += 1

        # ord. negatives
        i = 0
        o = self.y_origin
        while o <= 0:
            o += self.y_unit * dy
            i += 1
        while o < self.height:
            if self.ticks and 0 < self.x_origin < self.width:
                ide = self.create_line(a1, o, a2, o, **optionsTicks)
                self.addtag_withtag(ide, "ticks")
                self.addtag_withtag(ide, "repere")
            if self.grid:
                ide = self.create_line(0, o, self.width, o, **optionsGrid)
                self.addtag_withtag(ide, "grid")
                self.addtag_withtag(ide, "repere")
            if self.ylabel and i != 0 and 0 < self.x_origin < self.width:
                ide = self.create_text(a3, o, **optionsYlabel)
                self.itemconfigure(ide, text="{:>2}".format(round(- dy * i, arrondiY)))
                self.addtag_withtag(ide, "ylabel")
                self.addtag_withtag(ide, "repere")
            o += self.y_unit * dy
            i += 1


    #############################################
    #############################################
    # AXES
    #############################################
    #############################################
    
    def __createAxes__(self):
        listeCoords = [0, self.y_origin, self.width, self.y_origin]
        ide = self.create_line(*listeCoords,
                              tags="axes", arrow=tkinter.LAST,
                              width=2)
        ##
        listeCoords = [self.x_origin, self.height, self.x_origin, 0]
        ide = self.create_line(*listeCoords,
                              tags="axes", arrow=tkinter.LAST,
                              width=2)

    def __refreshAxes__(self, **options):
        self.delete("axes")
        listeCoords = [0, self.y_origin, self.width, self.y_origin]
        ide = self.create_line(*listeCoords, **options)
        self.addtag_withtag("axes", ide)
        ##
        listeCoords = [self.x_origin, self.height, self.x_origin, 0]
        ide = self.create_line(*listeCoords, **options)
        self.addtag_withtag("axes", ide)
            
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
        a_enlever = []
        for k, v in options.items():
            if k == "width":
                epaisseur = v
                a_enlever.append(k)
            elif k == "style":
                style = v
                a_enlever.append(k)
        for k in a_enlever:
            del(options[k])
        xcan, ycan = self.__coordsCal2Can__(x, y)
        if 'style' in vars():
            if style == "oval":
                ide = self.create_oval(xcan - epaisseur, ycan - epaisseur,
                         xcan + epaisseur, ycan + epaisseur,
                         tags="supercanvas", **options)
            elif style == "rectangle":
                ide = self.create_rectangle(xcan - epaisseur, ycan - epaisseur,
                         xcan + epaisseur, ycan + epaisseur,
                         tags="supercanvas", **options)
        else:
            ide = self.create_oval(xcan - epaisseur, ycan - epaisseur,
                         xcan + epaisseur, ycan + epaisseur,
                         tags="supercanvas", **options)
        x1cal, y1cal = self.__coordsCan2Cal__(xcan - epaisseur, ycan - epaisseur)
        x2cal, y2cal = self.__coordsCan2Cal__(xcan + epaisseur, ycan + epaisseur)
        self.coordsInit[ide] = [x1cal, y1cal, x2cal, y2cal]
        return ide

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
            ide = self.create_line(*liste,
                                  tags="supercanvas",
                                  **options)
            self.coordsInit[ide] = listeXY
        return ide

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
        return self.drawLine(line, **options)

    def drawBoxPlot(self, liste, **options):
        liste.sort()
        lon = len(liste)
        mini = min(liste)
        maxi = max(liste)
        mediane = (liste[lon // 2] + liste[-(lon // 2) - 1]) / 2
        moyenne = sum(liste) / lon
        q1 = liste[math.ceil(lon / 4)]
        q3 = liste[math.ceil(3 * lon / 4)]
        # print(mini, q1, mediane, q3, maxi)
        #
        hauteur = 0
        epaisseur = 1
        #
        aSupprimer = []
        for k, v in options.items():
            if k == "hauteur":
                hauteur = v
                aSupprimer.append("hauteur")
            if k == "epaisseur":
                epaisseur = v
                aSupprimer.append("epaisseur")
        for opt in aSupprimer:
            del options[opt]

        miH = (2 * hauteur + epaisseur) / 2
        self.drawLine([(mini, hauteur),
                       (mini, hauteur + epaisseur)], **options)
        self.drawLine([(mini, miH), (q1, miH)], **options)
        self.drawLine([(q1, hauteur),
                       (q1, hauteur + epaisseur)], **options)
        self.drawLine([(q1, hauteur), (q3, hauteur)], **options)
        self.drawLine([(q1, hauteur + epaisseur),
                       (q3, hauteur + epaisseur)], **options)
        self.drawLine([(mediane, hauteur),
                       (mediane, hauteur + epaisseur)], **options)
        self.drawLine([(q3, hauteur),
                       (q3, hauteur + epaisseur)], **options)
        self.drawLine([(q3, miH), (maxi, miH)], **options)
        self.drawLine([(maxi, hauteur),
                       (maxi, hauteur + epaisseur)], **options)
