from datetime import datetime, timezone

from publishing.telegram import TelegramSendResult, TemporaryVideo
from video_main import (
    add_video_to_history,
    choose_search_query,
    format_video_caption,
    publish_video,
    select_unpublished_video,
)


def video():
    return {
        "title": "Весёлое видео с животными",
        "url": "https://www.pexels.com/video/42/",
        "source": "Pexels",
        "published_at": None,
        "video_url": "https://video.test/42.mp4",
        "creator_name": "Cats & Dogs",
        "creator_url": "https://www.pexels.com/@cats-dogs/",
        "pexels_id": 42,
    }


def test_query_rotation_uses_different_day_and_evening_slots():
    daytime = choose_search_query(datetime(2026, 9, 16, 8, tzinfo=timezone.utc))
    evening = choose_search_query(datetime(2026, 9, 16, 15, tzinfo=timezone.utc))

    assert daytime != evening


def test_selection_skips_url_already_in_history():
    old = video()
    fresh = {**video(), "url": "https://www.pexels.com/video/43/"}

    assert select_unpublished_video([old, fresh], [{"url": old["url"]}]) == fresh


def test_video_history_entry_remains_url_only():
    history = []

    add_video_to_history(video(), history)

    assert history[0]["pexels_id"] == 42
    assert "event_fingerprint" not in history[0]


def test_caption_credits_creator_and_pexels():
    caption = format_video_caption(video())

    assert "Cats &amp; Dogs" in caption
    assert "Pexels" in caption
    assert "https://www.pexels.com/video/42/" in caption


def test_dry_run_downloads_and_removes_video_without_telegram(tmp_path):
    path = tmp_path / "video.mp4"
    path.write_bytes(b"video")

    def download(url, max_size):
        return TemporaryVideo(path, "video/mp4", 5)

    changed = publish_video(
        video(),
        [],
        True,
        download_video=download,
        send_video=lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("Telegram must not be called")
        ),
    )

    assert changed is False
    assert path.exists() is False


def test_confirmed_video_send_updates_history_once(tmp_path):
    path = tmp_path / "video.mp4"
    path.write_bytes(b"video")
    history = []

    changed = publish_video(
        video(),
        history,
        False,
        download_video=lambda *args: TemporaryVideo(path, "video/mp4", 5),
        send_video=lambda *args, **kwargs: TelegramSendResult(True),
    )

    assert changed is True
    assert history[0]["url"] == video()["url"]
    assert path.exists() is False


def test_uncertain_video_send_does_not_update_history(tmp_path):
    path = tmp_path / "video.mp4"
    path.write_bytes(b"video")
    history = []

    changed = publish_video(
        video(),
        history,
        False,
        download_video=lambda *args: TemporaryVideo(path, "video/mp4", 5),
        send_video=lambda *args, **kwargs: TelegramSendResult(
            False,
            "ReadTimeout",
            uncertain=True,
        ),
    )

    assert changed is False
    assert history == []
    assert path.exists() is False
