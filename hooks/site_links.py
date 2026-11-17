import os
import posixpath
import re
from urllib.parse import unquote


_LINK = re.compile(r"\[(?P<label>[^\]\n]+)\]\((?P<target><[^>\n]+>|[^)\n]+)\)")
_SERVER_ROOT = "../DarkflameServer/"
_ASSET_ROOT = "../res/"
_SERVER_REPOSITORY = "https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/"
_ITEM_LISTS = {"LEGO Universe Item List.md", "LEGO Universe Item List.csv"}
_NPC_LISTS = {"LEGO Universe NPC List.md", "LEGO Universe NPC List.csv"}


def _relative_url(source_directory, destination):
    return posixpath.relpath(destination, source_directory or ".")


def _table_slug(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"table-{slug}"


def on_page_markdown(markdown, page, **kwargs):
    source_directory = os.path.dirname(page.file.src_uri)

    if page.file.src_uri == "db/README.md":
        return (
            "# CDClient Table Schemas\n\n"
            "This public reference documents table names, columns, and their "
            "purpose. It does not publish the full local table contents.\n\n"
            "Browse the [schema catalog](Schema.md) for all table fields."
        )

    def replace(match):
        label = match.group("label")
        target = match.group("target")
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        target_path, separator, fragment = target.partition("#")
        normalized = os.path.normpath(
            os.path.join(source_directory, unquote(target_path))
        ).replace("\\", "/")

        if normalized in _ITEM_LISTS:
            destination = _relative_url(source_directory, "wiki/items/README.md")
            return f"[Item database]({destination})"

        if normalized in _NPC_LISTS:
            destination = _relative_url(
                source_directory, "wiki/quests/NPC Index.md"
            )
            return f"[Quest character index]({destination})"

        if normalized.startswith("db/") and normalized.lower().endswith(
            (".md", ".csv")
        ):
            table = posixpath.splitext(posixpath.basename(normalized))[0]
            if table not in {"README", "Schema"}:
                destination = _relative_url(source_directory, "db/Schema.md")
                return f"[{table} schema]({destination}#{_table_slug(table)})"

        if normalized.startswith(_SERVER_ROOT):
            source_path = normalized[len(_SERVER_ROOT):]
            return f"[{label}]({_SERVER_REPOSITORY}{source_path}{separator}{fragment})"

        if normalized.startswith(_ASSET_ROOT):
            return f"`{label}` (local map asset; not included in this site)"

        return match.group(0)

    return _LINK.sub(replace, markdown)
