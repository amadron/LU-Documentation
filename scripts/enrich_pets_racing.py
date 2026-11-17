"""Enrich the generated pet (wiki/pets/) and racing (wiki/racing/) pages with English client strings.

The pet and racing database pages were generated without the client locale, so they show
template names from the Objects table and placeholders such as "Achievement 678". This
post-processor rewrites those pages in place using the English (en_US) strings from the
client's locale.xml and a few facts from the client database. It is idempotent: running it
again on already enriched pages produces no further changes.

Usage (from the documentation root):
    py -3 scripts/enrich_pets_racing.py [--locale PATH] [--db PATH] [--check]

Defaults: ../client/locale/locale.xml and ../server/resServer/CDServer.sqlite next to the
documentation root. --check only reports which files would change.

What it does
  pets/      species titles and link labels from Objects_<lot>_name (for example "Mantis",
             not "Praying Mantis"); English client name/description rows on every LOT page;
             mission/achievement names and client task text in the task tables, with shared
             tasks (such as the Speed Tamer achievements) marked as not pet-specific; a client
             string check on unnamed LOTs; client-name columns in the README item and ability
             tables.
  racing/    mission/achievement names instead of "Quest 624"/"Achievement 678" placeholders
             (also correcting earlier community-name guesses), complete mission-ID target lists,
             "Space Blizzard Racetrack (1261)" instead of "Zone 1261", client NPC/object names,
             client track and foot-race activity names, and plain-text paths instead of broken
             links to map files outside the documentation tree.
"""

import argparse
import re
import sqlite3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import game_paths  # location of the unmodified game data

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
DEFAULT_LOCALE = game_paths.LOCALE
DEFAULT_DB = game_paths.CDSERVER_DB

# Characters that Markdown could interpret inside table cells or link labels.
_ESCAPES = {"\\": "&#92;", "*": "&#42;", "_": "&#95;", "[": "&#91;", "]": "&#93;",
            "<": "&lt;", ">": "&gt;", "|": "&#124;", "`": "&#96;"}
# locale.xml stores a few Windows-1252 punctuation bytes as C1 control characters.
_C1 = {chr(c): bytes([c]).decode("cp1252", "replace") for c in range(0x80, 0xA0)}


def esc(text):
    return "".join(_ESCAPES.get(ch, ch) for ch in text)


def load_locale(path):
    strings = {}
    for _, elem in ET.iterparse(path, events=("end",)):
        if elem.tag != "phrase":
            continue
        for tr in elem.findall("translation"):
            if tr.get("locale") == "en_US" and tr.text:
                text = "".join(_C1.get(ch, ch) for ch in tr.text).strip()
                if text:
                    strings[elem.get("id")] = text
        elem.clear()
    return strings


class Data:
    def __init__(self, locale_path, db_path):
        self.loc = load_locale(locale_path)
        self.db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

    def q(self, sql, *args):
        return self.db.execute(sql, args).fetchall()

    def obj_name(self, lot):
        return self.loc.get(f"Objects_{lot}_name")

    def obj_desc(self, lot):
        return self.loc.get(f"Objects_{lot}_description")

    def db_obj_name(self, lot):
        row = self.q("SELECT name FROM Objects WHERE id = ?", lot)
        return (row[0][0] or "").strip() if row else None

    def mission_name(self, mid):
        return self.loc.get(f"Missions_{mid}_name")

    def is_mission(self, mid):
        row = self.q("SELECT isMission FROM Missions WHERE id = ?", mid)
        return bool(row and row[0][0])

    def task_text(self, uid, mid):
        for key in (f"MissionTasks_{uid}_description", f"MissionText_{mid}_description",
                    f"MissionText_{mid}_in_progress"):
            if key in self.loc:
                return self.loc[key]
        return None


def tamable_lots(data):
    return {int(k.split("_")[1]) for k, v in data.loc.items()
            if k.startswith("Objects_") and k.endswith("_description") and v == "Tamable Pet"}


def species(data, lot):
    name = data.obj_name(lot)
    return re.sub(r"\s+Pet$", "", name) if name else None


# ---------------------------------------------------------------------------------------------
# Pets
# ---------------------------------------------------------------------------------------------

