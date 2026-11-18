# Worlds, Zones, and Maps — Methodology

[Zones and maps](./README.md) | [Worlds guide](../Worlds%20Guide.md)

This is a curated guide to known worlds, activity instances, properties, and
historical destinations, not an exhaustive `ZoneTable` export or a claim that
every destination is playable. IDs and categories identify local reference
entries; availability and travel rules depend on the deployment.

The zone pages link to existing quest, item, pet, and race references only
when the corresponding page exists. Those pages document their own evidence
and limitations. In particular, quest-zone associations may be objective
locations rather than quest starts, and static map placements do not prove
live or reachable spawns.

## What "usable" means

There is no single database flag that establishes that a map is playable.
Keep these evidence levels separate:

- **Cataloged:** this curated guide has a page for the ID. Inclusion is not a
  playability claim.
- **Accessible-zone candidate:** the inspected DarkflameServer revision's
  `dZoneManager::CheckIfAccessibleZone` returns true when a `ZoneTable` row
  exists and `AssetManager` finds `maps/` plus that row's `zoneName`. This is a
  narrow check used only by selected code paths; it does not check `locStatus`,
  parse the zone, validate its scenes, or prove that a player has a working
  route to it.
- **Loaded zone:** the server resolves that exact resource path, parses the
  zone file, and loads the intended scene/level resources. A missing zone file
  aborts zone loading, but a missing referenced level can be logged while
  initialization continues. `WORLD_READY` alone therefore does not prove that
  all map content loaded.
- **Player-usable:** in addition to loading, the target deployment needs a
  client-compatible resource/data set, a working entry and exit path, and any
  required activity, mission, script, feature-gate, and event configuration.
  This requires testing on a named server/client revision; static database
  rows and placements cannot prove it.

The server constructs the zone path from `ZoneTable.zoneName`; a `.luz` file
with the same filename elsewhere in the client resources is not necessarily a
path match. For example, the local Space Blizzard asset shares a filename with
zone 556's stored path, but the exact paths differ, and activity instance 1261
has no `ZoneTable` row. See the [track evidence](../racing/tracks/space-blizzard.md).
The Unreleased Content inventory reports local files matched by filename, so
file presence in that inventory should not be read as proof that the stored
zone path resolves.

The server-side prerequisites and a runtime validation sequence are detailed
in [Create or Extend a Zone](../../server/content-authoring/create-or-extend-a-zone.md)
and [Test and Troubleshoot Content](../../server/content-authoring/test-and-troubleshoot.md).

The seasonal Space Blizzard track is a special case: its locally parsed
assets and activity evidence identify instance 1261, but the racing
methodology reports no exact ZoneTable asset-path match. It must not be
treated as proof of a currently available zone. Its name is the official
activity name for activity 60. The ZoneTable row whose map file matches the
track's filename is zone 556 ("Winter Racetrack"), which has `locStatus` 0
and no localized name; its stored path does not exactly match the local track
asset path.

No original map image is published here. The catalog is text and links to
previously documented location evidence; it does not provide graphical maps
or claim that every location has coordinate coverage.

Zone names, summaries, and loading-screen tips are the official English
(`en_US`) client strings from `locale.xml` (`ZoneTable_<id>_DisplayDescription`,
`ZoneTable_<id>_summary`, `ZoneLoadingTips_<id>_*`, and
`Activities_<id>_ActivityName` for activity instances). When no localized
string exists, the internal ZoneTable name is shown and labeled as such.

The status column uses the client ZoneTable `locStatus` flag: 2 is shown as
released, 1 as not fully released (Avant Grove, 1151), and 0 as unreleased
(Gnarled Forest Survival, 1301, and Forbidden Valley Siege, 1401). The flag
describes the client data, not what a given server enables. The zone loader
and the server's accessible-zone check do not use this flag as a load gate.

Test and developer maps, unreleased placeholder rows (such as the large
properties and Craggle Rock), the temporary "LUP Station" map (1500), the
20000-series rows without map files, and custom server content are not
listed.

Zone reference pages were generated using
`scripts/build_player_references.py` and enriched with client strings by
`scripts/enrich_zones.py`. The raw local tables are not included in the
public website.
