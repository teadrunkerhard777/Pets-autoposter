from collectors.pexels_video_collector import collect_pexels_videos


class PexelsResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_collector_uses_api_key_and_selects_compact_mp4(monkeypatch):
    request = {}
    payload = {
        "videos": [{
            "id": 42,
            "duration": 12,
            "url": "https://www.pexels.com/video/42/",
            "user": {"name": "Pet Author", "url": "https://pexels.test/pet"},
            "video_files": [
                {
                    "file_type": "video/mp4",
                    "link": "https://video.test/large.mp4",
                    "width": 2160,
                    "height": 3840,
                    "file_size": 40_000_000,
                },
                {
                    "file_type": "video/mp4",
                    "link": "https://video.test/vertical.mp4",
                    "width": 720,
                    "height": 1280,
                    "file_size": 8_000_000,
                },
            ],
        }]
    }

    def get(url, **kwargs):
        request.update(url=url, **kwargs)
        return PexelsResponse(payload)

    monkeypatch.setattr("collectors.pexels_video_collector.requests.get", get)
    items = collect_pexels_videos(
        "secret-key",
        "funny cat",
        "portrait",
        30,
        40,
        49 * 1024 * 1024,
    )

    assert request["headers"] == {"Authorization": "secret-key"}
    assert request["params"]["query"] == "funny cat"
    assert items[0]["video_url"] == "https://video.test/vertical.mp4"
    assert items[0]["creator_name"] == "Pet Author"


def test_collector_rejects_long_videos_and_oversized_files(monkeypatch):
    payload = {
        "videos": [
            {
                "duration": 60,
                "url": "https://pexels.test/long",
                "video_files": [],
            },
            {
                "duration": 10,
                "url": "https://pexels.test/large",
                "video_files": [{
                    "file_type": "video/mp4",
                    "link": "https://video.test/large.mp4",
                    "width": 720,
                    "height": 1280,
                    "file_size": 60_000_000,
                }],
            },
        ]
    }
    monkeypatch.setattr(
        "collectors.pexels_video_collector.requests.get",
        lambda *args, **kwargs: PexelsResponse(payload),
    )

    assert collect_pexels_videos("key", "pets", "portrait", 30, 40, 49_000_000) == []
