import csv
import html
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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
    (1303, "Keelhaul Canyon Racetrack", "Racetrack"),
    (1350, "Chantey Shanty", "Property"),
    (1400, "Forbidden Valley", "World"),
    (1401, "Forbidden Valley Siege", "Activity"),
    (1402, "Forbidden Valley Dragon Battle", "Activity"),
    (1403, "Dragonmaw Chasm Racetrack", "Racetrack"),
    (1450, "Raven Bluff", "Property"),
    (1600, "Starbase 3001", "World"),
    (1700, "LEGO Club", "Historical destination"),
    (1800, "Crux Prime", "World"),
    (1900, "Nexus Tower", "World"),
    (2000, "Ninjago Monastery", "World"),
    (2001, "Battle Against Frakjaw", "Activity"),
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


def build_skills(root, tables, evidence):
    output = root / "wiki" / "skills"
    output.mkdir(parents=True, exist_ok=True)
    item_pages = {path.stem for path in (root / "wiki" / "items").glob("*.md")}
    skills, objects, equip, sets = player_skill_data(tables, item_pages)
    check_stale_pages(output, skills)
    names = validate_skill_names(evidence, skills)
    definitions = {row["skillID"]: row for row in tables["SkillBehavior"]}
    index = [
        "# Player Skill Database", "",
        "[Game Guide](../README.md) | [Items](../items/README.md) | "
        "[Faction guide](../Faction%20Guide.md) | [Methodology](./Methodology.md)", "",
        "Browse skill IDs connected to equipment slots or equipment-set bonuses. "
        "Some entries have a **community name candidate** based on an equipment "
        "cross-reference, not a verified localized client name. Others remain "
        "unnamed. These are candidates, not a complete list of every player "
        "ability or proof that an item works on your server.", "",
        f"Community-name candidates: **{len(names)} of {len(skills)} skills**. "
        "See each named page for the source and item match.", "",
        "Equipment and set references are static associations, not instructions "
        "for obtaining or unlocking an ability. Item pages provide acquisition evidence.", "",
        "| Skill ID | Name | Equipment examples | Set associations |",
        "| --- | --- | --- | --- |",
    ]
    for skill in sorted(skills, key=int):
        data = skills[skill]
        candidate = names.get(skill)
        name = escape(candidate["name"]) if candidate else ""
        items = sorted(data["items"], key=int)
        examples = ", ".join(item_link(lot, objects, item_pages) for lot in items[:3])
        if len(items) > 3:
            examples += f" and {len(items) - 3} more"
        label = f"[{name}](./{skill}.md) (candidate)" if candidate else "Name unknown"
        index.append(f"| [{skill}](./{skill}.md) | {label} | {examples or 'None recorded'} | {len(data['sets'])} |")
        definition = definitions.get(skill)
        lines = [
            f"# {name}" if candidate else f"# Skill {skill}", "",
            "[Player skills](./README.md) | [Methodology](./Methodology.md)", "",
        ]
        if candidate:
            source = evidence["sources"][candidate["source"]]
            item = item_link(candidate["item"], objects, item_pages)
            lines += [
                f"**Skill ID:** {skill}", "",
                f"**Community name candidate:** {name}. "
                f"[{escape(source['label'])}]({source['url']}) associates this "
                f"name with {escape(candidate['community_item'])}; the local data "
                f"associates {item} with skill {skill}. This indirect match is "
                "not a verified localized client name and could refer to another "
                "action of the item.", "",
            ]
        else:
            lines += [
                "This is a candidate player skill linked to equipment or a set bonus. "
                "Its localized name and complete effect are not established by this index.", "",
            ]
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
        "or activity is available on your server.", "",
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


def main():
    database = ROOT / "db"
    names = ("Objects", "ItemComponent", "ComponentsRegistry", "ObjectSkills",
             "ItemSetSkills", "ItemSets", "SkillBehavior", "ZoneTable")
    tables = {name: load_table(database, name) for name in names}
    evidence = json.loads(Path(__file__).with_name("skill_name_evidence.json").read_text(encoding="utf-8"))
    print(f"Built {build_skills(ROOT, tables, evidence)} skill pages and {build_zones(ROOT, tables)} zone pages.")


if __name__ == "__main__":
    main()
