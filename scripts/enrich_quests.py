#!/usr/bin/env python3
"""Enrich the generated quest database (wiki/quests) with official client strings.

The quest/achievement pages were originally generated without the client
``locale.xml``.  This script updates them in place with the official English
(en_US) client strings:

* ``Missions_<id>_name``            -> page title (H1), every title link in the
                                       quest database, CSV title column
* ``MissionText_<id>_<suffix>``     -> "Official client text" in the Description
                                       section (description / offer / turn-in ...)
* ``MissionTasks_<uid>_description`` -> "Objectives" list and the per-objective
                                       detail sections
* ``MissionEmail_<row>_*``          -> completion mail sender / subject / body

Definitions without a client name keep their previous title (community
candidate title or numeric placeholder).  The script is idempotent: running it
again rebuilds the same sections instead of appending to them.

Usage (from the repository root or anywhere)::

    py -3 scripts/enrich_quests.py [--locale PATH] [--db PATH] [--quests DIR] [--dry-run]

Only files below ``wiki/quests`` are modified.
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import re
import sqlite3
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

import game_paths  # location of the unmodified game data

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEFAULT_QUESTS = os.path.join(REPO, "wiki", "quests")
DEFAULT_LOCALE = str(game_paths.LOCALE)
DEFAULT_DB = str(game_paths.CDSERVER_DB)

LOCALE = "en_US"

# MissionText suffixes shown on the pages, in display order, with labels.
TEXT_FIELDS = [
    ("description", "Description"),
    ("offer", "Offer text"),
    ("offer_repeatable", "Repeat offer text"),
    ("accept_chat_bubble", "Accept reply"),
    ("in_progress", "In-progress text"),
    ("completion_succeed_tip", "Objectives-complete tip"),
    ("ready_to_complete", "Turn-in text"),
]

ESCAPES = {
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    "|": "&#124;", "*": "&#42;", "_": "&#95;", "[": "&#91;", "]": "&#93;",
    "`": "&#96;", "\\": "&#92;", "~": "&#126;",
}

OFFICIAL_EVIDENCE = "Official client name (locale.xml en_US)"
COMMUNITY_EVIDENCE = "Unique historical signature association; not ID-verified"


def esc(text: str) -> str:
    return "".join(ESCAPES.get(ch, ch) for ch in text)


def clean_raw(text: str) -> str:
    """Normalise a client string without Markdown (used for CSV output)."""
    text = text.replace("\ufffd", "\u2019")  # broken apostrophes in the client file
    text = re.sub(r"(?i)<br\s*/?>", " ", text)
    text = re.sub(r"(?i)</?(font|b|i|u)\b[^>]*>", "", text)
    text = text.replace("\\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def to_md(text: str) -> str:
    """Convert a client string to escaped Markdown; <font> highlights become bold."""
    text = text.replace("\ufffd", "\u2019")
    text = re.sub(r"(?i)<br\s*/?>", " ", text).replace("\\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    out, bold = [], False
    for part in re.split(r"(?i)(</?font\b[^>]*>|</?b>)", text):
        if not part:
            continue
        low = part.lower()
        if low.startswith("<font") or low == "<b>":
            bold = True
            continue
        if low.startswith("</font") or low == "</b>":
            bold = False
            continue
        part = re.sub(r"(?i)</?(i|u)\b[^>]*>", "", part)
        if bold and part.strip():
            lead = part[: len(part) - len(part.lstrip())]
            trail = part[len(part.rstrip()):]
            out.append(f"{lead}**{esc(part.strip())}**{trail}")
        else:
            out.append(esc(part))
    return re.sub(r"\s+", " ", "".join(out)).strip()


# --------------------------------------------------------------------------- data

def load_locale(path: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for _, el in ET.iterparse(path, events=("end",)):
        if el.tag != "phrase":
            continue
        pid = el.get("id") or ""
        if pid.startswith("Mission"):
            for tr in el.findall("translation"):
                if tr.get("locale") == LOCALE and tr.text and tr.text.strip():
                    data[pid] = tr.text
        el.clear()
    return data


def read_csv(path: str):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames), list(reader)


def write_csv(path: str, fields, rows) -> bool:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return write_text(path, "\ufeff" + buf.getvalue())


DRY_RUN = False
CHANGED: list[str] = []


def _eol(raw: str) -> str:
    return "\r\n" if "\r\n" in raw else "\n"


def read_text(path: str) -> str:
    """Read a file with its line endings normalised to LF."""
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read().replace("\r\n", "\n")


def write_text(path: str, text: str) -> bool:
    """Write LF text back using the file's existing line-ending style."""
    with open(path, encoding="utf-8", newline="") as fh:
        old = fh.read()
    text = text.replace("\r\n", "\n").replace("\n", _eol(old))
    if old == text:
        return False
    CHANGED.append(path)
    if not DRY_RUN:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    return True


