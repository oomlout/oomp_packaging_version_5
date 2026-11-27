import copy

def main(**kwargs):
    kwargs["run_svg"] = kwargs.get("run_svg", True)
    kwargs["run_blender"] = kwargs.get("run_blender", True)
    kwargs["run_readme"] = kwargs.get("run_readme", True)
    run_oomp_populate = kwargs.get("run_oomp_populate", True)
    #run_oomp_populate = False
    kwargs["run_oomp_populate"] = run_oomp_populate

    run_oomp = kwargs.get("run_oomp", True)
    #run_oomp = False
    kwargs["run_oomp"] = run_oomp

    run_scad = kwargs.get("run_scad", True)
    #run_scad = False
    kwargs["run_scad"] = run_scad

    run_action = kwargs.get("run_action", True)
    #run_action = False
    kwargs["run_action"] = run_action

    generate_stl = kwargs.get("generate_stl", False)
    #generate_stl = True
    kwargs["generate_stl"] = generate_stl

    run(**kwargs)

def run(**kwargs):
    run_svg = kwargs.get("run_svg", False)
    run_blender = kwargs.get("run_blender", False)
    run_readme = kwargs.get("run_readme", False)

    if kwargs.get("run_oomp_populate", True):
        import working_oomp_populate
        working_oomp_populate.main(**kwargs)

    if kwargs.get("run_oomp", True):
        import working_oomp
        working_oomp.main(**kwargs)

    if kwargs.get("run_scad", True):        
        kwargs2 = copy.deepcopy(kwargs)
        if kwargs.get("generate_stl", False):
            kwargs2["typ"] = "all"
        import working_scad
        working_scad.main(**kwargs2)

    if kwargs.get("run_action", True):
        import working_action
        working_action.main(**kwargs)    

    if run_svg:
        import working_svg
        working_svg.main(**kwargs)
    if run_blender:
        import working_blender
        working_blender.main(**kwargs)
    if run_readme:
        import working_readme
        working_readme.main(**kwargs)
        import working_systempak_catalogue
        working_systempak_catalogue.main(**kwargs)
        if not kwargs.get("model_id"):
            import working_systempak_index
            working_systempak_index.main(**kwargs)
        import working_systempak_examples
        working_systempak_examples.main(**kwargs)
        if not kwargs.get("model_id"):
            import working_systempak_new_samples
            working_systempak_new_samples.main(**kwargs)




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Generate packaging parts using saved catalogue details.")
    parser.add_argument("--harvest", action="store_true", help="Refresh SystemPAK details and save the YAML catalogue.")
    args = parser.parse_args()
    main(harvest=args.harvest)
