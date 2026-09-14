# Pets Autoposter

Rule-based Telegram autoposter for a Russian-language cats-and-dogs channel. It collects free public material, selects kind and engaging animal-centred stories, and formats a concise attributed post.

## Editorial scope

- cats and dogs as the primary characters and ranking priority;
- rescues, adoption, reunions, friendship, funny discoveries, and good deeds;
- occasional warm or fascinating stories about other animals when no suitable cat or dog story is available;
- fresh news and readable articles with strong source photography.

The channel is not about officials, the pet industry, or routine veterinary warnings. It does not diagnose animals, prescribe treatment, promote breeding or sales, turn rumours into news, or use distressing material merely for attention.

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

- «Хорошие новости про животных» — a curated positive animal-news feed;
- «Щенячий Ангел — Фото дня» — short, frequently updated shelter stories with original pet photos;
- «Питомцы Mail» — fresh cat-and-dog reporting with large article images, admitted through the positive-story filter;
- Faunora — frequent animal reporting, admitted only through a strict positive-story filter;
- «РосПриют» — adoption and rescue stories, also admitted only through the positive-story filter.

All active sources publish in Russian. «Ветеринария и жизнь — Питомцы» and РКФ
remain registered but disabled because their veterinary, industry, and
specialist agendas do not fit the channel. ASPCA is English-language and too
infrequent for the configured news window; unattended Blue Cross requests
currently receive HTTP 403.

Each run publishes at most one concise preview. Positive cat and dog stories
receive the highest editorial weight. Source rotation happens only after this
channel priority, so
a one-item batch still rotates publications across the active feeds. The
curated evergreen queue is retained for future experiments but is not connected
to the active sources and has no reserved publication slot.

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
