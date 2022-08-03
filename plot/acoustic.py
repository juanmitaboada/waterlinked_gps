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

                # Acoustic
                if kind == "A":
                    # Acoustic: (X, Y, Z)
                    # 1637329651.1429172,A,1.3329839706420898,-0.47698575258255005,0.18903954327106476
                    (x, y, z) = data
                    x = float(x)
                    y = float(y)
                    z = -float(z)

                    aydata.append(x)
                    axdata.append(y)
                    azdata.append(z)

                    # print("Acoustic: ({}, {}, {})".format(x, y, z))

                # Global
                else:
                    raise IOError("ERROR: unknown kind with kind '{}'".format(kind))

                # Read new line
                line = F.readline()

            # === ACOUSTIC ===
            print("=== ACOUSTIC ===")
            # Figure Acoustic
            afig = plt.figure()
            aax = Axes3D(afig, auto_add_to_figure=False)
            afig.add_axes(aax)

            if not COLORS:
                # Plot
                aax.plot(axdata, aydata, azdata)

            else:

                # Plot Acoustic
                for i in range(len(azdata) - 1):
                    color = (azdata[i] - min(azdata)) / abs(min(azdata) - max(azdata))
                    aax.plot(
                        axdata[i : i + 2],
                        aydata[i : i + 2],
                        azdata[i : i + 2],
                        color=plt.cm.jet(color),
                    )

                # Set limits on graph
                aax.set_xlim([min(axdata), max(axdata)])
                aax.set_ylim([min(aydata), max(aydata)])
                aax.set_zlim([min(azdata), max(azdata)])

            # Show
            plt.show()

    else:
        print("ERROR: file '{}' not found!".format(source))
else:
    print("Usage: {} <filename>".format(sys.argv[0]))
