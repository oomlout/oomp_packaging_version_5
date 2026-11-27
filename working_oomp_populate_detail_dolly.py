"""Saved supplier dimensions in millimetres. Each entry describes one dolly."""


def populate(**kwargs):
    dollies = []
    dollies.append({
        "taxonomy_3": "simple", "taxonomy_4": "590_x_290_mm",
        "title": "Wooden platform dolly", "supplier": "Metatell",
        "url_source": "https://www.ebay.co.uk/itm/355741479607",
        "supplier_reference": "eBay 355741479607", "material": "MDF with foam grip pads",
        "model_dimensions": {"length": 590, "width": 290, "height": 75, "deck": 18, "wheel": 42},
        "wheel_basis": "estimated", "wheel_layout": "Four castors",
        "listing_note": "Approximate platform dimensions. Sold as a pair. Seller lists a maximum load of 200 kg.",
        "model_note": "One platform with an integral carry slot and four foam pads. Wheel diameter, pad and slot sizes, and castor positions are estimates.",
    })
    dollies.append({
        "taxonomy_3": "bale_arm_crate_single", "taxonomy_4": "600_x_400_mm",
        "title": "Single bale-arm crate dolly", "supplier": "Plastic Box Sales",
        "url_source": "https://plasticboxsales.co.uk/product/plastic-dolly-600x400-single-or-400x300-boxes-and-crates/",
        "supplier_reference": "u60.40 dolly", "material": "HDPE",
        "model_dimensions": {"length": 610, "width": 410, "height": 170, "deck": 30, "wheel": 100,
                             "seat_length": 603, "seat_width": 405, "seat_depth": 23},
        "wheel_basis": "listed", "wheel_layout": "Four swivel castors",
        "listing_note": "Fits 600 × 400 or 400 × 300 mm crates. Listed unit weight 4 kg. Sold in packs of three.",
        "model_note": "Yellow example with a central opening and a raised retaining rim. Opening shape, deck thickness, and castor placement are approximate.",
    })
    dollies.append({
        "taxonomy_3": "bale_arm_crate_double", "taxonomy_4": "800_x_600_mm",
        "title": "Double bale-arm crate dolly", "supplier": "Plastic Box Sales",
        "url_source": "https://plasticboxsales.co.uk/product/800x600-plastic-double-dolly/",
        "supplier_reference": "u800.600 dolly-1", "material": "Polypropylene",
        "model_dimensions": {"length": 798, "width": 598, "height": 171, "deck": 42, "wheel": 100},
        "wheel_basis": "listed", "wheel_layout": "Four nylon wheels. The description specifies two fixed, one swivel and one braked swivel. The specifications table says four swivel.",
        "listing_note": "Carries two stacks of 600 × 400 mm crates or four stacks of 400 × 300 mm crates. Listed unit weight 9.7 kg.",
        "model_note": "Black deck with two openings and red retainers. Deck thickness, openings, clips, and castor positions are approximate. The model simplifies the wheel mounts and omits brake hardware.",
    })
    for dolly in dollies:
        dolly["taxonomy_1"] = "packaging"
        dolly["taxonomy_2"] = "dolly"
    return dollies
