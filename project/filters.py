"""Relevance and editorial metadata for the pets channel."""

import re

from project.visuals import cover_path_for, visual_type_for


PET_KEYWORDS = (
    "cat", "cats", "kitten", "kittens", "feline", "dog", "dogs",
    "puppy", "puppies", "pet", "pets", "animal welfare", "adoption",
    "shelter", "rescue", "veterinary", "vet", "кошка", "кошки", "кошек", "кошкой", "кот", "кота", "коту", "котом", "коте", "коты", "котов", "котён", "котят",
    "собак", "щен", "пёс", "пес", "пса", "псу", "псом", "псе", "псы", "псов",
    "песик", "питом", "приют", "животн", "ветеринар",
    "лиса", "лисы", "лисён", "волк", "еж", "ёж", "енот", "выдр", "нерп",
    "тюлен", "пингвин", "медвед", "лошад", "ослик", "белк", "заяц", "сова", "совы", "сову", "совой",
)
SPECIES_KEYWORDS = {
    "cats": ("cat", "cats", "kitten", "kittens", "feline", "кошка", "кошки", "кошек", "кошкой", "кот", "кота", "коту", "котом", "коте", "коты", "котов", "котён", "котят", "мейн-кун", "мейн кун"),
    "dogs": (
        "dog", "dogs", "puppy", "puppies", "canine", "собак", "щен", "пёс",
        "пес", "пса", "псу", "псом", "псе", "псы", "псов", "песик",
    ),
    "small_pets": ("rabbit", "hamster", "guinea pig", "parrot", "bird", "рыбк", "кролик", "хомяк", "попуг"),
    "other_animals": (
        "fox", "wolf", "hedgehog", "raccoon", "otter", "seal", "penguin",
        "horse", "donkey", "elephant", "dolphin", "whale", "panda", "tiger",
        "lion", "deer", "beaver", "walrus", "monkey", "лиса", "лисы", "лисён", "волк", "еж", "ёж",
        "енот", "выдр", "нерп", "тюлен", "пингвин", "медвед", "лошад",
        "ослик", "белк", "заяц", "сова", "совы", "сову", "совой", "слон",
        "дельфин", "кит", "панд", "тигр", "льв", "лев", "олен", "косул",
        "бобр", "морж", "обезьян", "кабан", "журавл", "аист", "лебед",
    ),
}
EVENT_CATEGORY_KEYWORDS = (
    ("positive_story", ("спас", "обрёл дом", "обрела дом", "обрели дом", "нашёл дом", "нашла дом", "нашли дом", "новая семья", "подруж", "воссоедини", "счастлив", "добрая история", "трогательн")),
    ("urgent_safety", ("recall", "outbreak", "warning", "poison", "toxic", "отзыв", "вспышк", "предупрежд", "отрав", "токсич")),
    ("animal_welfare", ("rescue", "shelter", "adoption", "cruelty", "приют", "спас", "пристро", "жесток")),
    ("health", ("health", "disease", "veterinary", "vet", "здоровье", "заболев", "болезн", "инфекц", "диагност", "лечен", "ветеринар")),
    ("care", ("care", "nutrition", "behavior", "training", "grooming", "уход", "питани", "поведен", "дрессиров", "воспитани")),
)
EDITORIAL_SIGNAL_KEYWORDS = {
    "official": ("official", "confirmed", "announced", "официаль", "подтвержд"),
    "seasonal": ("summer", "winter", "holiday", "seasonal", "летн", "зимн", "праздник", "сезон"),
    "practical": ("how to", "tips", "guide", "checklist", "совет", "как ", "памятк"),
    "positive": ("спас", "обрёл дом", "обрела дом", "нашёл дом", "нашла дом", "нашли дом", "подруж", "счастлив", "трогательн", "забавн", "милый", "милое", "необычн"),
}
EVERGREEN_CONTENT_TYPES = {"cat_fact", "pet_care", "adoption_story", "breed"}
TRUSTED_PET_SOURCES = {
    "ASPCA News",
    "Blue Cross News",
    "Ветеринария и жизнь — Питомцы",
    "РосПриют",
    "РКФ",
    "Хорошие новости про животных",
    "Faunora",
}
CURATED_POSITIVE_SOURCES = {
    "Хорошие новости про животных",
    "Щенячий Ангел — Фото дня",
}
BODY_LED_CORE_SOURCES = {"Щенячий Ангел — Фото дня"}
STRICT_POSITIVE_SOURCES = {
    "Faunora",
    "Питомцы Mail",
    "РосПриют",
    "Кошаки форева — Кошачьи новости",
    "Бумеранг добра — Истории о животных",
}
POSITIVE_STORY_KEYWORDS = (
    "спас", "помог", "обрёл дом", "обрела дом", "обрели дом", "нашёл дом",
    "нашла дом", "нашли дом", "новая семья", "пристро", "усынов", "взяли домой",
    "подруж", "воссоедини", "вернул", "счастлив", "трогательн", "добрая история",
    "забавн", "милый", "милое", "необычн", "необыкнов", "удивительн", "играет",
    "дружба", "чемпионат", "соревнован", "исследование", "ученые выяснили",
    "учёные выяснили", "рекорд",
)
EDITORIAL_MISMATCH_KEYWORDS = (
    "чиновник", "министр", "министра", "министром", "министры", "ведомств",
    "законопроект", "конференц", "совещан",
    "глава города", "глава района", "администрация города", "полиция", "мчс",
    "112", "форум", "рынок", "маркировк", "предупред", "отпуг", "хищник",
    "военн", "боев", "фронт", "запорож", "спецоперац",
    "загрязнен", "загрязнён", "засух", "обмелен", "соленост", "солёност",
    "массовая гибель", "массовой гибели", "экологическая катастроф",
    "подарки от", "доставка подарков", "благотворительная акция", "благотворительной акции",
    "учебно-кинологичес",
    "ветеринар предупред", "ветврач предупред",
    "болезн", "инфекц", "бешенств", "погиб", "убил", "истяз", "отстрел",
    "пострадав", "травм", "тяжёлые раны", "тяжелые раны", "его раны", "её раны",
    "ее раны", "их раны", "раненый", "раненая", "раненые", "ранено", "ранение",
    "ранения", "воспал", "голодн", "напал", "атаковал",
    "опасн", "отрав", "перевозки выросли",
)
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
    headline_species = _matches_by_name(
        _item_text(news_item, ("title",)),
        SPECIES_KEYWORDS,
    )
    relevant = is_evergreen or bool(species) or (
        news_item.get("source") in TRUSTED_PET_SOURCES and _contains_any(text, PET_KEYWORDS)
    )
    source = news_item.get("source")
    if relevant and source in STRICT_POSITIVE_SOURCES:
        relevant = (
            bool(headline_species)
            and _contains_any(text, POSITIVE_STORY_KEYWORDS)
            and not _contains_any(text, EDITORIAL_MISMATCH_KEYWORDS)
        )
    elif relevant and source in CURATED_POSITIVE_SOURCES:
        relevant = (
            (bool(species) or _contains_any(text, PET_KEYWORDS))
            and not _contains_any(text, EDITORIAL_MISMATCH_KEYWORDS)
        )
    category = f"evergreen_{requested_type}" if is_evergreen else _event_category(text) if relevant else None
    signals = _matches_by_name(text, EDITORIAL_SIGNAL_KEYWORDS) if relevant else []

    news_item["matched_topics"] = _unique([*species, category] if relevant else [])
    news_item["matched_species"] = species
    news_item["primary_species"] = primary_species or species
    news_item["headline_species"] = headline_species
    news_item["channel_species"] = (
        headline_species
        or (primary_species if source in BODY_LED_CORE_SOURCES else [])
    )
    news_item["editorial_signals"] = signals
    news_item["event_participants"] = []
    news_item["event_locations"] = []
    news_item["content_queue"] = queue
    news_item["content_type"] = requested_type if is_evergreen else "news"
    news_item["is_rumor"] = False
    news_item["needs_vet_disclaimer"] = relevant and _contains_any(text, MEDICAL_DISCLAIMER_KEYWORDS)
    news_item["event_category"] = category
    news_item["visual_type"] = visual_type_for(news_item) if relevant else None
    cover_identity = news_item.get("url") or news_item.get("title") or ""
    cover_path = cover_path_for(news_item["visual_type"], cover_identity)
    news_item["fallback_image_path"] = str(cover_path) if cover_path else None
    return relevant


def _item_text(news_item, keys=("title", "description", "article_text")):
    return " ".join(str(news_item.get(key, "")) for key in keys).casefold()


def _contains_any(text, keywords):
    return any(_contains_keyword(text, keyword) for keyword in keywords)


def _contains_keyword(text, keyword):
    exact_keywords = {
        "кот", "еж", "ёж", "пес", "пёс", "пса", "псу", "псе", "псы",
        "министр", "министра", "министром", "министры",
    }
    if keyword.isascii() or keyword in exact_keywords:
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
