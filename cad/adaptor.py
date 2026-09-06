#!/usr/bin/env python3
"""
Generates the printed adaptor that joins the 8" driver to the DN100 PVC pipe,
plus a small test ring for checking the pipe fit before committing to the big print.

    python3 cad/adaptor.py

Everything is driven by the constants below — edit and re-run.

Geometry notes
--------------
The driver mounts on the FRONT face (z=0) with its cone facing into the chamber and
its basket in free air. That matters: it means the funnel only has to clear the cone
dish, not the 92 mm-deep basket. Mounting it the other way round would need a funnel
big enough to swallow the whole basket.

No bolt holes. Jaycar publish the 212 mm bolt circle for the CW2196 but not how many
holes it has, so the front face carries a shallow scribed groove at that diameter —
mark through the driver's own flange and drill to match.

The pipe socket is a slip fit over the pipe OD, sealed with silicone. It is NOT
solvent welded: PVC cement works by dissolving PVC and will not touch PLA or PETG.
"""

import math
import struct

# ---------------------------------------------------------------- parameters

DRIVER_CUTOUT_D = 182.0  # Jaycar CW2196 cutout
DRIVER_BOLT_CIRCLE_D = 212.0  # scribed onto the front face
FLANGE_OD = 245.0
FLANGE_THICKNESS = 10.0

PIPE_OD = 110.0  # DN100 PVC DWV
SOCKET_CLEARANCE = 0.6  # slip fit; increase if your pipe is tight
SOCKET_DEPTH = 45.0
SOCKET_WALL = 7.7

TAPER_LENGTH = 45.0  # 182 -> pipe bore. 38 deg from vertical, prints without support
CONE_WALL = 4.0

SCRIBE_DEPTH = 1.0
SCRIBE_HALF_WIDTH = 1.0

SEGMENTS = 360  # angular resolution of the revolve

# ---------------------------------------------------------------- profile

socket_bore_r = (PIPE_OD + SOCKET_CLEARANCE) / 2.0
socket_outer_r = socket_bore_r + SOCKET_WALL
cutout_r = DRIVER_CUTOUT_D / 2.0
flange_r = FLANGE_OD / 2.0
scribe_r = DRIVER_BOLT_CIRCLE_D / 2.0

z_flange_back = FLANGE_THICKNESS
z_taper_end = z_flange_back + TAPER_LENGTH
z_back = z_taper_end + SOCKET_DEPTH

# Closed cross-section in (r, z), counter-clockwise. Revolved about the z axis.
# Never touches r=0, so the result is a watertight tube-topology solid.
PROFILE = [
    # inner surface, front to back
    (cutout_r, 0.0),
    (cutout_r, z_flange_back),
    (socket_bore_r, z_taper_end),
    (socket_bore_r, z_back),
    # back annular face
    (socket_outer_r, z_back),
    # outer surface, back to front
    (socket_outer_r, z_taper_end),
    (cutout_r + CONE_WALL, z_flange_back),
    (flange_r, z_flange_back),
    (flange_r, 0.0),
    # front face, with the bolt-circle scribe groove
    (scribe_r + SCRIBE_HALF_WIDTH, 0.0),
    (scribe_r, SCRIBE_DEPTH),
    (scribe_r - SCRIBE_HALF_WIDTH, 0.0),
]

TEST_RING_PROFILE = [
    (socket_bore_r, 0.0),
    (socket_bore_r, 15.0),
    (socket_outer_r, 15.0),
    (socket_outer_r, 0.0),
]

# ---------------------------------------------------------------- meshing


def revolve(profile, segments):
    """Revolve a closed (r, z) profile about the z axis into a triangle list."""
    tris = []
    for i in range(segments):
        a0 = 2 * math.pi * i / segments
        a1 = 2 * math.pi * (i + 1) / segments
        c0, s0 = math.cos(a0), math.sin(a0)
        c1, s1 = math.cos(a1), math.sin(a1)

        for j in range(len(profile)):
            r0, z0 = profile[j]
            r1, z1 = profile[(j + 1) % len(profile)]
            if r0 == r1 and z0 == z1:
                continue

            p00 = (r0 * c0, r0 * s0, z0)
            p01 = (r0 * c1, r0 * s1, z0)
            p10 = (r1 * c0, r1 * s0, z1)
            p11 = (r1 * c1, r1 * s1, z1)

            tris.append((p00, p10, p11))
            tris.append((p00, p11, p01))
    return tris


def normal(a, b, c):
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    length = math.sqrt(nx * nx + ny * ny + nz * nz)
    return (0.0, 0.0, 0.0) if length == 0 else (nx / length, ny / length, nz / length)


def write_stl(path, tris, header):
    with open(path, "wb") as f:
        f.write(header.encode("ascii")[:80].ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            f.write(struct.pack("<3f", *normal(a, b, c)))
            for v in (a, b, c):
                f.write(struct.pack("<3f", *v))
            f.write(struct.pack("<H", 0))


def internal_volume_litres():
    """Dead volume the adaptor adds to the chamber, front face to the pipe end."""
    v = math.pi * cutout_r**2 * FLANGE_THICKNESS
    r0, r1 = cutout_r, socket_bore_r
    v += (math.pi * TAPER_LENGTH / 3.0) * (r0 * r0 + r0 * r1 + r1 * r1)
    return v / 1e6


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))

    body = revolve(PROFILE, SEGMENTS)
    write_stl(os.path.join(here, "adaptor.stl"), body, "leg-sucker DN100 to 8in driver adaptor")

    ring = revolve(TEST_RING_PROFILE, SEGMENTS)
    write_stl(os.path.join(here, "pipe-fit-test-ring.stl"), ring, "leg-sucker pipe fit test ring")

    print(f"adaptor.stl                {len(body):>6} triangles")
    print(f"pipe-fit-test-ring.stl     {len(ring):>6} triangles")
    print()
    print(f"  flange              {FLANGE_OD:.1f} mm OD x {FLANGE_THICKNESS:.0f} mm")
    print(f"  driver cutout       {DRIVER_CUTOUT_D:.1f} mm")
    print(f"  bolt circle scribe  {DRIVER_BOLT_CIRCLE_D:.1f} mm")
    print(f"  pipe socket         {socket_bore_r * 2:.1f} mm bore x {SOCKET_DEPTH:.0f} mm deep")
    print(f"  overall length      {z_back:.1f} mm")
    print(f"  dead volume added   {internal_volume_litres():.2f} L")
