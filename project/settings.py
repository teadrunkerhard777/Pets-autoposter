"""Settings for the cats and domestic pets autoposter."""

NEWS_LOOKBACK_DAYS = 5
MAX_NEWS_PER_RUN = 2
MIN_PUBLICATION_SCORE = 5
EVERGREEN_SLOTS_PER_RUN = 0
POST_MODE = "single"

EVENT_DEDUP_SETTINGS = {
    "text_limit": 1600, "time_window_hours": 48, "min_shared_tokens": 5,
    "min_token_overlap": 0.45, "min_token_jaccard": 0.20, "dense_match_tokens": 7,
    "event_time_window_hours": 24, "event_date_window_days": 0,
    "min_shared_participants": 2,
    "stop_words": {"about", "after", "also", "from", "into", "more", "that", "their", "this", "with", "will", "your", "для", "как", "это", "или", "что", "the", "and"},
    "noise_prefixes": ("announce", "article", "company", "report", "source", "update", "анонс", "источник", "материал"),
}

DIVERSITY_SETTINGS = {
    "enabled": True, "text_limit": 1200, "core_min_shared_tokens": 4,
    "core_min_token_overlap": 0.30, "core_min_token_jaccard": 0.14,
    "core_dense_match_tokens": 5, "min_shared_tokens": 4,
    "min_token_overlap": 0.35, "min_token_jaccard": 0.16,
    "stop_words": EVENT_DEDUP_SETTINGS["stop_words"],
    "noise_prefixes": EVENT_DEDUP_SETTINGS["noise_prefixes"],
}
