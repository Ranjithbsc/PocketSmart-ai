
import json
import re
from typing import Any

from ..ai.gemini_client import GeminiClient
from ..ai.prompts import home_prompt, jewelry_prompt, party_prompt
from .catalog_service import load_catalog, platform_search_url


def _money(value: Any) -> float:
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return 0.0


def _normalize_result(result: dict, budget: float) -> dict:
    result = result if isinstance(result, dict) else {}
    result["total_budget"] = _money(budget)
    recs = result.get("recommendations", [])
    if not isinstance(recs, list):
        recs = []

    normalized = []
    running = 0.0
    for rec in recs:
        if not isinstance(rec, dict):
            continue
        price = _money(rec.get("estimated_price", 0))
        try:
            qty = max(1, int(rec.get("quantity", 1) or 1))
        except (TypeError, ValueError):
            qty = 1
        if running + price * qty > budget:
            qty = max(1, int((budget - running) // max(price, 1))) if price else 1
        if price and running + price * qty > budget:
            continue
        rec["estimated_price"] = price
        rec["quantity"] = qty
        rec["platform"] = rec.get("platform") or "Amazon"
        rec["search_url"] = rec.get("search_url") or platform_search_url(
            rec["platform"], rec.get("item", "product")
        )
        normalized.append(rec)
        running += price * qty

    result["recommendations"] = normalized
    result["estimated_total"] = round(
        sum(_money(x.get("estimated_price")) * max(1, int(x.get("quantity", 1))) for x in normalized),
        2,
    )
    result["remaining_budget"] = round(max(0, budget - result["estimated_total"]), 2)
    return result


def _fallback_home(payload: dict, catalog: list[dict]) -> dict:
    budget = payload["total_budget"]
    cats = [
        ("Lighting", 0.15, "lights"),
        ("Ceiling Fans", 0.20, "fans"),
        ("Furniture", 0.45, "furniture"),
        ("Dining", 0.20, "dining"),
    ]
    recs = []
    remaining = budget
    requested = {
        "lights": payload.get("num_lights", 0),
        "fans": payload.get("num_fans", 0),
        "furniture": payload.get("num_furniture", 0),
        "dining": payload.get("num_dining_tables", 0),
    }
    for category, share, key in cats:
        matches = [x for x in catalog if x["domain"] == "home" and x["category"] == key]
        qty = requested[key] or 1
        if not matches:
            continue
        item = matches[0]
        max_qty = max(1, int((budget * share) // item["price"]))
        qty = min(qty, max_qty)
        total = item["price"] * qty
        if total <= remaining:
            recs.append({
                "category": category,
                "item": item["name"],
                "description": item["description"],
                "estimated_price": item["price"],
                "quantity": qty,
                "platform": item["platform"],
                "search_url": platform_search_url(item["platform"], item["search_term"]),
                "why": f"Fits the fallback allocation for {category.lower()}.",
            })
            remaining -= total
    return _normalize_result({
        "total_budget": budget,
        "budget_breakdown": [
            {"category": c, "allocation": round(budget * s, 2), "reason": "Fallback allocation."}
            for c, s, _ in cats
        ],
        "recommendations": recs,
        "additional_suggestions": [
            "Prioritize essential fixtures before decorative items.",
            "Compare the linked search results before purchasing because prices can change.",
        ],
    }, budget)


def _fallback_party(payload: dict, catalog: list[dict]) -> dict:
    budget = payload["total_budget"]
    shares = [("Venue", 0.20, "venue"), ("Catering", 0.45, "catering"),
              ("Decoration", 0.20, "decoration"), ("Entertainment", 0.15, "entertainment")]
    recs = []
    remaining = budget
    guests = payload["num_guests"]
    for category, share, key in shares:
        matches = [x for x in catalog if x["domain"] == "party" and x["category"] == key]
        if not matches:
            continue
        item = matches[0]
        qty = 1
        if key == "catering":
            qty = guests
        total = item["price"] * qty
        if total > budget * share and key == "catering":
            qty = max(1, int((budget * share) // item["price"]))
            total = item["price"] * qty
        if total <= remaining:
            recs.append({
                "category": category,
                "item": item["name"],
                "description": item["description"],
                "estimated_price": item["price"],
                "quantity": qty,
                "platform": item["platform"],
                "search_url": platform_search_url(item["platform"], item["search_term"]),
                "why": f"Fallback option for {category.lower()}.",
            })
            remaining -= total
    return _normalize_result({
        "total_budget": budget,
        "budget_breakdown": [
            {"category": c, "allocation": round(budget * s, 2), "reason": "Fallback allocation."}
            for c, s, _ in shares
        ],
        "recommendations": recs,
        "venue_suggestions": [],
        "additional_suggestions": [
            "Get a per-head catering quote before confirming the venue.",
            "Keep a contingency reserve for last-minute event costs.",
        ],
    }, budget)


def _fallback_jewelry(payload: dict, catalog: list[dict], image_attached: bool) -> dict:
    budget = payload["total_budget"]
    matches = [x for x in catalog if x["domain"] == "jewelry" and x["price"] <= budget]
    recs = []
    for item in matches[:4]:
        recs.append({
            "category": item["category"],
            "item": item["name"],
            "description": item["description"],
            "estimated_price": item["price"],
            "quantity": 1,
            "platform": item["platform"],
            "search_url": platform_search_url(item["platform"], item["search_term"]),
            "why": f"Matches the {payload['style']} style preference and stays within budget.",
        })
    return _normalize_result({
        "total_budget": budget,
        "outfit_analysis": {
            "dominant_colors": ["Not analyzed"] if not image_attached else ["AI unavailable"],
            "style": payload["style"],
            "matching_notes": "Fallback mode: outfit image was not analyzed by Gemini.",
        },
        "recommendations": recs,
        "styling_tips": [
            "Match metal tone with the outfit's overall color temperature.",
            "For a statement necklace, keep earrings simpler.",
        ],
    }, budget)


def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Gemini did not return a JSON object")
    return json.loads(cleaned[start:end + 1])


class RecommendationService:
    def __init__(self, ai_client: GeminiClient | None = None):
        self.ai = ai_client or GeminiClient()

    def _ask(self, prompt: str, image_bytes: bytes | None = None, mime_type: str | None = None) -> dict | None:
        try:
            raw = self.ai.generate(prompt, image_bytes=image_bytes, mime_type=mime_type)
            if not raw:
                return None
            return _extract_json(raw)
        except Exception:
            return None

    def home(self, payload: dict) -> dict:
        catalog = [x for x in load_catalog() if x["domain"] == "home"]
        result = self._ask(home_prompt(payload, catalog))
        return _normalize_result(result, payload["total_budget"]) if result else _fallback_home(payload, catalog)

    def party(self, payload: dict) -> dict:
        catalog = [x for x in load_catalog() if x["domain"] == "party"]
        result = self._ask(party_prompt(payload, catalog))
        return _normalize_result(result, payload["total_budget"]) if result else _fallback_party(payload, catalog)

    def jewelry(self, payload: dict, image_bytes: bytes | None = None, mime_type: str | None = None) -> dict:
        catalog = [x for x in load_catalog() if x["domain"] == "jewelry"]
        result = self._ask(
            jewelry_prompt(payload, catalog, bool(image_bytes)),
            image_bytes=image_bytes,
            mime_type=mime_type,
        )
        return _normalize_result(result, payload["total_budget"]) if result else _fallback_jewelry(
            payload, catalog, bool(image_bytes)
        )
