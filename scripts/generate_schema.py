import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "db"
TABLE_REFERENCE = ROOT / "LEGO Universe CDClient Table Reference.md"
OUTPUT = DATABASE / "Schema.md"
TABLE_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*[\d,]+\s*\|\s*(.*?)\s*\|$")


def read_descriptions():
    descriptions = {}
    section = "Other tables"
    for line in TABLE_REFERENCE.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("## "):
            section = line.removeprefix("## ").strip()
            continue
        match = TABLE_ROW.match(line)
        if match:
            name, description = match.groups()
            descriptions[name] = (section, description)
    return descriptions


def read_columns(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return next(csv.reader(stream))


def main():
    descriptions = read_descriptions()
    tables = sorted(DATABASE.glob("*.csv"), key=lambda path: path.stem.casefold())
    grouped = defaultdict(list)

    for path in tables:
        section, description = descriptions.get(
            path.stem, ("Other tables", "No overview is recorded.")
        )
        grouped[section].append((path.stem, read_columns(path), description))

    lines = [
        "# CDClient Table Schema",
        "",
        f"This reference lists the names and columns of {len(tables)} tables "
        "from the local CDClient schema, with a short purpose summary.",
        "It contains no table rows or player data. Full local table exports "
        "are not part of this public site.",
        "",
        "## Browse by topic",
        "",
    ]
    for section in sorted(grouped, key=str.casefold):
        slug = re.sub(
            r"[^a-z0-9]+", "-", section.lower().replace("/", "")
        ).strip("-")
        lines.append(f"- [{section}](#{slug})")
    lines.append("")

    for section in sorted(grouped, key=str.casefold):
        lines.extend([f"## {section}", ""])
        for name, columns, description in grouped[section]:
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            lines.extend(
                [
                    f"### `{name}` {{#table-{slug}}}",
                    "",
                    description,
                    "",
                    "**Columns:** " + ", ".join(f"`{column}`" for column in columns),
                    "",
                ]
            )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(tables)} table schemas to {OUTPUT}")


if __name__ == "__main__":
    main()
