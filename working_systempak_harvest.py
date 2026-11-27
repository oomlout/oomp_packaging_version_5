"""Harvest SystemPAK tamper-evident details into OOMP source folders.

Default runs load the saved YAML catalogue. Use ``--harvest`` to refresh it.
Product responses are retained separately as ``source_systempak.html``.
"""

from __future__ import annotations

import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import requests
import yaml
from bs4 import BeautifulSoup

from oomp_populate_helper import build_oomp_id


CATEGORY_URLS = {
    "round": "https://systempak.net/product-category/tamper-evident-containers/round/",
    "rectangular": "https://systempak.net/product-category/tamper-evident-containers/rectangular/",
    "square": "https://systempak.net/product-category/tamper-evident-containers/square/",
}
# This sheet is indexed in SystemPAK's public archive but is not linked from
# the current product page.
TECH_SHEET_OVERRIDES = {
    "https://systempak.net/product/2000ml-rectangular-tamper-evident-containers-and-lids/": "https://systempak.net/wp-content/uploads/2024/03/TDS-2108-2000ML.pdf",
}
CACHE_PATH = Path("source_file/systempak_tamper_evident_catalogue.yaml")
LEGACY_CACHE_PATH = CACHE_PATH.with_suffix(".json")
# SystemPAK varies its response by user-agent; use the same ordinary browser
# headers used for the browser-assisted catalogue check.
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.8",
}


def _request(session: requests.Session, url: str) -> str:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def _product_urls_from_category(session: requests.Session, category_url: str) -> list[str]:
    """Follow pagination links advertised by the supplier category page."""
    pending, visited, product_urls = [category_url], set(), set()
    while pending:
        url = pending.pop(0)
        if url in visited:
            continue
        visited.add(url)
        soup = BeautifulSoup(_request(session, url), "html.parser")
        for product in soup.select("ul.products li.product"):
            link = product.select_one('a[href*="/product/"]')
            if link and link.get("href"):
                product_urls.add(link["href"])
        for link in soup.select(".woocommerce-pagination a.page-numbers[href]"):
            if link["href"] not in visited:
                pending.append(link["href"])
    return sorted(product_urls)


def _clean(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


def _additional_information(soup: BeautifulSoup) -> dict[str, str]:
    table = soup.select_one("table.woocommerce-product-attributes")
    if table is None:
        return {}
    details = {}
    for row in table.select("tr"):
        key, value = row.select_one("th"), row.select_one("td")
        if key and value:
            details[_clean(key.get_text(" ", strip=True))] = _clean(value.get_text(" ", strip=True))
    return details


def _tech_sheet_url(soup: BeautifulSoup) -> str:
    """Return the product-specific SystemPAK technical-sheet PDF, if present."""
    link = soup.select_one("a.download-tech-sheet[href]")
    return link["href"] if link else ""


def _first_match(pattern: str, value: str) -> str:
    match = re.search(pattern, value, flags=re.IGNORECASE)
    return match.group(1) if match else ""


def _detail(details: dict[str, str], key: str) -> str:
    """Supplier attributes vary between ``size`` and ``Size``."""
    return next((value for name, value in details.items() if name.casefold() == key.casefold()), "")


def _capacity_ml(value: str) -> str:
    millilitres = _first_match(r"(\d+(?:\.\d+)?)\s*ml", value)
    if millilitres:
        return millilitres.replace(".", "_")
    litres = _first_match(r"(\d+(?:\.\d+)?)\s*(?:litre|liter|l)\b", value)
    if not litres:
        return ""
    amount = float(litres) * 1000
    return str(int(amount) if amount.is_integer() else amount).replace(".", "_")


def _dimensions(details: dict[str, str], title: str, source_shape: str) -> tuple[str, str, str]:
    size = _detail(details, "size")
    if source_shape == "round":
        diameter = _first_match(r"(\d+(?:\.\d+)?)\s*mm\s+diameter", title)
        if not diameter:
            diameter = _first_match(r"(?:D|Diameter)\s*(\d+(?:\.\d+)?)\s*mm", size)
        height = _first_match(r"(?:H|Height)\s*(\d+(?:\.\d+)?)\s*mm", size)
        return diameter.replace(".", "_"), height.replace(".", "_"), ""
    length = _first_match(r"L\s*(\d+(?:\.\d+)?)\s*m{1,2}\b", size)
    width = _first_match(r"W\s*(\d+(?:\.\d+)?)\s*mm", size)
    height = _first_match(r"H\s*(\d+(?:\.\d+)?)\s*mm", size)
    # SystemPAK L × W × H becomes OOMP width × height × depth, matching the
    # existing takeaway-container rectangle naming convention.
    if not all((length, width, height)):
        plain_dimensions = re.search(r"(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*mm", size, re.I)
        if plain_dimensions:
            length, width, height = plain_dimensions.groups()
    return length.replace(".", "_"), width.replace(".", "_"), height.replace(".", "_")


def _product(session: requests.Session, url: str, source_shape: str) -> dict[str, Any]:
    html = _request(session, url)
    soup = BeautifulSoup(html, "html.parser")
    title_node = soup.select_one("h1.product_title")
    sku_node = soup.select_one(".sku-val, .sku")
    return {
        "source_shape": source_shape,
        "url_source": url,
        "title": _clean(title_node.get_text(" ", strip=True)) if title_node else url.rstrip("/").split("/")[-1],
        "sku": _clean(sku_node.get_text(" ", strip=True)).lower() if sku_node else "",
        "additional_information": _additional_information(soup),
        "tech_sheet_url": TECH_SHEET_OVERRIDES.get(url, _tech_sheet_url(soup)),
        "html": html,
    }


def _fetch_product(item: tuple[str, str]) -> dict[str, Any]:
    """Fetch one supplier page in a dedicated session for safe parallel reads."""
    source_shape, url = item
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)
    return _product(session, url, source_shape)


