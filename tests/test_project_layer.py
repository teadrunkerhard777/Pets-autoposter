from datetime import datetime, timezone

from bs4 import BeautifulSoup

from processing.filters import add_scores, filter_relevant, filter_by_minimum_score
from project.content.evergreen import EVERGREEN_SOURCES
from project.filters import is_relevant
from project.formatter import format_photo_caption, format_post
from project.scoring import calculate_score
from project.settings import MIN_PUBLICATION_SCORE
from project.sources import (
    SOURCES,
    SOURCE_IMAGE_EXTRACTORS,
    SOURCE_PUBLISHED_AT_EXTRACTORS,
)
from project.visuals import COVER_FILES, VISUAL_TYPES, cover_path_for


def item(title, description=""):
    return {
        "title": title,
        "description": description,
        "url": "https://example.test/item?a=1&b=2",
        "source": "Pets <Test>",
        "published_at": datetime(2026, 9, 8, tzinfo=timezone.utc),
    }


def test_filter_accepts_cats_and_rejects_unrelated_material():
    accepted = item("Как подготовить дом для котёнка", "Советы по уходу за питомцем")
    rejected = item("Футбольный клуб объявил нового тренера")

    assert filter_relevant([accepted, rejected], is_relevant) == [accepted]
    assert accepted["event_category"] == "care"
    assert accepted["matched_species"] == ["cats"]
    assert rejected["event_category"] is None


def test_filter_does_not_match_pet_keywords_inside_english_words():
    for title in ("A catastrophe was avoided", "A bobcat loader", "Dogmatic rules"):
        story = item(title)

        assert is_relevant(story) is False
        assert story["event_category"] is None


def test_cat_keyword_does_not_match_inside_russian_words():
    story = item("Лоси встретили собак, которых раньше не видели")

    assert is_relevant(story) is True
    assert story["matched_species"] == ["dogs"]


def test_rescue_story_gets_meaningful_category_and_priority():
    story = item("Приют нашёл семьи для спасённых кошек")

    assert is_relevant(story) is True
    assert story["event_category"] == "positive_story"
    assert calculate_score(story) >= MIN_PUBLICATION_SCORE
    assert story["editorial_priority"] == "major_story"


def test_positive_animal_story_gets_warm_category():
    story = item("Спасённый котёнок нашёл дом и новую семью")

    assert is_relevant(story) is True
    assert story["event_category"] == "positive_story"
    assert story["editorial_signals"] == ["positive"]
    assert "💛 ДОБРАЯ ИСТОРИЯ" in format_post(story)
    assert "#ДобрыеНовости" in format_post(story)


def test_headline_cat_and_dog_receive_equal_channel_priority():
    cat = item("Кот нашёл новый дом")
    dog = item("Собака нашла новый дом")
    fox = item("Лиса нашла новый дом")

    for story in (cat, dog, fox):
        assert is_relevant(story)

    assert calculate_score(cat) == calculate_score(dog)
    assert calculate_score(cat) > calculate_score(fox)


def test_faunora_requires_a_positive_animal_centred_story():
    warning = item("Ветеринар предупредил о болезнях ежей")
    warning["source"] = "Faunora"
    rescue = item("Четырёх котят спасли и нашли им новый дом")
    rescue["source"] = "Faunora"

    assert is_relevant(warning) is False
    assert is_relevant(rescue) is True


def test_faunora_rejects_official_warning_about_a_wild_animal():
    story = item(
        "В Нягани полиция отпугнула медведя: глава города предупредил о причинах",
        "Жителям рекомендовали сообщать о встрече с хищником в 112.",
    )
    story["source"] = "Faunora"

    assert is_relevant(story) is False
    assert story["event_category"] is None
    assert story["needs_vet_disclaimer"] is False


