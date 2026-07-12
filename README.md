# USMLE Reasoning Lab — companion site

Public, crawlable companion pages (transcript + quick answer + Q&A) for every
[USMLE Reasoning Lab](https://www.youtube.com/) video. This is the **GEO
(Generative Engine Optimization)** surface: AI answer engines (ChatGPT, Perplexity,
Google AI Overviews) read the **text around a video** — so we host the transcript
and a structured Q&A here, on an open page we own, and link it from each video
description. See `config/geo_playbook.md` in the main project for the strategy.

- **Live site:** https://wenchangyue.github.io/usmle-reasoning-lab/
- **Built with:** Jekyll on GitHub Pages (no theme; custom layouts).
- Each episode page emits `VideoObject` + `FAQPage` schema.org JSON-LD from its
  front matter (see `_layouts/episode.html`).

## Add an episode page

1. Copy `TEMPLATE-episode.md` → `_episodes/<slug>.md`.
2. Remove `published: false`; fill the front matter (title, video_id, youtube_url,
   upload_date, duration, description, quick_answer, faq, sources).
3. Paste the **human-reviewed transcript** (same text as the uploaded YouTube
   caption track) into the body under `## Transcript`.
4. Commit + push; GitHub Pages rebuilds automatically.

## Notes

- This repo lives **outside** the Google Drive project folder on purpose — a `.git`
  directory inside a synced Drive folder corrupts. The main project references this
  path in `PROJECT_NOTES.md`.
- Content is original teaching material; no commercial question-bank or recall
  content is reproduced. Educational use only.

Local path: `~/usmle-reasoning-lab`
