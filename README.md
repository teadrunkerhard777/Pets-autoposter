# Pets Autoposter

Rule-based Telegram autoposter for a Russian-language channel about cats and domestic pets. It collects free public animal-welfare material, selects relevant stories, and formats a concise attributed post.

## Editorial scope

- cats, dogs, and small domestic pets;
- responsible ownership, behaviour, care, adoption, shelters, and animal welfare;
- urgent safety notices from accountable sources;
- scheduled evergreen facts about cats and everyday pet care.

The channel does not diagnose animals, prescribe treatment, promote breeding or sales, or turn rumours into news. A material that signals an emergency or poisoning receives a clear instruction to contact a veterinary clinic.

## Sources

- «Ветеринария и жизнь — Питомцы» — health, care, and pet-industry reporting;
- «РосПриют» — shelters, adoption, and animal-welfare events;
- РКФ — dogs, responsible ownership, and canine events.

All active sources publish in Russian. ASPCA and Blue Cross remain registered
but disabled: ASPCA is English-language and too infrequent for the configured
news window, while unattended Blue Cross requests currently receive HTTP 403.

Each run publishes at most two concise previews. Breaking safety information
stays first; other positions prefer different sources to keep the channel mix
varied while the format is being evaluated.

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
