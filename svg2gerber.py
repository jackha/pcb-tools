""" Experimental svg to gerber converter. 

Cause no such thing exists apparently.  
"""

import gerber
from gerber.rs274x import GerberFile
from gerber.primitives import Line  # we're going to make lines!
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier
from xml.dom import minidom

# read svg. not so difficult, right?
from svg.path import parse_path
# my_path = parse_path('M 100 100 L 300 100')

svg_filename = 'test/oshw-logo.svg'
doc = minidom.parse(svg_filename)  # parseString also exists
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()
# all paths, leaf elements have properties start and end (complex numbers).
parsed_paths = [parse_path(p) for p in path_strings]

# write as gerber. not so difficult, right?
statements = []
settings = dict(
	notation='',
	units='mm',
	zero_suppression=False,
	zeros=False,
	format='',
	angle_units='radian')
primitives = []  # [Line((0,0), (10,10)),]
filename = 'output.GML'

# fill primitives
for p in parsed_paths:
	for pp in p:
		new_line = Line(
			(pp.start.real, pp.start.imag), (pp.end.real, pp.end.imag))
		primitives.append(new_line)

test_gerber = gerber.read('test/test.GML')  # cannibalize test file :-)
import pdb; pdb.set_trace()
# apparently, the result is the same as test.GML (primitives are not used...)
g = GerberFile(
	test_gerber.statements, 
	test_gerber.settings, 
	primitives)

#import pdb; pdb.set_trace()
g.write('joee.GML')

#import pdb; pdb.set_trace()