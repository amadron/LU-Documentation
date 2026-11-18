"""Build the player skill (wiki/skills/) and zone (wiki/zones/) reference pages.

Usage (from the documentation root, with the table exports in db/*.csv):
    py -3 scripts/build_player_references.py [locale.xml]

Skill names and tooltips come from the English (en_US) client locale; the default
path is ../client/locale/locale.xml next to the documentation root.
"""

import csv
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import game_paths  # location of the unmodified game data


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCALE = game_paths.LOCALE
SKILL_KEY = re.compile(r"SkillBehavior_(\d+)_(name|descriptionUI)$")
# Labels for the tokens in client tooltips such as "%(DamageCombo) 1+2+3 %(ChargeUp)...".
# AltCombo values appear on Ninjago-era equipment and Spinjitzu skills; the client rollover labels that line
# "Skeletons Combo" (UI_ITEM_ROLLOVER_SKELETON_COMBO).
TOOLTIP_LABELS = {
    "DamageCombo": "Damage",
    "AltCombo": "Damage vs. Skeletons",
    "ChargeUp": "Charge attack",
}
SLOTS = {"special_r", "special_l", "hair", "clavicle"}
NON_PLAYER_NAME = re.compile(r"\b(?:test|unused|debug|proxy|gm|developer)\b", re.I)
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
TRACKS = {
    1203: "vertigo-loop",
    1261: "space-blizzard",
    1303: "keelhaul-canyon",
    1403: "dragonmaw-chasm",
}


def load_table(database, name):
    with (database / f"{name}.csv").open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def escape(value):
    text = html.escape(str(value), quote=False).replace("\r", " ").replace("\n", " ")
    return re.sub(r"[\\|`*_\[\]~]", lambda match: f"&#{ord(match.group())};", text)


def escape_block(value):
    """Escape text that starts a Markdown line so it cannot become a list, heading, or quote."""
    text = escape(value)
    if re.match(r"[-+#](?:\s|$)|\d+[.)](?:\s|$)", text):
        text = f"&#{ord(text[0])};{text[1:]}"
    return text


def load_skill_locale(path, language="en_US"):
    """Return {skill_id: {"name": ..., "description": ...}} from the client locale.xml."""
    result = defaultdict(dict)
    for _, element in ET.iterparse(path):
        if element.tag != "phrase":
            continue
        match = SKILL_KEY.match(element.get("id", ""))
        if match:
            for translation in element.findall("translation"):
                if translation.get("locale") == language and (translation.text or "").strip():
                    field = "name" if match.group(2) == "name" else "description"
                    result[match.group(1)][field] = translation.text.strip()
        element.clear()
    return dict(result)


def _sentence(text):
    return text if text.endswith((".", "!", "?")) else f"{text}."


def render_tooltip(text):
    """Turn '%(DamageCombo) 1+2+3 %(ChargeUp)Blocks attacks' into 'Damage: 1+2+3. Charge attack: Blocks attacks.'"""
    text = " ".join((text or "").split())
    if not text:
        return ""
    parts = []
    lead = re.split(r"%\(\w+\)", text, maxsplit=1)[0].strip()
    if lead:
        parts.append(_sentence(lead))
    for key, value in re.findall(r"%\((\w+)\)([^%]*)", text):
        value = value.strip()
        if value:
            label = TOOLTIP_LABELS.get(key)
            parts.append(f"{label}: {_sentence(value)}" if label else _sentence(value))
    return " ".join(parts)


def official_skill(locale, skill):
    entry = (locale or {}).get(skill, {})
    return entry.get("name", ""), render_tooltip(entry.get("description", ""))


