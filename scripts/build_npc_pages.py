"""Build per-template NPC and enemy reference pages.

Usage (from the documentation root):
    py -3 scripts/build_npc_pages.py

The generator reads the local, ignored NPC catalog CSV and the committed
world-marker CSV. It does not publish the source catalog itself.
"""

import csv
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = "LEGO Universe NPC List.csv"
MARKERS = Path("scripts") / "location_map_world_markers.csv"
OUTPUT = Path("wiki") / "npcs"
INDEX_SIZE = 200

ACTOR_TYPES = {
    "NPC": "NPC",
    "Enemies": "Enemy",
    "UserGeneratedNPCs": "User-created NPC",
}
MARKER_CATEGORIES = {"npcs", "enemies", "shops"}

IDENTITY_FIELDS = (
    ("Object type", "ObjectType"),
    ("Classification", "Classification"),
    ("Name source", "NameSource"),
    ("Registered NPC components", "NPCComponentMarkers"),
)
COMPONENT_FIELDS = (
    ("NPC template ID", "NpcTemplateID"),
    ("Minifigure component ID", "MinifigComponentID"),
    ("Combat AI component ID", "CombatAIComponentID"),
    ("Movement AI component ID", "MovementAIComponentID"),
    ("Mission offer component ID", "MissionOfferComponentID"),
    ("Pet component ID", "PetComponentID"),
    ("Pet creator component ID", "PetCreatorComponentID"),
    ("Possessable component ID", "PossessableComponentID"),
)
BEHAVIOR_FIELDS = (
    ("Combat behavior type", "CombatBehaviorType"),
    ("Combat role", "CombatRole"),
    ("Aggro radius", "AggroRadius"),
    ("Tether speed", "TetherSpeed"),
    ("Pursuit speed", "PursuitSpeed"),
    ("Soft tether radius", "SoftTetherRadius"),
    ("Hard tether radius", "HardTetherRadius"),
    ("Movement type", "MovementType"),
    ("Wander radius", "WanderRadius"),
    ("Wander speed", "WanderSpeed"),
    ("Wander chance", "WanderChance"),
    ("Attached path", "AttachedPath"),
    ("Pet form", "PetForm"),
    ("Pet element type", "PetElementType"),
    ("Pet tamability", "PetTamability"),
)
MISSION_FIELDS = (
    ("Mission IDs", "MissionIDs"),
    ("Missions offered", "MissionsOffered"),
    ("Missions accepted", "MissionsAccepted"),
    ("Mission details", "MissionDetails"),
)
INDEX_FILES = {
    "NPC": "npcs",
    "Enemies": "enemies",
    "UserGeneratedNPCs": "user-created-npcs",
}


