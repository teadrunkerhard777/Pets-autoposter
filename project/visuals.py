"""Project-owned visual roles for cats and pets posts."""

VISUAL_TYPES = {"NEWS", "SAFETY", "CARE", "WELFARE", "CAT_FACT"}


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
