"""Regenerate wiki/zones pages with official English client strings.

Reads the client locale (locale.xml) and the SQLite copy of the client
database (CDServer.sqlite) and rewrites wiki/zones/<zoneID>.md plus
wiki/zones/README.md. The output is deterministic, so the script is
idempotent: running it twice produces identical files.

Usage:
    py -3 scripts/enrich_zones.py [--locale PATH] [--db PATH]

Custom developer content (zone 1650 "Lego City", LOT 16900) is deliberately
excluded.
"""

import argparse
import html
import re
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

import game_paths  # location of the unmodified game data


ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = ROOT.parent
DEFAULT_LOCALE = game_paths.LOCALE
DEFAULT_DB = game_paths.CDSERVER_DB

# (zoneID, fallback name, kind). Names are replaced by the official English
# client string when one exists. Excluded on purpose: test/dev maps, the
# unreleased large properties (1152, 1252, 1352), 1202, 1452, 1801, the
# "LUP Station" temp map 1500, the asset-less 20000-series rows and the
# custom zone 1650.
ZONES = (
    (1000, "Venture Explorer", "World"),
    (1001, "Return to the Venture Explorer", "Instance"),
    (1100, "Avant Gardens", "World"),
    (1101, "Avant Gardens Survival", "Activity"),
    (1102, "Spider Queen Battle", "Activity"),
    (1150, "Block Yard", "Property"),
    (1151, "Avant Grove", "Property"),
    (1200, "Nimbus Station", "World"),
    (1201, "Pet Cove", "World"),
    (1203, "Vertigo Loop Racetrack", "Racetrack"),
    (1204, "The Battle of Nimbus Station", "Activity"),
    (1250, "Nimbus Rock", "Property"),
    (1251, "Nimbus Isle", "Property"),
    (1261, "Space Blizzard Racetrack", "Seasonal racetrack"),
    (1300, "Gnarled Forest", "World"),
    (1301, "Gnarled Forest Survival", "Activity"),
    (1302, "Cannon Cove Shooting Gallery", "Activity"),
    (1303, "Keelhaul Canyon Racetrack", "Racetrack"),
    (1350, "Chantey Shanty", "Property"),
    (1400, "Forbidden Valley", "World"),
    (1401, "Forbidden Valley Siege", "Activity"),
    (1402, "Forbidden Valley Dragon Battle", "Activity"),
    (1403, "Dragonmaw Chasm Racetrack", "Racetrack"),
    (1450, "Raven Bluff", "Property"),
    (1600, "Starbase 3001", "World"),
    (1601, "DeepFreeze", "World Builder Planet"),
    (1602, "Robot City", "World Builder Planet"),
    (1603, "MoonBase", "World Builder Planet"),
    (1604, "Portabello", "World Builder Planet"),
    (1700, "LEGO Club", "Historical destination"),
    (1800, "Crux Prime", "World"),
    (1900, "Nexus Tower", "World"),
    (2000, "Ninjago Monastery", "World"),
    (2001, "Battle Against Frakjaw!", "Activity"),
)
EXCLUDED = {1650}
TRACKS = {
    1203: "vertigo-loop",
    1261: "space-blizzard",
    1303: "keelhaul-canyon",
    1403: "dragonmaw-chasm",
}
# Zone 1261 has no ZoneTable row; its official name is the activity name.
ACTIVITY_NAMES = {1261: 60}
# ZoneTable row whose map file matches the 1261 track asset.
WINTER_TRACK_ROW = 556

STATUS_SHORT = {
    2: "Released",
    1: "Not fully released (locStatus 1)",
    0: "Unreleased (locStatus 0)",
}


def escape(value):
    text = html.escape(str(value), quote=False).replace("\r", " ").replace("\n", " ")
    return re.sub(r"[\\|`*_\[\]~]", lambda match: f"&#{ord(match.group())};", text)


def load_locale(path):
    wanted = ("ZoneTable_", "ZoneLoadingTips_", "Activities_")
    strings = {}
    for _, element in ET.iterparse(path, events=("end",)):
        if element.tag != "phrase":
            continue
        key = element.get("id", "")
        if key.startswith(wanted):
            for translation in element.findall("translation"):
                if translation.get("locale") == "en_US" and translation.text:
                    strings[key] = translation.text.strip()
        element.clear()
    return strings


