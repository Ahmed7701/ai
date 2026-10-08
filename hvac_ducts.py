"""Adds sheet-metal supply-air ducts + diffusers (schematic) to a DXF plan.
Usage: python hvac_ducts.py in.dxf out.dxf
Coordinates are assumptions read from the plan; sizes are NOT calculated."""
import sys, ezdxf
from shapely.geometry import box
from shapely.ops import unary_union

src, dst = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(src)
ms = doc.modelspace()
for name, color in (("M-DUCT-SA", 3), ("M-DIFUSER", 2), ("A-SUP-texts", 7), ("M-AHU", 6), ("A-RET-texts", 7)):
    if name not in doc.layers:
        doc.layers.add(name, color=color)

def rect(x1, y1, x2, y2):
    return box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

def hduct(x1, x2, y, w):
    return rect(x1, y - w / 2, x2, y + w / 2)

def vduct(x, y1, y2, w):
    return rect(x - w / 2, y1, x + w / 2, y2)

Y_MAIN, X_SPINE = 51.0, 121.4
parts = [
    hduct(100.0, X_SPINE + 0.25, Y_MAIN, 0.8),            # main from AHU
    vduct(X_SPINE, 44.5, 55.0, 0.5),                      # spine west of RET ducts
]
diffusers = []

# Type B machines: branches up/down to a diffuser above each machine
for cx in (111.85, 117.05):
    parts += [vduct(cx, Y_MAIN, 54.2, 0.5), vduct(cx, 47.5, Y_MAIN, 0.5)]
    diffusers += [(cx, 54.6), (cx, 47.1)]

# Type A zone: branches in the gaps between strips (cross RET ducts overhead)
for y in (45.5, 48.3, 51.0, 53.55):
    parts.append(hduct(X_SPINE, 134.2, y, 0.4))
    diffusers += [(130.0, y), (133.0, y)]

for poly in (unary_union(parts),):
    for g in getattr(poly, "geoms", [poly]):
        ms.add_lwpolyline(list(g.exterior.coords), close=True, dxfattribs={"layer": "M-DUCT-SA"})

for x, y in diffusers:                                    # 0.6 m square diffuser with X
    h = 0.3
    ms.add_lwpolyline([(x-h, y-h), (x+h, y-h), (x+h, y+h), (x-h, y+h)], close=True, dxfattribs={"layer": "M-DIFUSER"})
    ms.add_line((x-h, y-h), (x+h, y+h), dxfattribs={"layer": "M-DIFUSER"})
    ms.add_line((x-h, y+h), (x+h, y-h), dxfattribs={"layer": "M-DIFUSER"})

ahu = rect(97.0, 49.8, 100.0, 52.2)
ms.add_lwpolyline(list(ahu.exterior.coords), close=True, dxfattribs={"layer": "M-AHU"})
for txt, x, y, l in (("AHU", 97.8, 50.8, "M-AHU"), ("SA 800x350", 105.0, 51.6, "A-SUP-texts"),
                     ("SA 500x300", X_SPINE + 0.4, 55.3, "A-SUP-texts"),
                     ("RA DUCT", 123.0, 55.4, "A-RET-texts")):
    ms.add_text(txt, height=0.3, dxfattribs={"layer": l, "insert": (x, y)})
doc.saveas(dst)