def _save_catalogue(products: list[dict[str, Any]]) -> None:
    """Keep the YAML readable by storing raw HTML in the source folders."""
    details = []
    for product in products:
        if "html" in product:
            folder = Path("parts_source") / build_oomp_id(product_to_oomp(product))
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "source_systempak.html").write_text(product["html"], encoding="utf-8")
        details.append({key: value for key, value in product.items() if key != "html"})
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = CACHE_PATH.with_suffix(".yaml.tmp")
    temporary.write_text(
        yaml.safe_dump(details, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    temporary.replace(CACHE_PATH)


def harvest_systempak(*, refresh: bool = False) -> list[dict[str, Any]]:
    """Load local details by default; contact SystemPAK only on explicit refresh."""
    if not refresh:
        if CACHE_PATH.exists():
            products = yaml.safe_load(CACHE_PATH.read_text(encoding="utf-8"))
            if not isinstance(products, list) or not products:
                raise ValueError(f"Expected a non-empty product list in {CACHE_PATH}")
            return products
        if not LEGACY_CACHE_PATH.exists():
            raise FileNotFoundError(
                f"No saved SystemPAK catalogue at {CACHE_PATH}. "
                "Run python working_systempak_harvest.py --harvest to create it."
            )
        products = json.loads(LEGACY_CACHE_PATH.read_text(encoding="utf-8"))
        # Older cache files may predate the SystemPAK ``sku-val`` selector.
        for product in products:
            if not product.get("sku"):
                soup = BeautifulSoup(product["html"], "html.parser")
                sku_node = soup.select_one(".sku-val, .sku")
                product["sku"] = _clean(sku_node.get_text(" ", strip=True)).lower() if sku_node else ""
            if not product.get("tech_sheet_url"):
                product["tech_sheet_url"] = TECH_SHEET_OVERRIDES.get(
                    product["url_source"], _tech_sheet_url(BeautifulSoup(product["html"], "html.parser"))
                )
        _save_catalogue(products)
        return products
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)
    product_requests, seen_urls = [], set()
    for source_shape, category_url in CATEGORY_URLS.items():
        for url in _product_urls_from_category(session, category_url):
            if url not in seen_urls:
                seen_urls.add(url)
                product_requests.append((source_shape, url))
    # Product pages are independent read-only requests. Keeping this modestly
    # parallel makes the refresh practical without placing a large burst on the
    # supplier site.
    with ThreadPoolExecutor(max_workers=16) as executor:
        products = list(executor.map(_fetch_product, product_requests))
    products.sort(key=lambda item: (item["source_shape"], item["title"], item["url_source"]))
    if not products:
        raise ValueError("SystemPAK returned no products; the saved catalogue was not replaced.")
    _save_catalogue(products)
    return products


def product_to_oomp(product: dict[str, Any]) -> dict[str, Any]:
    details, source_shape = product["additional_information"], product["source_shape"]
    capacity = _capacity_ml(_detail(details, "capacity")) or _capacity_ml(product["title"])
    if not capacity:
        raise ValueError(f"No capacity found for {product['url_source']}")
    sku = product["sku"] or product["url_source"].rstrip("/").split("/")[-1]
    option: dict[str, Any] = {
        "taxonomy_1": "packaging", "taxonomy_2": "takeaway_container",
        "taxonomy_3": "circle" if source_shape == "round" else "rectangle",
        "taxonomy_4": f"{capacity}_ml_capacity",
        "taxonomy_14": "systempak", "taxonomy_15": sku, "url_source": product["url_source"],
        "source_title": product["title"], "source_shape": source_shape,
        "systempak_additional_information": details,
        "url_technical_sheet": product.get("tech_sheet_url", ""),
    }
    first, second, third = _dimensions(details, product["title"], source_shape)
    if source_shape == "round":
        if first:
            option["taxonomy_5"] = f"{first}_mm_diameter"
        if second:
            option["taxonomy_6"] = f"{second}_mm_depth"
        option["taxonomy_7"] = "tamper_evident"
    else:
        if all((first, second, third)):
            option.update({
                "taxonomy_5": f"{first}_mm_width", "taxonomy_6": f"{second}_mm_height",
                "taxonomy_7": f"{third}_mm_depth",
            })
        option["taxonomy_8"] = "tamper_evident"
    return option


def write_oomp_artifacts(
    extras: list[dict[str, Any]], products: list[dict[str, Any]], *, download: bool = False
) -> None:
    """Save raw source and every Additional information field with its OOMP."""
    by_url = {product["url_source"]: product for product in products}
    technical_sheets: list[tuple[str, Path]] = []
    captured_sheets: list[tuple[dict[str, Any], Path]] = []
    for extra in extras:
        product = by_url.get(extra.get("url_source"))
        if product is None:
            continue
        folder = Path("parts_source") / build_oomp_id(extra)
        folder.mkdir(parents=True, exist_ok=True)
        if "html" in product:
            (folder / "source_systempak.html").write_text(product["html"], encoding="utf-8")
        (folder / "additional_information.yaml").write_text(
            yaml.safe_dump(product["additional_information"], allow_unicode=True, sort_keys=False), encoding="utf-8"
        )
        tech_sheet_url = product.get("tech_sheet_url", "")
        if tech_sheet_url:
            if download:
                technical_sheets.append((tech_sheet_url, folder / "technical_sheet.pdf"))
        else:
            captured_sheets.append((product, folder / "technical_sheet.pdf"))
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(lambda item: _download_technical_sheet(*item), technical_sheets))
    for product, destination in captured_sheets:
        _create_captured_technical_sheet(product, destination)


