"""Generate two SystemPAK presentation examples from saved dimensions."""
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
RECT = "packaging_takeaway_container_rectangle_100_ml_capacity_109_mm_width_86_mm_height_29_mm_depth_tamper_evident_systempak_209"
ROUND = "packaging_takeaway_container_circle_120_ml_capacity_69_mm_diameter_52_mm_depth_tamper_evident_systempak_2005"
ROUND_SCAD = """
$fn=96;
module body() {
 difference() {
  union() {
   cylinder(h=46, d1=60, d2=67);
   translate([0,0,45]) cylinder(h=5, d=68);
  }
  translate([0,0,1]) cylinder(h=50, d1=58, d2=65);
 }
}
module lid() {
 translate([0,0,49]) difference() {
  union() {
   cylinder(h=3, d=69);
   cylinder(h=0.8, d=69);
  }
  translate([0,0,-0.01]) cylinder(h=2.1, d=65.5);
 }
}
component="assembled";
if(component=="body" || component=="assembled") body();
if(component=="lid" || component=="assembled") lid();
"""

def diagram(title, length, width, height, circular=False):
    from html import escape
    # SVG y increases toward the floor. Inset both ends of the base for nesting.
    base_y = 385
    centre_x = 200
    scale = min(216 / length, 148 / width, 100 / height)
    half_rim = length * scale / 2
    lid_y = base_y - height * scale
    if circular:
        half_foot = half_rim * 60 / 69
        plan = f'<circle cx="200" cy="153" r="{half_rim}" class="shape"/><circle cx="200" cy="153" r="{half_rim-5}" class="inner"/>'
        top_label = f"Ø {width} mm"
        width_label = ""
    else:
        half_foot = half_rim * 0.83
        plan_height = width * scale
        plan = (f'<rect x="{centre_x-half_rim}" y="{153-plan_height/2}" width="{2*half_rim}" height="{plan_height}" rx="20" class="shape"/>'
                f'<rect x="{centre_x-half_rim+5}" y="{158-plan_height/2}" width="{2*half_rim-10}" height="{plan_height-10}" rx="15" class="inner"/>')
        top_label = f"{length} mm"
        width_label = f"{width} mm"
    wall_top_y = lid_y + 6
    side = (f'<path class="shape" id="body-side" d="M{centre_x-half_rim+2} {wall_top_y} '
            f'L{centre_x+half_rim-2} {wall_top_y} L{centre_x+half_foot} {base_y} L{centre_x-half_foot} {base_y} Z"/>'
            f'<rect x="{centre_x-half_rim}" y="{lid_y}" width="{2*half_rim}" height="6" rx="2" class="shape"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="620" height="440" viewBox="0 0 620 440">
<title>{escape(title)} dimensioned overview</title><style>text{{font:16px Arial;fill:#243b40}} .title{{font-size:22px;font-weight:bold}} .shape{{fill:#d6e9e9;stroke:#23555b;stroke-width:2}} .inner{{fill:none;stroke:#7fa6a8}} .dim{{fill:none;stroke:#42686d}} .small{{font-size:13px}}</style>
<rect width="620" height="440" fill="white"/><text x="24" y="34" class="title">{escape(title)}</text>
<text x="24" y="65" class="small">PLAN</text>{plan}<path class="dim" d="M{centre_x-half_rim} 237v8 M{centre_x+half_rim} 237v8 M{centre_x-half_rim} 241h{2*half_rim}"/><text x="200" y="263" text-anchor="middle">{top_label}</text>
<text x="335" y="177">{width_label}</text>
<text x="24" y="337" class="small">SIDE</text>{side}<path class="dim" d="M325 {lid_y}h10 M325 {base_y}h10 M330 {lid_y}V{base_y}"/><text x="343" y="{(lid_y+base_y)/2}">{height} mm</text>
<text x="24" y="421" class="small">Closed overall dimensions · details and wall profiles are approximate</text></svg>'''

def main(**kwargs):
    selector = kwargs.get("model_id")
    if selector and selector not in (ROUND, RECT):
        return
    output = ROOT / "models" / "systempak_examples"
    output.mkdir(parents=True, exist_ok=True)
    (output / "round_2005.scad").write_text(ROUND_SCAD, encoding="utf8")
    (output / "round_2005.svg").write_text(diagram("120 ml round · SKU 2005",69,69,52,True),encoding="utf8")
    (output / "rectangle_209.svg").write_text(diagram("100 ml rectangle · SKU 209",109,86,29),encoding="utf8")
    if not selector or selector == ROUND:
        with TemporaryDirectory() as tmp:
            temp=Path(tmp)
            scad=temp/"round.scad"
            scad.write_text(ROUND_SCAD,encoding="utf8")
            for component in ("body","lid"):
                subprocess.run(["openscad.com","--backend=Manifold","-D",f'component="{component}"',"-o",str(temp/f"{component}.stl"),str(scad)],check=True,capture_output=True)
            renderer=temp/"render_pot.py"
            renderer.write_text((ROOT/"models/render_pot.py").read_text(encoding="utf8").replace("cam.data.ortho_scale = scale * 1.85", "cam.data.ortho_scale = scale * 2.8"),encoding="utf8")
            subprocess.run(["blender","-b","--factory-startup","--python-exit-code","1","-P",str(renderer),"--",str(temp)],check=True,stdout=subprocess.DEVNULL)
            shutil.copy2(temp/"presentation.png",output/"round_2005.png")
    make_sheet(output=output)

def make_sheet(**kwargs):
    from io import BytesIO
    from PIL import Image, ImageDraw, ImageFont
    import cairosvg
    output=kwargs["output"]
    sheet=Image.new("RGB",(1500,1160),"#f2f4f3")
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype("arial.ttf",26)
    items=[("100 ml rectangle · SKU 209",ROOT/"parts"/RECT/"presentation.png",output/"rectangle_209.svg"),
           ("120 ml round · SKU 2005",output/"round_2005.png",output/"round_2005.svg")]
    for row,(title,render,svg) in enumerate(items):
        y=row*580
        draw.text((25,y+15),title,font=font,fill="#173b40")
        image=Image.open(render).convert("RGB")
        image.thumbnail((730,510),Image.Resampling.LANCZOS)
        sheet.paste(image,(15,y+55))
        drawing=Image.open(BytesIO(cairosvg.svg2png(url=str(svg),output_width=720))).convert("RGB")
        sheet.paste(drawing,(760,y+55))
    sheet.save(output/"contact_sheet.jpg",quality=90,optimize=True)

if __name__ == "__main__":
    main()
