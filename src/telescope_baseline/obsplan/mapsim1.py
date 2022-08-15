#!/usr/bin/env python3
"""Make mapping svg file.

usage:
  map1.py [-h|--help] -m efl_per_cellsize -o out.svg

options:
  --help                show this help message and exit
  -m efl_per_cellsize   parameter efl_per_cellsize (efl / Cell scale)
  -o out.svg            output file
"""
import numpy as np
import math
import svgwrite
from docopt import docopt


class Mapsim1:
    def __init__(self, efl_per_cellsize:int = 6320, outfile:str = 'map.svg'):
        self.efl_per_cellsize = efl_per_cellsize
        self.outfile = outfile

        # Drawing parameters
        self.mm = 3.543307
        self.deg = 14 * self.mm  # 1 deg = 40mm
        self.paper_width = 297 * self.mm
        self.paper_hight = 210 * self.mm
        self.xcenter = self.paper_width / 2
        self.ycenter = self.paper_hight / 2

        # Model parameters
        self.cells_per_pix = 13
        self.pixel_size = 10
        self.efl = self.efl_per_cellsize * self.pixel_size / self.cells_per_pix
        self.pfov = 10e-3 / self.efl * 180 / math.pi
        self.num_pixels = 1952
        self.chip_spacing_a = 22.4 / self.efl * 180 / math.pi
        self.chip_spacing_b = 22.4 / self.efl * 180 / math.pi

        self.text = 'EFL={:.3f}'.format(self.efl)

        # Field parameters
        self.widex = 2
        self.widey = 2
        self.gc = 0.7
        self.gdw = 1.5
        self.gdh = 0.3

    def degxys(self, x, y):
        return (x * self.deg * self.mm, y * self.deg * self.mm)

    def degxy(self, x, y):
        return ((x * self.deg * self.mm + self.xcenter, y * self.deg * self.mm + self.ycenter))

    # Add a field
    def addfield(self, center_x, center_y, position_angle, dwg, id):
        field = dwg.add(dwg.g(id='field{}'.format(id)))
        for i in range(4):
            x = np.empty(4)
            y = np.empty(4)
            if i == 0 or i == 1:
                x[0] = -self.chip_spacing_a / 2 - self.num_pixels * self.pfov / 2
            else:
                x[0] = self.chip_spacing_a / 2 - self.num_pixels * self.pfov / 2
            if i == 0 or i == 2:
                y[0] = -self.chip_spacing_b / 2 - self.num_pixels * self.pfov / 2
            else:
                y[0] = self.chip_spacing_b / 2 - self.num_pixels * self.pfov / 2
            x[1] = x[0] + self.num_pixels * self.pfov
            x[2] = x[1]
            x[3] = x[0]
            y[1] = y[0]
            y[2] = y[1] + self.num_pixels * self.pfov
            y[3] = y[2]
            xd = x + center_x
            yd = y + center_y
            points = (self.degxy(xd[0], yd[0]), self.degxy(xd[1], yd[1]),
                      self.degxy(xd[2], yd[2]), self.degxy(xd[3], yd[3]))
            field.add(dwg.polygon(points=points))
            field.fill('red', opacity=0.2)

    def make_image(self):
        # Prepare a container for all elements
        dwg = svgwrite.Drawing(self.outfile, size=(297 * self.mm, 210 * self.mm))

        # Add an axis group
        axis = dwg.add(dwg.g(id='axis'))
        axis.add(dwg.line(start=self.degxy(-self.widex, -self.widey),
                          end=self.degxy(self.widex, - self.widey), stroke='black', stroke_width=2))
        axis.add(dwg.line(start=self.degxy(-self.widex, 0),
                          end=self.degxy(self.widex, 0), stroke='black', stroke_width=1))
        axis.add(dwg.line(start=self.degxy(-self.widex, self.widey),
                          end=self.degxy(self.widex, self.widey), stroke='black', stroke_width=2))
        axis.add(dwg.line(start=self.degxy(-self.widex, -self.widey),
                          end=self.degxy(-self.widex, self.widey), stroke='black', stroke_width=2))
        axis.add(dwg.line(start=self.degxy(0, -self.widey),
                          end=self.degxy(0, self.widey), stroke='black', stroke_width=1))
        axis.add(dwg.line(start=self.degxy(self.widex, -self.widey),
                          end=self.degxy(self.widex, self.widey), stroke='black', stroke_width=2))

        # Add Text
        title = dwg.add(dwg.g(id='axis'))
        title.add(dwg.text(self.text, insert=self.degxy(-self.gc, 0.8)))

        # Add the central region
        cent = dwg.add(dwg.g(id='cent'))
        cent.add(dwg.rect(insert=self.degxy(-self.gc, -self.gc), size=self.degxys(2 * self.gc, 2 * self.gc)))
        cent.fill('green', opacity=0.1)

        # Add the disk region
        disk = dwg.add(dwg.g(id='disk'))
        disk.add(dwg.rect(insert=self.degxy(-self.gc, -self.gdh), size=self.degxys(self.gc + self.gdw, 2 * self.gdh)))
        disk.fill('blue', opacity=0.1)

        self.addfield(-self.gc + self.chip_spacing_a / 2 + self.num_pixels * self.pfov / 2, -self.gc +
                 self.chip_spacing_b / 2 + self.num_pixels * self.pfov / 2, 0, dwg, 0)
        self.addfield(-self.gc + self.chip_spacing_a / 2 + self.num_pixels * self.pfov / 2, -self.gc +
                 self.chip_spacing_b / 2 * 3 + self.num_pixels * self.pfov / 2, 0, dwg, 1)
        self.addfield(-self.gc + self.chip_spacing_a / 2 + self.num_pixels * self.pfov / 2, -self.gc +
                 self.chip_spacing_b / 2 * 7 + self.num_pixels * self.pfov / 2, 0, dwg, 1)
        self.addfield(-self.gc + self.chip_spacing_a * 3 / 2 + self.num_pixels * self.pfov / 2, - self.gc +
                 self.chip_spacing_b / 2 * 7 + self.num_pixels * self.pfov / 2, 0, dwg, 1)
        dwg.save()


if __name__ == '__main__':
    args = docopt(__doc__)
    efl_per_cellsize = int(args['-m'])
    outfile = args['-o']
    Mapsim1(efl_per_cellsize, outfile).make_image()
