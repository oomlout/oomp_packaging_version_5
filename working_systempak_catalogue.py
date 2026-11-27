"""Generate SystemPAK catalogue illustrations using saved supplier dimensions."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import re
import shutil
import subprocess

from oomp_populate_helper import build_oomp_id
from working_systempak_harvest import harvest_systempak, product_to_oomp
from working_systempak_examples import diagram

ROOT = Path(__file__).resolve().parent

# These supplier technical sheets supply dimensions omitted from the saved listing.
SHEET_DIMENSIONS = {
    "2001": (47, 47, 27.9),
    "2002": (48, 48, 31),
    "210": (108, 86, 30),
    "214": (108, 86, 95),
}

def specification(product, **kwargs):
    sku = product["sku"]
    info = product["additional_information"]
    raw = info.get("size") or ""
    if sku in SHEET_DIMENSIONS:
        length, width, height = SHEET_DIMENSIONS[sku]
        basis = "supplier technical sheet, container dimensions"
    elif product["source_shape"] == "round":
        numbers = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", raw)]
        if len(numbers) != 2:
            raise ValueError(f"{sku} cannot read dimensions from {raw!r}")
        length, width, height = numbers[0], numbers[0], numbers[1]
        basis = "supplier listing size field"
    else:
        numbers = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", raw)]
        if len(numbers) < 3:
            raise ValueError(f"{sku} cannot read dimensions from {raw!r}")
        length, width, height = numbers[:3]
        basis = "supplier listing size field"
    title = product["title"]
    discrepancy = ""
    if sku == "2001":
        discrepancy = "The listing title says 25 ml while the legacy OOMP identifier says 30 ml. Dimensions follow the technical sheet."
    elif sku == "2002":
        discrepancy = "The technical sheet states a 48 mm diameter while the listing title and OOMP identifier say 47 mm."
    elif sku == "2103":
        discrepancy = "The listing gives two sizes, 184.5 × 118 × 38 mm and 192 × 128 × 35 mm. This model uses the first."
    elif sku == "2031":
        discrepancy = "The title says 170 mm diameter while the listing size field says 160 mm. This model uses the size field."
    elif sku == "2039":
        discrepancy = "The title says 97 mm diameter while the listing size field says 95 mm. This model uses the size field."
    elif sku in ("2401c", "2401w"):
        discrepancy = "The title gives a nominal 214 mm diameter while the size field says 226 mm. This model uses the size field."
    elif sku == "2004":
        discrepancy = "The linked technical sheet identifies SKU 2003. This model uses the 2004 listing size."
    elif sku == "2403c":
        discrepancy = "The linked technical sheet identifies the white 2403W variant. This model uses the clear variant listing size."
    elif sku == "2402w":
        discrepancy = "The linked technical sheet is labelled 5.5 litre while the listing describes an 11 litre bucket. This model uses the listing size."
    colour = info.get("Colour", "")
    title_colour = title.lower()
    if "white" in title_colour and colour.strip().lower() == "clear":
        discrepancy += (" " if discrepancy else "") + "The title specifies white while the colour field says clear. The render follows the title."
    if "clear" in title_colour and colour.strip().lower() == "white":
        discrepancy += (" " if discrepancy else "") + "The title specifies clear while the colour field says white. The render follows the title."
    handle = "handle" in title.lower()
    from bs4 import BeautifulSoup
    folder = ROOT / "parts_source" / build_oomp_id(product_to_oomp(product))
    capture = folder / "source_systempak.html"
    photo = ""
    if capture.exists():
        tag = BeautifulSoup(capture.read_text(encoding="utf8"), "html.parser").select_one('meta[property="og:image"]')
        if tag:
            photo = tag.get("content", "")
    return {"photo": photo, "sku": sku, "title": title, "shape": product["source_shape"],
            "length": length, "width": width, "height": height, "basis": basis,
            "source_size": raw, "colour": colour, "handle": handle,
            "discrepancy": discrepancy, "source": product["url_source"], "technical_sheet": product.get("tech_sheet_url", ""),
            "model_note": "The body taper, wall thickness, lid seating and any handle use simplified estimates. The circular reference omits the tamper-evident tab." if product["source_shape"] == "round" else "The body taper, wall thickness, lid seating and tab use simplified estimates."}

def records(**kwargs):
    selector = kwargs.get("model_id")
    products = harvest_systempak(refresh=False)
    for product in products:
        record = product_to_oomp(product)
        part_id = build_oomp_id(record.copy())
        if selector and part_id != selector:
            continue
        if product["sku"] == "209":
            continue
        yield part_id, product, specification(product)

def source_model(spec, **kwargs):
    length = spec["length"]
    width = spec["width"]
    height = spec["height"]
    round_part = spec["shape"] == "round"
    # The entire model occupies the listed height. Feet and walls are estimates.
    cap = min(3, height * .12)
    wall = min(1.2, height * .06)
    body_height = height - cap * .7
    body_width = width - 2 * wall - 1.5
    body_length = length - 2 * wall - 1.5
    if round_part:
        handle_shape = ""
        if spec["handle"]:
            handle_shape = f'''module handle() {{
 radius={width*.50};
 z_top={body_height-5};
 for (angle=[0:8:172]) hull() {{
  for (a=[angle,angle+8]) {{
   translate([radius*cos(a), -radius*sin(a)-{wall}, z_top-{height*.22}*sin(a)])
    sphere(r={wall*.8},$fn=12);
  }}
 }}
}}
if (component=="handle" || component=="assembled") handle();
'''
        return f"""// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {{
 difference() {{
  union() {{
   cylinder(h={body_height}, d1={body_width*.85}, d2={body_width});
   translate([0,0,{body_height-3}]) cylinder(h=3, d={body_width});
   translate([0,0,{body_height-6}]) cylinder(h=2, d={width-.5});
  }}
  translate([0,0,{wall}]) cylinder(h={height}, d1={body_width*.85-2*wall}, d2={body_width-2*wall});
 }}
}}
module lid() {{
 translate([0,0,{height-cap}]) difference() {{
  cylinder(h={cap}, d={width});
  translate([0,0,-.01]) cylinder(h={cap*.65}, d={width-2*wall-1});
 }}
}}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
{handle_shape}
"""
    radius = min(width * .15, 13)
    shoulder = min(width * .06, 5.7)
    draft = min(width * .024, 2.1)
    collar = min(8.7, height * .22)
    body_height = height - 2
    return f"""// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {{
 systempak("body", {width}, {length-1}, {body_height}, {width}, {length}, {height}, {radius}, 0.85, {shoulder}, {draft}, {collar}, 12);
 systempak("lid", {width}, {length-1}, {body_height}, {width}, {length}, {height}, {radius}, 0.85, {shoulder}, {draft}, {collar}, 12);
}} else systempak(component, {width}, {length-1}, {body_height}, {width}, {length}, {height}, {radius}, 0.85, {shoulder}, {draft}, {collar}, 12);
"""

def generate(**kwargs):
    for part_id, product, spec in records(**kwargs):
        folder = ROOT / "parts" / part_id
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "systempak_model.scad").write_text(source_model(spec), encoding="utf8")
        if spec["shape"] != "round":
            shutil.copyfile(ROOT / "models/systempak_rectangle.scad", folder / "systempak_rectangle.scad")
        (folder / "systempak_model.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
        drawing = diagram(spec["title"], spec["length"], spec["width"], spec["height"], spec["shape"] == "round")
        drawing = drawing.replace("Closed overall dimensions · details and wall profiles are approximate",
                                  "Supplier stated size · details and wall profiles are approximate")
        (folder / "systempak_dimensions.svg").write_text(drawing, encoding="utf8")

def render_one(folder, spec, **kwargs):
    with TemporaryDirectory() as directory:
        temp = Path(directory)
        scad = folder / "systempak_model.scad"
        for component in ("body", "lid"):
            subprocess.run(["openscad.com", "--backend=Manifold", "-D", f'component="{component}"',
                            "-o", str(temp / f"{component}.stl"), str(scad)], check=True, capture_output=True)
        if spec["handle"]:
            subprocess.run(["openscad.com", "--backend=Manifold", "-D", 'component="handle"',
                            "-o", str(temp / "handle.stl"), str(scad)], check=True, capture_output=True)
        renderer = (ROOT / "models" / "render_pot.py").read_text(encoding="utf8")
        if spec["handle"]:
            renderer = renderer.replace('lid = load("lid")', 'lid = load("lid")\nhandle = load("handle")')
        renderer = renderer.replace("cam.data.ortho_scale = scale * 1.85", "cam.data.ortho_scale = max(scale * 2.8, h * 4.2)")
        colour = spec["colour"].lower()
        title = spec["title"].lower()
        is_white = "white" in title or ("clear" not in title and colour.strip() == "white")
        is_black = "black" in title or colour.strip() == "black"
        if is_black:
            renderer = renderer.replace('(0.96, 0.99, 0.99)', '(0.015, 0.018, 0.02)').replace('default_value = 0.93', 'default_value = 0.0')
            renderer = renderer.replace('lid = load("lid")', 'lid = load("lid")\nclear_lid, clear_shader = material("Clear lid", (0.96, 0.99, 0.99), 0.13)\nclear_shader.inputs["Transmission Weight"].default_value = 0.93\nlid.data.materials.clear()\nlid.data.materials.append(clear_lid)')
        elif is_white:
            renderer = renderer.replace('default_value = 0.93', 'default_value = 0.0')
        (temp / "render.py").write_text(renderer, encoding="utf8")
        subprocess.run(["blender", "-b", "--factory-startup", "--python-exit-code", "1",
                        "-P", str(temp / "render.py"), "--", str(temp)], check=True, stdout=subprocess.DEVNULL)
        for name in ("presentation.png", "assembled.png"):
            shutil.copyfile(temp / name, folder / ("systempak_" + name))

def publish(folder, spec, **kwargs):
    sku = spec["sku"]
    title = spec["title"]
    note = spec["model_note"]
    warning = "The handle is shown lowered and is an approximate shape.\n\n" if spec["handle"] else ""
    if spec["discrepancy"]:
        warning += spec["discrepancy"] + "\n\n"
    source = spec["source"]
    technical_sheet = spec["technical_sheet"]
    dimensions = f'{spec["length"]:g} × {spec["width"]:g} × {spec["height"]:g} mm'
    (folder / "README.md").write_text(
        f"# {title}\n\n![Open container and lid](systempak_presentation.png)\n\n"
        f"Supplier dimensions {dimensions} ({spec['basis']}).\n\n{note}\n\n{warning}"
        "![Dimensioned overview](systempak_dimensions.svg)\n\n"
        "[Editable OpenSCAD](systempak_model.scad) · [Parameters and source](systempak_model.json) · "
        "[Seated lid](systempak_assembled.png)\n\n"
        f"[Supplier listing]({source})" + (f" · [Technical sheet]({technical_sheet})" if technical_sheet else "") + (f" · [Supplier photo]({spec['photo']})" if spec["photo"] else "") + "\n\n"
        f"Regenerate with `python action_make_all.py --part {folder.name}`.\n", encoding="utf8")

def update_reference(**kwargs):
    selector = kwargs.get("model_id")
    reference_id = "packaging_takeaway_container_rectangle_100_ml_capacity_109_mm_width_86_mm_height_29_mm_depth_tamper_evident_systempak_209"
    if selector and selector != reference_id:
        return
    folder = ROOT / "parts" / reference_id
    drawing = diagram("100 ml rectangle · SKU 209", 109, 86, 29)
    (folder / "systempak_dimensions.svg").write_text(drawing, encoding="utf8")
    readme = folder / "README.md"
    if readme.exists():
        body = readme.read_text(encoding="utf8")
        marker = "## Dimensioned overview"
        if marker not in body:
            body += "\n" + marker + "\n\n![Dimensioned overview](systempak_dimensions.svg)\n"
            readme.write_text(body, encoding="utf8")


def main(**kwargs):
    skip_existing = kwargs.get("skip_existing", False)
    generate(**kwargs)
    update_reference(**kwargs)
    for part_id, product, spec in records(**kwargs):
        folder = ROOT / "parts" / part_id
        if not skip_existing or not (folder / "systempak_presentation.png").exists():
            render_one(folder, spec, **kwargs)
        publish(folder, spec, **kwargs)
        print(f"Built {part_id}", flush=True)

if __name__ == "__main__":
    import sys
    main(skip_existing="--resume" in sys.argv)
