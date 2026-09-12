"""Free, verified sources for the cats and pets channel."""

from datetime import datetime, timedelta, timezone


now = datetime.now(timezone.utc)

SOURCES = [
    {
        "name": "Pets Autoposter local fixture",
        "type": "static",
        "enabled": False,
        "items": [
            {
                "title": "Как подготовить безопасный дом для котёнка",
                "url": "https://example.invalid/pets/safe-home-kitten",
                "published_at": now - timedelta(hours=2),
                "description": "Практическая памятка об уходе и безопасной среде для нового питомца.",
                "article_text": "Уберите опасные растения и мелкие предметы, подготовьте воду, лоток и тихое место для отдыха.",
                "image_url": None,
            },
            {
                "title": "Приют нашёл дом для десятков кошек и собак",
                "url": "https://example.invalid/pets/shelter-adoption",
                "published_at": now - timedelta(hours=4),
                "description": "История ответственного пристройства животных из приюта.",
                "article_text": "Волонтёры помогли питомцам встретить новые семьи и рассказали о подготовке к адаптации.",
                "image_url": None,
            },
            {
                "title": "Факт о кошках: почему им нужен предсказуемый распорядок",
                "url": "https://example.invalid/pets/cat-routine",
                "published_at": now - timedelta(days=30),
                "scheduled_at": now - timedelta(minutes=20),
                "content_queue": "evergreen",
                "content_type": "cat_fact",
                "description": "Плановый материал о повседневных потребностях домашней кошки.",
                "article_text": "Стабильные время кормления, игры и спокойное место помогают кошке чувствовать себя увереннее.",
                "image_url": None,
            },
        ],
    },
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
]

SOURCE_EXTRACTORS = {}
SOURCE_IMAGE_EXTRACTORS = {}
SOURCE_PUBLISHED_AT_EXTRACTORS = {}
SOURCE_STOP_MARKERS = {}
