"""Add official client names and tooltips to the existing wiki/skills/ pages in place.

The table exports that build_player_references.py needs (db/*.csv) are not always
available. This script updates the already generated pages using only the client
locale and scripts/skill_name_evidence.json, producing the same page header and
index as a full regeneration. It is idempotent.

Usage (from the documentation root):
    py -3 scripts/enrich_skills.py [locale.xml]
"""

import re
import sys
from pathlib import Path

import build_player_references as refs


SKILLS = refs.ROOT / "wiki" / "skills"
SETTINGS = "## Recorded settings"
ROW = re.compile(r"^\| \[(\d+)\]\(\./\1\.md\) \| (.*?) \| (.*) \| (\d+) \|$")


def read(path):
    raw = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), newline


def write(path, text, newline):
    data = text.replace("\n", newline).encode("utf-8")
    if path.read_bytes() == data:
        return False
    path.write_bytes(data)
    return True


def page_item_link(text, lot):
    """The rendered link of an equipment item, taken from the page's own association list."""
    pattern = rf"^- (\[[^\n]*? \(LOT {lot}\)\]\(\.\./items/{lot}\.md\)) — slot "
    match = re.search(pattern, text, re.M)
    return match.group(1) if match else None


def enrich_page(path, locale, evidence, names):
    skill = path.stem
    text, newline = read(path)
    head, sep, body = text.partition(SETTINGS)
    if not sep:
        raise ValueError(f"{path}: missing '{SETTINGS}' section")
    candidate = names.get(skill)
    source = item = None
    if candidate:
        source = evidence["sources"][candidate["source"]]
        item = page_item_link(body, candidate["item"])
        if not item:
            raise ValueError(f"{path}: community-name item {candidate['item']} is not in the equipment list")
    official, description = refs.official_skill(locale, skill)
    header = "\n".join(refs.skill_header(skill, official, description, candidate, source, item))
    return write(path, header + "\n" + sep + body, newline)


def enrich_index(path, skills, locale, names):
    text, newline = read(path)
    lines = text.split("\n")
    start = lines.index("| Skill ID | Name | Equipment examples | Set associations |")
    rows = []
    for line in lines[start + 2:]:
        if not line:
            continue
        match = ROW.match(line)
        if not match:
            raise ValueError(f"{path}: unexpected index row: {line}")
        skill, _, examples, set_count = match.groups()
        label = refs.skill_index_label(skill, refs.official_skill(locale, skill)[0], names.get(skill))
        rows.append(f"| [{skill}](./{skill}.md) | {label} | {examples} | {set_count} |")
    listed = {ROW.match(row).group(1) for row in rows}
    if listed != set(skills):
        raise ValueError(f"{path}: index rows do not match the skill pages")
    intro = refs.skill_index_intro(len(skills), *refs.skill_name_counts(skills, locale, names))
    return write(path, "\n".join(intro + rows) + "\n", newline)


def main():
    locale_path = Path(sys.argv[1]) if len(sys.argv) > 1 else refs.DEFAULT_LOCALE
    if not locale_path.is_file():
        raise SystemExit(f"Client locale not found: {locale_path} (pass the locale.xml path as an argument)")
    locale = refs.load_skill_locale(locale_path)
    evidence = refs.load_evidence()
    pages = sorted((p for p in SKILLS.glob("*.md") if p.stem.isdigit()), key=lambda p: int(p.stem))
    skills = {p.stem: {"items": set()} for p in pages}
    for page in pages:
        text = read(page)[0]
        skills[page.stem]["items"] = set(re.findall(r"^- \[[^\n]*?\]\(\.\./items/(\d+)\.md\) — slot ", text, re.M))
    names = refs.validate_skill_names(evidence, skills)
    changed = sum(enrich_page(page, locale, evidence, names) for page in pages)
    changed += enrich_index(SKILLS / "README.md", skills, locale, names)
    official, historical, candidates = refs.skill_name_counts(skills, locale, names)
    print(f"{len(pages)} skill pages: {official} official names, {historical} historical community "
          f"names, {candidates} community candidates, {len(pages) - official - candidates} unnamed. "
          f"{changed} files changed.")


if __name__ == "__main__":
    main()
