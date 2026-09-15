"""Collect and publish at most one light-hearted Pexels animal video."""

import html
import os
from datetime import datetime, timezone

from collectors.pexels_video_collector import collect_pexels_videos
from config import DRY_RUN
from core.environment import configure_ssl
from core.run_lock import AlreadyRunningError, single_instance_lock
from project.video_settings import (
    VIDEO_CAPTIONS,
    VIDEO_MAX_DURATION_SECONDS,
    VIDEO_MAX_SIZE_BYTES,
    VIDEO_ORIENTATION,
    VIDEO_RESULTS_PER_RUN,
    VIDEO_SEARCH_QUERIES,
    VIDEO_TIMEZONE,
)
from publishing.telegram import (
    VideoDownloadError,
    download_video_temp,
    send_telegram_video,
)
from processing.deduplicator import normalize_url
from storage.history import load_history, save_history


def choose_search_query(now=None):
    """Rotate searches between the local daytime and evening slots."""

    current = now or datetime.now(timezone.utc)
    local = current.astimezone(VIDEO_TIMEZONE)
    slot = 0 if local.hour < 17 else 1
    index = (local.date().toordinal() * 2 + slot) % len(VIDEO_SEARCH_QUERIES)
    return VIDEO_SEARCH_QUERIES[index]


def format_video_caption(item):
    caption = VIDEO_CAPTIONS[int(item.get("pexels_id") or 0) % len(VIDEO_CAPTIONS)]
    creator = html.escape(str(item.get("creator_name") or "автор Pexels"))
    creator_url = html.escape(
        str(item.get("creator_url") or item["url"]),
        quote=True,
    )
    page_url = html.escape(str(item["url"]), quote=True)
    return (
        f"{caption}\n\n"
        f'🎬 <a href="{creator_url}">{creator}</a> · '
        f'<a href="{page_url}">Pexels</a>'
    )


def select_unpublished_video(candidates, history):
    published_urls = {
        normalize_url(entry.get("url"))
        for entry in history
        if normalize_url(entry.get("url"))
    }
    return next(
        (
            item for item in candidates
            if normalize_url(item.get("url")) not in published_urls
        ),
        None,
    )


def add_video_to_history(item, history):
    """Keep video entries URL-only for compatibility with news deduplication."""

    history.append({
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "published_at": None,
        "source": item.get("source"),
        "pexels_id": item.get("pexels_id"),
    })


def publish_video(
    item,
    history,
    dry_run,
    download_video=download_video_temp,
    send_video=send_telegram_video,
):
    """Download once, publish once, and record only confirmed success."""

    temporary_video = None
    try:
        temporary_video = download_video(
            item["video_url"],
            VIDEO_MAX_SIZE_BYTES,
        )
        caption = format_video_caption(item)
        if dry_run:
            print("[DRY RUN] Telegram was not called")
            print(
                f"Video validated: {temporary_video.mime_type}, "
                f"{temporary_video.size_bytes} bytes"
            )
            print(caption)
            return False

        with temporary_video.path.open("rb") as video_file:
            result = send_video(
                video_file,
                caption,
                filename=temporary_video.path.name,
                mime_type=temporary_video.mime_type,
            )
        if result:
            add_video_to_history(item, history)
            return True
        return False
    except (VideoDownloadError, OSError) as error:
        print(f"Video warning: {type(error).__name__}")
        return False
    finally:
        if temporary_video and temporary_video.path.exists():
            temporary_video.path.unlink()


def run(now=None):
    configure_ssl()
    query = choose_search_query(now)
    candidates = collect_pexels_videos(
        api_key=os.getenv("PEXELS_API_KEY", "").strip(),
        query=query,
        orientation=VIDEO_ORIENTATION,
        per_page=VIDEO_RESULTS_PER_RUN,
        max_duration_seconds=VIDEO_MAX_DURATION_SECONDS,
        max_size_bytes=VIDEO_MAX_SIZE_BYTES,
    )
    history = load_history()
    selected = select_unpublished_video(candidates, history)
    print(f"Video query: {query}")
    print(f"Suitable videos: {len(candidates)}")

    if selected is None:
        print("No unpublished video is available; publication skipped.")
        return None

    print(f"Selected Pexels video: {selected.get('pexels_id')}")
    history_changed = publish_video(selected, history, DRY_RUN)
    if not DRY_RUN and history_changed:
        save_history(history)
    return selected


if __name__ == "__main__":
    try:
        with single_instance_lock():
            run()
    except AlreadyRunningError:
        print("Autoposter is already running; this run was stopped.")
