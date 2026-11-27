import copy
import working_scad

def main(**kwargs):
    kwargs["run_oomp_populate"] = True

    kwargs["run_oomp"] = True

    kwargs["run_action"] = not kwargs.get("model_id")
    #kwargs["run_action"] = False

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
    with chdir(Path(__file__).resolve().parent):
        main(**vars(parser.parse_args()))
