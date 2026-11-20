# kyledanielgordon.com

Static site for Kyle Daniel Gordon, orchestrator, arranger and conductor.
Hosted on GitHub Pages; every push to `main` deploys automatically (.github/workflows/pages.yml).

- `index.html` home
- `work/rosalia-lux/` LUX project page
- `work-with-kyle/` services
- `img/` images (file names carry project + name for search)

## Layout
- `public/` the live site (GitHub Pages publishes this folder)
- `tools/` the scripts that generate the pages from the design

## Artwork (standing rule, approved by Kyle 2026-11-20)
Poster and album art is always pulled from online, never left as a placeholder.
Add `"slug": "<image url>"` to `tools/art.json` and push; the "Fetch artwork" Action
downloads it to `art/<slug>.jpg`. Pull, run `tools/sync_art.py`, set the credit's image key, rebuild.
