lineDefaultOptions = {'activedash': ('activedash', '', '', '', ''), 'activefill': ('activefill', '', '', '', ''), 'activestipple': ('activestipple', '', '', '', ''), 'activewidth': ('activewidth', '', '', '0.0', '0.0'), 'arrow': ('arrow', '', '', 'none', 'none'), 'arrowshape': ('arrowshape', '', '', '8 10 3', '8 10 3'), 'capstyle': ('capstyle', '', '', 'butt', 'butt'), 'fill': ('fill', '', '', 'black', 'black'), 'dash': ('dash', '', '', '', ''), 'dashoffset': ('dashoffset', '', '', '0', '0'), 'disableddash': ('disableddash', '', '', '', ''), 'disabledfill': ('disabledfill', '', '', '', ''), 'disabledstipple': ('disabledstipple', '', '', '', ''), 'disabledwidth': ('disabledwidth', '', '', '0.0', '0.0'), 'joinstyle': ('joinstyle', '', '', 'round', 'round'), 'offset': ('offset', '', '', '0,0', '0,0'), 'smooth': ('smooth', '', '', '0', '0'), 'splinesteps': ('splinesteps', '', '', '12', '12'), 'state': ('state', '', '', '', ''), 'stipple': ('stipple', '', '', '', ''), 'tags': ('tags', '', '', '', ''), 'width': ('width', '', '', '1.0', '1.0')}

textDefaultOptions = {'activefill': ('activefill', '', '', '', ''), 'activestipple': ('activestipple', '', '', '', ''), 'anchor': ('anchor', '', '', 'center', 'center'), 'angle': ('angle', '', '', '0.0', '0.0'), 'disabledfill': ('disabledfill', '', '', '', ''), 'disabledstipple': ('disabledstipple', '', '', '', ''), 'fill': ('fill', '', '', 'black', 'black'), 'font': ('font', '', '', 'TkDefaultFont', 'TkDefaultFont'), 'justify': ('justify', '', '', 'left', 'left'), 'offset': ('offset', '', '', '0,0', '0,0'), 'state': ('state', '', '', '', ''), 'stipple': ('stipple', '', '', '', ''), 'tags': ('tags', '', '', '', ''), 'text': ('text', '', '', '', ''), 'underline': ('underline', '', '', '-1', '-1'), 'width': ('width', '', '', '0', '0')}

options = {}
for k, v in lineDefaultOptions.items():
    options[v[0]] = v[4]
print(options)


options = {}
for k, v in textDefaultOptions.items():
    options[v[0]] = v[4]
print(options)

