"""Regenerate a browsable SystemPAK catalogue and contact sheets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from working_systempak_catalogue import ROOT, records

def main(**kwargs):
    columns = kwargs.get("columns", 4)
    rows = kwargs.get("rows", 5)
    font = ImageFont.truetype("arial.ttf", 15)
    entries = list(records())
    reference = "packaging_takeaway_container_rectangle_100_ml_capacity_109_mm_width_86_mm_height_29_mm_depth_tamper_evident_systempak_209"
    entries.insert(0, (reference, {}, {"sku": "209", "title": "100ml Rectangular Tamper Evident Containers and Lids", "length": 109, "width": 86, "height": 29}))
    index = ROOT / "models/systempak_catalogue.md"
    lines = ["# SystemPAK catalogue", "", "Dimensions and construction details are recorded on each part page.", "",
             "| SKU | Product | Dimensions in mm | Part |",
             "| --- | --- | --- | --- |"]
    for part_id, product, spec in entries:
        folder = ROOT / "parts" / part_id
        dimensions = f'{spec["length"]:g} × {spec["width"]:g} × {spec["height"]:g}'
        lines.append(f'| {spec["sku"]} | {spec["title"]} | {dimensions} | [Part](../parts/{part_id}/README.md) |')
    index.write_text("\n".join(lines)+"\n",encoding="utf8")
    readme = ROOT / "README.md"
    original = readme.read_text(encoding="utf8") if readme.exists() else "# OOMP packaging\n"
    start_marker = "<!-- systempak catalogue -->"
    end_marker = "<!-- end systempak catalogue -->"
    section = start_marker + "\n## SystemPAK containers\n\n[Browse all SystemPAK parts](models/systempak_catalogue.md) and the [contact sheets](models/systempak_contact_sheets/).\n" + end_marker
    if start_marker in original and end_marker in original:
        before, remainder = original.split(start_marker, 1)
        original = before + section + remainder.split(end_marker, 1)[1]
    else:
        original = original.rstrip() + "\n\n" + section + "\n"
    readme.write_text(original, encoding="utf8")
    output = ROOT / "models/systempak_contact_sheets"
    output.mkdir(parents=True, exist_ok=True)
    page_size = columns * rows
    for start in range(0, len(entries), page_size):
        group = entries[start:start+page_size]
        sheet = Image.new("RGB", (columns*310, rows*255), "white")
        draw = ImageDraw.Draw(sheet)
        for index_number, (part_id, product, spec) in enumerate(group):
            x = index_number % columns * 310
            y = index_number // columns * 255
            filename = "presentation.png" if spec["sku"] == "209" else "systempak_presentation.png"
            image = Image.open(ROOT / "parts" / part_id / filename).convert("RGB")
            image.thumbnail((300, 220), Image.Resampling.LANCZOS)
            sheet.paste(image, (x+5, y+5))
            draw.text((x+8, y+229), f'{spec["sku"]} · {spec["title"][:28]}', font=font, fill="#153b40")
        sheet.save(output / f"systempak_{start//page_size+1:02d}.jpg", quality=88, optimize=True)

if __name__ == "__main__":
    main()