def test_pets_mail_uses_the_same_positive_story_gate():
    happy = item("Пёс Ганнер дождался человека и снова обрёл дом")
    happy["source"] = "Питомцы Mail"
    medical = item("Ветеринар объяснил, как лечить болезни собак")
    medical["source"] = "Питомцы Mail"

    assert is_relevant(happy) is True
    assert is_relevant(medical) is False


def test_pets_mail_accepts_a_light_dog_event():
    story = item("В Петербурге прошёл необыкновенный кросс для собак")
    story["source"] = "Питомцы Mail"

    assert is_relevant(story) is True


def test_cat_news_feed_accepts_a_light_cat_story_but_rejects_war_context():
    record = item("Мейн-кун с 29 пальцами попал в Книгу рекордов")
    record["source"] = "Кошаки форева — Кошачьи новости"
    war_story = item("Кошка приносила еду людям в осаждённом городе")
    war_story["source"] = "Кошаки форева — Кошачьи новости"

    assert is_relevant(record) is True
    assert is_relevant(war_story) is False


def test_kindness_feed_admits_only_explicit_positive_animal_stories():
    puppy = item("Щенка спасали всем городом")
    puppy["source"] = "Бумеранг добра — Истории о животных"
    owl = item("Редкую сову спасли и вернули в дикую природу")
    owl["source"] = "Бумеранг добра — Истории о животных"
    human_story = item("Пастух спас шесть человек")
    human_story["source"] = "Бумеранг добра — Истории о животных"

    assert is_relevant(puppy) is True
    assert is_relevant(owl) is True
    assert owl["channel_species"] == ["other_animals"]
    assert is_relevant(human_story) is False


def test_positive_sources_reject_war_context():
    story = item("Военные на Запорожском направлении спасли собак")
    story["source"] = "Faunora"

    assert is_relevant(story) is False


def test_positive_sources_reject_environmental_problems_without_an_animal_hero():
    story = item("Рекордная солёность моря привела к появлению новых видов рыб")
    story["source"] = "Faunora"

    assert is_relevant(story) is False


def test_administrator_does_not_match_minister_block_word():
    story = item(
        "Необыкновенный кросс для собак",
        "Администратор площадки рассказал о весёлом соревновании.",
    )
    story["source"] = "Питомцы Mail"

    assert is_relevant(story) is True


def test_rospriut_rejects_official_events_without_a_kind_story():
    event = item("Чиновники обсудили питомцев на отраслевом форуме")
    event["source"] = "РосПриют"

    assert is_relevant(event) is False


def test_curated_positive_source_can_publish_an_unusual_wild_animal_story():
    story = item("Лисёнок впервые играет с новой игрушкой")
    story["source"] = "Хорошие новости про животных"

    assert is_relevant(story) is True
    assert story["matched_species"] == ["other_animals"]


def test_photo_story_source_uses_body_species_when_title_is_a_pet_name():
    story = item("Люпин ловит утро", "Щенок мчится навстречу новому дню")
    story["source"] = "Щенячий Ангел — Фото дня"

    assert is_relevant(story) is True
    assert story["headline_species"] == []
    assert story["channel_species"] == ["dogs"]


def test_photo_story_source_rejects_a_sponsor_post_without_an_animal_hero():
    story = item(
        "Спасибо за подарки от Добролап",
        "В приют приехала доставка подарков в рамках благотворительной акции.",
    )
    story["source"] = "Щенячий Ангел — Фото дня"

    assert is_relevant(story) is False


def test_positive_source_rejects_poisoning_even_when_an_animal_was_saved():
    story = item("Неизвестный отравил кота, которого затем спасли")
    story["source"] = "Faunora"

    assert is_relevant(story) is False


def test_positive_sources_reject_distressing_headlines():
    for source in (
        "Faunora",
        "Хорошие новости про животных",
        "РосПриют",
        "Кошаки форева — Кошачьи новости",
        "Бумеранг добра — Истории о животных",
    ):
        story = item("Спасённый лисёнок получил тяжёлые травмы и раны")
        story["source"] = source

        assert is_relevant(story) is False


