# Maintenance

The source of truth is `data/gpt-6-1-terra-usecase-curated.json`. It contains only the public selected cases. Translations live in `data/locales/`. Research queues and audit working files are kept outside this repository.

Each independent work has one stable `case-N` anchor, a source-linked title, creator attribution, a practical takeaway, source-grounded notes, all selected source visuals, and Type/Date metadata. Preserve disclosed video acceleration, model labels and cost conditions. Keep negative results. Do not reconstruct missing prompts.

Review new sources, group reposts with their original work, verify attribution and media, update English first, then translate all visible prose. Preserve source URLs, case numbers, dates, prompt bytes and media identities.

Run `python3 scripts/build_readmes.py --english-only`, review English, then `python3 scripts/build_readmes.py`. Check reproducibility with `python3 scripts/build_readmes.py --check`. Inspect desktop and narrow layouts, links, anchors, media playback and translations before publishing. Star History is omitted below ten verified live stars.
