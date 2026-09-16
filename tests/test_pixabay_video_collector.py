from collectors.pixabay_video_collector import collect_pixabay_videos


class PixabayResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_collector_uses_safe_animal_search_and_selects_mp4(monkeypatch):
    request = {}
    payload = {
        "hits": [{
            "id": 77,
            "duration": 14,
            "pageURL": "https://pixabay.com/videos/id-77/",
            "videos": {
                "large": {
                    "url": "https://cdn.test/large.mp4",
                    "width": 3840,
                    "height": 2160,
                    "size": 45_000_000,
                },
                "medium": {
                    "url": "https://cdn.test/medium.mp4",
                    "width": 1920,
                    "height": 1080,
                    "size": 12_000_000,
                },
            },
        }]
    }

    def get(url, **kwargs):
        request.update(url=url, **kwargs)
        return PixabayResponse(payload)

    monkeypatch.setattr("collectors.pixabay_video_collector.requests.get", get)
    items = collect_pixabay_videos(
        "secret-key",
        "funny cat",
        30,
        40,
        49 * 1024 * 1024,
    )

    assert request["params"]["key"] == "secret-key"
    assert request["params"]["category"] == "animals"
    assert request["params"]["safesearch"] == "true"
    assert items[0]["video_url"] == "https://cdn.test/medium.mp4"
    assert items[0]["media_id"] == "pixabay:77"


def test_collector_rejects_long_and_oversized_videos(monkeypatch):
    payload = {
        "hits": [
            {
                "id": 1,
                "duration": 60,
                "pageURL": "https://pixabay.test/1",
                "videos": {},
            },
            {
                "id": 2,
                "duration": 10,
                "pageURL": "https://pixabay.test/2",
                "videos": {
                    "medium": {
                        "url": "https://cdn.test/large.mp4",
                        "width": 1920,
                        "height": 1080,
                        "size": 60_000_000,
                    }
                },
            },
        ]
    }
    monkeypatch.setattr(
        "collectors.pixabay_video_collector.requests.get",
        lambda *args, **kwargs: PixabayResponse(payload),
    )

    assert collect_pixabay_videos("key", "pets", 30, 40, 49_000_000) == []
