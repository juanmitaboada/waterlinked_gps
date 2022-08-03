#!/usr/bin/env python

import os
import sys
import gpxpy.gpx
import simplekml

if len(sys.argv) == 2:

    source = sys.argv[1]

    if os.path.exists(source):
        targetgpx = "{}.gpx".format(".".join(source.split(".")[:-1]))
        targetkml = "{}.kml".format(".".join(source.split(".")[:-1]))

        if source != targetgpx:

            with open(source, "r") as F:

                # Prepare new GPX file
                gpx = gpxpy.gpx.GPX()
                # Prepare new KML file
                kml = simplekml.Kml()

                # Create first track in our GPX:
                gpx_track = gpxpy.gpx.GPXTrack()
                gpx.tracks.append(gpx_track)

                # Create first segment in our GPX track:
                gpx_segment = gpxpy.gpx.GPXTrackSegment()
                gpx_track.segments.append(gpx_segment)

                # Read line
                line = F.readline()
                coords = []
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

                        # print("Acoustic: ({}, {}, {})".format(x, y, z))

                    # Global
                    elif kind == "G":
                        # Global: (Lat, Long, Depth)
                        if len(data) == 2:
                            # 1637329651.1517253,G,36.59739303588867,-4.511945724487305
                            (lat, lon) = data
                            lat = float(lat)
                            lon = float(lon)

                            # Add GPX point
                            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))
                            # print("Global: ({}, {}, {})".format(lat, lon))

                            # Add new coord
                            coords.append((lon, lat))

                        elif len(data) == 3:
                            # 1637329651.1517253,G,36.59739303588867,-4.511945724487305,0.18903954327106476
                            (lat, lon, depth) = data
                            lat = float(lat)
                            lon = float(lon)
                            depth = -float(depth)

                            # Add point
                            gpx_segment.points.append(
                                gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=depth)
                            )
                            # print("Global: ({}, {}, {})".format(lat, lon, depth))

                            # Add new coor
                            coords.append((lon, lat, depth))

                        else:
                            raise IOError(
                                "ERROR: wrong length of line for Global Position register"
                            )

                    else:
                        raise IOError("ERROR: unknown kind with kind '{}'".format(kind))

                    # Read new line
                    line = F.readline()

            # Save GPX file to disk
            print("Writting GPX to {}...".format(targetgpx), end="")
            with open(targetgpx, "w") as F:
                F.write(gpx.to_xml())
            print("done")

            # Attach line to KML file
            line = kml.newlinestring(
                name="Rov track", description="Rov track", coords=coords
            )
            line.style.linestyle.color = "ff0000ff"
            line.style.linestyle.width = 10

            # Save KML file to disk
            print("Writting KML to {}...".format(targetkml), end="")
            kml.save(targetkml)
            print("done")

        else:
            print("ERROR: source can not be a GPX file!")

    else:
        print("ERROR: file '{}' not found!".format(source))
else:
    print("Usage: {} <filename>".format(sys.argv[0]))
