# OOMP packaging project conventions

Design each output so a maintainer can regenerate it with `python action_make_all.py` using the saved inputs and installed tools. Put the recipe in the repository. If an output needs an illustration or a supplier measurement, keep the approved asset or measurement as an input so the build can reuse it without an AI session.

## Where changes belong

1. Define packaging families in `working_oomp_populate_detail_<family>.py`, with a `populate(**kwargs)` routine that returns the entries. Register the family in `working_oomp_populate.py`. This stage uses the shared OOMP ID and writing helpers to produce `parts_source/<id>/working.yaml`.
2. Use `working_oomp.py` to load those records, apply per-part `parts/<id>/working_manual.yaml` overrides, and prepare the part data for downstream work. Put corrections that apply across a family back in its declarations or saved source data.
3. Put each kind of output in `working_<function>.py`. For example, `working_scad.py` handles CAD. Wire the stage into `working.py` and enable it through the thin `action_make_all.py` entry point. Keep full and part-scoped builds on the same implementation where both apply.

## Readable Python

For a hand-maintained list of dictionaries, initialize a descriptively named empty list and write one explicit `.append(...)` per entry on subsequent lines. For routines with options, accept `**kwargs` and read each configurable value into a named local with its default at the top. Forward options with `**kwargs` when calling the next stage. For example, a packaging size table could read as follows.

```python
def get_bag_sizes(**kwargs):
    thickness_micron = kwargs.get("thickness_micron", 100)

    sizes = []
    sizes.append({"width_mm": 115, "height_mm": 170, "thickness_micron": thickness_micron})
    sizes.append({"width_mm": 150, "height_mm": 200, "thickness_micron": thickness_micron})
    return sizes
```

## Regenerating outputs

Keep supplier refreshes explicit. Packaging already saves the SystemPAK catalogue at `source_file/systempak_tamper_evident_catalogue.yaml`. Ordinary population reads that snapshot. To verify a new output, rebuild a representative part from saved inputs, check the result, and rerun to confirm it can be reproduced. For a registered packaging CAD model the scoped command is `python action_make_all.py --part <canonical_id>`.

The existing full packaging build calls `working_action.py`, which invokes Roboclick in AI mode. Account for that legacy step when verifying unattended regeneration. New outputs must build from their saved inputs without requiring AI.

## Examples in sibling checkouts

- [Tool catalogue build notes](../oomp_tool_version_5/BUILD.md) trace editable declarations and saved references through to generated part files.
- [Panel-mount stage runner](../oomp_electronic_panel_mount_version_5/working.py) shows explicit defaults and forwarding options to individual stages.
- [Bolt catalogue population](../oomp_hardware_bolt_version_5/working_oomp_populate.py) collects separate family generators and uses shared OOMP identity helpers.
