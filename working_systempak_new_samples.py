"""Build two further SystemPAK sample illustrations from saved supplier dimensions."""
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import subprocess
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cairosvg
from working_systempak_examples import diagram

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "models" / "systempak_examples"
ROUND_SCAD = """
$fn=96;
module body() {
 difference() {
  union() {
   cylinder(h=39, d1=83, d2=93);
   translate([0,0,38]) cylinder(h=5, d=94);
  }
  translate([0,0,1]) cylinder(h=43, d1=81, d2=91);
 }
}
module lid() {
 translate([0,0,42]) difference() {
  cylinder(h=3, d=95);
  translate([0,0,-0.01]) cylinder(h=2.1, d=91.5);
 }
}
component="assembled";
if(component=="body" || component=="assembled") body();
if(component=="lid" || component=="assembled") lid();
"""
RECT_SCAD = """
use <profile.scad>
component="assembled";
systempak(component, 86, 108, 38, 86, 109, 40, 13, 0.85, 5.7, 2.1, 8.7, 12);
"""

def main(**kwargs):
    OUTPUT.mkdir(exist_ok=True)
    samples = []
    samples.append({"sku": "212", "title": "250 ml rectangle · SKU 212", "length": 109, "width": 86, "height": 40, "circular": False, "scad": RECT_SCAD})
    samples.append({"sku": "2009", "title": "180 ml round · SKU 2009", "length": 95, "width": 95, "height": 45, "circular": True, "scad": ROUND_SCAD})
    for sample in samples:
        sku = sample["sku"]
        (OUTPUT / f"sample_{sku}.scad").write_text(sample["scad"], encoding="utf8")
        if sku == "212":
            shutil.copyfile(ROOT / "models/systempak_rectangle.scad", OUTPUT / "profile.scad")
        svg = diagram(sample["title"], sample["length"], sample["width"], sample["height"], sample["circular"])
        (OUTPUT / f"sample_{sku}.svg").write_text(svg, encoding="utf8")
        with TemporaryDirectory() as directory:
            temp = Path(directory)
            shutil.copyfile(OUTPUT / f"sample_{sku}.scad", temp / "model.scad")
            if sku == "212":
                shutil.copyfile(OUTPUT / "profile.scad", temp / "profile.scad")
            for component in ("body", "lid"):
                subprocess.run(["openscad.com", "--backend=Manifold", "-D", f'component="{component}"', "-o", str(temp / f"{component}.stl"), str(temp / "model.scad")], check=True, capture_output=True)
            renderer = (ROOT / "models/render_pot.py").read_text(encoding="utf8")
            renderer = renderer.replace("cam.data.ortho_scale = scale * 1.85", "cam.data.ortho_scale = scale * 2.8")
            (temp / "render.py").write_text(renderer, encoding="utf8")
            subprocess.run(["blender", "-b", "--factory-startup", "--python-exit-code", "1", "-P", str(temp / "render.py"), "--", str(temp)], check=True, stdout=subprocess.DEVNULL)
            shutil.copyfile(temp / "presentation.png", OUTPUT / f"sample_{sku}.png")
    sheet = Image.new("RGB", (1500, 1160), "#f2f4f3")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("arial.ttf", 26)
    for index, sample in enumerate(samples):
        y = index * 580
        draw.text((25, y + 15), sample["title"], font=font, fill="#173b40")
        picture = Image.open(OUTPUT / f'sample_{sample["sku"]}.png').convert("RGB")
        picture.thumbnail((730, 510), Image.Resampling.LANCZOS)
        sheet.paste(picture, (15, y + 55))
        drawing = Image.open(BytesIO(cairosvg.svg2png(url=str(OUTPUT / f'sample_{sample["sku"]}.svg'), output_width=720))).convert("RGB")
        sheet.paste(drawing, (760, y + 55))
    sheet.save(OUTPUT / "contact_sheet_new_sizes.jpg", quality=90, optimize=True)

if __name__ == "__main__":
    main()