def load_db(path):
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        zones = {row[0]: {"locStatus": row[1], "mapFolder": row[2], "name": row[3]}
                 for row in connection.execute(
                     "SELECT zoneID, locStatus, zoneName, DisplayDescription FROM ZoneTable")}
        tips = {}
        for tip_id, zone in connection.execute(
                "SELECT id, zoneid FROM ZoneLoadingTips WHERE zoneid > 0 AND locStatus = 2 ORDER BY id"):
            tips.setdefault(zone, []).append(tip_id)
        activities = {row[0]: {"locStatus": row[1], "instanceMapID": row[2]}
                      for row in connection.execute(
                          "SELECT ActivityID, locStatus, instanceMapID FROM Activities")}
    finally:
        connection.close()
    return zones, tips, activities


def evidence_links(root, zone):
    links = []
    for directory, label in (("quests", "Quest locations"), ("items", "Item sources"), ("pets", "Pet locations")):
        target = root / "wiki" / directory / "locations" / f"zone-{zone}.md"
        if target.is_file():
            links.append((label, f"../{directory}/locations/zone-{zone}.md"))
    if zone in TRACKS:
        target = root / "wiki" / "racing" / "tracks" / f"{TRACKS[zone]}.md"
        if not target.is_file():
            raise FileNotFoundError(target)
        links.append(("Racing details and entry evidence", f"../racing/tracks/{TRACKS[zone]}.md"))
    return links


def status_lines(zone, row, strings, zones, activities):
    if row is None:
        activity_id = ACTIVITY_NAMES[zone]
        activity = activities.get(activity_id, {})
        winter = zones.get(WINTER_TRACK_ROW)
        lines = [
            "- **Release status:** No ZoneTable row exists for this ID, so the "
            "client has no zone-level status for it. The ID is the instance map of "
            f"activity {activity_id} (activity `locStatus` {activity.get('locStatus')}), "
            "which also supplies the official name.",
        ]
        if winter:
            map_file = winter["mapFolder"].replace("\\", "/").rsplit("/", 1)[-1]
            lines.append(
                f"- **Related ZoneTable row:** zone {WINTER_TRACK_ROW}, internal name "
                f"&quot;{escape(winter['name'])}&quot;, references the same map file "
                f"(`{map_file}`) under a different folder. That row has `locStatus` "
                f"{winter['locStatus']} (unreleased) and no localized client name, so "
                "it is not listed as a separate zone page.")
        return lines
    status = row["locStatus"]
    if status == 2:
        text = "Released: ZoneTable `locStatus` 2."
    elif status == 1:
        text = ("Not flagged as fully released: ZoneTable `locStatus` 1. The client "
                "still ships an official localized name for it.")
    else:
        text = ("Unreleased: ZoneTable `locStatus` 0 and no localized client name. "
                "The row references a map file, but it was not flagged for release in "
                "this client build.")
    return [f"- **Release status:** {text}"]


def activity_lines(zone, strings, activities):
    lines = []
    for activity_id in sorted(a for a, data in activities.items() if data["instanceMapID"] == zone):
        name = strings.get(f"Activities_{activity_id}_ActivityName")
        label = f" — {escape(name)}" if name else ""
        status = activities[activity_id]["locStatus"]
        lines.append(f"- **Activity:** {activity_id}{label} (Activities `instanceMapID` {zone}, activity `locStatus` {status})")
    return lines


def official_name(zone, row, strings, fallback):
    if zone in ACTIVITY_NAMES:
        key = f"Activities_{ACTIVITY_NAMES[zone]}_ActivityName"
        return strings.get(key, fallback), key
    key = f"ZoneTable_{zone}_DisplayDescription"
    if key in strings:
        return strings[key], key
    return (row["name"] if row and row["name"] else fallback), None


