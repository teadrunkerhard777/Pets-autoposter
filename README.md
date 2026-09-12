# Pets Autoposter

Rule-based Telegram autoposter for a Russian-language channel about cats and domestic pets. It collects free public animal-welfare material, selects relevant stories, and formats a concise attributed post.

## Editorial scope

- cats, dogs, and small domestic pets;
- responsible ownership, behaviour, care, adoption, shelters, and animal welfare;
- urgent safety notices from accountable sources;
- fresh news and useful articles about everyday life with pets.

The channel does not diagnose animals, prescribe treatment, promote breeding or sales, or turn rumours into news. A material that signals an emergency or poisoning receives a clear instruction to contact a veterinary clinic.

## Visual format

Posts use one of five visual roles: general pet news, safety, everyday care,
animal welfare, or a cat fact. A suitable lead image from the attributed source
remains the first choice. When it is missing or cannot be safely delivered, the
autoposter uses one of two matching project-owned covers from `assets/covers/`.
The article URL selects the variant consistently, adding variety without
changing the image when a run is retried.

The covers contain no headline, logo, or event-specific claim, so the same set
can support experiments with post length and editorial format without implying
that an illustration documents a real event. See [MEDIA_POLICY.md](MEDIA_POLICY.md).

## Sources

- «Ветеринария и жизнь — Питомцы» — health, care, and pet-industry reporting;
- «РосПриют» — shelters, adoption, and animal-welfare events;
- РКФ — dogs, responsible ownership, and canine events.

All active sources publish in Russian. ASPCA and Blue Cross remain registered
but disabled: ASPCA is English-language and too infrequent for the configured
news window, while unattended Blue Cross requests currently receive HTTP 403.

Each run publishes at most one concise preview. Breaking safety information
stays first. The curated evergreen queue is retained for future experiments but
is not connected to the active sources and has no reserved publication slot.

## Quick start

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -m pytest
.venv/bin/python main.py
```

`AUTOPOSTER_DRY_RUN` defaults to `true`: a local run never calls Telegram or changes `storage/published.json`.

Deployment and safe control-run instructions are in [DEPLOYMENT.md](DEPLOYMENT.md).

See [PROJECT_CONCEPT.md](PROJECT_CONCEPT.md), [SOURCES.md](SOURCES.md), and [EDITORIAL_POLICY.md](EDITORIAL_POLICY.md) for the channel rules.