PET_LINK = re.compile(r"\[([^\]\n]+?) \((\d+)\)\]\((\./|\.\./)(\d+)\.md\)")
TASK_HEADER_OLD = "| Definition | Kind | Local task fields | Definition metadata |"
TASK_HEADER = "| Definition | Kind | Client task text (locale.xml) | Local task fields | Definition metadata |"
TASK_SEP = "| --- | --- | --- | --- | --- |"
TASK_LINK = re.compile(r"\[(?:Quest/achievement|Quest|Achievement) (\d+)(?:: [^\]]*)?\]\((\.\./quests/\d+\.md)\)")
SHARED_NOTE = "**Shared tasks:**"
CLIENT_CHECK = "## Client string check"
README_CHECK = "**Completeness check against the client strings:**"


def pet_link_labels(text, data, tamable):
    def repl(m):
        lot = int(m.group(2))
        if lot != int(m.group(4)) or lot not in tamable:
            return m.group(0)
        return f"[{esc(species(data, lot))} ({lot})]({m.group(3)}{lot}.md)"
    return PET_LINK.sub(repl, text)


def pet_template_rows(lines, data, lot):
    lines = [l for l in lines if not l.startswith(("| English client name (locale.xml) |",
                                                   "| English client description (locale.xml) |"))]
    for i, line in enumerate(lines):
        if line.startswith("| Client description |"):
            name, desc = data.obj_name(lot), data.obj_desc(lot)
            lines[i + 1:i + 1] = [
                f"| English client name (locale.xml) | {esc(name) if name else f'(no Objects&#95;{lot}&#95;name string)'} |",
                f"| English client description (locale.xml) | {esc(desc) if desc else f'(no Objects&#95;{lot}&#95;description string)'} |",
            ]
            break
    return lines


def pet_task_table(lines, data):
    out, shared = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line in (TASK_HEADER_OLD, TASK_HEADER):
            out += [TASK_HEADER, TASK_SEP]
            i += 2
            while i < len(lines) and lines[i].startswith("| [") and "quests/" in lines[i]:
                cells = [c.strip() for c in lines[i].strip()[1:-1].split(" | ")]
                link, fields, meta = cells[0], cells[-2], cells[-1]
                m = TASK_LINK.search(link)
                mid = int(m.group(1))
                base = "Quest" if data.is_mission(mid) else "Achievement"
                name = data.mission_name(mid)
                label = f"{base} {mid}: {esc(name)}" if name else f"{base} {mid}"
                fm = re.search(r"target (\d+); group ([^;]*);", fields)
                target = int(fm.group(1))
                group = [] if fm.group(2) == "(none)" else [g for g in fm.group(2).split(",") if g]
                uid = None
                for row in data.q("SELECT uid, targetGroup FROM MissionTasks WHERE id = ? AND taskType = 22 "
                                  "AND target = ?", mid, target):
                    if [g for g in (row[1] or "").split(",") if g] == group:
                        uid = row[0]
                kind = base
                if group:
                    n = 1 + len(group)
                    kind += f"; shared task: taming any of the {n} listed pet templates counts"
                    shared.append((base, mid, name, n))
                text = data.task_text(uid, mid)
                text = f"“{esc(text)}”" if text else "(no client string)"
                out.append(f"| [{label}]({m.group(2)}) | {kind} | {text} | {fields} | {meta} |")
                i += 1
            # Replace or add the shared-task note directly after the table.
            if i + 1 < len(lines) and lines[i] == "" and lines[i + 1].startswith(SHARED_NOTE):
                i += 2
            if shared:
                parts = []
                for base, mid, name, n in shared:
                    parts.append(f"{base} {mid}" + (f" (“{esc(name)}”)" if name else "") + f" covers {n} templates")
                out += ["", SHARED_NOTE + " " + "; ".join(parts) + ". Taming any of the listed pet templates "
                        "advances these tasks, so they are general taming objectives, not requirements or rewards "
                        "specific to this pet."]
            continue
        out.append(line)
        i += 1
    return out


