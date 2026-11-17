# Racing database — methodology and limitations

[Overview](./README.md) | [Racing quests](./Racing%20Quests%20and%20Achievements.md) | [Coverage.json](./Coverage.json)

Generated **2026-11-17** from local tables/assets and reviewed against DarkflameServer source revision `8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`. No local server/game code or shared wiki navigation was changed.

## What is included

The four Activities explicitly configured by the local race-controller scripts are IDs 39 (Gnarled Forest), 42 (Nimbus Station), 54 (Forbidden Valley), and 60 (winter track). They have 80 ActivityRewards rows total. Their instance maps are joined from `Activities.instanceMapID` to `ZoneTable.zoneID`; for mapped activities, the ZoneTable path `maps/<zoneName>` is then parsed and matched to LUZ scene/LVL assets. The seasonal instance has an asset and embedded ID but no exact ZoneTable path match.

Additional activities are included only when source evidence identifies them: generic script-registered foot races, the Avant Gardens Monument Race, and the separately scripted AG timed obstacle course. Legacy/test-named data is labeled separately.

## Join/evidence rules

- `Activities.ActivityID` is joined to the `activityID` sent by each track-specific server controller. Its `instanceMapID` is a zone-map ID; it is not a race name or entry NPC.
- `ActivityRewards.objectTemplate` is treated as the activity ID only for the activity-result lookup. `activityRating`, `LootMatrixIndex`, and `CurrencyIndex` are retained as separate values.
- A static entry-object coordinate is published only when an object LOT/component identifies the activity and the object appears in a parsed LVL under the corresponding ZoneTable map. Missing/ambiguous entries stay unresolved.
- NPC/entry descriptions and static LOTs are not interpreted as reachable or live. Map objects and spawner waypoints can overlap, be gated, or be disabled.
- Existing quest data is linked by actual typed objective rows (task type 23 or activity objective 23) and separately by the Quest Summary's Racing source category. Mission and achievement pages are reused, not duplicated. Source category alone is not proof of a playable race.
- Public Fandom data is supplemental historical evidence, revision-pinned in [Community Sources](./Community%20Sources.md). Similar names never establish a local ID join.

## English client names

The pages were first generated without the client locale. They have since been enriched by `scripts/enrich_pets_racing.py` in the documentation repository, which reads the English (en_US) strings of the client's `locale.xml` together with `CDServer.sqlite`:

- quest and achievement names from `Missions_<id>_name`, replacing “Quest N”/“Achievement N” placeholders and three earlier community-name guesses (637, 663, 1884);
- mission-ID objective targets (Racemaster, Go Outside and Play) listed by client name, with long target lists shortened to the first eight names plus a count;
- track names from `ZoneTable_<id>_DisplayDescription` and `Activities_<id>_ActivityName`; world 1261 has no ZoneTable row, so it is labeled with the activity name “Space Blizzard Racetrack (1261)”;
- NPC and object names from `Objects_<lot>_name` (for example “Natso Fast - Foot Race Host”), with the Objects template name kept in parentheses; foot-race activity names from `Activities_<id>_ActivityName`;
- links to map files outside the documentation tree were replaced by plain `client/res/maps/...` paths.

The script is idempotent and only edits `wiki/pets/` and `wiki/racing/`. Objects without a client string (for example the Race Activator templates 10413, 11178 and 11418) keep their template names.

## Track setup and racing-task semantics

The four controller scripts configure `MainPath`, vehicle object 7703, three laps, 2–6 one-player teams, 60,000 ms wait, 3,000 ms start delay, and place scoring values. Static Activities rows list optional cost LOT 3039 ×1 for the four activity IDs. Cost presence is reported as stored configuration, not proof it is always charged.

`eRacingTaskParam` changes the namespace and interpretation of task fields: values 4/5 refer to mission completions, 17 to smashed LOTs, and common track/time targets otherwise use world IDs or time thresholds. Lap and total time comparisons use milliseconds. See [quest methodology](../quests/Methodology.md#typed-objective-targets) and the linked individual objective pages.

## Rewards: rated activity matrix, not a per-race drop rate

The server selects the eligible ActivityRewards row with the greatest `activityRating <= result rating`. It then resolves that row's matrix and currency. The listed currency index is not converted into an unconditional amount in these pages.

For each matrix, the candidate LOT list and modeled probability are recomputed from LootMatrix, LootTable, RarityTable, and ItemComponent. The implementation preserves duplicate loot-table rows and follows the local rarity-fallback selection. It estimates the chance of at least one LOT **per matrix invocation** before player eligibility filters; it is not a per-race or per-player drop chance. MissionDrop filtering, personal/team loot rules, faction-token proxy conversion/discard, activity override, and any live differences can change receipt. The source and details are on each track page.

## File formats, coverage and unresolved rows

- `Activities`: 158 local rows; four track-controller activity IDs above, plus inactive/unmapped values such as 23.
- `ActivityRewards`: 291 rows overall; 80 belong to the four track IDs.
- Typed racing objectives: 84 rows across 84 definitions; 1 orphan(s) without a Missions parent.
- Racing category links: 66; these include all of the existing source category pages, including definitions without an attached generic racing objective.
- Local race/track-named Objects rows: 247; this broad name-based set is an audit inventory, not a count of playable races.
- Race/foot-race script rows: 62; only explicit active controller/manager associations are treated as activities.
- Map assets parsed: 39 LUZ files, 34 matched by exact ZoneTable asset path; errors: 0.

Raw values and exceptional assets are in [Coverage.json](./Coverage.json). Orphan racing objective(s): mission 1405, UID 1937.

## Source implementation

- Race controllers: activity 39 [GfRaceServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/ai/RACING/TRACK_GF/GfRaceServer.cpp); activity 42 [NsRaceServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/ai/RACING/TRACK_NS/NsRaceServer.cpp); activity 54 [FvRaceServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/ai/RACING/TRACK_FV/FvRaceServer.cpp); activity 60 [NsWinterRaceServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/ai/RACING/TRACK_NS_WINTER/NsWinterRaceServer.cpp).
- [RacingControlComponent.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/RacingControlComponent.cpp), [Loot.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/Loot.cpp), [Activities.csv](../../db/Activities.csv), [ActivityRewards.csv](../../db/ActivityRewards.csv).
- Generic foot race: [BaseFootRaceManager.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/ai/ACT/FootRace/BaseFootRaceManager.cpp); separate AG obstacle course: [NpcAgCourseStarter.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/02_server/Map/AG/NpcAgCourseStarter.cpp).
- Monument Race triggers: [AgMonumentRaceGoal.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/02_server/Map/AG/AgMonumentRaceGoal.cpp) and [AgMonumentRaceCancel.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/02_server/Map/AG/AgMonumentRaceCancel.cpp); their `race_manager` implementation is unresolved, so they are not attributed to the AG obstacle-course starter.
- Racing task parameters: [eRacingTaskParam.h](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eRacingTaskParam.h).

## Validation expectations

The racing-specific checker verifies all four configured track activities, reward/matrix resolution, linkable quest/achievement pages, page sizes, and generated table widths. A parent-level wiki-wide checker separately covers cross-folder links and Markdown conventions.
