"""Short attributed evergreen posts for the pets channel."""

from datetime import datetime, timedelta, timezone


QUEUE_READY_AT = datetime.now(timezone.utc) - timedelta(minutes=20)

EVERGREEN_SOURCES = [
    {
        "name": "Ветеринария и жизнь",
        "type": "static",
        "enabled": True,
        "source_kind": "specialist_pet_media",
        "language": "ru",
        "trust": 0.90,
        "items": [
            {
                "title": "Домашний чек-лист: что действительно нужно питомцу",
                "url": "https://vetandlife.ru/consumer/chto-dolzhno-byt-u-kazhdogo-vladelca-pitomca-doma-chek-list/",
                "published_at": None,
                "published_date": "2026-04-11",
                "scheduled_at": QUEUE_READY_AT,
                "content_queue": "evergreen",
                "content_type": "pet_care",
                "description": "Короткая памятка о базовой домашней среде для кошек и собак.",
                "article_text": (
                    "У питомца должны быть отдельные миски для еды и свежей воды, "
                    "спокойное место для отдыха, безопасные игрушки и подходящие "
                    "средства ухода. Переноска пригодится не только в путешествии, "
                    "но и для обычного визита в клинику. Собакам нужны адресник и "
                    "надёжный поводок, кошкам — устойчивый лоток и когтеточка. "
                    "Полезные вещи выбирайте под возраст, размер и привычки "
                    "конкретного животного, а не по длине списка покупок."
                ),
                "image_url": None,
            },
            {
                "title": "Домашние птицы: сначала пространство, потом питомец",
                "url": "https://vetandlife.ru/pets/kakih-ptic-mozhno-zavesti-v-kachestve-pitomcev/",
                "published_at": None,
                "published_date": "2025-04-04",
                "scheduled_at": QUEUE_READY_AT,
                "content_queue": "evergreen",
                "content_type": "pet_care",
                "description": "Что важно оценить до появления канарейки, кореллы или другой птицы.",
                "article_text": (
                    "Разным домашним птицам нужны разные условия, но маленькая "
                    "клетка не подходит ни одной активной птице. Заранее оцените "
                    "доступное пространство, защиту от сквозняков, возможность "
                    "двигаться и потребность вида в общении. Некоторым птицам "
                    "требуется пара, другим — ежедневное внимание человека. "
                    "Игрушки, жердочки и купалка подбираются под размер и поведение "
                    "питомца, а дверца клетки должна надёжно закрываться."
                ),
                "image_url": None,
            },
        ],
    },
    {
        "name": "В Добрые Руки",
        "type": "static",
        "enabled": True,
        "source_kind": "veterinary_clinic_education",
        "language": "ru",
        "trust": 0.85,
        "items": [
            {
                "title": "Осенняя памятка для владельцев кошек и собак",
                "url": "https://goodhands.vet/blog/terapiya/9-osennikh-riskov-dlya-koshek-i-sobak/",
                "published_at": None,
                "published_date": "2026-08-25",
                "scheduled_at": QUEUE_READY_AT,
                "content_queue": "evergreen",
                "content_type": "pet_care",
                "description": "Сезонные бытовые риски без назначения лечения.",
                "article_text": (
                    "Осенью после прогулки полезно осмотреть лапы и шерсть собаки, "
                    "а промокшего питомца — аккуратно высушить. Клещи могут "
                    "оставаться активными и в прохладную погоду, поэтому график "
                    "защиты лучше обсуждать с ветеринаром, а не отменять по "
                    "календарю. Бытовую химию, лекарства и сезонные реагенты "
                    "держите вне доступа животных. Резкое изменение поведения или "
                    "самочувствия — повод обратиться в клинику."
                ),
                "image_url": None,
            },
            {
                "title": "Кошка на даче: как снизить риск побега",
                "url": "https://goodhands.vet/blog/ukhod/berem-koshku-na-dachu-kak-podgotovitsya-bezopasno/",
                "published_at": None,
                "published_date": "2026-07-28",
                "scheduled_at": QUEUE_READY_AT,
                "content_queue": "evergreen",
                "content_type": "pet_care",
                "description": "Подготовка переноски, дома и контактов владельца.",
                "article_text": (
                    "До поездки проверьте переноску, сетки на окнах и места, через "
                    "которые кошка может выбежать из дома. Адресник или другая "
                    "актуальная идентификация повышают шанс быстро вернуть "
                    "потерявшегося питомца. На новом месте сначала выделите "
                    "спокойную закрытую комнату с водой, лотком и знакомой "
                    "подстилкой. Не выпускайте кошку осваивать участок сразу после "
                    "дороги и не оставляйте открытыми двери."
                ),
                "image_url": None,
            },
            {
                "title": "Поводок для собаки: удобство важнее внешнего вида",
                "url": "https://goodhands.vet/blog/ukhod/kak-pravilno-vybrat-povodok-dlya-sobaki/",
                "published_at": None,
                "published_date": "2022-02-09",
                "scheduled_at": QUEUE_READY_AT,
                "content_queue": "evergreen",
                "content_type": "pet_care",
                "description": "Базовые ориентиры для безопасной прогулки.",
                "article_text": (
                    "Поводок выбирают с учётом размера, силы и поведения собаки. "
                    "Карабин должен легко закрываться, но не раскрываться от "
                    "случайного удара, а лента или трос — оставаться целыми без "
                    "потёртостей. Для обучения и спокойных прогулок удобнее модели, "
                    "которые позволяют уверенно контролировать дистанцию. Регулярно "
                    "проверяйте швы и крепления: даже хороший поводок со временем "
                    "изнашивается."
                ),
                "image_url": None,
            },
            {
                "title": "Ящерица дома: террариум готовят заранее",
                "url": "https://goodhands.vet/blog/ukhod/kakuyu-yashcheritsu-zavesti-novichku-i-chto-nuzhno-znat-ob-ukhode/",
                "published_at": None,
                "published_date": "2025-07-30",
                "scheduled_at": QUEUE_READY_AT,
                "content_queue": "evergreen",
                "content_type": "pet_care",
                "description": "Почему экзотический питомец начинается с изучения условий вида.",
                "article_text": (
                    "До появления ящерицы нужно выбрать вид и подготовить террариум "
                    "под его взрослый размер. Температура, влажность, освещение, "
                    "укрытия и рацион различаются даже у внешне похожих рептилий. "
                    "Оборудование лучше запустить и проверить заранее, а контакты "
                    "ветеринара, работающего с экзотическими животными, найти до "
                    "покупки питомца. Импульсивный выбор без готовой среды создаёт "
                    "лишний риск для животного."
                ),
                "image_url": None,
            },
        ],
    },
]
