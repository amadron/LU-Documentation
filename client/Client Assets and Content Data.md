# Client assets and content data

[Client overview](./README.md) | [Data model](../LEGO%20Universe%20Data%20Model%20and%20Public%20Research.md) | [CDClient tables](../LEGO%20Universe%20CDClient%20Table%20Reference.md)

The client contains the complete game content. The server sends references to it (object
templates, effect IDs, zone IDs, text IDs), never the content itself. A client and a server
therefore have to use **the same content version**; otherwise objects, missions, or whole zones
do not match.

## Packed and unpacked installations

The live client stored `res` in packed archives (`res/pack/*.pk`) with an index and version
files (`versions/`), and the patcher kept them up to date. The installation documented here is
**unpacked**: every file is a normal file under `res`. DarkflameServer can read both layouts
([AssetManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dClient/AssetManager.cpp)):
a packed client is recognized by `client` + `versions` or `res/pack`, an unpacked one by
`res/cdclient.fdb`.

## Folder layout of `res`

| Folder | Files | Main types | Content |
| --- | ---: | --- | --- |
| `mesh` | 13,411 | `.nif` 10,051, `.dds` 3,204 | 3D models and their textures |
| `textures` | 10,667 | `.dds` 9,796, `.gfx` 829 | Textures, icons, and image movies for the UI |
| `animations` | 6,252 | `.kf` 2,578, `.etk` 1,451, `.kfm` 730, `.h` 730, `.settings` 728 | Animations (`.kf` sequences, `.kfm` animation sets, `.etk` event tracks such as sounds or effects at a frame) |
| `brickprimitives` | 5,934 | `.g`, `.g1` ... `.g5` | Brick geometry in detail levels |
| `forkp` | 13,697 | `.psb` 11,366, `.txt` 2,299 | Particle systems ("forkp" effects) |
| `physics` | 4,157 | `.hkx` 4,136 | Havok collision shapes |
| `maps` | 2,529 | see below | Zones, scenes, terrain, minimaps, asset lists |
| `BrickModels` | 2,542 | `.lxfml` 2,429 | Pre-built brick models |
| `ui` | 2,005 | `.dds` 1,818, `.gfx` 181 | User interface movies |
| `scripts` | 1,799 | `.lua` 1,798 | Lua scripts (client and server) |
| `macros` | 267 | `.scm` 266 | Lists of slash commands for testing |
| `audio` | 142 | `.fsb` 98, `.fev` 42 | FMOD sound banks and event projects |
| `shaders` | 34 | `.fxo` 32, `.fxp` 2 | Compiled shader effects |
| `names` | 39 | `.txt` | Name parts for character creation (`minifigname_first/middle/last`) and translations |
| `fonts` | 6 | `.nff` | Bitmap fonts |
| `Movies` | 3 | `.bik` | Videos |
| `license` | 6 | `.txt` | EULA and terms of service, also localized |

Single files at the top of `res`: `cdclient.fdb` (content database), `brickdb.zip` (brick
database), `brickdefaults.paxml`, 31 mouse cursors (`.cur`), `uisettings.xml`, chat word lists,
character-creation letter lists, crash and bug report templates, `logo.bmp`, and
`resmgrstuff.txt` (a list of large files such as terrains and the brick database, apparently for
the resource manager).

## The content database `cdclient.fdb`

`cdclient.fdb` (about 42 MB) is the game's content database in LEGO Universe's own **FDB**
format: a set of tables with typed columns and hash-bucketed rows. It defines all object
templates and their components, skills and behaviors, missions, items, loot, vendors, zones,
activities, and more. The [CDClient table reference](../LEGO%20Universe%20CDClient%20Table%20Reference.md)
describes the tables.

The client and the server read the same data: DarkflameServer converts it to SQLite
(`CDServer.sqlite`). Examples of what the client takes from it:

- **Components of an object.** When the server constructs an object with a LOT, the client looks
  up the template's components in `ComponentsRegistry` and expects the serialized data in the
  matching layout. In the 2011 data, 42,521 registry rows connect templates to 83 component
  types.
