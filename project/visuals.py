"""Project-owned visual roles for cats and pets posts."""

from pathlib import Path

VISUAL_TYPES = {"NEWS", "SAFETY", "CARE", "WELFARE", "CAT_FACT"}
COVER_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "covers"
COVER_FILES = {
    "NEWS": "news.png",
    "SAFETY": "safety.png",
    "CARE": "care.png",
    "WELFARE": "welfare.png",
    "CAT_FACT": "cat_fact.png",
}


def visual_type_for(news_item):
    category = news_item.get("event_category")
    if category == "urgent_safety":
        return "SAFETY"
    if category == "animal_welfare" or category == "evergreen_adoption_story":
        return "WELFARE"
    if category in {"health", "care", "evergreen_pet_care"}:
        return "CARE"
    if category == "evergreen_cat_fact" or "cats" in news_item.get("matched_species", []):
        return "CAT_FACT"
    return "NEWS"


def cover_path_for(visual_type):
    """Return the project-owned fallback cover for a visual role."""

    filename = COVER_FILES.get(visual_type)
    return COVER_DIRECTORY / filename if filename else None