def test_positive_sources_reject_a_gentle_title_with_distressing_body():
    story = item("Двух собак спасли после необычной встречи")
    story["source"] = "Хорошие новости про животных"
    story["article_text"] = "Животные страдали от голода, их раны воспалились."

    assert is_relevant(story) is False


def test_urgent_veterinary_story_has_disclaimer_without_giving_treatment():
    story = item("Veterinary warning: urgent signs of poisoning in cats")

    assert is_relevant(story) is True
    assert story["needs_vet_disclaimer"] is True
    assert "обратитесь в ветклинику" in format_post(story)


def test_general_safety_language_does_not_create_breaking_news():
    story = item("Цифровой контроль защищает безопасность кормов для собак")

    assert is_relevant(story) is True
    assert story["event_category"] != "urgent_safety"


def test_well_wishes_do_not_create_health_story():
    story = item("Желаем всем собакам здоровья и активной жизни")

    assert is_relevant(story) is True
    assert story["event_category"] == "pet_news"


def test_infection_story_is_classified_as_health():
    story = item("Мочевые инфекции у собак и кошек")

    assert is_relevant(story) is True
    assert story["event_category"] == "health"


def test_hashtags_use_species_from_headline_before_incidental_body_mentions():
    story = item("Парацетамол опасен для кошек")
    story["article_text"] = "В материале также сравнивается метаболизм собак."

    assert is_relevant(story) is True
    assert story["matched_species"] == ["cats", "dogs"]
    assert story["primary_species"] == ["cats"]
    assert "#Кошки" in format_post(story)
    assert "#Собаки" not in format_post(story)


def test_evergreen_cat_fact_is_accepted_and_formatted():
    story = item("Факт о кошках: зачем нужен распорядок")
    story.update(content_queue="evergreen", content_type="cat_fact")

    assert is_relevant(story) is True
    assert story["event_category"] == "evergreen_cat_fact"
    assert "😺 ФАКТ О КОШКАХ" in format_post(story)
    assert "#Кошки" in format_post(story)


def test_formatter_escapes_html_and_caption_stays_limited():
    story = item("Кошка <Мурка>", "<&> word " * 1000)
    is_relevant(story)

    post = format_post(story)
    assert "&lt;Мурка&gt;" in post
    assert '>Pets &lt;Test&gt;</a>' in post
    assert 'href="https://example.test/item?a=1&amp;b=2"' in post
    assert "🔗" in post
    assert ">Читать источник</a>" in post
    assert len(format_photo_caption(story)) <= 1000
    assert len(post) < 2000


def test_formatter_uses_editorial_timezone_for_calendar_date():
    story = item("Кошка нашла дом")
    story["published_at"] = datetime(2026, 9, 10, 23, 31, tzinfo=timezone.utc)
    is_relevant(story)

    assert "📅 11 сентября 2026" in format_post(story)


def test_curated_checklist_gets_scannable_bullets():
    story = item("Домашняя памятка", "Проверьте воду. Уберите лекарства.")
    story.update(
        content_queue="evergreen",
        content_type="pet_care",
        presentation_format="checklist",
    )
    assert is_relevant(story)

    preview = format_post(story)

    assert "✅ СОХРАНИТЕ ЧЕК-ЛИСТ" in preview
    assert "• Проверьте воду." in preview
    assert "• Уберите лекарства." in preview


def test_curated_quick_guide_gets_numbered_steps():
    story = item("Прогулка", "Проверьте карабин. Осмотрите поводок.")
    story.update(
        content_queue="evergreen",
        content_type="pet_care",
        presentation_format="quick_guide",
    )
    assert is_relevant(story)

    preview = format_post(story)

    assert "🧭 КОРОТКАЯ ИНСТРУКЦИЯ" in preview
    assert "1. Проверьте карабин." in preview
    assert "2. Осмотрите поводок." in preview


