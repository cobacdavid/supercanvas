This package provides a `supercanvas` widget based on the original
`tkinter` canvas.  It provides a quickly useable canvas with a
usual cartesian coordinate system.

As it remains a canvas, I've tried to keep canvas's items
behaviour. So options of items created are usual options and items
created return id (as a number) of the object so that you can
`itemconfigure` it.

Note: `tticks` tag is no more used, replaced by `xlabel` and
`ylabel` tags.


# Full commands list

``` python3
from supercanvas import *

```


``` python3

supercanvas(rootname, **options)

```

`options` could be ususal `tkinter` options and boolean variables:
`axes`, `ticks`, `xlabel`, `ylabel` `grid`, `zero` and `follow`.

These variables dis/enable features of `supercanvas`.


`supercanvas` setup methods:

``` python3

.setOrigin(x, y)
.getOrigin()

.setViewX(x1, x2)
.setViewY(y1, y2)
.getView()

.setUnit(x, y)
.getUnit()

.setTicks(dx, dy)
.getTicks()

.setDim(scanvas_width, scanvas_height)
.getDim()

```

`supercanvas` setup variables:

``` python3

.axes   # boolean
.ticks  # boolean
.xlabel # boolean
.ylabel # boolean
.grid   # boolean
.zero   # boolean

.step   # float or int: distance between successive argument values in drawFunction/Param

```


`supercanvas` drawing methods:


``` python3

.export()       # save supercanvas in an eps file whose name is timestamped

.drawPoint(x, y, **options)
.drawLine(list, **options)        # flat-list or list of tuples
.drawFunction(function, a, b, **options)
.drawParam(x-function, y_function, a, b, **options)
.drawSeq(function, 1st_term, final_rank, **options)

```

`supercanvas` tags to identify objects: `axes`, `ticks`, `xlabel`,
`ylabel` `grid` and `zero`.

These tags enable you to configure objects tagged with the usual way:

For example:

``` python3

.itemconfigure("axes", fill="red", dashed=(5, 2))


```



`hsv_to_rgb(h, s, v)` is based on [this SO code](https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion)


``` python3

beginmagicTk() # output to store
endMagicTk(name_of_previous_output)

```



### Real documentation begins at this point

If you just want to have this `supercanvas` alone with no other
widget, see `magicTk` section at the end.

### class object

``` python3

>>> from supercanvas import *

```

Once package importation completed, you have to create a
supercanvas the usual way.

``` python3

r = tkinter.Tk()
c = supercanvas(r, bg="white", width=800, height=600)

```


### origin and units

By default, origin is located at `supercanvas`'s center and units
are both 1 pixel (and axes are drawn in french style with
arrows). You can change this with `setOrigin` and `setUnit`
methods:

 
``` python3

c.setUnit(80, 100)
c.setOrigin(50, 200)

```

One new feature of 0.4 version is to introduce `setViewX` and
`setViewY` which allows you to forget about `setUnit` and
`setOrigin`. You use these two methods to indicate limits of your
drawing frame, that's so simple!

``` python3

c.setViewX(-5, 5)
c.setViewY(-1.05, 3.1)

```


### axes and ticks

By default, axes, ticks, tticks, grid ans zero are shown/drawn. If
you want them not to appear, you pass options `axes`, `ticks`,
`xlabel`, `ylabel`, `grid` and `zero` to `False` in the
`supercanvas` command.

Or you can these variables to `False` into your script. 


`setTicks` method allow you to set distance between ticks.


``` python3

c.axes = False
c.setTicks(1, .5)

```


### supercanvas items

`supercanvas` provides four drawing methods `drawPoint`, `drawLine`, `drawFunction`, `drawParam` and `drawSeq`.


* `drawPoint` method creates a point at the desired coords.

``` python3

f = lambda x:x**2
x = 3
c.drawPoint(x, f(x), fill="red", outline="red")

```

It's based on `create_oval` so you can pass each option related to
`Oval` object.

* `drawLine` method creates a line with a list of coords.

``` python3

c.drawLine([(-2, 2), (-1, 0), (0, 3)], fill="blue", width=3)

```

`drawLine` also supports a flat list of coords:

``` python3

c.drawLine([-2, 2, -1, 0, 0, 3], fill="blue", width=3)

```

gives the same line.


* `drawFunction` method creates a line representing a function passed.


``` python3

f = lambda x: 3 * x ** 2 + 2 
c.drawLine(f, -2, 7, fill="green")

```

-2 and 7 are the lower and upper values of argumentt's function.

You can use `step` method to specify difference between two
consecutive argguments, default is 1.


``` python3

f = lambda x: 3 * x ** 1.2 + 2
c.step = .1
c.drawLine(f, -2, 7, fill="green")

```


*  `drawParam` method creates a line representing a parametric curve.


this code creates a unit circle:


``` python3

f = lambda x: math.cos(x)
g = lambda x: math.sin(x)
c.step = .01
c.drawParam(f, g, 0, 2 * math.pi)

```

* `drawSeq` method creates a broken line representing visual serach
  of a recursive sequence based on a function i.e. \$ u_{n+1} =
  f(u_n)\$.


Function and identity function do not need to be drawn but it
visually helps to understand line construction.


``` python3

f = lambda x: 1/(1+x)
c.step = .01
c.drawFunction(f, 0, 2)
c.drawSeq(f, 1, 5)

```

