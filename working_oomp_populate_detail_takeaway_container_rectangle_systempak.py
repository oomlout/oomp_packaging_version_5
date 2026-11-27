"""OOMP entries for SystemPAK rectangular and square containers.

Square products intentionally use the rectangle taxonomy.
"""

from pathlib import Path

from working_systempak_harvest import product_to_oomp


def populate(*, products, **kwargs):
    records = [product_to_oomp(product) for product in products if product["source_shape"] in {"rectangular", "square"}]
    root = Path(__file__).resolve().parent
    for record in records:
        profile = Path("models/systempak") / (record["taxonomy_15"] + ".json")
        if (root / profile).is_file():
            record["model_profile"] = profile.as_posix()
    return records
