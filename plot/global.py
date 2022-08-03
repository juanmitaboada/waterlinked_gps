#!/usr/bin/env python

import os
import sys

from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d, Axes3D
import matplotlib.pyplot as plt
import numpy as np

COLORS = False
TOP_COLOR = 100

if len(sys.argv) == 2:

    source = sys.argv[1]

    if os.path.exists(source):

        with open(source, "r") as F:

            # Read line
            line = F.readline()
            axdata = []
            aydata = []
            azdata = []
            gxdata = []
            gydata = []
            gzdata = []
            while line:

                # Split line
                linesp = line.split("\n")[0].split(",")

                # Get metadata
                epoch = linesp[0]
                kind = linesp[1]
                data = linesp[2:]

                # Global
                if kind == "G":
                    # Global: (Lat, Long, Depth)
                    if len(data) == 2:
                        # 1637329651.1517253,G,36.59739303588867,-4.511945724487305
                        (lat, lon) = data
                        lat = float(lat)
                        lon = float(lon)

                        gydata.append(lat)
                        gxdata.append(lon)
                        gzdata.append(0)

                    elif len(data) == 3:
                        # 1637329651.1517253,G,36.59739303588867,-4.511945724487305,0.18903954327106476
                        (lat, lon, depth) = data
                        lat = float(lat)
                        lon = float(lon)
                        depth = -float(depth)

                        gydata.append(lat)
                        gxdata.append(lon)
                        gzdata.append(depth)

                    else:
                        raise IOError(
                            "ERROR: wrong length of line for Global Position register"
                        )

                else:
                    raise IOError("ERROR: unknown kind with kind '{}'".format(kind))

                # Read new line
                line = F.readline()

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
                    gax.plot(
                        gxdata[i : i + 2],
                        gydata[i : i + 2],
                        gzdata[i : i + 2],
                        color=plt.cm.jet(color),
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
