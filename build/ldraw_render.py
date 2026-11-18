"""Draws one LEGO piece from the LDraw parts library as a PNG.

This is a tool, not part of the page build. It is run once, by hand, when a
piece is added to build/parts.py, and the PNG files it writes into parts/ are
committed. render.py only reads those PNG files, so the site still builds from
any clone without the LDraw library.

    python3 build/ldraw_render.py /path/to/ldraw            # every piece
    python3 build/ldraw_render.py /path/to/ldraw 40490_0    # one piece

The LDraw parts library is at https://library.ldraw.org/ and is licensed
CC BY 4.0 (older files CC BY 2.0). The drawings are made from its geometry by
the code below: a flat-shaded picture with a depth buffer, and the library's own
edge lines drawn on top.
"""
import math
import os
import sys

import numpy as np
from PIL import Image

SS = 3            # supersampling
CANVAS = (360, 270)   # final size in px
MAX_PX_PER_LDU = 4.4  # small pieces are not blown up past this


class Lib:
    def __init__(self, root):
        self.root = root
        self.cache = {}
        self.colours = {}
        self._index = {}
        for sub in ("parts", "p", "parts/s", "p/48", "p/8", "models"):
            d = os.path.join(root, sub)
            if not os.path.isdir(d):
                continue
            pre = ""
            if sub == "parts/s":
                pre = "s\\"
            elif sub == "p/48":
                pre = "48\\"
            elif sub == "p/8":
                pre = "8\\"
            for name in os.listdir(d):
                key = (pre + name).lower()
                self._index.setdefault(key, os.path.join(d, name))
        self._colours()

    def _colours(self):
        with open(os.path.join(self.root, "LDConfig.ldr"), encoding="utf-8", errors="replace") as fh:
            for line in fh:
                t = line.split()
                if len(t) > 8 and t[1] == "!COLOUR":
                    code = int(t[t.index("CODE") + 1])
                    val = t[t.index("VALUE") + 1]
                    edge = t[t.index("EDGE") + 1]
                    self.colours[code] = (self._hex(val), self._hex(edge))

    @staticmethod
    def _hex(s):
        s = s.lstrip("#")
        return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))

    def load(self, name):
        key = name.lower().replace("/", "\\")
        if key in self.cache:
            return self.cache[key]
        path = self._index.get(key)
        if path is None:
            raise FileNotFoundError(name)
        rows = []
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                t = line.split()
                if not t or t[0] == "0":
                    continue
                kind = t[0]
                if kind == "1" and len(t) >= 15:
                    m = np.array([float(x) for x in t[2:14]])
                    rows.append((1, int(t[1]), m, " ".join(t[14:])))
                elif kind in ("2", "3", "4", "5"):
                    n = {"2": 6, "3": 9, "4": 12, "5": 12}[kind]
                    try:
                        col = int(t[1])
                    except ValueError:
                        col = 16
                    pts = np.array([float(x) for x in t[2:2 + n]]).reshape(-1, 3)
                    rows.append((int(kind), col, pts, None))
        self.cache[key] = rows
        return rows


def collect(lib, name, colour, M=None, T=None, edge_of=None, out=None):
    """Walks a file and its subfiles. Fills out['tri'], out['edge'], out['cond']."""
    if out is None:
        out = {"tri": [], "tricol": [], "edge": [], "edgecol": [], "cond": [], "condcol": []}
    if M is None:
        M = np.eye(3)
        T = np.zeros(3)
    for kind, col, data, sub in lib.load(name):
        if col == 16:
            c = colour
        elif col == 24:
            c = ("edge", colour)
        else:
            c = col
        if kind == 1:
            t = data[0:3]
            m = data[3:12].reshape(3, 3)
            sc = colour if col in (16, 24) else col
            try:
                collect(lib, sub, sc, M @ m, M @ t + T, None, out)
            except FileNotFoundError:
                print("   missing subfile", sub, file=sys.stderr)
        else:
            pts = data @ M.T + T
            if kind == 3:
                out["tri"].append(pts)
                out["tricol"].append(c)
            elif kind == 4:
                out["tri"].append(pts[[0, 1, 2]])
                out["tricol"].append(c)
                out["tri"].append(pts[[0, 2, 3]])
                out["tricol"].append(c)
            elif kind == 2:
                out["edge"].append(pts)
                out["edgecol"].append(c)
            elif kind == 5:
                out["cond"].append(pts)
                out["condcol"].append(c)
    return out


