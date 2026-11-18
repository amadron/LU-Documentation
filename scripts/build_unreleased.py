"""Build wiki/Unreleased Content.md: content defined in the client data that players never saw.

Usage (from the documentation root):
    py -3 scripts/build_unreleased.py [--db PATH] [--client PATH]

Evidence used (all read-only):
- ZoneTable/Activities locStatus (0 = never localized, 1 = partially, 2 = released)
- whether a zone's map file ships in client/res/maps
- object names the developers marked "[DNL]" (do not localize), "DO NOT USE" or "unused"
- set members, pets and puzzles without an object definition or placement
"""

import argparse
import html
import os
import re
import sqlite3
import sys
from pathlib import Path

import game_paths  # location of the unmodified game data


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = game_paths.CDSERVER_DB
DEFAULT_CLIENT = game_paths.CLIENT_RES
OUTPUT = ROOT / "wiki" / "Unreleased Content.md"
FDB_TOOLS = ROOT.parent / "tools"  # tools/fdb_sync.py (dev folder) can parse cdclient.fdb
EXCLUDED_ZONES = {1650}  # custom development content, not original game data
TEST_ZONE = re.compile(r"test|dev|temp|sandbox|_qa|prototype|template|demo|scratch|benchmark|fake|empty", re.I)
FLAGGED = re.compile(r"\[DNL\]|\bDNL\b|DO NOT USE|\(do not use\)|\bunused\b|NOT NEEDED", re.I)
# Named zones that are defined but whose map is not shipped; picked because they are referenced
# elsewhere in the client data or by name in the community (see notes).
PLANNED_ZONES = {
    1252: "Large property for Nimbus Station.",
    1352: "Large property for Gnarled Forest.",
    1452: "Large property for Forbidden Valley (\"Craggle Rock\").",
    1500: "\"LUP Station\" — its official summary reads \"Temp map for LUP content\". The released Starbase 3001 (1600) map sits in the same LUP_Station folder.",
    1801: "\"Nexus Tower Battlefield Crater\"; planned next to Crux Prime, whose map folder is Aura_Mar.",
    20000: "Named entry with its map removed; the released World Builder planets use zones 1601–1604.",
    20022: "Older entry with the same name as the released zone 1603; its map was removed.",
    20061: "Older entry with the same name as the released zone 1604; its map was removed.",
    20101: "Older entry with the same name as the released zone 1601; its map was removed.",
    20147: "Older entry with the same name as the released zone 1602; its map was removed.",
}
ZONE_NOTES = {
    556: (
        "Winter racetrack; a local asset has this filename, but its path does not exactly match "
        "the stored ZoneTable path. The seasonal race shipped as activity "
        "\"Space Blizzard Racetrack\" (1261), see the [Racing Guide](./Racing%20Guide.md)."
    ),
    1152: "Large property for Avant Gardens.",
    1202: "A duck shooting gallery for Nimbus Station; single-player activity 7583 is defined for it.",
    1301: "Survival mode for Gnarled Forest.",
    1401: "Siege mode for Forbidden Valley; activity 37 is defined for 2–4 players.",
}


def escape(value):
    text = html.escape(str(value), quote=False).replace("\r", " ").replace("\n", " ")
    return re.sub(r"[\\|`*_\[\]~]", lambda match: f"&#{ord(match.group())};", text)


def load_locale(path):
    text = path.read_text(encoding="utf-8")
    return {m.group(1): html.unescape(m.group(2)).strip() for m in re.finditer(
        r'<phrase id="([^"]+)">.*?<translation locale="en_US">(.*?)</translation>', text, re.S)}