def build(root, strings, zones, tips, activities):
    output = root / "wiki" / "zones"
    output.mkdir(parents=True, exist_ok=True)
    index = [
        "# Worlds, Zones, and Maps", "",
        "[Game Guide](../README.md) | [Worlds guide](../Worlds%20Guide.md) | "
        "[Methodology](./Methodology.md)", "",
        "Browse a curated selection of known worlds, activity instances, "
        "properties, World Builder Planets, and historical destinations. Names "
        "are the official English client strings. These pages link to existing "
        "textual map evidence; they do not include original map graphics.", "",
        "A record or mapped placement does not guarantee that the area, entrance, "
        "or activity is available on your server. The status column reflects the "
        "client ZoneTable `locStatus` flag; see [Methodology](./Methodology.md).", "",
        "| Zone | Kind | Status | Related location evidence |",
        "| --- | --- | --- | --- |",
    ]
    for zone, fallback, kind in ZONES:
        if zone in EXCLUDED:
            raise ValueError(f"Zone {zone} is excluded custom content")
        row = zones.get(zone)
        if row is None and zone not in ACTIVITY_NAMES:
            raise KeyError(f"Zone {zone} has no ZoneTable row")
        name, name_key = official_name(zone, row, strings, fallback)
        summary = strings.get(f"ZoneTable_{zone}_summary")
        links = evidence_links(root, zone)
        if row is None:
            status = "No ZoneTable row (activity instance)"
        else:
            status = STATUS_SHORT.get(row["locStatus"], f"locStatus {row['locStatus']}")
        refs = f"{len(links)} reference" + ("" if len(links) == 1 else "s")
        index.append(f"| [{escape(name)} ({zone})](./{zone}.md) | {kind} | {status} | {refs} |")

        lines = [
            f"# {escape(name)} — zone {zone}", "",
            "[Zones and maps](./README.md) | [Worlds guide](../Worlds%20Guide.md)", "",
            f"**Category:** {kind}. **Zone / instance ID:** {zone}.", "",
        ]
        if summary:
            lines += [f"> {escape(summary)}", ""]
        lines += ["## Official client text", ""]
        if name_key:
            lines.append(f"- **Name:** {escape(name)} (`{name_key}`)")
        else:
            lines.append(f"- **Name:** {escape(name)} (internal ZoneTable name; no localized client string)")
        if summary:
            lines.append(f"- **Summary:** {escape(summary)} (`ZoneTable_{zone}_summary`)")
        lines += status_lines(zone, row, strings, zones, activities)
        lines += activity_lines(zone, strings, activities)
        lines.append("")
        for tip_id in tips.get(zone, []):
            title = strings.get(f"ZoneLoadingTips_{tip_id}_title")
            texts = [strings.get(f"ZoneLoadingTips_{tip_id}_tip{n}") for n in (1, 2)]
            texts = [text for text in texts if text]
            if not title and not texts:
                continue
            lines += ["### Loading screen tip", ""]
            if title:
                lines.append(f"**{escape(title)}**")
                lines.append("")
            lines += [f"- {escape(text)}" for text in texts]
            lines.append("")
        lines += ["## Explore the evidence", ""]
        if row is not None:
            lines += ["This ID has a ZoneTable record in the local snapshot.", ""]
        else:
            lines += [
                "No ZoneTable row was found for this ID in the snapshot. "
                "The linked racing page describes the separate seasonal asset evidence.", "",
            ]
        lines += [f"- [{label}]({target})" for label, target in links]
        if not links:
            lines.append("- No linked location evidence is available in this catalog.")
        lines += [
            "", "Quest associations can reflect an objective or mapped candidate, "
            "not necessarily a quest start. Item and pet coordinates are static "
            "map evidence, not guaranteed active spawns. See each linked page "
            "for conditions and limitations.", "",
        ]
        (output / f"{zone}.md").write_text("\n".join(lines), encoding="utf-8")
    (output / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return len(ZONES)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--locale", type=Path, default=DEFAULT_LOCALE)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = parser.parse_args()
    strings = load_locale(args.locale)
    zones, tips, activities = load_db(args.db)
    count = build(ROOT, strings, zones, tips, activities)
    print(f"Wrote {count} zone pages and README.md")


if __name__ == "__main__":
    main()
