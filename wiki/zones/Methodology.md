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

The seasonal Space Blizzard track is a special case: its locally parsed
assets and activity evidence identify instance 1261, but the racing
methodology reports no exact ZoneTable asset-path match. It must not be
treated as proof of a currently available zone. Its name is the official
activity name for activity 60. The ZoneTable row whose map file matches the
track asset is zone 556 ("Winter Racetrack"), which has `locStatus` 0 and no
localized name.

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
describes the client data, not what a given server enables.

Test and developer maps, unreleased placeholder rows (such as the large
properties and Craggle Rock), the temporary "LUP Station" map (1500), the
20000-series rows without map files, and custom server content are not
listed.

Zone reference pages were generated using
`scripts/build_player_references.py` and enriched with client strings by
`scripts/enrich_zones.py`. The raw local tables are not included in the
public website.
