# USMLE Reasoning Lab — companion site

Crawlable companion pages (transcript + quick answer + Q&A) for rights-cleared,
medically reviewed long-form videos from
[USMLE Reasoning Lab](https://www.youtube.com/@USMLEReasoningLab). This is the **GEO
(Generative Engine Optimization)** surface: AI answer engines (ChatGPT, Perplexity,
Google AI Overviews) read the **text around a video** — so we host the transcript
and a structured Q&A here, on an open page we own, and link it from each video
description. See `config/geo_playbook.md` in the main project for the strategy.

- **Live site:** https://wenchangyue.github.io/usmle-reasoning-lab/
- **Built with:** Jekyll on GitHub Pages (no theme; custom layouts).
- Each episode page emits `VideoObject` + `FAQPage` schema.org JSON-LD from its
  front matter (see `_layouts/episode.html`).

## Add an episode page

1. Before upload, confirm that the episode is rights-cleared and medical-QA-cleared,
   and that its final caption track has been reviewed.
2. Copy `TEMPLATE-episode.md` → `_episodes/<slug>.md`.
3. Fill the front matter except `video_id`, `youtube_url`, and `upload_date`; keep
   `published: false`. The YouTube uploader first uploads privately, then fills
   those fields, publishes the page, updates `llms.txt`, and verifies both links.
4. Paste the **human-reviewed transcript** (same text as the uploaded YouTube
   caption track) into the body under `## Transcript`.
5. Put the stable companion URL in the YouTube description draft. The uploader
   commits and pushes the page after it receives the private video's stable ID.

## Notes

- This repo lives **outside** the Google Drive project folder on purpose — a `.git`
  directory inside a synced Drive folder corrupts. The main project references this
  path in `PROJECT_NOTES.md`.
- Content is original teaching material; no commercial question-bank or recall
  content is reproduced. Educational use only.

Local path: `~/usmle-reasoning-lab`
