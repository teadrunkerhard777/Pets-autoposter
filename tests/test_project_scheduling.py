from datetime import datetime, timedelta, timezone

from project.filters import is_relevant
from project.scoring import calculate_score
from project.scheduling import filter_time_eligible
from project.selection import select_editorial_mix
from project.settings import EVERGREEN_SLOTS_PER_RUN


NOW = datetime(2026, 9, 8, 12, tzinfo=timezone.utc)


def test_active_configuration_reserves_no_evergreen_slots():
    assert EVERGREEN_SLOTS_PER_RUN == 0


def story(title, **values):
    return {
        "title": title,
        "description": "Материал о домашних животных",
        "url": f"https://example.test/{id(values)}",
        "source": "Test",
        "published_at": NOW - timedelta(hours=1),
        **values,
    }


def score(value):
    assert is_relevant(value)
    value["score"] = calculate_score(value, now=NOW)
    return value


def test_time_filter_keeps_fresh_news_and_due_evergreen_only():
    fresh = story("Советы по уходу за кошкой")
    old = story("Старая новость о собаке", published_at=NOW - timedelta(days=10))
    ready = story("Факт о кошках", content_queue="evergreen", content_type="cat_fact", scheduled_at=NOW - timedelta(minutes=1))
    future = story("Факт о кошках позже", content_queue="evergreen", content_type="cat_fact", scheduled_at=NOW + timedelta(minutes=1))

    assert filter_time_eligible([fresh, old, ready, future], lookback_days=5, now=NOW) == [fresh, ready]


def test_editorial_mix_reserves_a_slot_for_due_evergreen_content():
    reactive = [score(story("Советы по уходу за кошкой")), score(story("Советы по уходу за собакой"))]
    evergreen = score(story("Факт о кошках", content_queue="evergreen", content_type="cat_fact", scheduled_at=NOW))

    selected = select_editorial_mix(reactive + [evergreen], limit=2, diversity_settings={"enabled": False}, evergreen_slots=1)
    assert len(selected) == 2
    assert sum(value.get("content_queue") == "evergreen" for value in selected) == 1


def test_editorial_mix_prefers_distinct_sources_after_breaking_news():
    breaking = score(story("Срочное предупреждение об отравлении кошки"))
    breaking["source"] = "Источник A"
    same_source = score(story("Ветеринар рассказал о здоровье собаки"))
    same_source["source"] = "Источник A"
    other_source = score(story("Приют ищет дом для собаки"))
    other_source["source"] = "Источник B"

    selected = select_editorial_mix(
        [breaking, same_source, other_source],
        limit=2,
        diversity_settings={"enabled": False},
        evergreen_slots=0,
    )

    assert selected == [breaking, other_source]
