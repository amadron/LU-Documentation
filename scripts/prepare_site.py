import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site-src"
SKIP_DIRECTORIES = {".git", ".venv", "__pycache__", "site", "site-src"}
SKIP_ROOT_FILES = {
    "LEGO Universe Item List.csv",
    "LEGO Universe Item List.md",
    "LEGO Universe NPC List.csv",
    "LEGO Universe NPC List.md",
}
PUBLIC_DATABASE_FILES = {"README.md", "Schema.md"}


def should_skip(relative_path):
    if len(relative_path.parts) == 1 and relative_path.name in SKIP_ROOT_FILES:
        return True
    if (
        len(relative_path.parts) == 2
        and relative_path.parts[0] == "db"
        and relative_path.name not in PUBLIC_DATABASE_FILES
    ):
        return True
    return False


def main():
    SOURCE.mkdir(exist_ok=True)
    copied = 0

    for current, directories, files in os.walk(ROOT):
        directories[:] = sorted(
            name for name in directories if name not in SKIP_DIRECTORIES
        )
        current_path = Path(current)
        relative_directory = current_path.relative_to(ROOT)
        for name in files:
            source_file = current_path / name
            relative_file = relative_directory / name
            if should_skip(relative_file):
                continue
            destination = SOURCE / relative_file
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination)
            copied += 1

    print(f"Prepared {copied} public documentation files in {SOURCE}")


if __name__ == "__main__":
    main()