def skill_header(skill, official, description, candidate, source, item):
    """Lines from the page title up to (not including) '## Recorded settings'.

    official/description: client locale name and rendered tooltip ("" if absent).
    candidate/source/item: community-name evidence, its source entry, and the
    rendered link to the matched item (None when there is no evidence).
    """
    community = escape(candidate["name"]) if candidate else ""
    title = escape(official) if official else community or f"Skill {skill}"
    lines = [f"# {title}", "", "[Player skills](./README.md) | [Methodology](./Methodology.md)", ""]
    evidence = ""
    if candidate:
        evidence = (
            f"[{escape(source['label'])}]({source['url']}) associates this name with "
            f"{escape(candidate['community_item'])}; the local data associates {item} "
            f"with skill {skill}."
        )
    if official:
        lines += [f"**Skill ID:** {skill}", "", "## Description", ""]
        lines.append(escape_block(description) if description else "The client locale has no English tooltip for this skill.")
        lines += ["", "Name and tooltip: official English client text (`locale.xml`, `en_US`).", ""]
        if candidate and candidate["name"].strip().casefold() != official.strip().casefold():
            lines += [
                f"**Historical community name:** {community}. {evidence} "
                "This indirect equipment match differs from the official client "
                "name, which takes precedence.", "",
            ]
    elif candidate:
        lines += [
            f"**Skill ID:** {skill}", "",
            f"**Community name candidate:** {community}. {evidence} This indirect "
            "match is not a verified localized client name and could refer to "
            "another action of the item.", "",
        ]
    else:
        lines += [
            "This is a candidate player skill linked to equipment or a set bonus. "
            "The client locale has no English name or tooltip for this skill ID, "
            "and its complete effect is not established by this index.", "",
        ]
    return lines


def skill_index_label(skill, official, candidate):
    if official:
        return f"[{escape(official)}](./{skill}.md)"
    if candidate:
        return f"[{escape(candidate['name'])}](./{skill}.md) (community candidate)"
    return "Name unknown"


def skill_index_intro(total, official, historical, candidates):
    lines = [
        "# Player Skill Database", "",
        "[Game Guide](../README.md) | [Items](../items/README.md) | "
        "[Faction guide](../Faction%20Guide.md) | [Methodology](./Methodology.md)", "",
        "Browse skill IDs connected to equipment slots or equipment-set bonuses. "
        "Names and descriptions are the official English client text from "
        "`locale.xml`; skills without a localized name are listed by ID. These "
        "are candidates, not a complete list of every player ability or proof "
        "that an item works on your server.", "",
        f"Official client names and tooltips: **{official} of {total} skills**. "
        f"Unnamed: **{total - official - candidates}**.",
    ]
    if candidates:
        lines[-1] += f" Community-name candidates without a client name: **{candidates}**."
    if historical:
        lines[-1] += (f" {historical} pages also keep a differing historical "
                      "community name with its source.")
    lines += [
        "",
        "Equipment and set references are static associations, not instructions "
        "for obtaining or unlocking an ability. Item pages provide acquisition evidence.", "",
        "| Skill ID | Name | Equipment examples | Set associations |",
        "| --- | --- | --- | --- |",
    ]
    return lines


def skill_name_counts(skills, locale, names):
    official = historical = candidates = 0
    for skill in skills:
        name = official_skill(locale, skill)[0]
        candidate = names.get(skill)
        if name:
            official += 1
            if candidate and candidate["name"].strip().casefold() != name.strip().casefold():
                historical += 1
        elif candidate:
            candidates += 1
    return official, historical, candidates


def name_of(row):
    return row.get("displayName", "").strip() or row.get("name", "").strip()


def is_technical_name(row):
    return any(NON_PLAYER_NAME.search(row.get(key, "")) for key in ("name", "displayName"))


