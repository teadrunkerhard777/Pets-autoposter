"""Project-owned visual roles for cats and pets posts."""

from hashlib import sha256
from pathlib import Path

VISUAL_TYPES = {"NEWS", "SAFETY", "CARE", "WELFARE", "CAT_FACT"}
COVER_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "covers"
COVER_FILES = {
    "NEWS": ("news.png", "news_2.png"),
    "SAFETY": ("safety.png", "safety_2.png"),
    "CARE": ("care.png", "care_2.png"),
    "WELFARE": ("welfare.png", "welfare_2.png"),
    "CAT_FACT": ("cat_fact.png", "cat_fact_2.png"),
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


def cover_path_for(visual_type, item_key=""):
    """Return a stable project-owned cover variant for one item."""

    filenames = COVER_FILES.get(visual_type)
    if not filenames:
        return None

    identity = str(item_key or visual_type).encode("utf-8")
    variant_index = sha256(identity).digest()[0] % len(filenames)
    return COVER_DIRECTORY / filenames[variant_index]