def test_relevant_scoring_respects_the_publication_threshold():
    story = item("Практические советы: как ухаживать за собакой")
    assert filter_relevant([story], is_relevant) == [story]
    add_scores([story], calculate_score)
    assert filter_by_minimum_score([story], MIN_PUBLICATION_SCORE) == [story]


def test_enabled_sources_are_only_verified_russian_feeds():
    enabled = [source for source in SOURCES if source["enabled"]]
    feeds = [source for source in enabled if source["type"] == "rss"]
    queues = [source for source in enabled if source["type"] == "static"]

    assert {source["name"] for source in feeds} == {
        "Хорошие новости про животных",
        "Faunora",
        "Щенячий Ангел — Фото дня",
        "РосПриют",
        "Кошаки форева — Кошачьи новости",
        "Бумеранг добра — Истории о животных",
    }
    assert queues == []
    assert {source["name"] for source in enabled if source["type"] == "html"} == {
        "Питомцы Mail",
    }
    assert all(source["language"] == "ru" for source in enabled)
    assert VISUAL_TYPES == {"NEWS", "SAFETY", "CARE", "WELFARE", "CAT_FACT"}


def test_veterinary_trade_feed_is_disabled_after_editorial_review():
    source = next(
        source for source in SOURCES
        if source["name"] == "Ветеринария и жизнь — Питомцы"
    )

    assert source["enabled"] is False


def test_rkf_is_registered_but_disabled_after_editorial_review():
    rkf = next(source for source in SOURCES if source["name"] == "РКФ")

    assert rkf["type"] == "rss"
    assert rkf["enabled"] is False


def test_evergreen_queue_has_attributed_dated_direct_items():
    items = [
        item
        for source in EVERGREEN_SOURCES
        for item in source["items"]
    ]

    assert all(item["content_queue"] == "evergreen" for item in items)
    assert all(item["content_type"] == "pet_care" for item in items)
    assert {item["presentation_format"] for item in items} == {
        "checklist", "quick_guide", "seasonal_checklist", "before_getting",
    }
    assert all(item["url"].startswith("https://") for item in items)
    assert all("example.invalid" not in item["url"] for item in items)
    assert all(item["published_at"] is None for item in items)
    assert all(item["published_date"] for item in items)
    assert all(item["scheduled_at"].tzinfo is not None for item in items)
    assert all(item["article_text"] for item in items)

    preview = format_post(items[0])
    assert "📅 11 апреля 2026" in preview


def test_every_visual_role_has_a_project_owned_png_cover():
    assert set(COVER_FILES) == VISUAL_TYPES
    assert all(len(filenames) == 2 for filenames in COVER_FILES.values())
    assert all(
        (cover_path_for(role, f"article-{index}").is_file())
        for role in VISUAL_TYPES
        for index in range(10)
    )
    assert all(
        {cover_path_for(role, f"article-{index}").name for index in range(20)}
        == set(COVER_FILES[role])
        for role in VISUAL_TYPES
    )


def test_cover_choice_is_stable_for_the_same_article():
    assert cover_path_for("NEWS", "https://example.test/story") == cover_path_for(
        "NEWS", "https://example.test/story",
    )


def test_rkf_logo_is_rejected_as_an_article_image():
    soup = BeautifulSoup(
        '<article><img class="wp-post-image" '
        'src="https://rkf.org.ru/wp-content/uploads/2023/06/lgn.png"></article>',
        "html.parser",
    )

    assert SOURCE_IMAGE_EXTRACTORS["РКФ"](soup) is None


def test_pets_mail_reads_exact_article_timestamp():
    soup = BeautifulSoup(
        '<meta property="article:published_time" '
        'content="2026-09-04T09:00:00+03:00">',
        "html.parser",
    )

    assert SOURCE_PUBLISHED_AT_EXTRACTORS["Питомцы Mail"](soup) == (
        "2026-09-04T09:00:00+03:00"
    )
