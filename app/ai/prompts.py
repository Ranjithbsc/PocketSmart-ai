
import json


BASE_RULES = """
You are PocketSmart AI, a practical budget planning assistant.
Return ONLY valid JSON. Do not wrap JSON in Markdown.
All monetary values must be in Indian Rupees (INR).
Never invent real-time prices, stock status, ratings, or product availability.
Use the supplied catalog only for concrete catalog items.
Keep the total recommended spend at or below the user's budget.
Be explicit when an item is an estimate rather than a verified live price.
"""


def home_prompt(payload: dict, catalog: list[dict]) -> str:
    return f"""
{BASE_RULES}
Plan a home interior purchase for this user:
{json.dumps(payload, ensure_ascii=False)}

Catalog:
{json.dumps(catalog, ensure_ascii=False)}

Return this JSON shape:
{{
  "total_budget": number,
  "estimated_total": number,
  "remaining_budget": number,
  "budget_breakdown": [
    {{"category": string, "allocation": number, "reason": string}}
  ],
  "recommendations": [
    {{
      "category": string,
      "item": string,
      "description": string,
      "estimated_price": number,
      "quantity": integer,
      "platform": string,
      "search_url": string,
      "why": string
    }}
  ],
  "additional_suggestions": [string]
}}
"""


def party_prompt(payload: dict, catalog: list[dict]) -> str:
    return f"""
{BASE_RULES}
Create a party budget plan:
{json.dumps(payload, ensure_ascii=False)}

Catalog:
{json.dumps(catalog, ensure_ascii=False)}

Return this JSON shape:
{{
  "total_budget": number,
  "estimated_total": number,
  "remaining_budget": number,
  "budget_breakdown": [
    {{"category": string, "allocation": number, "reason": string}}
  ],
  "recommendations": [
    {{
      "category": string,
      "item": string,
      "description": string,
      "estimated_price": number,
      "quantity": integer,
      "platform": string,
      "search_url": string,
      "why": string
    }}
  ],
  "venue_suggestions": [
    {{"name": string, "type": string, "estimated_cost": number, "search_url": string}}
  ],
  "additional_suggestions": [string]
}}
"""


def jewelry_prompt(payload: dict, catalog: list[dict], image_attached: bool) -> str:
    image_note = (
        "An outfit image is attached. Analyze only visible colors, patterns and style; "
        "do not identify the person."
        if image_attached
        else "No outfit image is attached."
    )
    return f"""
{BASE_RULES}
Create a jewelry recommendation plan:
{json.dumps(payload, ensure_ascii=False)}
{image_note}

Catalog:
{json.dumps(catalog, ensure_ascii=False)}

Return this JSON shape:
{{
  "total_budget": number,
  "estimated_total": number,
  "remaining_budget": number,
  "outfit_analysis": {{
    "dominant_colors": [string],
    "style": string,
    "matching_notes": string
  }},
  "recommendations": [
    {{
      "category": string,
      "item": string,
      "description": string,
      "estimated_price": number,
      "quantity": integer,
      "platform": string,
      "search_url": string,
      "why": string
    }}
  ],
  "styling_tips": [string]
}}
"""
