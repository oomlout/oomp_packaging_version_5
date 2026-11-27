
"""Populate packaging OOMP source records by product family."""

from oomp_populate_helper import build_oomp_id, write_extras


def main(**kwargs):
    selector = kwargs.get("model_id")
    refresh_systempak = kwargs.get("harvest", kwargs.get("refresh_systempak", False))
    extras = []

    from working_oomp_populate_detail_bag_grip_seal import populate as populate_bags
    from working_oomp_populate_detail_tin_hinged_lid import populate as populate_tins
    from working_oomp_populate_detail_tote import populate as populate_totes
    from working_oomp_populate_detail_dolly import populate as populate_dollies

    extras.extend(populate_bags(**kwargs))
    extras.extend(populate_tins(**kwargs))
    extras.extend(populate_totes(**kwargs))
    extras.extend(populate_dollies(**kwargs))

    # Reuse the saved YAML unless harvesting is explicitly requested.
    from working_systempak_harvest import harvest_systempak, write_oomp_artifacts
    from working_oomp_populate_detail_takeaway_container_round_systempak import populate as populate_systempak_round
    from working_oomp_populate_detail_takeaway_container_rectangle_systempak import populate as populate_systempak_rectangle

    products = harvest_systempak(refresh=refresh_systempak)
    extras.extend(populate_systempak_round(products=products, **kwargs))
    extras.extend(populate_systempak_rectangle(products=products, **kwargs))

    import working_oomp_populate_extra_detail
    working_oomp_populate_extra_detail.main(extras=extras)

    if selector:
        extras = [part for part in extras if build_oomp_id(part.copy()) == selector
                  and (part.get("model_profile") or part.get("taxonomy_2") == "dolly" or part.get("taxonomy_14") == "systempak")]
        if not extras:
            raise ValueError(f"No registered model for {selector}")
    write_extras(extras)
    write_oomp_artifacts(extras, products, download=refresh_systempak)
    return extras


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harvest", action="store_true", help="Refresh SystemPAK details and save the YAML catalogue.")
    args = parser.parse_args()
    main(harvest=args.harvest)
