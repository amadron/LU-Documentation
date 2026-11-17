"""Enrich the generated item database (wiki/items/) with official English client strings.

The item pages were generated from the client database without the client
locale. This script updates them in place (idempotently) from:

* ``client/locale/locale.xml`` (en_US): ``Objects_<LOT>_name``,
  ``Objects_<LOT>_description`` and ``Missions_<id>_name``;
* ``server/resServer/CDServer.sqlite``: raw ``Objects.name`` /
  ``Objects.description`` for the "internal" fallbacks.

Changes:

* item title -> client name when it differs (the DB name stays visible in the
  field table as "Internal name"); link labels ``[Name (LOT n)](n.md)`` in the
  item folder, the type indexes and Item Summary.csv follow the new name;
* "Description" section -> localized tooltip; the raw DB description is shown
  as "Internal description" only when it differs; the "raw client object
  description" disclaimer remains only for items without a localized tooltip;
* reward tables: "Mission n" / "Achievement n" / "Mission mail n" get the
  localized mission title appended ("Mission 482: A Thunderous Collection");
* README.md coverage table, Item Summary.csv (DescriptionSource column) and
  Methodology.md describe the locale source.

Usage:
    py -3 scripts/enrich_items.py [--locale PATH] [--db PATH]
"""

import argparse
import csv
import html
import io
import re
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

import game_paths  # location of the unmodified game data

ROOT = Path(__file__).resolve().parent.parent
GAME_ROOT = ROOT.parent
ITEMS = ROOT / "wiki" / "items"
DEFAULT_LOCALE = game_paths.LOCALE
DEFAULT_DB = game_paths.CDSERVER_DB

# Custom development content that must never appear in the generated database.
IGNORED_LOTS = {16900}

RAW_DISCLAIMER = ("The text above is the raw client object description; it may be internal "
                  "text rather than a localized player tooltip.")
LOCALE_NOTE = "Player tooltip: official English client text (`locale.xml`, `en_US`)."
NO_DESCRIPTION = "No client object description is present in this snapshot."


# --------------------------------------------------------------------------- text helpers

def escape(value):
    """Escape like the generated pages: HTML entities for Markdown-sensitive characters."""
    text = html.escape(str(value), quote=False).replace("\r", " ").replace("\n", " ")
    return re.sub(r"[\\|`*_\[\]~]", lambda match: f"&#{ord(match.group())};", text)


def escape_block(value):
    """Escape text that starts a Markdown line so it cannot become a list, heading, or quote."""
    text = escape(value)
    if re.match(r"[-+#>]|\d+[.)]", text):
        text = f"&#{ord(text[0])};{text[1:]}"
    return text


def clean(value):
    """Strip client markup: <font>/other tags, %(...) tokens, literal and real line breaks."""
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\\n", " ").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"</?(?:font|b|i|u|br|color)\b[^>]*>", "", text, flags=re.I)
    text = re.sub(r"%\(([^)]*)\)[a-z]?", lambda m: f"<{m.group(1)}>", text)
    return re.sub(r"\s+", " ", text).strip()


def same_text(rendered, plain):
    """True when an already-escaped Markdown fragment shows the given plain text."""
    return html.unescape(rendered).strip() == plain


# --------------------------------------------------------------------------- data

def load_locale(path):
    strings = {}
    wanted = re.compile(r"(Objects_\d+_(?:name|description)|Missions_\d+_name)$")
    for _, element in ET.iterparse(path):
        if element.tag != "phrase":
            continue
        key = element.get("id") or ""
        if wanted.match(key):
            for translation in element.findall("translation"):
                if translation.get("locale") == "en_US" and (translation.text or "").strip():
                    strings[key] = clean(translation.text)
        element.clear()
    return strings


def load_objects(db_path):
    with sqlite3.connect(db_path) as connection:
        return {row[0]: (row[1] or "", row[2] or "") for row in
                connection.execute("SELECT id, name, description FROM Objects")}


# --------------------------------------------------------------------------- file IO (CRLF)

def read_text(path):
    with open(path, encoding="utf-8", newline="") as handle:
        raw = handle.read()
    return raw.replace("\r\n", "\n"), "\r\n" in raw


def write_if_changed(path, text, crlf, original):
    if text == original:
        return False
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text.replace("\n", "\r\n") if crlf else text)
    return True


# --------------------------------------------------------------------------- page edits

class Stats:
    def __init__(self):
        self.names = 0
        self.descriptions = 0
        self.internal_descriptions = 0
        self.raw_kept = 0
        self.missions = 0
        self.mission_ids = set()
        self.missing_mission_names = set()
        self.links = 0


