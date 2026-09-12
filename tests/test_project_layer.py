from datetime import datetime, timezone

from processing.filters import add_scores, filter_relevant, filter_by_minimum_score
from project.filters import is_relevant
from project.formatter import format_photo_caption, format_post
from project.scoring import calculate_score
from project.settings import MIN_PUBLICATION_SCORE
from project.sources import SOURCES
from project.visuals import VISUAL_TYPES


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


def test_relevant_scoring_respects_the_publication_threshold():
    story = item("Практические советы: как ухаживать за собакой")
    assert filter_relevant([story], is_relevant) == [story]
    add_scores([story], calculate_score)
    assert filter_by_minimum_score([story], MIN_PUBLICATION_SCORE) == [story]


def test_enabled_sources_are_verified_welfare_rss_feeds():
    enabled = [source for source in SOURCES if source["enabled"]]
    assert {source["name"] for source in enabled} == {
        "Ветеринария и жизнь — Питомцы",
        "РосПриют",
        "РКФ",
    }
    assert all(source["type"] == "rss" for source in enabled)
    assert all(source["language"] == "ru" for source in enabled)
    assert any(source["type"] == "static" for source in SOURCES)
    assert VISUAL_TYPES == {"NEWS", "SAFETY", "CARE", "WELFARE", "CAT_FACT"}
