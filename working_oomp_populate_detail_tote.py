"""Hand-maintained tote and crate entries."""


def populate(**kwargs):
    pharmacy_external_volume_l = 600 * 400 * 310 / 1_000_000

    return [
        {
            "taxonomy_1": "packaging", "taxonomy_2": "tote",
            "taxonomy_3": "bale_arm_crate",
        },
        {
            "taxonomy_1": "packaging", "taxonomy_2": "tote",
            "taxonomy_3": "stacking_nesting_crate", "taxonomy_4": "ventilated",
            "taxonomy_5": "600_mm_length", "taxonomy_6": "400_mm_width",
            "taxonomy_7": "199_mm_height", "taxonomy_8": "35_l_capacity",
            "taxonomy_14": "totebox", "taxonomy_15": "sn641902",
            "url_source": "https://www.totebox.co.uk/products/35l-heavy-duty-stacking-nesting-crate-ventilated-600x400x199mm",
        },
        {
            "taxonomy_1": "packaging", "taxonomy_2": "tote",
            "taxonomy_3": "pharmacy_style", "taxonomy_4": "600_mm_length",
            "taxonomy_5": "400_mm_width", "taxonomy_6": "310_mm_height",
            "taxonomy_7": "74_4_l_external_volume",
            "external_volume_l": pharmacy_external_volume_l,
            "capacity_note": "Calculated from external dimensions; usable internal capacity is unknown.",
        },
    ]
