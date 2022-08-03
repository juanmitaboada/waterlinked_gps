#!/usr/bin/env python

import os
import sys
import random

from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d, Axes3D
import matplotlib.pyplot as plt
import numpy as np

COLORS = True
maxtep = 0.01

# get_color = plt.cm.terrain
get_color = plt.cm.rainbow
# get_color = plt.cm.gist_ncar
# get_color = plt.cm.prism


def inter(elements):
    new = []
    first = True
    for e in elements:
        if not first:
            diff = last + e
            if last > e:
                i = last - (last - e) / 2
            else:
                i = e - (e - last) / 2
            new.append(i)
            last = e
        else:
            first = False
            last = e

    return new


if len(sys.argv) == 2:

    source = sys.argv[1]

    if os.path.exists(source):

        with open(source, "r") as F:

            # Read line
            line = F.readline()
            data = []
            gxdata = []
            gydata = []
            gzdata = []
            value = None
            while line:

                # Split line
                ldata = line.split("\n")[0].split(" ")

                # Global: (Lat, Long, Depth)
                # 1637329651.1517253,G,36.59739303588867,-4.511945724487305,0.18903954327106476
                (lat, lon, depth) = ldata
                lat = float(lat)
                lon = float(lon)
                depth = -float(depth)

                data.append((lat, lon, depth))
                if value:
                    value = min(value, 0 - depth)
                else:
                    value = 0 - depth

                # Read new line
                line = F.readline()

            # HEAD
            for (lat, lon, depth) in data:
                break
            gxdata.append(lat)
            gydata.append(lon)
            gzdata.append(0)

            # BODY
            acu = 0
            for (lat, lon, depth) in data[0:-1]:
                if random.random() > 0.8:
                    acu += random.random() * maxtep
                else:
                    acu -= random.random() * maxtep
                gxdata.append(lat)
                gydata.append(lon + acu)
                gzdata.append(depth + value)

            # TAIL
            acu += random.random() * maxtep
            for (lat, lon, depth) in data[-1:]:
                break
            gxdata.append(lat)
            gydata.append(lon + acu)
            gzdata.append(0)

            for i in range(0, 3):
                gxdata = inter(gxdata)
                gydata = inter(gydata)
                gzdata = inter(gzdata)

            # === GLOBAL ===
            print("=== GLOBAL ===")
            # Figure Global
            gfig = plt.figure()
            gax = Axes3D(gfig, auto_add_to_figure=False)
            gfig.add_axes(gax)

            if not COLORS:
                # Plot
                gax.plot(gxdata, gydata, gzdata)
            else:

                # Plot Global
                for i in range(len(gzdata) - 1):
                    color = (gzdata[i] - min(gzdata)) / abs(min(gzdata) - max(gzdata))
                    print(gzdata[i], color)
                    # color = i / (len(gzdata) - 1)
                    gax.plot(
                        gxdata[i : i + 2],
                        gydata[i : i + 2],
                        gzdata[i : i + 2],
                        color=get_color(color),
                    )

                # Set limits on graph
                gax.set_xlim([min(gxdata), max(gxdata)])
                gax.set_ylim([min(gydata), max(gydata)])
                gax.set_zlim([min(gzdata), max(gzdata)])

            # Show
            plt.show()

    else:
        print("ERROR: file '{}' not found!".format(source))
else:
    print("Usage: {} <filename>".format(sys.argv[0]))
