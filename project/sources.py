"""Free, verified sources for the cats and pets channel."""


def _extract_rkf_image(soup):
    """Reject RKF's site-logo featured image instead of publishing branding."""

    image = soup.select_one("article img.wp-post-image")
    image_url = image.get("src", "").strip() if image else ""
    blocked_names = ("/lgn.png", "/rkf-logo_rus.png")
    return None if image_url.casefold().endswith(blocked_names) else image_url or None

SOURCES = [
    {
        "name": "ASPCA News",
        "type": "rss",
        "url": "https://www.aspca.org/rss.xml",
        # The channel is Russian-language and this feed updates too rarely for
        # the configured five-day news window.
        "enabled": False,
        "limit": 20,
        "source_kind": "animal_welfare_organization",
        "language": "en",
        "feed_timeout": 15,
        "trust": 0.95,
    },
    {
        "name": "Blue Cross News",
        "type": "rss",
        "url": "https://www.bluecross.org.uk/rss.xml",
        # Disabled: repeated unattended requests currently receive HTTP 403.
        # Do not work around the source's access controls.
        "enabled": False,
        "limit": 20,
        "source_kind": "animal_welfare_organization",
        "language": "en",
        "feed_timeout": 15,
        "trust": 0.90,
    },
    {
        "name": "Ветеринария и жизнь — Питомцы",
        "type": "rss",
        "url": "https://vetandlife.ru/pets/feed/",
        # Technically reliable, but its veterinary and industry agenda does
        # not match this channel's positive animal-centred direction.
        "enabled": False,
        "limit": 20,
        "use_feed_content": True,
        "source_kind": "specialist_pet_media",
        "language": "ru",
        "feed_timeout": 15,
        "trust": 0.90,
    },
    {
        "name": "Хорошие новости про животных",
        "type": "rss",
        "url": "https://goodnewsanimal.ru/news/rss/",
        "enabled": True,
        "limit": 30,
        "use_feed_content": True,
        "source_kind": "positive_animal_media",
        "language": "ru",
        "feed_timeout": 15,
        "feed_retries": 2,
        "trust": 0.95,
    },
    {
        "name": "Faunora",
        "type": "rss",
        "url": "https://faunora.ru/rss.xml",
        "enabled": True,
        "limit": 30,
        "use_feed_content": True,
        "source_kind": "animal_news_media",
        "language": "ru",
        "headers": {"User-Agent": "Mozilla/5.0 AutoposterTemplate/1.0"},
        "feed_timeout": 15,
        "feed_retries": 2,
        "trust": 0.85,
    },
    {
        "name": "РосПриют",
        "type": "rss",
        "url": "https://rospriut.ru/news/feed/",
        "enabled": True,
        "limit": 20,
        "use_feed_content": True,
        "feed_stop_markers": ("Сообщение ",),
        "source_kind": "animal_welfare_media",
        "language": "ru",
        "feed_timeout": 15,
        "feed_retries": 2,
        "trust": 0.85,
    },
    {
        "name": "РКФ",
        "type": "rss",
        "url": "https://rkf.org.ru/category/novosti/feed/",
        # Disabled after live evaluation: the feed is dominated by corporate
        # and specialist event announcements and rarely exposes article art.
        "enabled": False,
        "limit": 20,
        "use_feed_content": True,
        "feed_stop_markers": ("Сообщение ",),
        "source_kind": "dog_welfare_organization",
        "language": "ru",
        "feed_timeout": 15,
        "trust": 0.90,
    },
]

SOURCE_EXTRACTORS = {}
SOURCE_IMAGE_EXTRACTORS = {"РКФ": _extract_rkf_image}
SOURCE_PUBLISHED_AT_EXTRACTORS = {}
SOURCE_STOP_MARKERS = {}