In the previsous example, \$u_1=f(u_0)\$ until we reach
\$u_5\$. Construction stops when we just have to read \$u_5\$ on
x-axis.


### grab/release background

You can move the whole `supercanvas` content in grabing /
releasing the background. It will refresh coords.

### zooming

You can zoom the whole `supercanvas` content with mousewheel.

### `supercanvas` options

* `axes`

passing `axes=False` to `supercanvas` options disable axes, default
is `True`. For the moment, you cannot change axes style...

* `ticks`

passing `ticks=False` to `supercanvas` options disable ticks, default is `True`.

* `xlabel` and `ylabel`

passing `xlabel=False` to `supercanvas` options disable text labels
on x-axis, default is `True`. Same thing for `ylabel`

* `grid`

passing `grid=False` to `supercanvas` options disable the grid, default is `True`.

* `zero`

passing `zero=False` to `supercanvas` options disable zero apparition, default is `True`.

* `follow`

passing `follow=False` to `supercanvas` options disable cursor follow with coords, default is `True`.

### exporting

`supercanvas` provides an `export` method. At each call, this
creates an `eps` (encapsulated postscript, so a vector graphics)
file which name is a timestamp, so successive exports are sorted.

Export images are in a `exportImages` directory created on the
current directory if it doesn't exist.


### create an animation for linux users

You can find an [eps2png perl script](https://metacpan.org/source/JV/eps2png-2.7/src/eps2png.pl) by Johan Vromans.

It's a quite fast script. Once in the `exportImages` directory, you
run it:

``` bash

$ eps2png *.eps

```

It creates you png files with the same names. Then with [convert command of ImageMagick](https://imagemagick.org/script/convert.php), you run:


Note: It's better to pass `-width` and `-height` options to this
conversion command to respect initial size. Sometimes you will need also
to adapt antialiasing with `-antialias` option (1, 2, 4 or 8).


``` bash

$ convert -delay 10 *.png animation.gif

```

to output a gif with the delay specified between images.

See example 4 below for a full complete example.


### full examples

* example 1

Points and functions using `drawPoint` and `drawLine`.


``` python3

from supercanvas import *
import math
r = tkinter.Tk()

c = supercanvas(r, bg="white", width=800, height=600, ticks=False)
c.setUnit(100, 100)

f=lambda x:math.cos(x)
g=lambda x:math.sin(x)

p = .1
a, b = -3, 3
x = a
listePointsF = []
listePointsG = []
for i in range(int(1 + (b - a) / p)):
    # creating points 
    c.drawPoint(x, f(x), fill="red", outline="red")
    # two lists
    # function f with tuples
    listePointsF += (x, f(x))
    # function g with flat list
    listePointsG += [x]+[g(x)]
    x += p

# drawings of the two curves
c.drawLine(listePointsF, fill="green")
c.drawLine(listePointsG, fill="blue", width=3)

# balancing canvas on the root
c.pack(expand=True)

# q to quit
r.bind("<q>", quit)
tkinter.mainloop()

```


* example 2

Function using `drawFunction`.

``` python3

from supercanvas import *
import math
r = tkinter.Tk()

c = supercanvas(r, bg="#00964a")
c.setOrigin(30, 150)
c.setUnit(10, 80)

f = lambda x: math.sin(x) / x
c.step=.1
c.drawFunction(f, c.step, 10*math.pi, width=3, fill="white")

c.pack()
r.bind("<q>", quit)
tkinter.mainloop()

```

* example 3

Cardioid curve using `drawParam`

``` python3

from supercanvas import *
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


```


* example 4

Lissajous animated curve with possibility to export.


``` python3

from supercanvas import *

import math
w = beginMagicTk()
# canvas dimension
dim = 600
# offset: mid-with of the linewidth
offset = 25
#
c = supercanvas(w, bg="white", width=dim, height=dim,
                axes=False, ticks=False)
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


```

* example 5

Customizing axes and drawn elements 


``` python3

w = beginMagicTk()
dim = 600
c = supercanvas(w, bg="white", width=dim, height=dim,
                axes=True,
                ticks=True,
                xlabel=False,
                ylabel=False,
                grid=True)
c.setUnit(100, 100)
c.itemconfigure("axes", fill="red", width=1)
c.itemconfigure("grid", fill="darkblue", dash=(5, 2, 1, 2))
c.itemconfigure("ticks", fill="blue", width=5)
c.step=.1
c.drawFunction(lambda x:.5 * x**2, -5, 5,
               fill="darkgreen", dash=(5, 2), width=4)

endMagicTk(w)

```

### magicTk

Because remembering `tkinter` commands for just one widget is
awful, `supercanvas` provides two commands `beginMagicTk` and
`endMagicTk`.

Key `q` is bind to close/exit event.

Here's how to use them in a standalone example file:

``` python3

from supercanvas import *
w = beginMagicTk()

c = supercanvas(w, bg="white")
c.setUnit(100, 20)
c.setTicks(.5, 2)

f = lambda x: x ** 3
c.step=.1
c.drawFunction(f, -3, 3)

endMagicTk(w)

```

Assign first command output, use it in `supercanvas` and
`endMagicTk` commands.

If you want to `update` supercanvas content for animation for
example, you shouldn't use this since `endMagicTk` contains the
command to show the canvas, so maybe too late for you.


### further

Much much more!


### about

supercanvas is rather an attempt to publish on the `PyPi` packages
index than a fully completed python project, I do not recommend
supercanvas usage for professionnal use. You have to consider this
package as an experiment.