def load_client_status(client):
    """Release status must come from the unmodified client database (cdclient.fdb): a local server
    database can have been edited, e.g. to unlock zones for testing."""
    sys.path.insert(0, str(FDB_TOOLS))
    from fdb_sync import Fdb
    fdb = Fdb(str(client / "cdclient.fdb"))  # opened read-only; nothing is saved

    def rows(table, *names):
        info = fdb.tables[table]
        cols = [c[1] for c in info["cols"]]
        index = [cols.index(n) for n in names]
        for bucket in range(info["buckets"]):
            for row in fdb.bucket_rows(table, bucket):
                yield tuple(row[i] for i in index)

    zones = {z: (status, name, desc) for z, status, name, desc in
             rows("ZoneTable", "zoneID", "locStatus", "zoneName", "DisplayDescription")}
    activities = dict(rows("Activities", "ActivityID", "locStatus"))
    return zones, activities


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--client", type=Path, default=DEFAULT_CLIENT)
    args = parser.parse_args()
    db = sqlite3.connect(args.db)
    client_zones, client_activities = load_client_status(args.client)
    strings = load_locale(args.client.parent / "locale" / "locale.xml")
    maps = args.client / "maps"
    shipped = {}
    for folder, _, files in os.walk(maps):
        for name in files:
            if name.lower().endswith(".luz"):
                shipped[name.lower()] = os.path.relpath(os.path.join(folder, name), args.client).replace(os.sep, "/")
    wiki = ROOT / "wiki"

    def page(folder, ident, label):
        target = wiki / folder / f"{ident}.md"
        return f"[{label}](./{folder}/{ident}.md)" if target.exists() else label

    def object_name(lot):
        row = db.execute("select coalesce(nullif(displayName, ''), name) from Objects where id=?", (lot,)).fetchone()
        return strings.get(f"Objects_{lot}_name") or (row[0] if row and row[0] else f"LOT {lot}")

    out = [
        "# Unreleased and Cut Content",
        "",
        "[Game Guide](./README.md) | [Worlds](./Worlds%20Guide.md) | [Zones and maps](./zones/README.md) | "
        "[Faction Guide](./Faction%20Guide.md)",
        "",
        "The final game client still contains content that players never saw: worlds that were",
        "never opened, characters that were replaced, and gear that was planned but not finished.",
        "This page lists what the client data shows, with the evidence for each entry.",
        "",
        "!!! note \"How to read this page\"",
        "    A definition in the data is not proof of what the developers intended. Entries are",
        "    included when the data marks them as never released: a status of *not localized*",
        "    (`locStatus` 0) on worlds and activities, names the developers tagged *[DNL]* (do not",
        "    localize), *DO NOT USE* or *unused*, or references to objects that do not exist.",
        "    Seasonal content that was switched on only for events is listed separately.",
        "    Test and developer maps are left out.",
        "",
    ]

    # 1. Worlds whose map ships in the client but were never released.
    released_maps = {Path((n or "").replace("\\", "/")).name.lower(): z
                     for z, (status, n, _) in client_zones.items() if status == 2}
    duplicates = []
    rows = []
    for zone, (status, name, desc) in sorted(client_zones.items()):
        if status != 0:
            continue
        if zone in EXCLUDED_ZONES or not name or name.endswith("__removed") or TEST_ZONE.search(f"{name} {desc}"):
            continue
        luz = Path(name.replace("\\", "/")).name.lower()
        if luz not in shipped:
            continue
        if luz in released_maps:
            duplicates.append((zone, desc or name, released_maps[luz]))
            continue
        label = escape(strings.get(f"ZoneTable_{zone}_DisplayDescription") or desc or name)
        rows.append(f"| {page('zones', zone, str(zone))} | {label} | `{escape(shipped[luz])}` "
                    f"| {'Partly localized' if status == 1 else 'Not localized'} | {ZONE_NOTES.get(zone, '')} |")
    out += ["## Worlds that ship in the client but were never opened", "",
            "These map files are present in the client, but their zone entries were never localized",
            "and no launch pad leads to them. The listed path is the local client asset path matched",
            "by filename; it is not proof that the ZoneTable's stored path resolves to that asset.", "",
            "| Zone | Internal name | Map file | Status | Notes |", "| --- | --- | --- | --- | --- |"] + rows + [""]
    if duplicates:
        out += ["Some never-localized zone entries only point at the map of a released world and are",
                "old duplicate entries, not separate areas: "
                + "; ".join(f"{zone} \"{escape(desc)}\" (map of {page('zones', target, str(target))})"
                            for zone, desc, target in duplicates) + ".", ""]

    # 2. Planned worlds without a shipped map.
    rows = []
    for zone, note in PLANNED_ZONES.items():
        row = client_zones.get(zone)
        if not row:
            continue
        status, name, desc = row
        luz = Path((name or "").replace("\\", "/")).name.lower()
        if luz in shipped:
            continue
        label = escape(strings.get(f"ZoneTable_{zone}_DisplayDescription") or desc or name)
        rows.append(f"| {zone} | {label} | {'Removed' if (name or '').endswith('__removed') else '`' + escape(name) + '` (missing)'} | {note} |")
    out += ["## Planned worlds without a map", "",
            "The zone table names these areas, but the client has no map for them.", "",
            "| Zone | Name | Map file | Notes |", "| --- | --- | --- | --- |"] + rows + [""]

    # 3. Seasonal and partly released content.
    frakjaw = (client_activities.get(58),) if 58 in client_activities else None
    out += ["## Seasonal and partly released content", "",
            "- **Space Blizzard Racetrack** (activity 60, see [zone 1261](./zones/1261.md)) was a winter",
            "  event race. It has no ZoneTable row of its own; zone 556 \"Winter Racetrack\" has the same",
            "  map filename but a different stored path and is not localized. Instance 1261 has no",
            "  ZoneTable row, so the server's normal map lookup cannot resolve a zone asset for that ID;",
            "  activity and asset evidence alone do not establish that it loads or is reachable.",
            "- **Seasonal map objects** are switched on by event gates in the map files. DarkflameServer",
            "  enables them through the `event_1` … `event_8` settings in `worldconfig.ini`.",
            "- **Avant Grove** ([zone 1151](./zones/1151.md)) is only partly localized (locStatus 1).",
            f"- **Frakjaw Battle** (activity 58) has activity locStatus {frakjaw[0] if frakjaw else '?'}, although its",
            "  zone [Battle Against Frakjaw!](./zones/2001.md) is released.", ""]

    # 4. Replaced characters and other objects marked as not for use.
    rows = []
    for lot, name, display in db.execute("select id, name, displayName from Objects order by id"):
        text = f"{name or ''} {display or ''}"
        if lot == 16900 or not FLAGGED.search(text):
            continue
        shown = display or name
        rows.append(f"| {page('items', lot, str(lot))} | {escape(name or '')} | {escape(shown or '')} |")
    out += ["## Characters and objects marked as not for use", "",
            "The developers tagged these templates *[DNL]* (do not localize), *DO NOT USE* or *unused*.",
            "The most telling group are the four **original faction representatives**: Dirk Manleigh",
            "(Sentinels), Logan Moonshot (Venture League), Ellgren Stackwell (Assembly) and Silas Penumbra",
            "(Paradox). The 2010 guide still names Silas Penumbra; in the released game the faction",
            "introductions are handled by other characters (see the [Faction Guide](./Faction%20Guide.md)).",
            "The *[DNL] Valiant …* entries are named after the valiant gear; the data does not show",
            "what they were for.", "",
            "| LOT | Internal name | Display name |", "| --- | --- | --- |"] + rows + [""]

    # 5. Gear: set members without an object definition, test kits.
    missing = {}
    for set_id, ids, kit_rank in db.execute("select setID, itemIDs, kitRank from ItemSets where kitRank between 1 and 3"):
        kit = strings.get(f"ItemSets_{set_id}_kitName") or f"Set {set_id}"
        for lot in (int(x) for x in ids.split(",") if x.strip()):
            if not db.execute("select 1 from Objects where id=?", (lot,)).fetchone():
                missing.setdefault((kit, lot), []).append(kit_rank)
    rows = [f"| {page('classes', kit.lower().replace(' ', '-'), escape(kit))} | {lot} | "
            f"{', '.join(map(str, sorted(ranks)))} |" for (kit, lot), ranks in sorted(missing.items())]
    out += ["## Unfinished gear", "",
            "**Missing valiant weapons.** The rank-3 sets of the four later classes list a valiant weapon",
            "that has no object definition, while the eight original classes have one. Only the hidden",
            "off-hand proxy items exist for some of them.", "",
            "| Class | Missing LOT | Listed in rank set |", "| --- | --- | --- |"] + rows + [
            "",
            "**Test kits.** Item sets 45–47 (*Test Rank 1–3* sword, hat, shirt, pants, shield, shoulders)",
            "are developer test equipment and were never localized.",
            "", "See the [class pages](./classes/README.md) for the released kits.", ""]

    # 6. Pets.
    orphan_puzzles = [lot for (lot,) in db.execute("select NPCLot from TamingBuildPuzzles")
                      if not db.execute("select 1 from Objects where id=?", (lot,)).fetchone()]
    out += ["## Pets", "",
            "- **Lion:** the pet is defined and has a taming puzzle, but no map spawns it and no",
            "  mission points to a location. See the [Pet Guide](./Pet%20Guide.md).",
            ]
    if orphan_puzzles:
        out.append("- **Taming puzzles without a pet:** "
                   + ", ".join(page("pets", lot, f"LOT {lot}") for lot in orphan_puzzles)
                   + " — puzzle rows exist, but no object, name or placement.")
    out += ["", "## Hidden missions are not cut content", "",
            "Most missions that were never localized are *Hidden* missions: invisible trackers the game",
            "uses for flags and progress (for example the faction-join markers 544, 555, 566 and 577).",
            "They are part of the released game. Only a few are developer tests, such as",
            f"{page('quests', 1730, 'mission 1730')} \"TEST - Gather tasks (fixification)\" and mission 1893.", "",
            "## Source and limitations", "",
            "Generated by `scripts/build_unreleased.py`. Release status (`ZoneTable`, `Activities`) is read",
            "from the original client database `cdclient.fdb`; `Objects`, `ItemSets` and",
            "`TamingBuildPuzzles` come from the server copy of it, plus the English client locale and the list of map",
            "files in the client. Notes on what an area was meant to be come from its internal name or",
            "summary. Content that was released and later removed from the client cannot be seen here.",
            "Custom content of this server installation is excluded.", ""]

    OUTPUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
