# OOMP packaging

<!-- dolly catalogue -->
## Dollies

| Part | External size | Views |
| --- | --- | --- |
| [Double bale-arm crate dolly](parts/packaging_dolly_bale_arm_crate_double_800_x_600_mm/README.md) | 798 × 598 × 171 mm | [Drawing](parts/packaging_dolly_bale_arm_crate_double_800_x_600_mm/working.svg) · [Render](parts/packaging_dolly_bale_arm_crate_double_800_x_600_mm/three_d_model/render.png) |
| [Single bale-arm crate dolly](parts/packaging_dolly_bale_arm_crate_single_600_x_400_mm/README.md) | 610 × 410 × 170 mm | [Drawing](parts/packaging_dolly_bale_arm_crate_single_600_x_400_mm/working.svg) · [Render](parts/packaging_dolly_bale_arm_crate_single_600_x_400_mm/three_d_model/render.png) |
| [Wooden platform dolly](parts/packaging_dolly_simple_590_x_290_mm/README.md) | 590 × 290 × 75 mm | [Drawing](parts/packaging_dolly_simple_590_x_290_mm/working.svg) · [Render](parts/packaging_dolly_simple_590_x_290_mm/three_d_model/render.png) |

### Regeneration

Edit the [dolly declarations](working_oomp_populate_detail_dolly.py) for dimensions and supplier details, and the [shared OpenSCAD template](models/dolly.scad) for geometry.
Run `python action_make_all.py --part <canonical_id>` for one dolly or `python action_make_all.py` for the catalogue. Each part page includes its exact command.
Use the project's OOMP/OOBB Python environment with NumPy, trimesh, PyYAML and Shapely 2, plus OpenSCAD with the Manifold backend and Blender on PATH.
<!-- end dolly catalogue -->

<!-- systempak catalogue -->
## SystemPAK containers

[Browse all SystemPAK parts](models/systempak_catalogue.md) and the [contact sheets](models/systempak_contact_sheets/).
<!-- end systempak catalogue -->