- **Models, icons, and names** of objects and items.
- **Skill behaviors**: the client predicts and animates skills from the `Behavior*` tables.
- **Missions**: tasks, rewards, and texts shown in the mission UI.
- **Zones**: `ZoneTable` maps a zone ID to the `.luz` file to load (1,056 rows).

The world server can require the client's file to match its own: when `check_fdb=1`, the client
sends an MD5 checksum of its `cdclient.fdb` during world validation, and the server rejects
clients whose checksum differs.

## World files in `res/maps`

The binary layouts are described in [World file formats](./Client%20World%20File%20Formats.md).

| Type | Count | Content |
| --- | ---: | --- |
| `.luz` | 39 | **Zone file**: spawn point, list of scenes (`.lvl`), terrain file, boundaries, paths (NPC routes, moving platforms, spawner networks), and the revision numbers of its scenes |
| `.lvl` | 661 | **Scene / level file**: placed objects with LOT, position, rotation, scale, and configuration (LDF key-value data); also lighting, sky, and environment settings |
| `.raw` | 39 | Terrain: height map, texture blending, and vegetation |
| `.lutriggers` | 63 | Triggers: events and commands for trigger volumes in a scene |
| `.aud` | 77 | Audio placement for a zone |
| `.evc` | 5 | XML environment data that binds scenes to configurations ("DO NOT EDIT THIS FILE") |
| `.ast`, `.zal` | 26, 39 | Asset lists: files to preload for a zone (`assetlists` folder) |
| `.dds` | 1,580 | Minimaps and terrain textures |

Top-level folders: `01_live_maps` (main worlds: Avant Gardens, Forbidden Valley, Gnarled
Forest, LEGO Club, LUP station, Nimbus Station, the starter space ship, ...), `2011_live_maps`,
`seasonal_live maps`, `nexustower`, `njhub` (Ninjago Monastery), `nsmed`, `fvracetrack`,
`earthgauntlet`, `minimaps`, and `assetlists`.

The server loads the same `.luz`/`.lvl` files to create the world's objects. It sends the zone
ID and a **checksum over the scene revisions** to the client; if it does not match the client's
files, the client reports "The client's map files revision checksum does not match the server's
checksum." and does not enter the zone.

## Localization

All texts are in `locale/locale.xml` (about 9 MB): 24,701 phrases, each with translations for
`en_US`, `de_DE`, and `en_GB`. A phrase has an ID such as `ACT_RACE_EXIT_THE_RACE?`; UI movies,
content data, and scripts refer to the ID. Texts for content records (for example item names)
use IDs derived from the table and row.

- The language is chosen with `LOCALE` in `boot.cfg`.
- Voice-over exists in more languages than the texts (see
  [Audio](./Client%20Audio%20and%20Video.md#event-projects)).
- Some images and movies have language-specific variants in `_loc` folders.
- Unicode text handling uses ICU (`icudt42.dll`).

Server messages that carry text for display usually carry a text ID, not the text, so that each
client shows its own language (`MSG_CLIENT_GENERAL_TEXT_FOR_LOCALIZATION`). Texts that are only
in the server, such as names chosen by players or free chat, arrive as plain text.

## Chat word lists

LEGO Universe was made for children and restricted chat:

| File | Lines | Purpose (inferred from the name and content) |
| --- | ---: | --- |
| `chatplus_en_us.txt` | 8,576 | Allowed words for whitelist chat |
| `chatplus_en_us.dcf` | — | The same list in a compiled form |
| `chatminus_en_us.txt` | 5,753 | Words for the reduced chat mode |
| `german_whitelist.txt` | 3,618 | Allowed German words |
| `characterCreationLetters.txt`, `characterCreationVowels.txt` | — | Letters used to compose names at character creation |

The client uses the lists to give feedback while typing; the final decision about a message is
made by the server (`STRING_CHECK` and the server's own filter).
