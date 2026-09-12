"""Relevance and editorial metadata for the pets channel."""

import re

from project.visuals import cover_path_for, visual_type_for


PET_KEYWORDS = (
    "cat", "cats", "kitten", "kittens", "feline", "dog", "dogs",
    "puppy", "puppies", "pet", "pets", "animal welfare", "adoption",
    "shelter", "rescue", "veterinary", "vet", "кошка", "кошки", "кошек", "кошкой", "кот", "котён",
    "собак", "щен", "питом", "приют", "животн", "ветеринар",
)
SPECIES_KEYWORDS = {
    "cats": ("cat", "cats", "kitten", "kittens", "feline", "кошка", "кошки", "кошек", "кошкой", "кот", "котён"),
    "dogs": ("dog", "dogs", "puppy", "puppies", "canine", "собак", "щен"),
    "small_pets": ("rabbit", "hamster", "guinea pig", "parrot", "bird", "рыбк", "кролик", "хомяк", "попуг"),
}
EVENT_CATEGORY_KEYWORDS = (
    ("urgent_safety", ("recall", "outbreak", "warning", "poison", "toxic", "отзыв", "вспышк", "предупрежд", "отрав", "токсич")),
    ("animal_welfare", ("rescue", "shelter", "adoption", "cruelty", "приют", "спас", "пристро", "жесток")),
    ("health", ("health", "disease", "veterinary", "vet", "здоровье", "заболев", "болезн", "инфекц", "диагност", "лечен", "ветеринар")),
    ("care", ("care", "nutrition", "behavior", "training", "grooming", "уход", "питани", "поведен", "дрессиров", "воспитани")),
)
EDITORIAL_SIGNAL_KEYWORDS = {
    "official": ("official", "confirmed", "announced", "официаль", "подтвержд"),
    "seasonal": ("summer", "winter", "holiday", "seasonal", "летн", "зимн", "праздник", "сезон"),
    "practical": ("how to", "tips", "guide", "checklist", "совет", "как ", "памятк"),
}
EVERGREEN_CONTENT_TYPES = {"cat_fact", "pet_care", "adoption_story", "breed"}
TRUSTED_PET_SOURCES = {
    "ASPCA News",
    "Blue Cross News",
    "Ветеринария и жизнь — Питомцы",
    "РосПриют",
    "РКФ",
}
MEDICAL_DISCLAIMER_KEYWORDS = (
    "emergency", "urgent", "poison", "toxic", "отрав", "токсич",
    "экстренн", "срочн",
)


def is_relevant(news_item):
    """Accept pet material and attach only channel-owned metadata."""

    text = _item_text(news_item)
    queue = news_item.get("content_queue") or "news"
    requested_type = news_item.get("content_type")
    is_evergreen = queue == "evergreen" and requested_type in EVERGREEN_CONTENT_TYPES
    species = _matches_by_name(text, SPECIES_KEYWORDS)
    primary_species = _matches_by_name(
        _item_text(news_item, ("title", "description")),
        SPECIES_KEYWORDS,
    )
    relevant = is_evergreen or bool(species) or (
        news_item.get("source") in TRUSTED_PET_SOURCES and _contains_any(text, PET_KEYWORDS)
    )
    category = f"evergreen_{requested_type}" if is_evergreen else _event_category(text) if relevant else None
    signals = _matches_by_name(text, EDITORIAL_SIGNAL_KEYWORDS) if relevant else []

    news_item["matched_topics"] = _unique([*species, category] if relevant else [])
    news_item["matched_species"] = species
    news_item["primary_species"] = primary_species or species
    news_item["editorial_signals"] = signals
    news_item["event_participants"] = []
    news_item["event_locations"] = []
    news_item["content_queue"] = queue
    news_item["content_type"] = requested_type if is_evergreen else "news"
    news_item["is_rumor"] = False
    news_item["needs_vet_disclaimer"] = relevant and _contains_any(text, MEDICAL_DISCLAIMER_KEYWORDS)
    news_item["event_category"] = category
    news_item["visual_type"] = visual_type_for(news_item) if relevant else None
    cover_path = cover_path_for(news_item["visual_type"])
    news_item["fallback_image_path"] = str(cover_path) if cover_path else None
    return relevant


def _item_text(news_item, keys=("title", "description", "article_text")):
    return " ".join(str(news_item.get(key, "")) for key in keys).casefold()


def _contains_any(text, keywords):
    return any(_contains_keyword(text, keyword) for keyword in keywords)


def _contains_keyword(text, keyword):
    if keyword.isascii():
        return re.search(rf"(?<!\w){re.escape(keyword)}(?!\w)", text) is not None
    return keyword in text


def _matches_by_name(text, groups):
    return [name for name, keywords in groups.items() if _contains_any(text, keywords)]


def _event_category(text):
    for category, keywords in EVENT_CATEGORY_KEYWORDS:
        if _contains_any(text, keywords):
            return category
    return "pet_news"


def _unique(values):
    return list(dict.fromkeys(value for value in values if value))
