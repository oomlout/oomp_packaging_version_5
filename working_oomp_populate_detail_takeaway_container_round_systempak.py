"""OOMP entries for SystemPAK's round tamper-evident range."""

from working_systempak_harvest import product_to_oomp


def populate(*, products, **kwargs):
    return [product_to_oomp(product) for product in products if product["source_shape"] == "round"]
