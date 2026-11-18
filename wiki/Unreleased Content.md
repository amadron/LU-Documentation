# Unreleased and Cut Content

[Game Guide](./README.md) | [Worlds](./Worlds%20Guide.md) | [Zones and maps](./zones/README.md) | [Faction Guide](./Faction%20Guide.md)

The final game client still contains content that players never saw: worlds that were
never opened, characters that were replaced, and gear that was planned but not finished.
This page lists what the client data shows, with the evidence for each entry.

!!! note "How to read this page"
    A definition in the data is not proof of what the developers intended. Entries are
    included when the data marks them as never released: a status of *not localized*
    (`locStatus` 0) on worlds and activities, names the developers tagged *[DNL]* (do not
    localize), *DO NOT USE* or *unused*, or references to objects that do not exist.
    Seasonal content that was switched on only for events is listed separately.
    Test and developer maps are left out.

## Worlds that ship in the client but were never opened

These map files are present in the client, but their zone entries were never localized
and no launch pad leads to them. The listed path is the local client asset path matched
by filename; it is not proof that the ZoneTable's stored path resolves to that asset.

| Zone | Internal name | Map file | Status | Notes |
| --- | --- | --- | --- | --- |
| 556 | Winter Racetrack | `maps/seasonal&#95;live maps/december/ns&#95;winter&#95;racetrack/nd&#95;nimbus&#95;station&#95;winter-racetrack.luz` | Not localized | Winter racetrack; a local asset has this filename, but its path does not exactly match the stored ZoneTable path. The seasonal race shipped as activity "Space Blizzard Racetrack" (1261), see the [Racing Guide](./Racing%20Guide.md). |
| 1152 | Avant Gardens Large Property | `maps/2011&#95;live&#95;maps/pp&#95;ag&#95;large/nd&#95;ag&#95;property&#95;large.luz` | Not localized | Large property for Avant Gardens. |
| 1202 | NS Shooting Gallery | `maps/01&#95;live&#95;maps/nimbus&#95;station/shooting&#95;gallery/nd&#95;ns&#95;sg&#95;ducks.luz` | Not localized | A duck shooting gallery for Nimbus Station; single-player activity 7583 is defined for it. |
| [1301](./zones/1301.md) | Gnarled Forest Survival | `maps/01&#95;live&#95;maps/gnarled&#95;forest/survival/nd&#95;gf&#95;survival&#95;battle.luz` | Not localized | Survival mode for Gnarled Forest. |
| [1401](./zones/1401.md) | Forbidden Valley Siege | `maps/01&#95;live&#95;maps/forbidden&#95;valley/siege/nd&#95;fv&#95;siege.luz` | Not localized | Siege mode for Forbidden Valley; activity 37 is defined for 2–4 players. |

Some never-localized zone entries only point at the map of a released world and are
old duplicate entries, not separate areas: 375 "Gnarled Forest Deep Dive Map" (map of [1300](./zones/1300.md)); 545 "FV race track" (map of [1403](./zones/1403.md)).

## Planned worlds without a map

The zone table names these areas, but the client has no map for them.

