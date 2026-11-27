"""Orthographic drawings from the same coloured geometry that Blender renders."""

from html import escape

import numpy as np
import shapely
import trimesh

from dolly_model import CAD_TO_GLTF, records


def projection(mesh, axes):
    triangles = mesh.triangles[:, :, axes]
    polygons = shapely.polygons(triangles)
    outline = shapely.union_all(polygons[shapely.area(polygons) > 0.0001], grid_size=.01)
    rings = []
    for piece in shapely.get_parts(outline):
        if piece.geom_type == "Polygon":
            rings.extend([piece.exterior, *piece.interiors])
    return rings


def view(meshes, axes, cx, cy, scale):
    paths = []
    for name in ("wheels", "mounts", "deck", "trim"):
        rings = projection(meshes[name], axes)
        paths_data = []
        for ring in rings:
            points = " ".join(f"{cx+x*scale:.2f},{cy-y*scale:.2f}" for x,y in ring.coords)
            paths_data.append(f"M{points}Z")
        paths.append(f'<path class="{name}" fill-rule="evenodd" d="{" ".join(paths_data)}"/>')
    return "\n".join(paths)


def dimension(x1, y1, x2, y2, label):
    vertical = x1 == x2
    ticks = (f"M{x1-4},{y1}h8 M{x2-4},{y2}h8" if vertical else
             f"M{x1},{y1-4}v8 M{x2},{y2-4}v8")
    x, y = (x1+x2)/2, (y1+y2)/2
    angle = -90 if vertical else 0
    return (f'<path class="dim" d="M{x1},{y1} L{x2},{y2} {ticks}"/>'
            f'<text transform="translate({x} {y}) rotate({angle})" dy="-5" class="measure">{label}</text>')


def drawing(folder, part):
    dims = part["model_dimensions"]
    length, width, height = (dims[key] for key in ("length", "width", "height"))
    scene = trimesh.load_scene(folder / "three_d_model/working.glb")
    meshes = scene.geometry
    for mesh in meshes.values():
        mesh.apply_transform(np.linalg.inv(CAD_TO_GLTF))
    scale = min(440/length, 215/width, 305/width)
    half_l, half_w, h = length*scale/2, width*scale/2, height*scale
    plan = view(meshes, [0,1], 290, 230, scale)
    side = view(meshes, [0,2], 290, 490, scale)
    end = view(meshes, [1,2], 748, 276, scale)
    length_dim = dimension(290-half_l, 230+half_w+16, 290+half_l, 230+half_w+16, length)
    width_dim = dimension(290+half_l+20, 230-half_w, 290+half_l+20, 230+half_w, width)
    height_dim = dimension(290+half_l+20, 490-h, 290+half_l+20, 490, height)
    wheel = f'Ø {dims["wheel"]} mm' + (" (estimate)" if part["wheel_basis"] == "estimated" else "")
    extra = ""
    if "seat_depth" in dims:
        extra = f'Seat · {dims["seat_length"]} × {dims["seat_width"]} × {dims["seat_depth"]} mm'
    elif part["taxonomy_3"] == "simple":
        extra = f'Board thickness · {dims["deck"]} mm'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="976" height="550" viewBox="0 0 976 550">
<title>{escape(part["title"])} — dimensioned reference</title>
<desc>Plan, side and end elevations at a common scale. Dimensions in millimetres.</desc>
<style>
text {{font-family:Arial,sans-serif;fill:#18383d}} .title {{font-size:28px;font-weight:bold}}
.label {{font-size:13px;font-weight:bold;letter-spacing:1px}} .detail {{font-size:16px}}
.measure {{font-size:14px;text-anchor:middle}} .dim {{stroke:#45656a;fill:none}}
.views path {{stroke:#224b53;stroke-width:1;stroke-linejoin:round}}
.deck {{fill:#bfd7d7}} .wheels {{fill:#647b82}} .mounts {{fill:#e0e7e8}} .trim {{fill:#8fb2b5}}
</style><rect width="976" height="550" fill="white"/>
<text x="32" y="43" class="title">{escape(part["title"])}</text>
<text x="32" y="69" class="detail">Reference geometry · Dimensions in millimetres</text>
<path d="M32 83H944 M32 380H944 M570 94V517" fill="none" stroke="#c1d1d2"/>
<text x="32" y="109" class="label">PLAN</text><text x="600" y="109" class="label">END</text>
<text x="32" y="407" class="label">SIDE</text><text x="600" y="407" class="label">SPECIFICATION</text>
<g class="views">{plan}{side}{end}</g>{length_dim}{width_dim}{height_dim}
<text x="600" y="439" class="detail">Overall · {length} × {width} × {height} mm</text>
<text x="600" y="466" class="detail">Castors · 4 × {wheel}</text>
<text x="600" y="493" class="detail">{escape(part["material"])}</text>
<text x="600" y="520" class="detail">{extra}</text>
</svg>\n'''


def main(**kwargs):
    for folder, part in records(**kwargs):
        (folder / "working.svg").write_text(drawing(folder, part), encoding="utf-8")


if __name__ == "__main__":
    main()
