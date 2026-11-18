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

Location-map overlays for zones with minimaps and exact item or pet coordinates
are generated from the existing location tables. They also include world
markers extracted from local `.luz` and `.lvl` resources. To refresh those
markers, provide the client resource root, then rebuild the overlays:

```powershell
py -3 scripts\extract_location_map_world_markers.py --client-res "C:\path\to\res\res"
py -3 scripts\build_location_maps.py
```

The extracted coordinate CSV is committed; client binaries are not. Run
`scripts\prepare_site.py` after refreshing the overlays.

NPC and enemy template pages are generated from the local
`LEGO Universe NPC List.csv` catalog and the committed world-marker CSV:

```powershell
py -3 scripts\build_npc_pages.py
py -3 scripts\build_location_maps.py
py -3 scripts\prepare_site.py
```

The NPC catalog CSV is local and ignored by Git; the generated reference pages
and map links are committed. Pages show registered template data and potential
map placements, not live entities or guaranteed server availability.

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