| Zone | Name | Map file | Notes |
| --- | --- | --- | --- |
| 1252 | Nimbus Station Large Property | `01&#95;Live&#95;Maps/Nimbus&#95;Station/Property/Large/nd&#95;ns&#95;property&#95;large.luz` (missing) | Large property for Nimbus Station. |
| 1352 | Gnarled Forest Large Property | `01&#95;Live&#95;Maps/Gnarled&#95;Forest/Property/Large/nd&#95;gf&#95;property&#95;large.luz` (missing) | Large property for Gnarled Forest. |
| 1452 | Craggle Rock | `01&#95;Live&#95;Maps/Forbidden&#95;Valley/Property/Large/nd&#95;fv&#95;property&#95;large.luz` (missing) | Large property for Forbidden Valley ("Craggle Rock"). |
| 1500 | LUP Station | `01&#95;Live&#95;Maps/LUP&#95;Station/nd&#95;lup&#95;station.luz` (missing) | "LUP Station" — its official summary reads "Temp map for LUP content". The released Starbase 3001 (1600) map sits in the same LUP_Station folder. |
| 1801 | Nexus Tower Battlefield Crater | `2011&#95;Live&#95;Maps/Aura&#95;Mar&#95;Crater/nd&#95;aura&#95;mar&#95;crater.luz` (missing) | "Nexus Tower Battlefield Crater"; planned next to Crux Prime, whose map folder is Aura_Mar. |
| 20000 | MBL Station | Removed | Named entry with its map removed; the released World Builder planets use zones 1601–1604. |
| 20022 | Moonbase | Removed | Older entry with the same name as the released zone 1603; its map was removed. |
| 20061 | Port-a-bello | Removed | Older entry with the same name as the released zone 1604; its map was removed. |
| 20101 | Deep Freeze | Removed | Older entry with the same name as the released zone 1601; its map was removed. |
| 20147 | Robot City | Removed | Older entry with the same name as the released zone 1602; its map was removed. |

## Seasonal and partly released content

- **Space Blizzard Racetrack** (activity 60, see [zone 1261](./zones/1261.md)) was a winter
  event race. It has no ZoneTable row of its own; zone 556 "Winter Racetrack" has the same
  map filename but a different stored path and is not localized. Instance 1261 has no
  ZoneTable row, so the server's normal map lookup cannot resolve a zone asset for that ID;
  activity and asset evidence alone do not establish that it loads or is reachable.
- **Seasonal map objects** are switched on by event gates in the map files. DarkflameServer
  enables them through the `event_1` … `event_8` settings in `worldconfig.ini`.
- **Avant Grove** ([zone 1151](./zones/1151.md)) is only partly localized (locStatus 1).
- **Frakjaw Battle** (activity 58) has activity locStatus 1, although its
  zone [Battle Against Frakjaw!](./zones/2001.md) is released.

## Characters and objects marked as not for use

The developers tagged these templates *[DNL]* (do not localize), *DO NOT USE* or *unused*.
The most telling group are the four **original faction representatives**: Dirk Manleigh
(Sentinels), Logan Moonshot (Venture League), Ellgren Stackwell (Assembly) and Silas Penumbra
(Paradox). The 2010 guide still names Silas Penumbra; in the released game the faction
introductions are handled by other characters (see the [Faction Guide](./Faction%20Guide.md)).
The *[DNL] Valiant …* entries are named after the valiant gear; the data does not show
what they were for.

