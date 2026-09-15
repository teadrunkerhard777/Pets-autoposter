from datetime import datetime, timedelta, timezone

from project.filters import is_relevant
from project.scoring import calculate_score
from project.scheduling import filter_time_eligible
from project.selection import (
    apply_source_cooldowns,
    prefer_source_rotation,
    select_editorial_mix,
)
from project.settings import (
    EVERGREEN_SLOTS_PER_RUN,
    MAX_NEWS_PER_RUN,
    SOURCE_COOLDOWN_PUBLICATIONS,
)


NOW = datetime(2026, 9, 8, 12, tzinfo=timezone.utc)


def test_active_configuration_reserves_no_evergreen_slots():
    assert EVERGREEN_SLOTS_PER_RUN == 0


def test_active_configuration_selects_one_item_per_run():
    assert MAX_NEWS_PER_RUN == 1


def test_faunora_waits_for_three_other_publications():
    faunora = story("Белка играет на ярмарке", source="Faunora")
    alternative = story("Нерпу выпустили в море", source="Другой источник")
    history = [
        {"source": "Faunora"},
        {"source": "Источник A"},
        {"source": "Источник B"},
    ]

    assert apply_source_cooldowns(
        [faunora, alternative],
        history,
        SOURCE_COOLDOWN_PUBLICATIONS,
    ) == [alternative]

    history.append({"source": "Источник C"})
    assert apply_source_cooldowns(
        [faunora],
        history,
        SOURCE_COOLDOWN_PUBLICATIONS,
    ) == [faunora]


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


def test_source_rotation_prefers_unseen_then_least_recent_source():
    source_a = story("Статья A", source="Источник A", editorial_priority="major_story")
    source_b = story("Статья B", source="Источник B", editorial_priority="major_story")
    source_c = story("Статья C", source="Источник C", editorial_priority="standard")
    history = [
        {"source": "Источник B"},
        {"source": "Источник A"},
    ]

    assert prefer_source_rotation([source_a, source_b, source_c], history) == [
        source_c,
        source_b,
        source_a,
    ]


def test_source_rotation_never_moves_regular_story_above_breaking_news():
    regular = story("Статья РКФ", source="РКФ", editorial_priority="standard")
    breaking = story(
        "Срочное предупреждение",
        source="Ветеринария и жизнь — Питомцы",
        editorial_priority="breaking",
    )
    history = [{"source": "Ветеринария и жизнь — Питомцы"}]

    assert prefer_source_rotation([regular, breaking], history) == [breaking, regular]


def test_source_rotation_keeps_cats_and_dogs_ahead_of_other_animals():
    dog = story(
        "Собака нашла новую семью",
        source="Недавний источник",
        editorial_priority="major_story",
        headline_species=["dogs"],
    )
    wild = story(
        "Лоси играют в лесу",
        source="Новый источник",
        editorial_priority="major_story",
        headline_species=["other_animals"],
    )
    history = [{"source": "Недавний источник"}]

    assert prefer_source_rotation([dog, wild], history) == [dog, wild]
