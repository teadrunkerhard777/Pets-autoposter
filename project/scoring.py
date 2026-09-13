"""Editorial scoring for relevant cats and pets stories."""


CATEGORY_SCORES = {
    "positive_story": 9, "urgent_safety": 10, "animal_welfare": 7, "health": 6, "care": 5,
    "pet_news": 4, "evergreen_cat_fact": 5, "evergreen_pet_care": 5,
    "evergreen_adoption_story": 6, "evergreen_breed": 4,
}
SIGNAL_SCORES = {"official": 2, "seasonal": 2, "practical": 2, "positive": 3}
SPECIES_SCORES = {"cats": 2, "dogs": 1, "small_pets": 1, "other_animals": 1}
CONFIRMATION_BONUSES = {1: 0, 2: 1}


def calculate_score(news_item, now=None):
    """Rank already relevant material; never decide relevance here."""

    score = CATEGORY_SCORES.get(news_item.get("event_category"), 0)
    score += sum(SPECIES_SCORES.get(species, 0) for species in news_item.get("matched_species", []))
    score += sum(SIGNAL_SCORES.get(signal, 0) for signal in news_item.get("editorial_signals", []))
    if news_item.get("needs_vet_disclaimer"):
        score += 1
    category = news_item.get("event_category")
    if category == "urgent_safety":
        news_item["editorial_priority"] = "breaking"
    elif category in {"positive_story", "animal_welfare", "health"}:
        news_item["editorial_priority"] = "major_story"
    elif news_item.get("content_queue") == "evergreen":
        news_item["editorial_priority"] = "scheduled"
    else:
        news_item["editorial_priority"] = "standard"
    sources = news_item.get("confirmed_sources") or [news_item.get("source")]
    news_item["confirmed_sources"] = list(dict.fromkeys(filter(None, sources)))
    news_item["score_before_confirmation"] = max(0, score)
    news_item["confirmation_bonus"] = CONFIRMATION_BONUSES.get(
        len(news_item["confirmed_sources"]),
        2,
    )
    return max(0, score) + news_item["confirmation_bonus"]
