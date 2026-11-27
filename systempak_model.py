"""Build registered SystemPAK reference models using the published OOMP ID."""

import json
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import trimesh
import yaml

ROOT = Path(__file__).resolve().parent
FIELDS = (
    "width",
    "length",
    "height",
    "lid_width",
    "lid_length",
    "closed_height",
    "corner_radius",
    "wall",
    "shoulder",
    "draft",
    "collar_height",
    "tab_width",
)


def build(folder, profile, export=True):
    settings = json.loads((ROOT / profile).read_text(encoding="utf-8"))
    family = settings["family"]
    if family != "systempak_rectangle":
        raise ValueError(f"Unsupported profile {family}")
    with TemporaryDirectory(dir=folder) as tmp:
        stage = Path(tmp)
        shutil.copyfile(ROOT / "models" / (family + ".scad"), stage / "profile.scad")
        args = ", ".join(str(float(settings[key])) for key in FIELDS)
        for part in ("body", "lid"):
            source = stage / (part + ".scad")
            source.write_text(f'use <profile.scad>\nsystempak("{part}", {args});\n', encoding="utf-8")
            if export:
                exe = shutil.which("openscad.com") or shutil.which("openscad")
                if not exe:
                    raise RuntimeError("OpenSCAD with the Manifold backend is required")
                target = source.with_suffix(".stl")
                subprocess.run(
                    [
                        exe,
                        "--backend=Manifold",
                        "--hardwarnings",
                        "--export-format=binstl",
                        "-o",
                        str(target),
                        str(source),
                    ],
                    check=True,
                    capture_output=True,
                )
                mesh = trimesh.load_mesh(target)
                dims = (
                    [settings[k] for k in ("width", "length", "height")]
                    if part == "body"
                    else [settings[k] for k in ("lid_width", "lid_length")]
                )
                if (
                    not mesh.is_volume
                    or len(mesh.split()) != 1
                    or not np.allclose(mesh.extents[: len(dims)], dims, atol=0.025)
                ):
                    raise ValueError(f"{part}: expected one closed solid {dims}, got {mesh.extents}")
        (stage / "assembled.scad").write_text("include <body.scad>\ninclude <lid.scad>\n", encoding="utf-8")
        (stage / "model.json").write_text(
            json.dumps(
                dict(
                    settings,
                    id=folder.name,
                    units="mm",
                    axes="X short, Y long, Z up; floor at Z=0",
                    body_file="body.stl",
                    lid_file="lid.stl",
                ),
                indent=2,
            )
            + "\n"
        )
        (stage / "README.md").write_text(
            f"# SystemPAK {folder.name.rsplit('_',1)[-1]} reference model\n\n"
            f"![Open pot and lifted lid](presentation.png)\n\n"
            f"Open pot {settings['length']} × {settings['width']} × {settings['height']} mm. "
            f"Closed envelope {settings['lid_length']} × {settings['lid_width']} × {settings['closed_height']} mm. "
            f"{settings['basis']}\n\n"
            "[3D model with removable lid](systempak.glb) · [Seated lid render](assembled.png) · [Open pot](body.stl) · [Removable lid](lid.stl) · [Assembled OpenSCAD view](assembled.scad) · "
            "[Parameters and provenance](model.json)\n\n"
            f"[SystemPAK listing]({settings['source']}) · [Technical sheet]({settings['technical_sheet']}) · "
            f"[Reference photo]({settings['photo']})\n\n"
            f"From the packaging project root run `python action_make_all.py --part {folder.name}`. "
            f"The same registered model runs during the full make-all. Edit `{profile}` to change the profile.\n",
            encoding="utf-8",
        )
        if export:
            body, lid = (trimesh.load_mesh(stage / f"{n}.stl") for n in ("body", "lid"))
            if abs(lid.bounds[1, 2] - settings["closed_height"]) >= 0.025:
                raise ValueError("Assembled lid height differs from the registered closed envelope")
            overlap = trimesh.boolean.intersection([body, lid], engine="manifold")
            if overlap.volume > 0.01:
                raise ValueError(f"Lid intersects body by {overlap.volume:.3f} mm3")
            blender = shutil.which("blender")
            if not blender:
                raise RuntimeError("Blender is required for the packaging presentation")
            subprocess.run(
                [
                    blender,
                    "-b",
                    "--factory-startup",
                    "--python-exit-code",
                    "1",
                    "-P",
                    str(ROOT / "models" / "render_pot.py"),
                    "--",
                    str(stage),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
        for path in stage.iterdir():
            path.replace(folder / path.name)


def build_registered(selector=None, export=True):
    folders = ROOT / "parts"
    records = [folders / selector / "working.yaml"] if selector else sorted(folders.glob("*/working.yaml"))
    for file in records:
        record = yaml.safe_load(file.read_text(encoding="utf-8"))
        if record.get("model_profile"):
            build(file.parent, record["model_profile"], export)
        elif selector and record.get("taxonomy_2") != "dolly":
            raise ValueError(f"No packaging model registered for {selector}")