REWARD_ROW = re.compile(r"^\| (Mission mail|Mission|Achievement) (\d+)(?:: [^|]*?)? \|", re.M)
FACTION_MISSION = re.compile(r"mission \*\*(\d+)\*\*(?: \(([^)]*)\))?")
DESCRIPTION = re.compile(r"(## Description\n)(.*?)(\n\| Field \| Stored value \|)", re.S)
ITEM_LINK = re.compile(r"\[([^\]]*?) \(LOT (\d+)\)\]\(((?:\.\./)*)(\d+)\.md\)")


def mission_rows(text, strings, stats):
    def reward(match):
        kind, mission = match.group(1), int(match.group(2))
        name = strings.get(f"Missions_{mission}_name")
        if not name:
            stats.missing_mission_names.add(mission)
            return f"| {kind} {mission} |"
        stats.missions += 1
        stats.mission_ids.add(mission)
        return f"| {kind} {mission}: {escape(name)} |"

    def faction(match):
        mission = int(match.group(1))
        name = strings.get(f"Missions_{mission}_name")
        if not name:
            return match.group(0)
        stats.missions += 1
        stats.mission_ids.add(mission)
        return f"mission **{mission}** ({escape(name)})"

    return FACTION_MISSION.sub(faction, REWARD_ROW.sub(reward, text))


def description_block(lot, old_block, strings, objects, stats):
    tooltip = strings.get(f"Objects_{lot}_description")
    if not tooltip:
        if RAW_DISCLAIMER in old_block:
            stats.raw_kept += 1
        return old_block
    lines = [line for line in old_block.strip("\n").split("\n") if line.strip()]
    first = lines[0] if lines else ""
    shown = first if first and not first.startswith(NO_DESCRIPTION) and same_text(first, tooltip) \
        else escape_block(tooltip)
    parts = [shown, LOCALE_NOTE]
    raw = clean(objects.get(lot, ("", ""))[1])
    if raw and raw != tooltip:
        parts.append(f"**Internal description** (raw client database text): {escape(raw)}")
        stats.internal_descriptions += 1
    stats.descriptions += 1
    return "\n" + "\n\n".join(parts) + "\n"


def enrich_item_page(path, lot, strings, objects, names, stats):
    text, crlf = read_text(path)
    original = text
    lines = text.split("\n")
    if lines[0].startswith("# ") and lot in names:
        title = lines[0][2:]
        if not same_text(title, names[lot]):
            lines[0] = f"# {escape(names[lot])}"
            stats.names += 1
        text = "\n".join(lines)
    text = DESCRIPTION.sub(lambda m: m.group(1) + description_block(lot, m.group(2), strings, objects, stats)
                           + m.group(3), text, count=1)
    text = mission_rows(text, strings, stats)
    text = relabel_links(text, names, stats)
    return write_if_changed(path, text, crlf, original)


def relabel_links(text, names, stats):
    def label(match):
        lot = int(match.group(2))
        if lot != int(match.group(4)) or lot not in names or same_text(match.group(1), names[lot]):
            return match.group(0)
        stats.links += 1
        return f"[{escape(names[lot])} (LOT {lot})]({match.group(3)}{lot}.md)"
    return ITEM_LINK.sub(label, text)


def enrich_type_index(path, names, strings, stats):
    text, crlf = read_text(path)
    out = []
    for line in text.split("\n"):
        cells = line.split(" | ")
        match = re.match(r"\| (\d+)$", cells[0]) if len(cells) == 5 else None
        if match:
            lot = int(match.group(1))
            tooltip = strings.get(f"Objects_{lot}_description")
            if tooltip and not same_text(cells[3], tooltip):
                cells[3] = escape(tooltip)
            line = " | ".join(cells)
        out.append(line)
    new = relabel_links("\n".join(out), names, stats)
    return write_if_changed(path, new, crlf, text)


def enrich_summary_csv(path, names, strings, objects):
    with open(path, encoding="utf-8-sig", newline="") as handle:
        original = handle.read()
    rows = list(csv.reader(io.StringIO(original)))
    header = rows[0]
    if "DescriptionSource" not in header:
        header.append("DescriptionSource")
        for row in rows[1:]:
            row.append("")
    col = {name: index for index, name in enumerate(header)}
    for row in rows[1:]:
        lot = int(row[col["LOT"]])
        if lot in names:
            row[col["Name"]] = names[lot]
        tooltip = strings.get(f"Objects_{lot}_description")
        if tooltip:
            source = "locale.xml en_US"
            row[col["ClientDescription"]] = tooltip
        elif row[col["ClientDescription"]]:
            source = "Objects.description (raw, not localized)"
        else:
            source = ""
        row[col["DescriptionSource"]] = source
    buffer = io.StringIO()
    csv.writer(buffer, quoting=csv.QUOTE_ALL, lineterminator="\r\n").writerows(rows)
    if buffer.getvalue() == original:
        return False
    with open(path, "w", encoding="utf-8-sig", newline="") as handle:
        handle.write(buffer.getvalue())
    return True


