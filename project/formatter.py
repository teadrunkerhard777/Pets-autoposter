"""Russian Telegram presentation for the cats and pets channel."""

from datetime import date, datetime
from html import escape

from generation.text import fit_text_to_html_limit


MESSAGE_LIMIT = 4000
PHOTO_CAPTION_LIMIT = 1000
MESSAGE_BODY_PREVIEW_LIMIT = 1100
PHOTO_BODY_PREVIEW_LIMIT = 500
CATEGORY_LABELS = {
    "urgent_safety": "🚨 БЕЗОПАСНОСТЬ ПИТОМЦА", "animal_welfare": "🤍 ПОМОЩЬ ЖИВОТНЫМ",
    "health": "🩺 ЗДОРОВЬЕ", "care": "🐾 УХОД ЗА ПИТОМЦЕМ", "pet_news": "🐾 ПИТОМЦЫ",
    "evergreen_cat_fact": "😺 ФАКТ О КОШКАХ", "evergreen_pet_care": "🏠 ЗАБОТА О ПИТОМЦЕ",
    "evergreen_adoption_story": "🤍 ИСТОРИЯ ПРИЮТА", "evergreen_breed": "🐕 ПОРОДЫ И ХАРАКТЕРЫ",
}
CATEGORY_TAGS = {
    "urgent_safety": "#БезопасностьПитомца", "animal_welfare": "#ПомощьЖивотным",
    "health": "#ЗдоровьеПитомца", "care": "#УходЗаПитомцем", "pet_news": "#ДомашниеЖивотные",
    "evergreen_cat_fact": "#Кошки", "evergreen_pet_care": "#УходЗаПитомцем",
    "evergreen_adoption_story": "#ВозьмиИзПриюта", "evergreen_breed": "#ДомашниеЖивотные",
}


def format_post(news_item):
    return _format(news_item, MESSAGE_LIMIT, MESSAGE_BODY_PREVIEW_LIMIT)


def format_photo_caption(news_item):
    return _format(news_item, PHOTO_CAPTION_LIMIT, PHOTO_BODY_PREVIEW_LIMIT)


def _format(news_item, limit, body_preview_limit):
    title = escape(str(news_item.get("title") or "Без заголовка")[:500])
    source = escape(str(news_item.get("source") or "Источник не указан"))
    url = escape(str(news_item.get("url") or ""), quote=True)
    label = CATEGORY_LABELS.get(news_item.get("event_category"), CATEGORY_LABELS["pet_news"])
    header = f"{label}\n\n<b>{title}</b>"
    disclaimer = "⚠️ При тревожных симптомах обратитесь в ветклинику." if news_item.get("needs_vet_disclaimer") else ""
    footer = f"📅 Материал: {_format_date(news_item.get('published_at'), news_item.get('published_date'))}\n📰 {source}\n\n🔗 <a href=\"{url}\">Источник</a>\n\n{_hashtags(news_item)}"
    fixed = "\n\n".join(block for block in (header, disclaimer, footer) if block)
    available_body = min(
        body_preview_limit,
        max(0, limit - len(fixed) - 2),
    )
    body = fit_text_to_html_limit(
        news_item.get("article_text") or news_item.get("description", ""),
        available_body,
    )
    return "\n\n".join(block for block in (header, escape(body) if body else "", disclaimer, footer) if block)


def _hashtags(news_item):
    tags = [CATEGORY_TAGS.get(news_item.get("event_category"), "#ДомашниеЖивотные")]
    species_values = news_item.get("primary_species") or news_item.get(
        "matched_species",
        [],
    )
    tags.extend("#Кошки" if species == "cats" else "#Собаки" if species == "dogs" else "#Питомцы" for species in species_values)
    return " ".join(dict.fromkeys(tags))


def _format_date(value, date_value=None):
    if isinstance(value, datetime) and value.tzinfo:
        return value.strftime("%d.%m.%Y")

    try:
        parsed_date = date.fromisoformat(date_value)
    except (TypeError, ValueError):
        return "Дата не указана"

    return parsed_date.strftime("%d.%m.%Y")