def read_csv(path, required_fields):
    if not path.is_file():
        raise FileNotFoundError(f"Required NPC reference data not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not required_fields.issubset(reader.fieldnames or set()):
            raise ValueError(f"{path}: missing required columns")
        return list(reader)


def markdown_text(value):
    text = str(value).strip().replace("\r", " ").replace("\n", "<br>")
    return html.escape(text, quote=False).replace("|", "&#124;")


def markdown_link_text(value):
    return markdown_text(value).replace("[", "&#91;").replace("]", "&#93;")


def field_table(rows):
    present = [
        (label, markdown_text(value))
        for label, value in rows
        if str(value).strip()
    ]
    if not present:
        return ""
    lines = ["| Field | Recorded value |", "| --- | --- |"]
    lines.extend(f"| {label} | {value} |" for label, value in present)
    return "\n".join(lines)


def read_actors(path):
    rows = read_csv(path, {"LOT", "Name", "ObjectType", "Classification"})
    actors = {}
    for line_number, row in enumerate(rows, start=2):
        object_type = row["ObjectType"].strip()
        if object_type not in ACTOR_TYPES:
            continue
        try:
            lot = int(row["LOT"])
        except (TypeError, ValueError) as error:
            raise ValueError(f"{path}:{line_number}: invalid LOT {row['LOT']!r}") from error
        if lot in actors:
            raise ValueError(f"{path}:{line_number}: duplicate actor LOT {lot}")
        name = (
            row.get("Name", "").strip()
            or row.get("DisplayName", "").strip()
            or row.get("InternalName", "").strip()
            or f"Unresolved LOT {lot}"
        )
        actors[lot] = {
            "lot": lot,
            "name": name,
            "object_type": object_type,
            "row": row,
        }
    if not actors:
        raise ValueError(f"{path}: no NPC, enemy, or user-created NPC records found")
    return actors


def read_locations(path):
    rows = read_csv(path, {"zone", "category", "lot", "x", "y", "z", "details"})
    locations = {}
    for line_number, row in enumerate(rows, start=2):
        if row["category"] not in MARKER_CATEGORIES or not row["lot"].strip():
            continue
        try:
            lot = int(row["lot"])
            zone = int(row["zone"])
            position = tuple(float(row[axis]) for axis in ("x", "y", "z"))
        except (TypeError, ValueError) as error:
            raise ValueError(f"{path}:{line_number}: invalid actor location row") from error
        locations.setdefault(lot, []).append({
            "zone": zone,
            "category": row["category"],
            "position": position,
            "details": row["details"],
        })
    for rows_for_actor in locations.values():
        rows_for_actor.sort(key=lambda item: (
            item["zone"], item["category"], item["position"]
        ))
    return locations


def render_actor_page(actor, locations):
    lot = actor["lot"]
    row = actor["row"]
    name = markdown_text(actor["name"])
    lines = [
        f"# {name} (LOT {lot})",
        "",
        "[NPC and enemy catalog](./README.md) | "
        "[Quest NPC index](../quests/NPC%20Index.md) | "
        "[Pet database](../pets/README.md)",
        "",
        f"**Catalog type:** {ACTOR_TYPES[actor['object_type']]}",
        "",
        "This page describes a registered character or creature template. "
        "It is not a live entity or a guarantee that the template is enabled "
        "on a particular server.",
        "",
        "## Classification",
        "",
        field_table((("LOT", lot),) + tuple(
            (label, row.get(key, "")) for label, key in IDENTITY_FIELDS
        )),
    ]

    components = field_table(tuple(
        (label, row.get(key, "")) for label, key in COMPONENT_FIELDS
    ))
    if components:
        lines.extend(("", "## Component references", "", components))

    behavior = field_table(tuple(
        (label, row.get(key, "")) for label, key in BEHAVIOR_FIELDS
    ))
    if behavior:
        lines.extend((
            "",
            "## AI and creature data",
            "",
            behavior,
            "",
            "Values are recorded client catalog fields; numeric IDs and values "
            "are shown as stored and are not interpreted as guaranteed live "
            "server behavior.",
        ))

    missions = field_table(tuple(
        (label, row.get(key, "")) for label, key in MISSION_FIELDS
    ))
    if missions:
        lines.extend(("", "## Mission associations", "", missions))

    lines.extend(("", "## Mapped placements", ""))
    if locations:
        lines.extend((
            "These are source-recorded placements or spawner waypoints. "
            "They show potential locations, not live availability.",
            "",
            "| Zone | Marker type | X | Y | Z | Spawner / details |",
            "| --- | --- | ---: | ---: | ---: | --- |",
        ))
        for location in locations:
            zone = location["zone"]
            x, y, z = location["position"]
            marker_type = {
                "enemies": "Enemy",
                "npcs": "NPC",
                "shops": "Shop",
            }[location["category"]]
            details = markdown_text(location["details"]) or "—"
            lines.append(
                f"| [Zone {zone}](../zones/{zone}/) | {marker_type} | "
                f"{x:g} | {y:g} | {z:g} | {details} |"
            )
    else:
        lines.append(
            "No coordinate-based placement for this LOT appears in the "
            "current world-marker dataset. This does not prove that the "
            "template is unused or absent from other zones."
        )
    return "\n".join(lines) + "\n"


def render_index_page(title, actors, page_number, page_count):
    first = (page_number - 1) * INDEX_SIZE
    chunk = actors[first:first + INDEX_SIZE]
    lines = [
        f"# {title} - {page_number}",
        "",
        "[NPC and enemy catalog](../README.md)",
        "",
        "| Template | LOT | Classification |",
        "| --- | ---: | --- |",
    ]
    for actor in chunk:
        lot = actor["lot"]
        name = markdown_link_text(actor["name"])
        classification = markdown_text(actor["row"].get("Classification", "")) or "—"
        lines.append(
            f"| [{name} (LOT {lot})](../{lot}.md) | {lot} | {classification} |"
        )
    lines.append("")
    if page_count > 1:
        links = []
        for number in range(1, page_count + 1):
            if number == page_number:
                links.append(f"**{number}**")
            else:
                links.append(f"[{number}]({INDEX_FILES_FOR_TITLE[title]}-{number}.md)")
        lines.extend(("Pages: " + " · ".join(links), ""))
    return "\n".join(lines)


INDEX_FILES_FOR_TITLE = {
    "NPCs": "npcs",
    "Enemies": "enemies",
    "User-created NPCs": "user-created-npcs",
}


def render_readme(actors_by_type, page_counts, mapped_count):
    total = sum(len(actors) for actors in actors_by_type.values())
    lines = [
        "# NPCs and Enemies",
        "",
        "[Game Guide](../README.md) | "
        "[Quest NPC index](../quests/NPC%20Index.md) | "
        "[Pet database](../pets/README.md) | "
        "[Worlds, zones, and maps](../zones/README.md)",
        "",
        f"**{total:,} NPC, enemy, and user-created NPC templates have "
        "individual pages by LOT.** The catalog uses the local NPC template "
        "list; entries are definitions, not proof that a character is active "
        "or available in a particular server.",
        "",
        f"Coordinate-backed placements are available for {mapped_count} "
        "templates in the current world-marker dataset. Their coordinates "
        "identify potential spawns or placements, not live entities.",
        "",
        "## Browse by type",
        "",
        "| Type | Templates | Index pages |",
        "| --- | ---: | --- |",
    ]
    labels = {
        "NPC": "NPCs",
        "Enemies": "Enemies",
        "UserGeneratedNPCs": "User-created NPCs",
    }
    for object_type, actors in actors_by_type.items():
        label = labels[object_type]
        base = INDEX_FILES[object_type]
        links = [
            f"[{number}](indexes/{base}-{number}.md)"
            for number in range(1, page_counts[object_type] + 1)
        ]
        lines.append(
            f"| {label} | {len(actors)} | " + " · ".join(links) + " |"
        )
    lines.extend((
        "",
        "Indexes contain at most 200 templates each. Pages report available "
        "classification, registered components, AI/creature fields, mission "
        "associations, and mapped placements without inferring missing values.",
        "",
        "The local catalog also contains component-only registrations and "
        "other non-actor object types; those records are not included in this "
        "explicit NPC/enemy catalog. Pet-focused details are in the "
        "[Pet database](../pets/README.md).",
        "",
    ))
    return "\n".join(lines)


def write_if_changed(path, text):
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def build(root=ROOT, catalog_path=None):
    root = Path(root)
    catalog = Path(catalog_path) if catalog_path else root / CATALOG
    if not catalog.is_absolute():
        catalog = root / catalog
    actors = read_actors(catalog)
    locations = read_locations(root / MARKERS)

    actors_by_type = {
        object_type: sorted(
            (
                actor for actor in actors.values()
                if actor["object_type"] == object_type
            ),
            key=lambda actor: (actor["name"].casefold(), actor["lot"]),
        )
        for object_type in ACTOR_TYPES
    }
    output = root / OUTPUT
    updated_pages = 0
    for lot, actor in actors.items():
        updated_pages += write_if_changed(
            output / f"{lot}.md",
            render_actor_page(actor, locations.get(lot, [])),
        )

    page_counts = {}
    for object_type, type_actors in actors_by_type.items():
        base = INDEX_FILES[object_type]
        page_count = (len(type_actors) + INDEX_SIZE - 1) // INDEX_SIZE
        page_counts[object_type] = page_count
        title = {
            "NPC": "NPCs",
            "Enemies": "Enemies",
            "UserGeneratedNPCs": "User-created NPCs",
        }[object_type]
        for page_number in range(1, page_count + 1):
            updated_pages += write_if_changed(
                output / "indexes" / f"{base}-{page_number}.md",
                render_index_page(title, type_actors, page_number, page_count),
            )

    mapped_count = sum(lot in locations for lot in actors)
    updated_pages += write_if_changed(
        output / "README.md",
        render_readme(actors_by_type, page_counts, mapped_count),
    )
    return {
        "actors": len(actors),
        "mapped_actors": mapped_count,
        "updated_pages": updated_pages,
        "page_counts": page_counts,
    }


def main():
    stats = build()
    print(
        f"Built {stats['actors']} NPC/enemy pages "
        f"({stats['mapped_actors']} with mapped placements); "
        f"{stats['updated_pages']} files updated."
    )


if __name__ == "__main__":
    main()
