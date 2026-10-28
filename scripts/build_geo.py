"""Turn us-atlas states-albers-10m TopoJSON into SVG path strings keyed by state FIPS.

Output data/build/state_paths.json: {fips: "M...Z"} in a 975x610 viewBox. Shared borders
are decoded from the same arcs, so neighbors line up exactly.
"""
import json
from pathlib import Path
from states import BY_FIPS

ROOT = Path(__file__).resolve().parents[1]


def decode_arcs(topo):
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs


def ring(arcs, idxs):
    pts = []
    for i in idxs:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"


def main():
    topo = json.loads((ROOT / "data/raw/geo/states-albers-10m.json").read_text())
    arcs = decode_arcs(topo)
    out = {}
    for g in topo["objects"]["states"]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        out[g["id"]] = "".join(ring(arcs, r) for poly in polys for r in poly)
    if set(out) != set(BY_FIPS):
        raise SystemExit(f"state mismatch: {set(out) ^ set(BY_FIPS)}")
    (ROOT / "data/build").mkdir(parents=True, exist_ok=True)
    (ROOT / "data/build/state_paths.json").write_text(json.dumps(out, separators=(",", ":")))
    print(len(out), "states,", sum(map(len, out.values())) // 1024, "KB of path data")


if __name__ == "__main__":
    main()