def replace_once(text, old, new):
    return text.replace(old, new) if old in text else text


def enrich_readme(path, tooltip_count, name_count):
    text, crlf = read_text(path)
    row = "| Items with an official English tooltip (`locale.xml`, `en_US`) |"
    name_row = "| Items with an official English client name (`locale.xml`, `en_US`) |"
    text_new = re.sub(re.escape(row) + r" \d+ \|\n", "", text)
    text_new = re.sub(re.escape(name_row) + r" \d+ \|\n", "", text_new)
    anchor = "| Items with a client object description |"
    index = text_new.find(anchor)
    if index >= 0:
        end = text_new.index("\n", index) + 1
        text_new = (text_new[:end] + f"{name_row} {name_count} |\n" + f"{row} {tooltip_count} |\n"
                    + text_new[end:])
    return write_if_changed(path, text_new, crlf, text)


METHOD_OLD_SCOPE = ("Localized tooltips/mission titles were not available in a locale.xml file.")
METHOD_NEW_SCOPE = (
    "Item names, player tooltips, and mission/achievement titles come from the English client "
    "locale (`client/locale/locale.xml`, `en_US`: `Objects_<LOT>_name`, `Objects_<LOT>_description`, "
    "`Missions_<id>_name`), applied by `scripts/enrich_items.py`. Client markup (font tags, "
    "`%(...)` tokens, line breaks) is stripped. Fallbacks: without a localized name the page keeps "
    "the database display name (or internal name); without a localized tooltip the raw "
    "`Objects.description` is shown and labeled as raw client text; when a localized tooltip exists "
    "and the raw description differs, the raw text is kept as \"Internal description\". Missions "
    "without a localized title are shown by ID only.")
METHOD_OLD_MISSION = "IDs and type/subtype are shown because localized quest titles are unavailable."
METHOD_NEW_MISSION = ("IDs, localized mission/achievement titles (where `locale.xml` has one), and "
                      "type/subtype are shown.")


def enrich_methodology(path, stats_line):
    text, crlf = read_text(path)
    new = replace_once(text, METHOD_OLD_SCOPE, METHOD_NEW_SCOPE)
    new = replace_once(new, METHOD_OLD_MISSION, METHOD_NEW_MISSION)
    new = re.sub(r"\n- Localized client strings applied:[^\n]*\n", "\n", new)
    marker = "## Validation performed\n\n"
    if marker in new:
        new = new.replace(marker, marker + stats_line + "\n", 1)
    return write_if_changed(path, new, crlf, text)


# --------------------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--locale", type=Path, default=DEFAULT_LOCALE)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = parser.parse_args()
    for required in (args.locale, args.db):
        if not required.is_file():
            raise SystemExit(f"Input not found: {required}")

    strings = load_locale(args.locale)
    objects = load_objects(args.db)
    pages = {int(path.stem): path for path in ITEMS.glob("*.md") if path.stem.isdigit()}
    for lot in IGNORED_LOTS:
        pages.pop(lot, None)
    names = {lot: strings[f"Objects_{lot}_name"] for lot in pages if f"Objects_{lot}_name" in strings}

    stats = Stats()
    changed = 0
    for lot, path in sorted(pages.items()):
        changed += enrich_item_page(path, lot, strings, objects, names, stats)
    for path in sorted((ITEMS / "types").glob("*.md")):
        changed += enrich_type_index(path, names, strings, stats)
    for folder in ("sources", "locations"):
        for path in sorted((ITEMS / folder).glob("*.md")):
            text, crlf = read_text(path)
            new = mission_rows(relabel_links(text, names, stats), strings, stats)
            changed += write_if_changed(path, new, crlf, text)
    changed += enrich_summary_csv(ITEMS / "Item Summary.csv", names, strings, objects)

    tooltips = sum(1 for lot in pages if f"Objects_{lot}_description" in strings)
    changed += enrich_readme(ITEMS / "README.md", tooltips, len(names))
    stats_line = (f"- Localized client strings applied: {len(names)} item names, {tooltips} "
                  f"tooltips, {len(stats.mission_ids)} distinct mission/achievement titles "
                  f"({stats.missions} references).")
    changed += enrich_methodology(ITEMS / "Methodology.md", stats_line)

    print(f"Files changed: {changed}")
    print(f"Item pages: {len(pages)}; localized names: {len(names)}; titles changed: {stats.names}; "
          f"link labels changed: {stats.links}")
    print(f"Localized tooltips: {stats.descriptions}; internal descriptions shown: "
          f"{stats.internal_descriptions}; raw-only descriptions kept with disclaimer: {stats.raw_kept}")
    print(f"Mission/achievement references named: {stats.missions} "
          f"({len(stats.mission_ids)} distinct); without localized title: "
          f"{len(stats.missing_mission_names)} {sorted(stats.missing_mission_names)[:20]}")


if __name__ == "__main__":
    main()