def player_skill_data(tables, item_pages):
    objects = {row["id"]: row for row in tables["Objects"]}
    components = {row["id"]: row for row in tables["ItemComponent"]}
    equip = {}
    for row in tables["ComponentsRegistry"]:
        item = components.get(row["component_id"])
        obj = objects.get(row["id"])
        if (row["component_type"] == "11" and item and obj
                and item["equipLocation"] in SLOTS and name_of(obj)
                and not is_technical_name(obj)
                and row["id"] in item_pages):
            equip[row["id"]] = item["equipLocation"]

    skills = defaultdict(lambda: {"items": set(), "sets": set()})
    for row in tables["ObjectSkills"]:
        if row["castOnType"] == "0" and row["objectTemplate"] in equip:
            skills[row["skillID"]]["items"].add(row["objectTemplate"])

    by_set = defaultdict(list)
    for row in tables["ItemSetSkills"]:
        by_set[row["SkillSetID"]].append(row["SkillID"])
    sets = {}
    for row in tables["ItemSets"]:
        lots = [lot.strip() for lot in row["itemIDs"].split(",") if lot.strip()]
        members = [objects[lot] for lot in lots if lot in objects]
        if not members or any(is_technical_name(member) for member in members):
            continue
        sets[row["setID"]] = lots
        for count in range(2, 7):
            for skill in by_set[row[f"skillSetWith{count}"]]:
                skills[skill]["sets"].add((row["setID"], count))
    return dict(skills), objects, equip, sets


def item_link(lot, objects, item_pages):
    name = escape(name_of(objects.get(lot, {})) or f"LOT {lot}")
    if lot in item_pages:
        return f"[{name} (LOT {lot})](../items/{lot}.md)"
    return f"{name} (LOT {lot}; item page unavailable)"


def check_stale_pages(output, expected):
    existing = {path.stem for path in output.glob("[0-9]*.md") if path.stem.isdigit()}
    stale = sorted(existing - set(expected), key=int)
    if stale:
        raise RuntimeError(f"Obsolete generated pages in {output}: {', '.join(stale)}. Review and remove them before rebuilding.")


def validate_skill_names(evidence, skills):
    results = {}
    for candidate in evidence["names"]:
        skill = candidate["id"]
        if skill in results:
            raise ValueError(f"Duplicate community-name candidate for skill {skill}")
        if skill not in skills or candidate["item"] not in skills[skill]["items"]:
            raise ValueError(f"Skill {skill} is not associated with item {candidate['item']}")
        if candidate["source"] not in evidence["sources"]:
            raise ValueError(f"Missing source for skill {skill}")
        if not candidate["name"].strip() or not candidate["community_item"].strip():
            raise ValueError(f"Incomplete community-name evidence for skill {skill}")
        results[skill] = candidate
    return results