class Defs:
    """Title information for every Missions definition."""

    def __init__(self, summary_rows, loc):
        self.kind: dict[int, str] = {}
        self.official: dict[int, str] = {}   # raw official name
        self.community: dict[int, str] = {}  # raw historical community title
        for row in summary_rows:
            mid = int(row["ID"])
            self.kind[mid] = row["Kind"]
            if "HistoricalCommunityTitle" in row:
                if row["HistoricalCommunityTitle"]:
                    self.community[mid] = row["HistoricalCommunityTitle"]
            elif row["TitleEvidence"] == COMMUNITY_EVIDENCE:
                self.community[mid] = row["TitleOrFallback"]
            name = loc.get(f"Missions_{mid}_name")
            if name:
                self.official[mid] = clean_raw(name)
        # previous titles (community / placeholder) -> id, for unlinked mentions
        self.prev_lookup: dict[str, int] = {}
        counts = Counter(self.community.values())
        for mid, title in self.community.items():
            if counts[title] == 1:
                self.prev_lookup[title] = mid
        self.official_names = set(self.official.values())

    def placeholder(self, mid: int) -> str:
        return f"{self.kind[mid]} {mid}"

    def title(self, mid: int) -> str:
        """Raw display title (official, else community, else placeholder)."""
        return self.official.get(mid) or self.community.get(mid) or self.placeholder(mid)


# ------------------------------------------------------------- generic rewrites

LINK_RE = re.compile(r"\[((?:(?!\]\().)*?) &#91;(\d+)&#93;\]\(((?:\.\./)*)(\d+)\.md\)")
META_MD_RE = re.compile(r"(completion event\(s\): )(.+?)(?=\. This is an objective| \||$)", re.M)
META_RAW_RE = re.compile(r"(completion event\(s\): )(.+?)(?=\. This is an objective|$)")


def rewrite_links(text: str, defs: Defs) -> str:
    def repl(m):
        mid = int(m.group(2))
        if m.group(2) != m.group(4) or mid not in defs.kind:
            return m.group(0)
        return f"[{esc(defs.title(mid))} &#91;{mid}&#93;]({m.group(3)}{mid}.md)"
    return LINK_RE.sub(repl, text)


def _resolve_item(item: str, defs: Defs, md: bool):
    m = re.fullmatch(r"(.*) &#91;(\d+)&#93;" if md else r"(.*) \[(\d+)\]", item)
    if m and int(m.group(2)) in defs.kind:
        return int(m.group(2))
    m = re.fullmatch(r"(Quest|Achievement) (\d+)", item)
    if m and defs.kind.get(int(m.group(2))) == m.group(1):
        return int(m.group(2))
    for title, mid in defs.prev_lookup.items():
        if item != (esc(title) if md else title):
            continue
        # skip if the text is also the official name of a *different* definition
        if title in defs.official_names and defs.official.get(mid) != title:
            return None
        return mid
    return None


def rewrite_meta(text: str, defs: Defs, md: bool) -> str:
    """Rename mission references in 'Complete missions' objective summaries."""
    def repl(m):
        items = m.group(2).split(" / ")
        out = []
        for item in items:
            mid = _resolve_item(item, defs, md)
            if mid is None:
                out.append(item)
                continue
            name = defs.title(mid)
            if name == defs.placeholder(mid):
                out.append(name)
            else:
                out.append(f"{esc(name)} &#91;{mid}&#93;" if md else f"{name} [{mid}]")
        return m.group(1) + " / ".join(out)
    return (META_MD_RE if md else META_RAW_RE).sub(repl, text)


# ------------------------------------------------------------------ quest pages

TITLE_PARA_RE = re.compile(
    r"^\*\*(Community title association|Title unavailable|Official client name)(:\*\*|\*\*).*$", re.M)


