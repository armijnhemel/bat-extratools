import sys, cPickle
from pychart import *
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

theme.scale_factor = 2
theme.reinitialize()

## example copied from PyChart HOWTO, adapted for our own use

can = canvas.init(options.outputfile)

ar = area.T(x_coord = category_coord.T(data, 0),
            x_grid_style=line_style.gray50_dash1,
            x_axis=axis.X(label="Versions", format="/a-90{}%s"),
            y_axis=axis.Y(label="Frequency"),
            bg_style = fill_style.gray90,
            border_line_style = line_style.default,
            size = (len(data)*10,300),
            legend = legend.T(loc=(-70,20)))

chart_object.set_defaults(bar_plot.T, direction="vertical", data=data)

ar.add_plot(bar_plot.T(label="Frequency"))
ar.draw(can)