def build_skills(root, tables, evidence, locale=None):
    """Write wiki/skills/. locale is the result of load_skill_locale() (None = no client names)."""
    output = root / "wiki" / "skills"
    output.mkdir(parents=True, exist_ok=True)
    item_pages = {path.stem for path in (root / "wiki" / "items").glob("*.md")}
    skills, objects, equip, sets = player_skill_data(tables, item_pages)
    check_stale_pages(output, skills)
    names = validate_skill_names(evidence, skills)
    definitions = {row["skillID"]: row for row in tables["SkillBehavior"]}
    index = skill_index_intro(len(skills), *skill_name_counts(skills, locale, names))
    for skill in sorted(skills, key=int):
        data = skills[skill]
        candidate = names.get(skill)
        official, description = official_skill(locale, skill)
        items = sorted(data["items"], key=int)
        examples = ", ".join(item_link(lot, objects, item_pages) for lot in items[:3])
        if len(items) > 3:
            examples += f" and {len(items) - 3} more"
        label = skill_index_label(skill, official, candidate)
        index.append(f"| [{skill}](./{skill}.md) | {label} | {examples or 'None recorded'} | {len(data['sets'])} |")
        definition = definitions.get(skill)
        source = evidence["sources"][candidate["source"]] if candidate else None
        item = item_link(candidate["item"], objects, item_pages) if candidate else None
        lines = skill_header(skill, official, description, candidate, source, item)
        lines += ["## Recorded settings", ""]
        if definition:
            lines += [
                f"- **Imagination cost (client data):** {escape(definition['imaginationcost'] or 'not recorded')}",
                f"- **Cooldown value (client data):** {escape(definition['cooldown'] or 'not recorded')}",
                "",
                "These are stored values, not measured live behavior; set bonuses "
                "and equipment casts can follow different server paths.", "",
            ]
        else:
            lines += ["No matching SkillBehavior definition was found; cost and cooldown are unknown.", ""]
        lines += ["## Equipment associations", ""]
        if items:
            lines += [
                "These items have an ObjectSkills cast-on-type 0 association and a "
                "supported equipment slot. Follow each item link for source and requirement evidence.", "",
            ]
            lines += [
                f"- {item_link(lot, objects, item_pages)} — slot `{equip[lot]}`"
                for lot in items
            ]
            lines.append("")
        else:
            lines += ["No qualifying direct equipment association was found.", ""]
        lines += ["## Equipment-set associations", ""]
        if data["sets"]:
            for set_id, count in sorted(data["sets"], key=lambda pair: (int(pair[0]), pair[1])):
                links = ", ".join(item_link(lot, objects, item_pages) for lot in sets[set_id])
                lines.append(f"- **Set {set_id}, {count} equipped pieces:** {links}")
            lines.append("")
        else:
            lines += ["No qualifying set association was found.", ""]
        lines += [
            "A listed association does not establish that the skill, item, or set "
            "is obtainable or fully implemented in a particular deployment.", "",
        ]
        (output / f"{skill}.md").write_text("\n".join(lines), encoding="utf-8")
    (output / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return len(skills)


def build_zones(root, tables):
    output = root / "wiki" / "zones"
    output.mkdir(parents=True, exist_ok=True)
    check_stale_pages(output, (str(zone) for zone, _, _ in ZONES))
    zone_ids = {row["zoneID"] for row in tables["ZoneTable"]}
    index = [
        "# Worlds, Zones, and Maps", "",
        "[Game Guide](../README.md) | [Worlds guide](../Worlds%20Guide.md) | "
        "[Methodology](./Methodology.md)", "",
        "Browse a curated selection of known worlds, activity instances, "
        "properties, and historical destinations. These pages link to existing "
        "textual map evidence; they do not include original map graphics.", "",
        "A record or mapped placement does not guarantee that the area, entrance, "
        "or activity is available on your server. Neither catalog inclusion nor "
        "`locStatus` proves that the server can load or players can reach the map; "
        "see the methodology for the distinction.", "",
        "| Zone | Kind | Related location evidence |",
        "| --- | --- | --- |",
    ]
    for zone, name, kind in ZONES:
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
        index.append(f"| [{escape(name)} ({zone})](./{zone}.md) | {kind} | {len(links)} references |")
        lines = [
            f"# {escape(name)} — zone {zone}", "",
            "[Zones and maps](./README.md) | [Worlds guide](../Worlds%20Guide.md)", "",
            f"**Category:** {kind}. **Zone / instance ID:** {zone}.", "",
            "## Explore the evidence", "",
        ]
        if str(zone) in zone_ids:
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


def load_evidence():
    return json.loads(Path(__file__).with_name("skill_name_evidence.json").read_text(encoding="utf-8"))


def main():
    database = ROOT / "db"
    locale_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOCALE
    if not locale_path.is_file():
        raise SystemExit(f"Client locale not found: {locale_path} (pass the locale.xml path as an argument)")
    names = ("Objects", "ItemComponent", "ComponentsRegistry", "ObjectSkills",
             "ItemSetSkills", "ItemSets", "SkillBehavior", "ZoneTable")
    tables = {name: load_table(database, name) for name in names}
    locale = load_skill_locale(locale_path)
    print(f"Built {build_skills(ROOT, tables, load_evidence(), locale)} skill pages and {build_zones(ROOT, tables)} zone pages.")
    # build_zones writes plain pages; enrich_zones adds the official client text, release status,
    # and loading tips on top (it reads locale.xml and the CDServer database).
    import enrich_zones
    strings = enrich_zones.load_locale(locale_path)
    zones, tips, activities = enrich_zones.load_db(enrich_zones.DEFAULT_DB)
    print(f"Enriched {enrich_zones.build(ROOT, strings, zones, tips, activities)} zone pages.")


if __name__ == "__main__":
    main()
