import sys
from pychart import *
from optparse import OptionParser

'''
## Copyright 2012 Armijn Hemel for Tjaldur Software Governance Solutions
## Licensed under the GNU General Public License 2.0, see COPYING for details
'''

parser = OptionParser()
parser.add_option("-i", "--input", action="store", dest="inputfile", help="path to input file", metavar="FILE")
parser.add_option("-o", "--output", action="store", dest="outputfile", help="path to output file", metavar="FILE")
(options, args) = parser.parse_args()
if options.inputfile == None:
	parser.error("Path to input file needed")
if options.outputfile == None:
	parser.error("Path to output file needed")

#theme.get_options()

## example copied from PyChart HOWTO, adapted for our own use

data1 = {}
for i in range(0,256):
	data1[i] = 0
datafile = open('/usr/bin/vim')
offset = 0
datafile.seek(offset)
databuffer = datafile.read(100000)
while databuffer != '':
	for i in range(0,256):
		data1[i] = data1[i] + databuffer.count(chr(i))
	offset = offset + 100000
	datafile.seek(offset)
	databuffer = datafile.read(100000)

data = []
for i in range(0, 256):
	data.append((i,data1[i]))

can = canvas.init(options.outputfile)

ar = area.T(x_coord = category_coord.T(data, 0),
            x_grid_style=line_style.gray50_dash1,
            x_axis=axis.X(label="Byte values", format="/a-90{}%d"),
            y_axis=axis.Y(label="Frequency"),
            bg_style = fill_style.gray90,
            border_line_style = line_style.default,
            size = (2560,200),
            legend = legend.T(loc=(40,-30)))

chart_object.set_defaults(bar_plot.T, direction="vertical", data=data)

ar.add_plot(bar_plot.T(label="Amount of bytes"))
ar.draw(can)