def title_paragraph(mid: int, defs: Defs) -> str:
    key = f"`Missions_{mid}_name`"
    off, com = defs.official.get(mid), defs.community.get(mid)
    if off:
        para = f"**Official client name** from the client locale.xml ({key}, en&#95;US)."
        if com and com.casefold() != off.casefold():
            para += (f" Historical community name: {esc(com)} (a candidate association from public"
                     " wiki research; see the references below).")
        elif com:
            para += " The historical community association below agrees with this name."
        return para
    if com:
        return ("**Community title association:** the client locale.xml has no "
                f"{key} entry, so the historical name below is kept. It was inferred from a unique"
                " multi-field data signature, not a verified localized mission-ID mapping. The"
                " numeric ID and local objectives/rewards remain authoritative for this snapshot.")
    return ("**Title unavailable:** the client locale.xml has no "
            f"{key} entry, and no sufficiently conservative community match was established."
            " This page does not invent a quest name.")


def description_section(mid: int, uids, loc, obj_rows) -> tuple[str, bool]:
    lines = ["## Description", ""]
    texts = []
    for suffix, label in TEXT_FIELDS:
        raw = loc.get(f"MissionText_{mid}_{suffix}")
        if raw and clean_raw(raw):
            texts.append(f"**{label}:** {to_md(raw)}")
    if texts:
        lines += ["Official client text from locale.xml (en&#95;US):", ""]
        for t in texts:
            lines += [t, ""]
    else:
        lines += ["The client locale.xml has no description, offer, or turn-in text for this"
                  " definition.", ""]
    lines += ["### Objectives", "",
              "Client task text from locale.xml is shown where it exists; the indented line is"
              " the data-derived summary of the same MissionTasks row.", ""]
    for uid in uids:
        summary = esc(obj_rows[uid]["ReconstructedObjective"])
        task = loc.get(f"MissionTasks_{uid}_description")
        if task and clean_raw(task):
            lines += [f"- {to_md(task)}", f"    - Data summary: {summary}"]
        else:
            lines += [f"- {summary}", "    - No client task text; data-derived summary."]
    lines.append("")
    return "\n".join(lines) + "\n", bool(texts)


CLIENT_TASK_RE = re.compile(r"(^### Objective \d+: .*\(UID (\d+)\)\n\n)(\*\*Client task text:\*\* .*\n\n)?", re.M)
MAIL_BLOCK_RE = re.compile(r"\n\*\*Client mail text\*\*.*?(?=\n## |\n### |\Z)", re.S)


def update_page(text: str, mid: int, defs: Defs, loc, obj_rows, mails) -> tuple[str, bool]:
    kind = defs.kind[mid]
    # H1
    h1 = f"# {esc(defs.title(mid))} - {kind} {mid}" if defs.title(mid) != defs.placeholder(mid) \
        else f"# {kind} {mid}"
    text = re.sub(r"\A# .*", lambda _: h1, text, count=1)
    # title paragraph
    text, n = TITLE_PARA_RE.subn(lambda _: title_paragraph(mid, defs), text, count=1)
    if n != 1:
        raise RuntimeError(f"{mid}: title paragraph not found")
    # description
    uids = re.findall(r"^### Objective \d+: .*\(UID (\d+)\)$", text, re.M)
    section, has_text = description_section(mid, uids, loc, obj_rows)
    text, n = re.subn(r"^## Description\n.*?(?=^## )", lambda _: section, text, count=1, flags=re.M | re.S)
    if n != 1:
        raise RuntimeError(f"{mid}: description section not found")

    # client task text in objective details
    def task_repl(m):
        task = loc.get(f"MissionTasks_{m.group(2)}_description")
        if task and clean_raw(task):
            return m.group(1) + f"**Client task text:** {to_md(task)}\n\n"
        return m.group(1)
    text = CLIENT_TASK_RE.sub(task_repl, text)

    # completion mail texts
    text = MAIL_BLOCK_RE.sub("", text)
    mail_lines = []
    for row_id in mails.get(mid, []):
        parts = []
        for key, label in (("senderName", "From"), ("subjectText", "Subject"), ("bodyText", "Body")):
            raw = loc.get(f"MissionEmail_{row_id}_{key}")
            if raw and clean_raw(raw):
                parts.append(f"{label}: {to_md(raw)}")
        if parts:
            mail_lines.append(f"- Row {row_id}: " + " \u2014 ".join(parts))
    if mail_lines:
        block = "\n**Client mail text** (locale.xml, en&#95;US):\n\n" + "\n".join(mail_lines) + "\n"
        text = re.sub(r"(^### Completion mail / announcements\n\n(?:\|.*\n)+)",
                      lambda m: m.group(1) + block, text, count=1, flags=re.M)
    return text, has_text