def pet_client_check(lines, data, lot, tamable):
    """Explain why an unnamed puzzle/PET LOT is not counted as a tamable pet."""
    if data.obj_name(lot) or data.q("SELECT 1 FROM Objects WHERE id = ?", lot):
        return lines
    start = next((i for i, l in enumerate(lines) if l == CLIENT_CHECK), None)
    if start is not None:
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        del lines[start:end]
    body = [CLIENT_CHECK, "",
            f"The client database has no Objects row for LOT {lot}, and locale.xml has no "
            f"`Objects_{lot}_name` or `Objects_{lot}_description` string, so the game has no player-facing "
            f"name for it. locale.xml marks exactly {len(tamable)} objects as “Tamable Pet”; this LOT is not one "
            "of them, so it is not counted as a tamable pet."]
    puzzle = data.q("SELECT id, ValidPiecesLXF, Timelimit, NumValidPieces, TotalNumPieces, imagCostPerBuild "
                    "FROM TamingBuildPuzzles WHERE NPCLot = ?", lot)
    if puzzle:
        pid, lxf, tl, nv, tot, cost = puzzle[0]
        same = data.q("SELECT NPCLot, Timelimit, NumValidPieces, TotalNumPieces, imagCostPerBuild "
                      "FROM TamingBuildPuzzles WHERE ValidPiecesLXF = ? AND NPCLot != ? ORDER BY NPCLot", lxf, lot)
        if same:
            refs = []
            for other, otl, onv, otot, ocost in same:
                label = species(data, other) or data.db_obj_name(other) or f"LOT {other}"
                ident = (otl, onv, otot, ocost) == (tl, nv, tot, cost)
                refs.append(f"[{esc(label)} ({other})](./{other}.md)" + (" — identical time, pieces and cost"
                                                                          if ident else ""))
            body += ["", f"Its puzzle row (id {pid}) reuses a valid-pieces file that is also used by: "
                     + "; ".join(refs) + "."]
    tasks = data.q("SELECT id FROM MissionTasks WHERE target = ? OR ',' || targetGroup || ',' LIKE ?",
                   lot, f"%,{lot},%")
    if tasks:
        names = sorted({t[0] for t in tasks})
        body += ["", "It is referenced only as a member of shared task target groups: "
                 + ", ".join(f"[{'Quest' if data.is_mission(m) else 'Achievement'} {m}: "
                             f"{esc(data.mission_name(m) or str(m))}](../quests/{m}.md)" for m in names)
                 + ". Those tasks count any of the listed pets."]
    else:
        body += ["", "No mission or achievement task references this LOT."]
    body.append("")
    anchor = next((i for i, l in enumerate(lines) if l == "## Taming puzzle data"), None)
    if anchor is None:
        anchor = next((i for i, l in enumerate(lines) if l.startswith("## ") and i > 0), len(lines))
    lines[anchor:anchor] = body
    return lines


def pet_readme(lines, data, tamable):
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == "| Item type | Local object name | Item LOT | Client description |" or \
                line == "| Item type | Local object name | English client name (locale.xml) | Item LOT | Client description |":
            out += ["| Item type | Local object name | English client name (locale.xml) | Item LOT | Client description |",
                    "| --- | --- | --- | --- | --- |"]
            i += 2
            while i < len(lines) and lines[i].startswith("| "):
                cells = [c.strip() for c in lines[i].strip()[1:-1].split(" | ")]
                lot = int(re.search(r"LOT (\d+)", cells[-2]).group(1))
                name = data.obj_name(lot)
                out.append(f"| {cells[0]} | {cells[1]} | {esc(name) if name else '(no client string)'} | "
                           f"{cells[-2]} | {cells[-1]} |")
                i += 1
            continue
        if line in ("| ID | Ability name | Imagination cost | Raw locStatus |",
                    "| ID | Ability name | Client display name (locale.xml) | Imagination cost | Raw locStatus |"):
            out += ["| ID | Ability name | Client display name (locale.xml) | Imagination cost | Raw locStatus |",
                    "| --- | --- | --- | --- | --- |"]
            i += 2
            while i < len(lines) and lines[i].startswith("| "):
                cells = [c.strip() for c in lines[i].strip()[1:-1].split(" | ")]
                disp = data.loc.get(f"PetAbilities_{cells[0]}_DisplayName")
                out.append(f"| {cells[0]} | {cells[1]} | {esc(disp) if disp else '(none)'} | {cells[-2]} | {cells[-1]} |")
                i += 1
            continue
        if line.startswith(README_CHECK):
            i += 2 if i + 1 < len(lines) and lines[i + 1] == "" else 1
            continue
        if line == "## More pet references":
            names = ", ".join(sorted(species(data, l) for l in tamable))
            out += [README_CHECK + f" locale.xml marks exactly {len(tamable)} objects as “Tamable Pet” "
                    f"({names}), the same {len(tamable)} templates listed as Tamable above, so no tamable pet is "
                    "missing. LOT 5638 and LOT 16479 have taming-puzzle rows but no Objects row and no client "
                    "name; see their pages for details.", ""]
        out.append(line)
        i += 1
    return out


