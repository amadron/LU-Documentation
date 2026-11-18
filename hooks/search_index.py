import json
import logging
import re
from pathlib import Path

from mkdocs.plugins import event_priority


log = logging.getLogger("mkdocs")
_DETAIL = re.compile(r"^wiki/(?:items|quests|npcs)/\d+/$")
_CATALOG = re.compile(r"^wiki/(?:items|quests|npcs)/(?:sources|types|indexes|locations)/")


def compact_documents(documents):
    compacted = []
    for document in documents:
        page, separator, fragment = document["location"].partition("#")
        if _DETAIL.fullmatch(page):
            if separator and fragment != "description":
                continue
        elif _CATALOG.match(page):
            if separator:
                continue
            document = {**document, "text": ""}
        compacted.append(document)
    return compacted


@event_priority(-100)
def on_post_build(*, config):
    path = Path(config.site_dir) / "search" / "search_index.json"
    original_size = path.stat().st_size
    index = json.loads(path.read_text(encoding="utf-8"))
    original_count = len(index["docs"])
    index["docs"] = compact_documents(index["docs"])
    data = json.dumps(index, ensure_ascii=False, separators=(",", ":"))
    path.write_text(data, encoding="utf-8")
    log.info(
        "Compacted search index: %d to %d entries, %.1f to %.1f MiB",
        original_count, len(index["docs"]),
        original_size / 1024**2, path.stat().st_size / 1024**2,
    )
