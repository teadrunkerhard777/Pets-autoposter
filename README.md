# Pets Autoposter

Rule-based Telegram autoposter for a Russian-language channel about cats and domestic pets. It collects free public animal-welfare material, selects relevant stories, and formats a concise attributed post.

## Editorial scope

- cats, dogs, and small domestic pets;
- responsible ownership, behaviour, care, adoption, shelters, and animal welfare;
- urgent safety notices from accountable sources;
- scheduled evergreen facts about cats and everyday pet care.

The channel does not diagnose animals, prescribe treatment, promote breeding or sales, or turn rumours into news. A material that signals an emergency or poisoning receives a clear instruction to contact a veterinary clinic.

## Active sources

- ASPCA News — animal-welfare news;
- Blue Cross News — animal-welfare and responsible-pet-care news.

These sources currently publish in English. The autoposter preserves their original headlines and text with attribution; it does not claim to translate them. Add Russian sources only after their dates, direct article links, and extraction are verified.

## Quick start

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -m pytest
.venv/bin/python main.py
```

`AUTOPOSTER_DRY_RUN` defaults to `true`: a local run never calls Telegram or changes `storage/published.json`.

See [PROJECT_CONCEPT.md](PROJECT_CONCEPT.md), [SOURCES.md](SOURCES.md), and [EDITORIAL_POLICY.md](EDITORIAL_POLICY.md) for the channel rules.
