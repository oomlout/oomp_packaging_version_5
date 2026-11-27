def main(**kwargs):
    legacy_actions = kwargs.get("legacy_actions", False)
    kwargs["run_svg"] = kwargs.get("run_svg", True)
    kwargs["run_blender"] = kwargs.get("run_blender", True)
    kwargs["run_readme"] = kwargs.get("run_readme", True)
    kwargs["run_oomp_populate"] = True

    kwargs["run_oomp"] = True

    kwargs["run_action"] = legacy_actions and not kwargs.get("model_id")

    kwargs["run_scad"] = True

    kwargs["generate_stl"] = True

    import working
    working.run(**kwargs)

if __name__ == '__main__':
    import argparse
    from contextlib import chdir
    from pathlib import Path
    parser = argparse.ArgumentParser(description="Generate packaging catalogue or one registered model")
    parser.add_argument("--part", dest="model_id", help="Canonical packaging ID for a scoped CAD and render build")
    parser.add_argument("--legacy-actions", action="store_true", help="Also run legacy Roboclick AI and Corel actions on a full build")
    with chdir(Path(__file__).resolve().parent):
        main(**vars(parser.parse_args()))
