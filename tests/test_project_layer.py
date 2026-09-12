from datetime import datetime, timezone

from processing.filters import add_scores, filter_relevant, filter_by_minimum_score
from project.content.evergreen import EVERGREEN_SOURCES
from project.filters import is_relevant
from project.formatter import format_photo_caption, format_post
from project.scoring import calculate_score
from project.settings import MIN_PUBLICATION_SCORE
from project.sources import SOURCES
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


def test_welfare_story_gets_meaningful_category_and_priority():
    story = item("Приют нашёл семьи для спасённых кошек")

    assert is_relevant(story) is True
    assert story["event_category"] == "animal_welfare"
    assert calculate_score(story) >= MIN_PUBLICATION_SCORE
    assert story["editorial_priority"] == "major_story"


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
    assert "Pets &lt;Test&gt;" in post
    assert 'href="https://example.test/item?a=1&amp;b=2"' in post
    assert len(format_photo_caption(story)) <= 1000
    assert len(post) < 2000


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
        "Ветеринария и жизнь — Питомцы",
        "РосПриют",
        "РКФ",
    }
    assert queues == []
    assert all(source["language"] == "ru" for source in enabled)
    assert VISUAL_TYPES == {"NEWS", "SAFETY", "CARE", "WELFARE", "CAT_FACT"}


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
    assert "📅 Материал: 11.04.2026" in preview


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
