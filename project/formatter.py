"""Russian Telegram presentation for the cats and pets channel."""

from datetime import date, datetime
from html import escape
import re

from generation.text import fit_text_to_html_limit


MESSAGE_LIMIT = 4000
PHOTO_CAPTION_LIMIT = 1000
MESSAGE_BODY_PREVIEW_LIMIT = 1100
PHOTO_BODY_PREVIEW_LIMIT = 500
RUSSIAN_MONTHS = (
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
)
CATEGORY_LABELS = {
    "positive_story": "💛 ДОБРАЯ ИСТОРИЯ",
    "urgent_safety": "🚨 БЕЗОПАСНОСТЬ ПИТОМЦА", "animal_welfare": "🤍 ПОМОЩЬ ЖИВОТНЫМ",
    "health": "🩺 ЗДОРОВЬЕ", "care": "🐾 УХОД ЗА ПИТОМЦЕМ", "pet_news": "🐾 ЖИВОТНЫЕ",
    "evergreen_cat_fact": "😺 ФАКТ О КОШКАХ", "evergreen_pet_care": "🏠 ЗАБОТА О ПИТОМЦЕ",
    "evergreen_adoption_story": "🤍 ИСТОРИЯ ПРИЮТА", "evergreen_breed": "🐕 ПОРОДЫ И ХАРАКТЕРЫ",
}
CATEGORY_TAGS = {
    "positive_story": "#ДобрыеНовости",
    "urgent_safety": "#БезопасностьПитомца", "animal_welfare": "#ПомощьЖивотным",
    "health": "#ЗдоровьеПитомца", "care": "#УходЗаПитомцем", "pet_news": "#МирЖивотных",
    "evergreen_cat_fact": "#Кошки", "evergreen_pet_care": "#УходЗаПитомцем",
    "evergreen_adoption_story": "#ВозьмиИзПриюта", "evergreen_breed": "#ДомашниеЖивотные",
}
FORMAT_KICKERS = {
    "checklist": "✅ СОХРАНИТЕ ЧЕК-ЛИСТ",
    "quick_guide": "🧭 КОРОТКАЯ ИНСТРУКЦИЯ",
    "seasonal_checklist": "🍂 СЕЗОННАЯ ПАМЯТКА",
    "before_getting": "🏡 ДО ПОЯВЛЕНИЯ ПИТОМЦА",
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
    kicker = FORMAT_KICKERS.get(news_item.get("presentation_format"))
    header = "\n".join(block for block in (label, kicker) if block)
    header = f"{header}\n\n<b>{title}</b>"
    disclaimer = "⚠️ При тревожных симптомах обратитесь в ветклинику." if news_item.get("needs_vet_disclaimer") else ""
    footer = (
        f"📅 {_format_date(news_item.get('published_at'), news_item.get('published_date'))}\n"
        f"📰 <a href=\"{url}\">{source}</a>\n\n"
        f"🔗 <a href=\"{url}\">Читать источник</a>\n\n"
        f"{_hashtags(news_item)}"
    )
    fixed = "\n\n".join(block for block in (header, disclaimer, footer) if block)
    available_body = min(
        body_preview_limit,
        max(0, limit - len(fixed) - 2),
    )
    body = fit_text_to_html_limit(
        _structured_body(
            news_item.get("article_text") or news_item.get("description", ""),
            news_item.get("presentation_format"),
        ),
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


def _structured_body(value, presentation_format):
    """Give curated items a scannable shape without rewriting source facts."""

    text = " ".join(str(value or "").split())
    if presentation_format not in {
        "checklist", "quick_guide", "seasonal_checklist", "before_getting",
    }:
        return text

    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    if presentation_format == "quick_guide":
        return "\n".join(f"{index}. {sentence}" for index, sentence in enumerate(sentences, 1))
    if presentation_format == "before_getting":
        return "Сначала оцените условия:\n" + "\n".join(f"• {sentence}" for sentence in sentences)
    return "\n".join(f"• {sentence}" for sentence in sentences)


def _format_date(value, date_value=None):
    if isinstance(value, datetime) and value.tzinfo:
        parsed_date = value.date()
    else:
        try:
            parsed_date = date.fromisoformat(date_value)
        except (TypeError, ValueError):
            return "Дата не указана"

    return f"{parsed_date.day} {RUSSIAN_MONTHS[parsed_date.month - 1]} {parsed_date.year}"
