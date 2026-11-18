# LEGO Universe Documentation

This repository contains the Markdown source for a public, searchable
documentation website about LEGO Universe and DarkflameServer. The public
site includes table schemas and column explanations, not the full exported
CDClient table rows.

To reduce browser memory use, search indexes item and quest detail pages by
name, ID, and description rather than every technical section. Item and quest
source, type, location, and index pages are searchable by title only. Their
complete content remains available on the pages; player guides and other
documentation retain full-text search.

## Browse the content

Start at the [LEGO Universe Game Guide](wiki/README.md). It links to the
player guides, game-data databases, and technical server documentation.

## Preview the website locally

Install Python 3.12 or newer, then run these commands from the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
py -3 scripts\prepare_site.py
.\.venv\Scripts\mkdocs serve
```

Open the local address printed by MkDocs. To build the static website without
starting a preview server, run `.\.venv\Scripts\mkdocs build --strict`.

Location-map overlays for zones with both minimaps and exact item or pet
coordinates are generated from the existing location tables. After refreshing
those pages, run `py -3 scripts\build_location_maps.py` before
`scripts\prepare_site.py`.

## Publish with GitHub Pages

The workflow in `.github/workflows/pages.yml` builds and deploys the site
whenever changes are pushed to `main`. To use it:

1. Create a **public** GitHub repository for this documentation.
2. Push the contents of this folder to its `main` branch.
3. In the repository, open **Settings → Pages** and choose **GitHub Actions**
   as the build and deployment source.
4. The first successful workflow run publishes the site. Its URL appears in
   the workflow's deployment environment.

`scripts\prepare_site.py` creates the ignored `site-src` directory used by
MkDocs. The site build omits the full local table rows and flat root item/NPC
catalogs; it publishes their schema or relevant guide links instead. Adjacent
local `res` assets are not copied, and their links are identified as local
references. DarkflameServer source-code links point to the reviewed public
GitHub revision.

## Legal notice

LEGO®, the LEGO logo, and LEGO Universe are trademarks of the LEGO Group. This
documentation is a non-commercial fan project and is not sponsored, authorized,
or endorsed by the LEGO Group. Game names, texts, icons, and minimaps shown here
are taken from the game client for identification and reference only and remain
the property of the LEGO Group. No game files are distributed.

If you are a rights holder and want content removed, please open an issue in
this documentation's repository.
