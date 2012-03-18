from pychart import *
import sys, cPickle
from optparse import OptionParser

'''
## Copyright 2012 Armijn Hemel for Tjaldur Software Governance Solutions
## Licensed under the GNU General Public License 2.0, see COPYING for details
'''

parser = OptionParser()
parser.add_option("-i", "--input", action="store", dest="inputfile", help="path to input pickle", metavar="FILE")
parser.add_option("-o", "--output", action="store", dest="outputfile", help="path to output file", metavar="FILE")
(options, args) = parser.parse_args()
if options.inputfile == None:
	parser.error("Path to input file needed")
if options.outputfile == None:
	parser.error("Path to output file needed")

picklefile = open(options.inputfile, 'rb')
data = cPickle.load(picklefile)
picklefile.close()

can = canvas.init(options.outputfile)

theme.use_color = 1
theme.reinitialize()

#data = [("foo", 10),("bar", 20), ("baz", 30), ("ao", 40), ("oe", 40), ('ah', 50), ('woohoo', 60), ('unf', 100), ('yo', 22), ('blaat', 1000), ('blebber', 1000)]

ar = area.T(size=(400,400), legend=legend.T(loc=(0,-20)),
            x_grid_style = None, y_grid_style = None)

## http://home.gna.org/pychart/doc/module-color.html
## but reordered
fill_styles =[ fill_style.red,
fill_style.blue,
fill_style.yellow,
fill_style.black,
fill_style.darkorchid,
fill_style.darkseagreen,
fill_style.aquamarine1,
fill_style.green,
fill_style.goldenrod,
fill_style.brown,
fill_style.white,
fill_style.gray70,
fill_style.diag,
fill_style.gray50,
fill_style.white,
fill_style.rdiag,
fill_style.vert,
fill_style.gray30,
fill_style.gray20,
fill_style.gray10,
fill_style.diag2,
fill_style.rdiag2,
fill_style.diag3,
fill_style.horiz,
fill_style.gray90,
fill_style.rdiag3,
fill_style.wave,
fill_style.vwave,
fill_style.stitch,
fill_style.lines,
fill_style.diag_fine,
fill_style.diag2_fine,
fill_style.diag3_fine,
fill_style.rdiag_fine,
fill_style.rdiag2_fine,
fill_style.rdiag3_fine,
fill_style.horiz_fine,
fill_style.vert_fine ]

plot = pie_plot.T(data=data, radius = 150, arc_offsets=[0,0,0,0], fill_styles = fill_styles)
ar.add_plot(plot)
ar.draw()