| LOT | Internal name | Display name |
| --- | --- | --- |
| 1947 | DO NOT USE GF - Banana Crate | DO NOT USE GF - Banana Crate |
| [3478](./items/3478.md) | unused Quest Brick - Plate 1x1 round | unused Quest Brick - Plate 1x1 round |
| [3479](./items/3479.md) | unused Quest Brick - 1x1 plate | unused Quest Brick - 1x1 plate |
| [3480](./items/3480.md) | unused Quest Brick - 1x1 headlight brick | unused Quest Brick - 1x1 headlight brick |
| [3508](./items/3508.md) | unused Quest Brick - Whip/Aerial | unused Quest Brick - Whip/Aerial |
| [3907](./items/3907.md) | unused Inventor's Widget | unused Inventor's Widget |
| 4915 | Test exhibit/bouncer - DO NOT USE | Test exhibit/bouncer - DO NOT USE |
| 6576 | AG - Spaceship Bob 001 DO NOT USE | AG - Spaceship Bob 001 DO NOT USE |
| 7094 | Sentinel Rep | DNL - Dirk Manleigh - Sentinel Faction Rep |
| 7095 | Venture Rep | DNL - Logan Moonshot - Venture League Rep |
| 7096 | Assembly Rep | DNL -Ellgren Stackwell - Assembly Rep |
| 7097 | Paradox Rep | DNL - Silas Penumbra - Paradox Rep |
| [7433](./items/7433.md) | Unused Story Tablet 1 | Story Tablet 1 |
| [7434](./items/7434.md) | unused Story Tablet 2 | Story Tablet 2 |
| [7435](./items/7435.md) | unused Story Tablet 3 | Story Tablet 3 |
| [8231](./items/8231.md) | Old Car Module - Wheels | Do Not Use These Wheels |
| 12264 | Temp&#95;PirateBronson | &#91;DNL&#93; Temp Pirate - NOT NEEDED |
| 12327 | Temp&#95;BankGuard | &#91;DNL&#93; Temp Bank Guard - NOT NEEDED |
| 12382 | (do not use) POI Trigger Wall | POI Trigger Wall |
| 12383 | (do not use) POI Trigger Wall | POI Trigger Wall |
| 12489 | &#91;DNL&#93; Valiant Ship | &#91;DNL&#93; Valiant Ship |
| 12618 | &#91;DNL&#93; Valiant Cleaner | &#91;DNL&#93; Valiant Cleaner |
| 12629 | &#91;DNL&#93; Valiant Target Dummy | &#91;DNL&#93; Valiant Target Dummy |
| 12662 | &#91;DNL&#93; Valiant Mech | &#91;DNL&#93; Valiant Mech |
| 12804 | &#91;DNL&#93; Valiant Spiderling | &#91;DNL&#93; Valiant Spiderling |
| 12807 | &#91;DNL&#93; Valiant Owl | &#91;DNL&#93; Valiant Owl |
| 14011 | Dr. Overbuild DO NOT USE | Dr. Overbuild DO NOT USE |
| 16022 | &#91;DNL&#93; Ninjago Hound | &#91;DNL&#93; Ninjago Hound |
| 16921 | &#91;DNL&#93; Summoned Crocodile Ally | &#91;DNL&#93; Summoned Crocodile Ally |

## Unfinished gear

**Missing valiant weapons.** The rank-3 sets of the four later classes list a valiant weapon
that has no object definition, while the eight original classes have one. Only the hidden
off-hand proxy items exist for some of them.

| Class | Missing LOT | Listed in rank set |
| --- | --- | --- |
| [Adventurer](./classes/adventurer.md) | 13276 | 2, 3 |
| [Inventor](./classes/inventor.md) | 13278 | 3 |
| [Shinobi](./classes/shinobi.md) | 13275 | 3 |
| [Space Ranger](./classes/space-ranger.md) | 13277 | 3 |

**Test kits.** Item sets 45–47 (*Test Rank 1–3* sword, hat, shirt, pants, shield, shoulders)
are developer test equipment and were never localized.

See the [class pages](./classes/README.md) for the released kits.

## Pets

- **Lion:** the pet is defined and has a taming puzzle, but no map spawns it and no
  mission points to a location. See the [Pet Guide](./Pet%20Guide.md).
- **Taming puzzles without a pet:** [LOT 16479](./pets/16479.md), [LOT 5638](./pets/5638.md) — puzzle rows exist, but no object, name or placement.

## Hidden missions are not cut content

Most missions that were never localized are *Hidden* missions: invisible trackers the game
uses for flags and progress (for example the faction-join markers 544, 555, 566 and 577).
They are part of the released game. Only a few are developer tests, such as
[mission 1730](./quests/1730.md) "TEST - Gather tasks (fixification)" and mission 1893.

## Source and limitations

Generated by `scripts/build_unreleased.py`. Release status (`ZoneTable`, `Activities`) is read
from the original client database `cdclient.fdb`; `Objects`, `ItemSets` and
`TamingBuildPuzzles` come from the server copy of it, plus the English client locale and the list of map
files in the client. Notes on what an area was meant to be come from its internal name or
summary. Content that was released and later removed from the client cannot be seen here.
Custom content of this server installation is excluded.