def rot(ax, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    if ax == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if ax == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def fill_rgb(lib, c, overrides):
    if isinstance(c, tuple):
        base = c[1]
        base = base[1] if isinstance(base, tuple) else base
        return lib.colours.get(base, ((127, 127, 127), (51, 51, 51)))[1]
    if c in overrides:
        return overrides[c]
    return lib.colours.get(c, ((127, 127, 127), (51, 51, 51)))[0]


def edge_rgb(lib, c):
    if isinstance(c, tuple):
        base = c[1]
        base = base[1] if isinstance(base, tuple) else base
    else:
        base = c
    return lib.colours.get(base, ((127, 127, 127), (51, 51, 51)))[1]


# Black pieces are drawn in charcoal with pale edge lines, so their holes and
# corners still show. Clear pieces are drawn in a pale blue-grey.
FILL_OVERRIDES = {0: (52, 56, 60), 47: (214, 228, 236), 70: (104, 62, 30),
                  179: (176, 176, 180), 26: (164, 52, 140)}


def render(lib, files, pre=None, azim=-35, elev=28, canvas=CANVAS, edges_on=True):
    """files: list of (ldraw file, colour code, 3x3 matrix or None, offset or None)."""
    out = None
    for name, colour, m, t in files:
        out = collect(lib, name, colour,
                      np.eye(3) if m is None else np.array(m, float),
                      np.zeros(3) if t is None else np.array(t, float), None, out)
    tri = np.array(out["tri"]).reshape(-1, 3, 3)
    edges = np.array(out["edge"]).reshape(-1, 2, 3)
    cond = np.array(out["cond"]).reshape(-1, 4, 3)

    R = rot("x", elev) @ rot("y", azim)
    if pre is not None:
        R = R @ pre
    # LDraw: -y is up, -z is toward the viewer. Screen: x right, y down, small z near.
    tv = tri @ R.T
    ev = edges @ R.T
    cv = cond @ R.T

    allpts = tv.reshape(-1, 3)
    lo = allpts.min(0)
    hi = allpts.max(0)
    W, H = canvas[0] * SS, canvas[1] * SS
    pad = 10 * SS
    span = np.maximum(hi[:2] - lo[:2], 1e-6)
    scale = min((W - 2 * pad) / span[0], (H - 2 * pad) / span[1], MAX_PX_PER_LDU * SS)
    off = np.array([W / 2, H / 2]) - scale * (lo[:2] + hi[:2]) / 2

    def to_screen(p):
        q = p.copy()
        q[..., 0] = p[..., 0] * scale + off[0]
        q[..., 1] = p[..., 1] * scale + off[1]
        return q

    ts = to_screen(tv)
    es = to_screen(ev)
    cs = to_screen(cv)

    zbuf = np.full((H, W), np.inf)
    img = np.zeros((H, W, 3), np.float32)
    alpha = np.zeros((H, W), np.float32)

    # flat shading, two-sided
    n = np.cross(tv[:, 1] - tv[:, 0], tv[:, 2] - tv[:, 0])
    ln = np.linalg.norm(n, axis=1)
    ln[ln == 0] = 1
    n = n / ln[:, None]
    light = np.array([-0.35, -0.75, -0.56])
    light = light / np.linalg.norm(light)
    lam = np.abs(n @ light)
    shade = 0.70 + 0.38 * lam

    cols = np.array([fill_rgb(lib, c, FILL_OVERRIDES) for c in out["tricol"]], np.float32)
    cols = np.clip(cols * shade[:, None], 0, 255)

    for i in range(len(ts)):
        p = ts[i]
        x0 = max(int(math.floor(p[:, 0].min())), 0)
        x1 = min(int(math.ceil(p[:, 0].max())), W - 1)
        y0 = max(int(math.floor(p[:, 1].min())), 0)
        y1 = min(int(math.ceil(p[:, 1].max())), H - 1)
        if x1 < x0 or y1 < y0:
            continue
        ax, ay = p[0, 0], p[0, 1]
        bx, by = p[1, 0], p[1, 1]
        cx, cy = p[2, 0], p[2, 1]
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9:
            continue
        xs = np.arange(x0, x1 + 1) + 0.5
        ys = np.arange(y0, y1 + 1) + 0.5
        X, Y = np.meshgrid(xs, ys)
        w0 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den
        w1 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den
        w2 = 1 - w0 - w1
        inside = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
        if not inside.any():
            continue
        z = w0 * p[0, 2] + w1 * p[1, 2] + w2 * p[2, 2]
        zb = zbuf[y0:y1 + 1, x0:x1 + 1]
        m = inside & (z < zb)
        if not m.any():
            continue
        zb[m] = z[m]
        img[y0:y1 + 1, x0:x1 + 1][m] = cols[i]
        alpha[y0:y1 + 1, x0:x1 + 1][m] = 1

    # edge lines, and conditional lines where they are an outline
    lines = [es]
    linecols = [np.array([edge_rgb(lib, c) for c in out["edgecol"]], np.float32).reshape(-1, 3)]
    if len(cs):
        a, b, c1, c2 = cs[:, 0, :2], cs[:, 1, :2], cs[:, 2, :2], cs[:, 3, :2]
        d = b - a
        s1 = d[:, 0] * (c1[:, 1] - a[:, 1]) - d[:, 1] * (c1[:, 0] - a[:, 0])
        s2 = d[:, 0] * (c2[:, 1] - a[:, 1]) - d[:, 1] * (c2[:, 0] - a[:, 0])
        keep = (s1 * s2) > 0
        lines.append(cs[keep][:, :2, :])
        cc = np.array([edge_rgb(lib, c) for c in out["condcol"]], np.float32).reshape(-1, 3)
        linecols.append(cc[keep])
    L = np.concatenate(lines) if lines else np.zeros((0, 2, 3))
    if not edges_on:
        L = L[:0]
    LC = np.concatenate(linecols) if linecols else np.zeros((0, 3))
    zrange = max(hi[2] - lo[2], 1.0)
    bias = 0.012 * zrange + 0.9
    half = max(1, int(round(0.55 * SS)))
    for i in range(len(L)):
        a, b = L[i]
        npx = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
        tt = np.linspace(0, 1, npx + 1)
        xs = a[0] + (b[0] - a[0]) * tt
        ys = a[1] + (b[1] - a[1]) * tt
        zs = a[2] + (b[2] - a[2]) * tt - bias
        for dx in range(-half + 1, half + 1):
            for dy in range(-half + 1, half + 1):
                xi = (xs + dx - 0.5).astype(int)
                yi = (ys + dy - 0.5).astype(int)
                ok = (xi >= 0) & (xi < W) & (yi >= 0) & (yi < H)
                xi2, yi2, z2 = xi[ok], yi[ok], zs[ok]
                vis = z2 <= zbuf[yi2, xi2]
                img[yi2[vis], xi2[vis]] = LC[i]
                alpha[yi2[vis], xi2[vis]] = 1

    rgba = np.dstack([img, alpha[..., None] * 255]).astype(np.uint8)
    im = Image.fromarray(rgba, "RGBA")
    # premultiplied downsample so edges do not pick up black
    arr = np.asarray(im).astype(np.float32)
    arr[..., :3] *= arr[..., 3:4] / 255.0
    h2, w2 = H // SS, W // SS
    arr = arr.reshape(h2, SS, w2, SS, 4).mean(axis=(1, 3))
    a = arr[..., 3:4]
    rgb = np.where(a > 0, arr[..., :3] / np.maximum(a, 1e-6) * 255.0, 0)
    small = np.dstack([np.clip(rgb, 0, 255), a]).astype(np.uint8)
    return Image.fromarray(small, "RGBA")


def save(im, path):
    bbox = im.getbbox()
    if bbox:
        l, t, r, b = bbox
        pad = 4
        im = im.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))
    q = im.quantize(colors=96, method=Image.Quantize.FASTOCTREE)
    q.save(path, optimize=True)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    import parts as P
    root = sys.argv[1]
    only = set(sys.argv[2:])
    lib = Lib(root)
    outdir = os.path.join(os.path.dirname(here), "parts")
    os.makedirs(outdir, exist_ok=True)
    for d in P.DRAWINGS:
        if only and d["img"] not in only:
            continue
        pre = None
        for ax, deg in d.get("turn", []):
            r = rot(ax, deg)
            pre = r if pre is None else pre @ r
        im = render(lib, d["files"], pre=pre, azim=d.get("azim", -35), elev=d.get("elev", 28),
                    edges_on=d.get("edges", True))
        save(im, os.path.join(outdir, d["img"] + ".png"))
        print("drew", d["img"], im.size)


if __name__ == "__main__":
    main()
