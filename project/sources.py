"""Free, verified sources for the cats and pets channel."""

from project.content.evergreen import EVERGREEN_SOURCES

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
        "enabled": True,
        "limit": 20,
        "use_feed_content": True,
        "source_kind": "specialist_pet_media",
        "language": "ru",
        "feed_timeout": 15,
        "trust": 0.90,
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
        "enabled": True,
        "limit": 20,
        "use_feed_content": True,
        "feed_stop_markers": ("Сообщение ",),
        "source_kind": "dog_welfare_organization",
        "language": "ru",
        "feed_timeout": 15,
        "trust": 0.90,
    },
    *EVERGREEN_SOURCES,
]

SOURCE_EXTRACTORS = {}
SOURCE_IMAGE_EXTRACTORS = {}
SOURCE_PUBLISHED_AT_EXTRACTORS = {}
SOURCE_STOP_MARKERS = {}
