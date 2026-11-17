# Monument Race (Avant Gardens)

[Racing index](../README.md) | [Racing quests](../Racing%20Quests%20and%20Achievements.md)

Monument Race is a timed on-foot climb in Avant Gardens, distinct from car-racing activities 39, 42, 54, and 60. The local LUZ contains a dedicated `Monument_Race` scene (scene ID 38). Its level places a spawner template LOT 4967 (“AG - Finish Line”) configured with group `StartLine;race;race_manager`, `activityID=1`, and the server script `L_NPC_AG_COURSE_STARTER`; this is static map configuration, not proof of live availability. The public historical page describes the start line near Rusty Steele and goal near the monument summit. No entry NPC is inferred.

## Gameplay and rules

Historical instructions describe starting at the line, choosing one of the color-coded climbing routes, crossing the finish before the timer expires, and having the run canceled if the player leaves the course. Local compiled scripts confirm separate goal/cancel handlers, but they do not prove all historical route exploits or that every old unlock requirement applies to this snapshot.

The Monument goal script forwards a finish event from the `RaceGoal` proximity trigger, and the separate cancel script forwards course cancellation to the first entity in the `race_manager` group. The scene's LOT 4967 configuration is consistent with that manager role, but the triggers themselves do not directly identify a LOT. `NpcAgCourseStarter.cpp` handles start/timer/course events and is also registered in this scene; it is separately used by the AG obstacle-course starter LOT 3004. Do not conflate the Monument goal/cancel scripts, the LOT 4967 scene registration, and the separate LOT 3004 course just because they share script code. No separate `ActivityRewards` matrix is assigned to Monument Race. The shirt/cap/wand medals are linked on their existing achievement pages as related historical/local definitions, not finish-line loot inferred from these triggers.

### Historical route summary

The public page documents three color-coded routes with different build/jump obstacles and historical time thresholds for bronze/silver/gold. This database does not reproduce route-by-route walkthrough prose or treat those thresholds/reward items as locally verified. See the [revision-pinned Monument Race source](../Community%20Sources.md#monument-race) and the existing [quest/achievement pages](../Racing%20Quests%20and%20Achievements.md).

## Local map and objects

- **World/map:** Avant Gardens (1100), `01_Live_Maps/Avant_Gardens/nd_avant_gardens.luz`
- **Race scene:** `nd_avant_gardens_38_monument_race.lvl`, scene ID 38, name `Monument_Race`
- **Relevant local scene templates:** 4967 (AG - Finish Line), 6011 (AG - Rusty -  Assembly Foreman), 6012 (AG - Venture Scout), 6097 (AG - Rebuild Finish Line)
- **Static placements in the Monument Race scene:**

| Object LOT / name | Zone asset | Scene / level | XYZ (map units) | Evidence |
| --- | --- | --- | --- | --- |
| 4967 — AG - Finish Line | 1100 (ZoneTable 1100) | Monument_Race — nd_avant_gardens_38_monument_race.lvl | 123.77, 394.53, 202.4 | [nd_avant_gardens_38_monument_race.lvl](../../../../res/res/maps/01_Live_Maps/Avant_Gardens/nd_avant_gardens_38_monument_race.lvl); LDF activityID 1; transferZoneID —; groupID StartLine;race;race_manager; server script L_NPC_AG_COURSE_STARTER.lua |
| 4967 — AG - Finish Line | 1100 (ZoneTable 1100) | Monument_Race — nd_avant_gardens_38_monument_race.lvl | 310.37, 470.77, 298.6 | [nd_avant_gardens_38_monument_race.lvl](../../../../res/res/maps/01_Live_Maps/Avant_Gardens/nd_avant_gardens_38_monument_race.lvl); LDF activityID 1; transferZoneID —; groupID StartLine |
| 6011 — AG - Rusty -  Assembly Foreman | 1100 (ZoneTable 1100) | Monument_Race — nd_avant_gardens_38_monument_race.lvl | 127.19, 395.48, 183.49 | [nd_avant_gardens_38_monument_race.lvl](../../../../res/res/maps/01_Live_Maps/Avant_Gardens/nd_avant_gardens_38_monument_race.lvl); groupID Minimap_MissionGivers |
| 6012 — AG - Venture Scout | 1100 (ZoneTable 1100) | Monument_Race — nd_avant_gardens_38_monument_race.lvl | 321.05, 472, 296.85 | [nd_avant_gardens_38_monument_race.lvl](../../../../res/res/maps/01_Live_Maps/Avant_Gardens/nd_avant_gardens_38_monument_race.lvl); groupID Minimap_MissionGivers;FinishLine_NPC |
| 6097 — AG - Rebuild Finish Line | 1100 (ZoneTable 1100) | Monument_Race — nd_avant_gardens_38_monument_race.lvl | 310.4, 469.67, 299.2 | [nd_avant_gardens_38_monument_race.lvl](../../../../res/res/maps/01_Live_Maps/Avant_Gardens/nd_avant_gardens_38_monument_race.lvl); LDF activityID 6097; transferZoneID — |

Object placements in other Avant Gardens scenes, if any, are not treated as Monument Race entry/finish locations:

| Object LOT / name | Zone asset | Scene / level | XYZ (map units) | Evidence |
| --- | --- | --- | --- | --- |
| 6417 — AGFX - Platforming Statue FX1B | 1100 (ZoneTable 1100) | monument_a — nd_avant_gardens_19_monument_a.lvl | 111.08, 390, 281.41 | [nd_avant_gardens_19_monument_a.lvl](../../../../res/res/maps/01_Live_Maps/Avant_Gardens/nd_avant_gardens_19_monument_a.lvl) |
| 6615 — AG Monument Scene Tree Glom | 1100 (ZoneTable 1100) | MONUMENT — nd_avant_gardens_35_monument.lvl | 178.24, 398.02, 0.2 | [nd_avant_gardens_35_monument.lvl](../../../../res/res/maps/01_Live_Maps/Avant_Gardens/nd_avant_gardens_35_monument.lvl) |

The scene list contains the placed race-manager/start-line candidate, two mission-giver templates, and a rebuildable finish-line template. Their static placement/configuration does not establish a live route, and the goal trigger object is not conclusively mapped to a template. Other named Monument scenery in other Avant Gardens scenes is shown separately.

## Related definitions and sources

The local mission/achievement cross-links are [Mission 319](../../quests/319.md), [Mission 1877](../../quests/1877.md), [Mission 1884](../../quests/1884.md), [Achievement 179](../../quests/179.md), [Achievement 180](../../quests/180.md), and [Achievement 181](../../quests/181.md). The existing pages remain authoritative for prerequisites, tasks, and deterministic completion rewards. Historical source: [Monument Race (revision 161059)](../Community%20Sources.md#monument-race).

Monument trigger scripts: [AgMonumentRaceGoal.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/02_server/Map/AG/AgMonumentRaceGoal.cpp) and [AgMonumentRaceCancel.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/02_server/Map/AG/AgMonumentRaceCancel.cpp). The [AG obstacle-course handler](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/02_server/Map/AG/NpcAgCourseStarter.cpp) is described separately. The level/scene pairing is parsed from the local [Avant Gardens ZoneTable row](../../../db/ZoneTable.csv).