def _download_technical_sheet(url: str, destination: Path) -> None:
    """Download a technical sheet only when it is absent or not a valid PDF."""
    if destination.exists():
        with destination.open("rb") as existing:
            if existing.read(5) == b"%PDF-":
                return
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=30)
    response.raise_for_status()
    if not response.content.startswith(b"%PDF-"):
        raise ValueError(f"Technical sheet is not a PDF: {url}")
    destination.write_bytes(response.content)


def _create_captured_technical_sheet(product: dict[str, Any], destination: Path) -> None:
    """Create a transparent local data sheet when SystemPAK publishes no PDF."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import Paragraph, Table, TableStyle

    styles = getSampleStyleSheet()
    page_width, page_height = A4
    margin, width = 18 * mm, page_width - 36 * mm
    canvas = Canvas(str(destination), pagesize=A4)
    y = page_height - margin

    def draw_paragraph(text: str, style_name: str, gap: float) -> None:
        nonlocal y
        paragraph = Paragraph(text, styles[style_name])
        _, height = paragraph.wrap(width, y - margin)
        y -= height
        paragraph.drawOn(canvas, margin, y)
        y -= gap

    draw_paragraph("SystemPAK product technical data", "Title", 4 * mm)
    draw_paragraph(product["title"], "Heading2", 3 * mm)
    draw_paragraph(
        "Local OOMP capture. SystemPAK does not publish a dedicated technical-sheet PDF on this product page; the values below are transcribed from its Additional information section.",
        "BodyText",
        4 * mm,
    )
    rows = [[Paragraph("Field", styles["BodyText"]), Paragraph("Supplier value", styles["BodyText"])]]
    rows.extend([
        [Paragraph(str(key), styles["BodyText"]), Paragraph(str(value), styles["BodyText"])]
        for key, value in product["additional_information"].items()
    ])
    table = Table(rows, colWidths=(45 * mm, 130 * mm), repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B7C9D6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    _, height = table.wrap(width, y - margin)
    y -= height
    table.drawOn(canvas, margin, y)
    y -= 4 * mm
    draw_paragraph(f"Source: {product['url_source']}", "BodyText", 0)
    canvas.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harvest", action="store_true", help="Refresh the saved YAML from SystemPAK.")
    args = parser.parse_args()
    products = harvest_systempak(refresh=args.harvest)
    action = "Harvested and saved" if args.harvest else "Loaded"
    print(f"{action} {len(products)} SystemPAK products: {CACHE_PATH}")
