"""Where the documentation scripts read game data from.

The data must come from an unmodified game installation: the development copy next to this
repository contains custom content (e.g. zone 1650) and database edits made for testing.
Default: the original installation at <parent of the dev folder>/Lego Universe; override with the
environment variable LU_GAME_DIR (the folder that contains client/ and server/).
"""

import os
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = Path(os.environ.get("LU_GAME_DIR", DOCS_ROOT.parent.parent / "Lego Universe"))
CLIENT_RES = GAME_DIR / "client" / "res"
LOCALE = GAME_DIR / "client" / "locale" / "locale.xml"
CDSERVER_DB = GAME_DIR / "server" / "resServer" / "CDServer.sqlite"
CLIENT_FDB = CLIENT_RES / "cdclient.fdb"
