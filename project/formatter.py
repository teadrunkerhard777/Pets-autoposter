"""Russian Telegram presentation for the cats and pets channel."""

from datetime import datetime
from html import escape

from generation.text import fit_text_to_html_limit


MESSAGE_LIMIT = 4000
PHOTO_CAPTION_LIMIT = 1000
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
    return _format(news_item, MESSAGE_LIMIT)


def format_photo_caption(news_item):
    return _format(news_item, PHOTO_CAPTION_LIMIT)


def _format(news_item, limit):
    title = escape(str(news_item.get("title") or "Без заголовка")[:500])
    source = escape(str(news_item.get("source") or "Источник не указан"))
    url = escape(str(news_item.get("url") or ""), quote=True)
    label = CATEGORY_LABELS.get(news_item.get("event_category"), CATEGORY_LABELS["pet_news"])
    header = f"{label}\n\n<b>{title}</b>"
    disclaimer = "⚠️ При тревожных симптомах обратитесь в ветклинику." if news_item.get("needs_vet_disclaimer") else ""
    footer = f"📅 Материал: {_format_date(news_item.get('published_at'))}\n📰 {source}\n\n🔗 <a href=\"{url}\">Источник</a>\n\n{_hashtags(news_item)}"
    fixed = "\n\n".join(block for block in (header, disclaimer, footer) if block)
    body = fit_text_to_html_limit(news_item.get("article_text") or news_item.get("description", ""), max(0, limit - len(fixed) - 2))
    return "\n\n".join(block for block in (header, escape(body) if body else "", disclaimer, footer) if block)


def _hashtags(news_item):
    tags = [CATEGORY_TAGS.get(news_item.get("event_category"), "#ДомашниеЖивотные")]
    tags.extend("#Кошки" if species == "cats" else "#Собаки" if species == "dogs" else "#Питомцы" for species in news_item.get("matched_species", []))
    return " ".join(dict.fromkeys(tags))


def _format_date(value):
    return value.strftime("%d.%m.%Y") if isinstance(value, datetime) and value.tzinfo else "Дата не указана"
