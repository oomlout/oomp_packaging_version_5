"""Build small coloured catalogue models from the editable OpenSCAD source."""

import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

import numpy as np
import trimesh
import yaml

ROOT = Path(__file__).resolve().parent
# Convert millimetres with Z up to glTF metres with Y up.
CAD_TO_GLTF = np.array([[.001, 0, 0, 0], [0, 0, .001, 0], [0, -.001, 0, 0], [0, 0, 0, 1]])


def records(**kwargs):
    model_id = kwargs.get("model_id")
    parts_dir = Path(kwargs.get("parts_dir", ROOT / "parts"))
    folders = [parts_dir / model_id] if model_id else sorted(parts_dir.glob("packaging_dolly_*"))
    for folder in folders:
        path = folder / "working.yaml"
        if path.is_file():
            part = yaml.safe_load(path.read_text(encoding="utf-8"))
            if part.get("taxonomy_2") == "dolly":
                yield folder, part


def palette(style):
    colours = {"mounts": "#9bA2A6", "wheels": "#292b2f"}
    if style == "simple":
        colours.update(deck="#ca9876", trim="#28252a")
    elif style == "bale_arm_crate_single":
        colours.update(deck="#edaf16", trim="#e39d12", wheels="#c8c6b5")
    else:
        colours.update(deck="#34373b", trim="#c93032", wheels="#c3c4b9")
    return colours


def build_dollies(**kwargs):
    openscad = kwargs.get("openscad") or shutil.which("openscad.com") or shutil.which("openscad")
    for folder, part in records(**kwargs):
        if not openscad:
            raise RuntimeError("OpenSCAD is required to build the dolly models")
        build(folder, part, openscad=openscad)


def build(folder, part, **kwargs):
    openscad = kwargs["openscad"]
    dims = part["model_dimensions"]
    style = part["taxonomy_3"]
    colours = palette(style)
    parameters = dict(style=style, seat_depth=0, seat_length=0, seat_width=0)
    parameters.update(dims)
    parameters.update(deck_color=colours["deck"], trim_color=colours["trim"],
                      wheel_color=colours["wheels"], mount_color=colours["mounts"])
    header = [f"{name} = {json.dumps(value)};" for name, value in parameters.items()]
    template = (ROOT / "models/dolly.scad").read_text(encoding="utf-8")
    output = folder / "three_d_model"
    output.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=output) as temp:
        stage = Path(temp)
        source = stage / "working.scad"
        source.write_text("\n".join(header) + "\n\n" + template, encoding="utf-8")
        scene = trimesh.Scene()
        bounds = []
        for name, colour in colours.items():
            off = stage / f"{name}.off"
            subprocess.run([openscad, "--backend=Manifold", "--hardwarnings", "-D",
                            f'component="{name}"', "-o", str(off), str(source)], check=True)
            mesh = trimesh.load_mesh(off)
            bounds.extend(mesh.bounds)
            # glTF material factors are linear, while OpenSCAD hex colours are sRGB.
            srgb = np.frombuffer(bytes.fromhex(colour[1:]), dtype=np.uint8) / 255
            linear = np.where(srgb <= .04045, srgb/12.92, ((srgb+.055)/1.055)**2.4)
            material = trimesh.visual.material.PBRMaterial(
                name=name, baseColorFactor=[*linear, 1.0], metallicFactor=0.50 if name=="mounts" else 0,
                roughnessFactor=0.58)
            mesh.visual = trimesh.visual.TextureVisuals(material=material)
            mesh.apply_transform(CAD_TO_GLTF)
            scene.add_geometry(mesh, geom_name=name, node_name=name)
        expected = [dims["length"], dims["width"], dims["height"]]
        if not np.allclose(np.ptp(bounds, axis=0), expected, atol=0.02) or abs(np.min(bounds, axis=0)[2]) > .02:
            raise ValueError(f"{folder.name}: model bounds disagree with {expected} mm at floor Z=0")
        scene.export(stage / "working.glb")
        for filename in ("working.scad", "working.glb"):
            (stage / filename).replace(output / filename)