def process_pets(data, files):
    tamable = tamable_lots(data)
    pets = WIKI / "pets"
    for path in sorted(pets.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        rel = path.relative_to(pets).as_posix()
        if re.fullmatch(r"\d+\.md", rel):
            lot = int(rel[:-3])
            if lot in tamable:
                lines[0] = re.sub(r"^# .+? — LOT", f"# {esc(species(data, lot))} — LOT", lines[0])
            lines = pet_template_rows(lines, data, lot)
            lines = pet_task_table(lines, data)
            lines = pet_client_check(lines, data, lot, tamable)
        elif rel == "README.md":
            lines = pet_readme(lines, data, tamable)
        new = pet_link_labels("\n".join(lines), data, tamable)
        new = TASK_LINK.sub(lambda m: (f"[{'Quest' if data.is_mission(int(m.group(1))) else 'Achievement'} "
                                       f"{m.group(1)}"
                                       + (f": {esc(data.mission_name(int(m.group(1))))}"
                                          if data.mission_name(int(m.group(1))) else "")
                                       + f"]({m.group(2)})"), new)
        files[path] = (text, new)


# ---------------------------------------------------------------------------------------------
# Racing
# ---------------------------------------------------------------------------------------------

TABLE_MISSION = re.compile(r"\[(Quest|Achievement|Mission) (\d+)\]\(([^)\s]*quests/(\d+)\.md)\) — ([^|\n]*?)(?= \|)")
BARE_MISSION = re.compile(r"\[(Quest|Achievement|Mission) (\d+)(?: — [^\]]*)?\]\(([^)\s]*quests/(\d+)\.md)\)(?! — )")
MISSION_LIST = re.compile(r"(targets are mission IDs, not track IDs: )(.*?)(?=\. \[UID|\. \||\.$)")
OBJECT_CELL = re.compile(r"\| (\d+) — ([^|\n]+?) \|")
ITEM_LINK = re.compile(r"\[([^\]\n]+?) \(LOT (\d+)\)\]\(([^)\s]*items/(\d+)\.md)\)")
MAP_LINK = re.compile(r"\[([^\]\n]+)\]\((?:\.\./)+res/res/maps/([^)\s]+)\)")
CLIENT_TRACK = "- **Client name (locale.xml):**"
FOOT_NAMES = "### Client activity names (locale.xml)"


def mission_label(data, mid, fallback):
    name = data.mission_name(mid)
    return esc(name) if name else fallback


def object_label(data, lot, current):
    db_name = data.db_obj_name(lot)
    loc = data.obj_name(lot)
    if db_name is None:
        return current
    rendered_db = esc(db_name)
    plain = re.sub(r" \(template “.*”\)$", "", current)
    if plain not in (rendered_db, esc(loc or "")):
        return current  # not a name this script knows how to replace
    if loc and loc != db_name:
        return f"{esc(loc)} (template “{rendered_db}”)"
    return rendered_db


def racing_line(line, data):
    line = TABLE_MISSION.sub(lambda m: (f"[{m.group(1)} {m.group(2)}]({m.group(3)}) — "
                                        f"{mission_label(data, int(m.group(2)), m.group(5))}"), line)
    line = BARE_MISSION.sub(lambda m: (f"[{m.group(1)} {m.group(2)}"
                                       + (f" — {esc(data.mission_name(int(m.group(2))))}"
                                          if data.mission_name(int(m.group(2))) else "")
                                       + f"]({m.group(3)})"), line)
    uid = re.search(r"UID (\d+)", line)
    if uid and MISSION_LIST.search(line):
        row = data.q("SELECT target, targetGroup FROM MissionTasks WHERE uid = ?", int(uid.group(1)))
        if row:
            ids = [g for g in (row[0][1] or "").split(",") if g.strip()] or [str(row[0][0])]
            names = [esc(data.mission_name(int(g)) or f"Achievement {g}") for g in ids]
            shown = " / ".join(names[:8])
            if len(names) > 8:
                shown += f" and {len(names) - 8} more ({len(names)} listed definitions; see the linked page)"
            line = MISSION_LIST.sub(lambda m: m.group(1) + shown, line)
    line = line.replace("Zone 1261", "Space Blizzard Racetrack (1261)")
    line = OBJECT_CELL.sub(lambda m: f"| {m.group(1)} — {object_label(data, int(m.group(1)), m.group(2))} |", line)

    def item(m):
        lot = int(m.group(2))
        name = data.obj_name(lot)
        return f"[{esc(name) if name and lot == int(m.group(4)) else m.group(1)} (LOT {lot})]({m.group(3)})"
    line = ITEM_LINK.sub(item, line)
    line = MAP_LINK.sub(lambda m: f"`client/res/maps/{m.group(2).replace('%20', ' ')}`", line)
    return line


def racing_track(lines, data):
    activity = None
    for line in lines:
        m = re.match(r"- \*\*Server activity:\*\* (\d+)", line)
        if m:
            activity = int(m.group(1))
    if activity is None:
        return lines
    lines = [l for l in lines if not l.startswith(CLIENT_TRACK)]
    name = data.loc.get(f"Activities_{activity}_ActivityName")
    zone = data.q("SELECT instanceMapID FROM Activities WHERE ActivityID = ?", activity)
    zone = zone[0][0] if zone else None
    zone_name = data.loc.get(f"ZoneTable_{zone}_DisplayDescription")
    if zone_name:
        source = f"`Activities_{activity}_ActivityName` and `ZoneTable_{zone}_DisplayDescription`"
    else:
        source = (f"`Activities_{activity}_ActivityName`; there is no ZoneTable row or "
                  f"`ZoneTable_{zone}_DisplayDescription` string for instance {zone}")
    entry = f"{CLIENT_TRACK} {esc(name)} ({source})" if name else None
    for i, line in enumerate(lines):
        if line.startswith("- **Historical track name:**") and entry:
            lines.insert(i + 1, entry)
            break
    return lines


def racing_foot(lines, data):
    start = next((i for i, l in enumerate(lines) if l == FOOT_NAMES), None)
    if start is not None:
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("#")), len(lines))
        del lines[start:end]
    anchor = next((i for i, l in enumerate(lines) if l == "## Start, finish, and progress"), None)
    if anchor is None:
        return lines
    listed = set()
    for line in lines[:anchor]:
        m = re.match(r"\| \d+ — [^|]+ \| (\d+) \(", line)
        if m:
            listed.add(int(m.group(1)))
    rows, unlisted = [], []
    for aid, desc in data.q("SELECT objectTemplate, MIN(description) FROM ActivityRewards "
                            "WHERE description LIKE '%Foot Race%' GROUP BY objectTemplate ORDER BY objectTemplate"):
        name = data.loc.get(f"Activities_{aid}_ActivityName")
        if name:
            rows.append(f"| {aid} | {esc(name)} | {esc(desc)} |")
            if aid not in listed:
                unlisted.append(str(aid))
    if not rows:
        return lines
    block = [FOOT_NAMES, "",
             "The client's English activity names for the foot-race activity IDs (`Activities_<id>_ActivityName`), "
             "next to the stored ActivityRewards description. The names in parentheses are the NPCs that host each race."]
    if unlisted:
        block[-1] += ((" Activity " if len(unlisted) == 1 else " Activities ") + " and ".join(unlisted)
                      + (" has" if len(unlisted) == 1 else " have")
                      + " a client name and award row but no starter in the registration table above.")
    block += ["", "| Activity ID | Client activity name | Stored award description |", "| --- | --- | --- |"] + rows + [""]
    lines[anchor:anchor] = block
    return lines


def process_racing(data, files):
    racing = WIKI / "racing"
    for path in sorted(racing.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = [racing_line(l, data) for l in text.split("\n")]
        rel = path.relative_to(racing).as_posix()
        if rel.startswith("tracks/"):
            lines = racing_track(lines, data)
        if rel == "tracks/foot-races.md":
            lines = racing_foot(lines, data)
        files[path] = (text, "\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--locale", type=Path, default=DEFAULT_LOCALE)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--check", action="store_true", help="report changes without writing")
    args = ap.parse_args()
    for p in (args.locale, args.db):
        if not p.is_file():
            sys.exit(f"missing input: {p}")
    data = Data(args.locale, args.db)
    files = {}
    process_pets(data, files)
    process_racing(data, files)
    changed = [p for p, (old, new) in files.items() if old != new]
    for p in changed:
        if not args.check:
            eol = "\r\n" if b"\r\n" in p.read_bytes() else "\n"
            p.write_text(files[p][1], encoding="utf-8", newline=eol)
        print(("would update " if args.check else "updated ") + p.relative_to(ROOT).as_posix())
    print(f"{len(changed)} of {len(files)} pages {'would change' if args.check else 'changed'}")


if __name__ == "__main__":
    main()