# ----------------------------------------------------------- README/Methodology

METH_START, METH_END = "<!-- locale-enrichment:start -->", "<!-- locale-enrichment:end -->"


def methodology_block(stats) -> str:
    return f"""{METH_START}
## Client names and texts (locale.xml)

Titles and story texts come from the client **locale.xml** (en&#95;US
translations), applied by `scripts/enrich_quests.py`:

- `Missions_<id>_name` supplies the page title for **{stats['named']}** of
  {stats['defs']} definitions. The remaining **{stats['fallback']}** have no
  client name and keep their previous title: a candidate historical community
  title where one was associated ({stats['fallback_community']}), otherwise the
  numeric placeholder ({stats['fallback_placeholder']}). Community associations
  that differ from the client name are kept as a "Historical community name" note.
- `MissionText_<id>_description`, `_offer`, `_offer_repeatable`,
  `_accept_chat_bubble`, `_in_progress`, `_completion_succeed_tip`, and
  `_ready_to_complete` are shown as labelled client texts on
  **{stats['with_text']}** pages. NPC idle chat bubbles (`_chat_state_*`) are
  not reproduced.
- `MissionTasks_<uid>_description` supplies the client wording of
  **{stats['task_text']}** of {stats['tasks']} attached objective rows; the
  data-derived summary is kept alongside it because it names exact targets.
- `MissionEmail_<row>_senderName/subjectText/bodyText` adds the mail text for
  completion mails.

Client highlight markup (`<font>`) is rendered as bold, and Markdown-sensitive
characters are escaped. The [MissionText](../../db/MissionText.md) table itself
only holds presentation/animation references. Walkthrough steps remain
**original reconstructions from local objective data**, not hand-verified
puzzle walkthroughs; unsupported script-specific actions remain unknown.
{METH_END}"""


def update_methodology(path: str, stats) -> None:
    text = read_text(path)
    block = methodology_block(stats)
    if METH_START in text:
        text = re.sub(re.escape(METH_START) + r".*?" + re.escape(METH_END), lambda _: block, text, flags=re.S)
    else:
        old = re.compile(r"\[MissionText\]\(\.\./\.\./db/MissionText\.md\) contains presentation/animation"
                         r" references,.*?remain unknown\.\n", re.S)
        text, n = old.subn("", text, count=1)
        if n != 1:
            raise RuntimeError("Methodology: MissionText paragraph not found")
        text = text.replace("\n## Mission lifecycle", "\n" + block + "\n\n## Mission lifecycle", 1)
    text = text.replace(
        "This is conservative corroboration, **not verification that the historical\nquest title belongs",
        "Community associations are now secondary to the client names above. This is\nconservative "
        "corroboration, **not verification that the historical\nquest title belongs")
    text = text.replace("exact localized story text, or player eligibility.",
                        "that client texts match a particular server build, or player eligibility.")
    write_text(path, text)


def update_readme(path: str, stats) -> None:
    text = read_text(path)
    text = text.replace(
        "Names taken from community evidence are explicitly marked as candidate historical titles;"
        " numeric IDs remain stable lookup keys.",
        "Titles are the official English client names from locale.xml; definitions without a client"
        " name keep a marked community candidate title or a numeric placeholder. Numeric IDs remain"
        " stable lookup keys.")
    text = text.replace(
        "page gives an available description, character associations,",
        "page gives the official client texts where available, character associations,")
    text = text.replace(
        "legacy, test, or otherwise unavailable. Where original story text or steps\nare missing,",
        "legacy, test, or otherwise unavailable. Where client story text or steps\nare missing,")
    text = text.replace("A reconstructed description is not original quest dialogue;",
                        "A data-derived objective summary is not original quest dialogue;")
    rows = [
        ("Definitions with an official client name (locale.xml)", stats["named"]),
        ("Definitions with official client description/offer texts", stats["with_text"]),
        ("Objective rows with client task text", stats["task_text"]),
    ]
    for label, _ in rows:  # drop rows from a previous run, then re-insert in order
        text = re.sub(rf"^\| {re.escape(label)} \| .*\|\n", "", text, flags=re.M)
    block = "".join(f"\n| {label} | {value} |" for label, value in rows)
    text, n = re.subn(r"^(\| Definitions with conservative community associations \| .*\|)$",
                      lambda m: m.group(1) + block, text, count=1, flags=re.M)
    if n != 1:
        raise RuntimeError("README: evidence table row not found")
    write_text(path, text)


