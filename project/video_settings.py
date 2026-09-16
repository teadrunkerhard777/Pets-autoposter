"""Project-owned settings for light-hearted animal videos."""

from zoneinfo import ZoneInfo


VIDEO_TIMEZONE = ZoneInfo("Asia/Yekaterinburg")
VIDEO_SOURCES = ("Pexels", "Pixabay")
VIDEO_SEARCH_QUERIES = (
    "funny cat",
    "playful dog",
    "cute puppy playing",
    "funny kitten",
    "pets playing",
    "cute animals playing",
)
VIDEO_ORIENTATION = "portrait"
VIDEO_RESULTS_PER_RUN = 30
VIDEO_MAX_DURATION_SECONDS = 40
VIDEO_MAX_SIZE_BYTES = 49 * 1024 * 1024

VIDEO_CAPTIONS = (
    "🐾 Минутка хорошего настроения",
    "😄 Срочно отложите дела на несколько секунд",
    "🐶🐱 Кажется, у кого-то сегодня прекрасный день",
    "💛 Немного хвостатого антистресса",
)
