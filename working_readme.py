"""Publish the dolly part pages and refresh their section in the project index."""

from dolly_model import ROOT, records

START = "<!-- dolly catalogue -->"
END = "<!-- end dolly catalogue -->"


def part_page(part):
    dims = part["model_dimensions"]
    seat = ""
    if "seat_length" in dims:
        seat = f'| Internal seat (L × W × D) | {dims["seat_length"]} × {dims["seat_width"]} × {dims["seat_depth"]} mm |\n'
    if part["taxonomy_3"] == "simple":
        seat += f'| Platform thickness | {dims["deck"]} mm |\n'
    return f'''# {part["title"]}

![Three-quarter view of the dolly](three_d_model/render.png)

{part["listing_note"]}

| Specification | Per dolly |
| --- | --- |
| External length × width × height | {dims["length"]} × {dims["width"]} × {dims["height"]} mm |
{seat}| Wheel diameter | {dims["wheel"]} mm ({part["wheel_basis"]}) |
| Wheels | {part["wheel_layout"]} |
| Material | {part["material"]} |
| Supplier reference | {part["supplier_reference"]} |

{part["model_note"]} [Supplier listing · {part["supplier"]}]({part["url_source"]})

## Dimensioned drawing

![Plan, side and end views with dimensions](working.svg)

[Editable OpenSCAD model](three_d_model/working.scad) · [Lightweight colour model](three_d_model/working.glb) · [Full-size render](three_d_model/render.png)

Rebuild from the repository root with `python action_make_all.py --part {part["id"]}`. The supplier dimensions and modelling assumptions are in [the dolly declarations](../../working_oomp_populate_detail_dolly.py).
'''


def main(**kwargs):
    for folder, part in records(**kwargs):
        (folder / "README.md").write_text(part_page(part), encoding="utf-8")
    rows = []
    for folder, part in records():
        if (folder / "README.md").is_file():
            dims = part["model_dimensions"]
            rows.append(f'| [{part["title"]}](parts/{folder.name}/README.md) | '
                        f'{dims["length"]} × {dims["width"]} × {dims["height"]} mm | '
                        f'[Drawing](parts/{folder.name}/working.svg) · [Render](parts/{folder.name}/three_d_model/render.png) |')
    if rows:
        index = ROOT / "README.md"
        existing = index.read_text(encoding="utf-8") if index.exists() else "# OOMP packaging\n"
        section = "\n".join([START, "## Dollies", "", "| Part | External size | Views |",
                             "| --- | --- | --- |", *rows, "",
                             "### Regeneration", "",
                             "Edit the [dolly declarations](working_oomp_populate_detail_dolly.py) for dimensions "
                             "and supplier details, and the [shared OpenSCAD template](models/dolly.scad) for geometry.",
                             "Run `python action_make_all.py --part <canonical_id>` for one dolly or "
                             "`python action_make_all.py` for the catalogue. Each part page includes its exact command.",
                             "Use the project's OOMP/OOBB Python environment with NumPy, trimesh, PyYAML and Shapely 2, "
                             "plus OpenSCAD with the Manifold backend and Blender on PATH.", END])
        if START in existing and END in existing:
            before, rest = existing.split(START, 1)
            existing = before + section + rest.split(END, 1)[1]
        else:
            existing = existing.rstrip() + "\n\n" + section + "\n"
        index.write_text(existing, encoding="utf-8")


if __name__ == "__main__":
    main()
