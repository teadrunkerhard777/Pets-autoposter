from project.events import enrich_event_timing


def test_event_enrichment_does_not_invent_dates_from_pet_story_text():
    item = {"title": "Кошке нужен уход", "article_text": "В апреле 2018 года котёнок нашёл дом."}
    assert enrich_event_timing(item) is item
    assert "event_at" not in item
    assert "event_date" not in item