# ------------------------------------------------------------------------- main

def main() -> int:
    global DRY_RUN
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--quests", default=DEFAULT_QUESTS)
    ap.add_argument("--locale", default=DEFAULT_LOCALE)
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    DRY_RUN = args.dry_run
    qdir = args.quests

    loc = load_locale(args.locale)
    sum_path = os.path.join(qdir, "Quest Summary.csv")
    obj_path = os.path.join(qdir, "Objective Reference.csv")
    sum_fields, sum_rows = read_csv(sum_path)
    obj_fields, obj_rows = read_csv(obj_path)
    defs = Defs(sum_rows, loc)

    db = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    mails = defaultdict(list)
    for row_id, mission in db.execute("SELECT ID, missionID FROM MissionEmail ORDER BY ID"):
        mails[mission].append(row_id)
    db.close()

    # Objective Reference.csv (rename META references first: pages reuse these summaries)
    if "ClientTaskDescription" not in obj_fields:
        obj_fields.append("ClientTaskDescription")
    task_text = 0
    for row in obj_rows:
        row["ReconstructedObjective"] = rewrite_meta(row["ReconstructedObjective"], defs, md=False)
        raw = loc.get(f"MissionTasks_{row['UID']}_description")
        row["ClientTaskDescription"] = clean_raw(raw) if raw else ""
        task_text += bool(row["ClientTaskDescription"])
    write_csv(obj_path, obj_fields, obj_rows)
    by_uid = {row["UID"]: row for row in obj_rows}

    # Quest Summary.csv
    if "HistoricalCommunityTitle" not in sum_fields:
        sum_fields.append("HistoricalCommunityTitle")
    for row in sum_rows:
        mid = int(row["ID"])
        row["HistoricalCommunityTitle"] = defs.community.get(mid, "")
        row["TitleOrFallback"] = defs.title(mid)
        if mid in defs.official:
            row["TitleEvidence"] = OFFICIAL_EVIDENCE
        elif mid in defs.community:
            row["TitleEvidence"] = COMMUNITY_EVIDENCE
        else:
            row["TitleEvidence"] = "No localized title available"
        row["ReconstructedDescription"] = rewrite_meta(row["ReconstructedDescription"], defs, md=False)
    write_csv(sum_path, sum_fields, sum_rows)

    # Markdown files
    with_text = 0
    pages = 0
    for dirpath, _, files in os.walk(qdir):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            text = read_text(path)
            m = re.fullmatch(r"(\d+)\.md", name)
            if m and dirpath == qdir:
                mid = int(m.group(1))
                text, has_text = update_page(text, mid, defs, loc, by_uid, mails)
                with_text += has_text
                pages += 1
            text = rewrite_links(text, defs)
            text = rewrite_meta(text, defs, md=True)
            if os.path.basename(dirpath) == "indexes" or name == "README.md":
                text = text.replace("| Definition / candidate title |", "| Definition / title |")
            write_text(path, text)

    named = sum(1 for mid in defs.kind if mid in defs.official)
    fallback = len(defs.kind) - named
    fb_com = sum(1 for mid in defs.kind if mid not in defs.official and mid in defs.community)
    stats = {
        "defs": len(defs.kind), "named": named, "fallback": fallback,
        "fallback_community": fb_com, "fallback_placeholder": fallback - fb_com,
        "with_text": with_text, "task_text": task_text, "tasks": len(obj_rows),
    }
    update_methodology(os.path.join(qdir, "Methodology.md"), stats)
    update_readme(os.path.join(qdir, "README.md"), stats)

    renamed = sum(1 for mid in defs.official if defs.official[mid] != defs.community.get(mid))
    print(f"definitions: {stats['defs']} | pages: {pages} | official names: {named} "
          f"(differing from previous title: {renamed}) | fallback titles: {fallback} "
          f"(community {fb_com}, placeholder {fallback - fb_com})")
    print(f"pages with client texts: {with_text} | objective rows with client task text: "
          f"{task_text}/{len(obj_rows)}")
    print(f"files {'that would change' if DRY_RUN else 'changed'}: {len(CHANGED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
