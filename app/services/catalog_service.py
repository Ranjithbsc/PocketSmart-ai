
import json
from pathlib import Path
from urllib.parse import quote_plus


CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "catalog.json"


def load_catalog() -> list[dict]:
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def platform_search_url(platform: str, query: str) -> str:
    q = quote_plus(query)
    urls = {
        "Amazon": f"https://www.amazon.in/s?k={q}",
        "Flipkart": f"https://www.flipkart.com/search?q={q}",
        "IKEA": f"https://www.ikea.com/in/en/search/?q={q}",
        "Swiggy": f"https://www.swiggy.com/search?query={q}",
        "Zomato": f"https://www.zomato.com/search?query={q}",
        "OYO": f"https://www.oyorooms.com/search?location={q}",
    }
    return urls.get(platform, f"https://www.google.com/search?q={q}")


def select_catalog(domain: str, max_price: float, limit: int = 30) -> list[dict]:
    items = [x for x in load_catalog() if x.get("domain") == domain]
    affordable = [x for x in items if float(x.get("price", 0)) <= max_price]
    chosen = affordable or items
    result = []
    for item in chosen[:limit]:
        copy = dict(item)
        copy["search_url"] = platform_search_url(item["platform"], item["search_term"])
        result.append(copy)
    return result


def search_catalog_item(item_name: str) -> dict | None:
    normalized = item_name.lower()
    for item in load_catalog():
        if item["name"].lower() == normalized:
            copy = dict(item)
            copy["search_url"] = platform_search_url(item["platform"], item["search_term"])
            return copy
    return None
