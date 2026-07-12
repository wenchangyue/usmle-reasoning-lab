---
layout: default
title: Companion notes & transcripts
description: >-
  Full transcripts, quick answers, and Q&A for every USMLE Reasoning Lab
  episode — original USMLE Step 1/2 teaching questions worked one clue at a time.
---
# USMLE Reasoning Lab — companion notes

Full **transcripts**, a one-line **quick answer**, and a **Q&A** for every video on
the [USMLE Reasoning Lab](https://www.youtube.com/@) channel. Each page mirrors the
episode so you can read, search, and quote it — original teaching questions worked
one clue at a time.

## Episodes

{% if site.episodes.size > 0 %}
<ul>
{% for ep in site.episodes %}
  <li><a href="{{ ep.url | relative_url }}">{{ ep.title }}</a>{% if ep.exam %} <span class="meta">· {{ ep.exam }}</span>{% endif %}</li>
{% endfor %}
</ul>
{% else %}
_Episode pages will appear here as they publish._
{% endif %}
