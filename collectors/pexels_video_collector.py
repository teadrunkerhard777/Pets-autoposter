"""Small Pexels video collector with no third-party client dependency."""

import requests


PEXELS_VIDEO_SEARCH_URL = "https://api.pexels.com/v1/videos/search"
PEXELS_TIMEOUT = (10, 30)


class PexelsVideoError(Exception):
    """Expected Pexels configuration or response failure."""


def collect_pexels_videos(
    api_key,
    query,
    orientation,
    per_page,
    max_duration_seconds,
    max_size_bytes,
):
    """Return Telegram-compatible Pexels video candidates."""

    if not api_key:
        raise PexelsVideoError("PEXELS_API_KEY is missing")

    try:
        response = requests.get(
            PEXELS_VIDEO_SEARCH_URL,
            headers={"Authorization": api_key},
            params={
                "query": query,
                "orientation": orientation,
                "size": "small",
                "per_page": per_page,
            },
            timeout=PEXELS_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as error:
        raise PexelsVideoError(type(error).__name__) from error

    videos = payload.get("videos") if isinstance(payload, dict) else None
    if not isinstance(videos, list):
        raise PexelsVideoError("Pexels returned an invalid video list")

    candidates = []
    for video in videos:
        candidate = _normalize_video(
            video,
            max_duration_seconds=max_duration_seconds,
            max_size_bytes=max_size_bytes,
        )
        if candidate is not None:
            candidates.append(candidate)

    return candidates


def _normalize_video(video, max_duration_seconds, max_size_bytes):
    if not isinstance(video, dict):
        return None

    duration = video.get("duration")
    if not isinstance(duration, int) or not 1 <= duration <= max_duration_seconds:
        return None

    video_file = _best_video_file(video.get("video_files"), max_size_bytes)
    user = video.get("user") if isinstance(video.get("user"), dict) else {}
    page_url = video.get("url")

    if video_file is None or not isinstance(page_url, str):
        return None

    return {
        "title": "Весёлое видео с животными",
        "url": page_url,
        "source": "Pexels",
        "published_at": None,
        "article_text": "",
        "image_url": None,
        "video_url": video_file["link"],
        "video_width": video_file.get("width"),
        "video_height": video_file.get("height"),
        "video_duration": duration,
        "video_size": video_file.get("file_size"),
        "creator_name": user.get("name") or "автор Pexels",
        "creator_url": user.get("url") or page_url,
        "pexels_id": video.get("id"),
    }


def _best_video_file(video_files, max_size_bytes):
    if not isinstance(video_files, list):
        return None

    suitable = []
    for video_file in video_files:
        if not isinstance(video_file, dict):
            continue
        if video_file.get("file_type") != "video/mp4":
            continue
        if not isinstance(video_file.get("link"), str):
            continue

        file_size = video_file.get("file_size")
        if isinstance(file_size, int) and not 0 < file_size <= max_size_bytes:
            continue
        if file_size is not None and not isinstance(file_size, int):
            continue

        width = video_file.get("width") or 0
        height = video_file.get("height") or 0
        if not width or not height or max(width, height) > 1920:
            continue

        suitable.append(video_file)

    if not suitable:
        return None

    return min(
        suitable,
        key=lambda item: (
            item.get("width", 0) > item.get("height", 0),
            abs(max(item.get("width", 0), item.get("height", 0)) - 1080),
            item.get("file_size") or max_size_bytes,
        ),
    )
