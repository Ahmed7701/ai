"""Adds chilled-water pipe routes (schematic) to a copy of a DXF plan.
Usage: python hvac_pipes.py in.dxf out.dxf
All coordinates are assumptions read from the plan; adjust and re-run."""
import sys, ezdxf

src, dst = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(src)
ms = doc.modelspace()
for name, color in (("P-CHWS", 4), ("P-CHWR", 30), ("P-CHW-TXT", 7)):
    if name not in doc.layers:
        doc.layers.add(name, color=color)

W = 0.08  # pipe width in drawing units (m)

def pipe(layer, pts):
    ms.add_lwpolyline(pts, dxfattribs={"layer": layer, "const_width": W})

S, R = "P-CHWS", "P-CHWR"
PLANT_X = 100.0                      # assumed chiller connection point (west)
YS, YR = 51.45, 50.55                # headers in the aisle between B rows
VS, VR = 120.2, 120.9                # risers in aisle west of the RET ducts
TS, TR = 55.65, 55.35                # runs above the RET ducts
AS, AR = 127.15, 127.85              # trunks in aisle east of the RET ducts

# Type B machines (2 rows x 2): box centres x, upper-row bottom, lower-row top
for cx in (111.85, 117.05):
    pipe(S, [(cx - 0.4, YS), (cx - 0.4, 51.8)])      # upper: supply
    pipe(R, [(cx + 0.4, YR), (cx + 0.4, 51.8)])      # upper: return (crosses S header)
    pipe(S, [(cx - 0.4, YS), (cx - 0.4, 50.2)])      # lower: supply (crosses R header)
    pipe(R, [(cx + 0.4, YR), (cx + 0.4, 50.2)])      # lower: return

pipe(S, [(PLANT_X, YS), (VS, YS), (VS, TS), (AS, TS), (AS, 44.0)])
pipe(R, [(PLANT_X, YR), (VR, YR), (VR, TR), (AR, TR), (AR, 44.0)])

# Type A machines (5 strips): stubs east into each strip's left edge
for y in (44.0, 47.0, 49.6, 52.4, 54.7):
    pipe(S, [(AS, y + 0.2), (128.3, y + 0.2)])
    pipe(R, [(AR, y - 0.2), (128.3, y - 0.2)])

for txt, x, y in (("CHWS", 101, YS + 0.2), ("CHWR", 101, YR - 0.5)):
    ms.add_text(txt, height=0.3, dxfattribs={"layer": "P-CHW-TXT", "insert": (x, y)})

doc.saveas(dst)
