"""Editorial batch selection across reactive and scheduled content."""

from processing.diversity import select_diverse


PRIORITY_NEWS = {"breaking", "next_48_hours"}
EDITORIAL_PRIORITY_RANK = {
    "breaking": 5,
    "next_48_hours": 4,
    "next_7_days": 3,
    "major_story": 2,
    "standard": 1,
    "scheduled": 0,
}


def sort_by_editorial_priority(news_items):
    """Keep editorial tiers strict, then use score inside each tier."""

    return sorted(
        news_items,
        key=lambda item: (
            EDITORIAL_PRIORITY_RANK.get(
                item.get("editorial_priority"),
                EDITORIAL_PRIORITY_RANK["standard"],
            ),
            item.get("score", 0),
        ),
        reverse=True,
    )


def prefer_source_rotation(news_items, history):
    """Prefer the least recently published source after urgent stories."""

    urgent = [
        item for item in news_items
        if item.get("editorial_priority") in PRIORITY_NEWS
    ]
    regular = [
        item for item in news_items
        if item.get("editorial_priority") not in PRIORITY_NEWS
    ]
    source_recency = {}

    for distance, entry in enumerate(reversed(history)):
        if not isinstance(entry, dict):
            continue
        source = entry.get("source")
        if source and source not in source_recency:
            source_recency[source] = distance

    def rotation_key(item):
        source = item.get("source")
        if source not in source_recency:
            return (0, 0)
        return (1, -source_recency[source])

    return urgent + sorted(regular, key=rotation_key)


def select_editorial_mix(
    news_items,
    limit,
    diversity_settings,
    evergreen_slots,
):
    """Reserve evergreen slots unless urgent news needs the whole batch."""

    items = list(news_items)
    limit = max(0, int(limit))
    evergreen_slots = max(0, int(evergreen_slots))
    if limit == 0:
        return []

    reactive = [
        item for item in items
        if item.get("content_queue") != "evergreen"
    ]
    reactive = _spread_non_priority_sources(reactive)
    evergreen = [
        item for item in items
        if item.get("content_queue") == "evergreen"
    ]

    reserved = min(evergreen_slots, len(evergreen), limit)
    priority_count = sum(
        item.get("editorial_priority") in PRIORITY_NEWS
        for item in reactive
    )
    reserved = min(reserved, max(0, limit - priority_count))

    selected_evergreen = select_diverse(
        evergreen,
        reserved,
        diversity_settings,
    )
    selected_reactive = select_diverse(
        reactive,
        limit - len(selected_evergreen),
        diversity_settings,
    )

    return selected_reactive + selected_evergreen


def _spread_non_priority_sources(news_items):
    """Keep urgent order, then prefer a new source before repetitions."""

    priority = [
        item for item in news_items
        if item.get("editorial_priority") in PRIORITY_NEWS
    ]
    regular = [
        item for item in news_items
        if item.get("editorial_priority") not in PRIORITY_NEWS
    ]
    seen_sources = {
        item.get("source") for item in priority if item.get("source")
    }
    distinct = []
    repeated = []

    for item in regular:
        source = item.get("source")
        if source and source not in seen_sources:
            distinct.append(item)
            seen_sources.add(source)
        else:
            repeated.append(item)

    return priority + distinct + repeated
