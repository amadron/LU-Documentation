# Racing Guide and Database

[Game Guide](../README.md) | [Racing Guide](../Racing%20Guide.md) | [Quest Guide](../Quest%20Guide.md)

Want to race? Start with the short [Racing Guide](../Racing%20Guide.md) for
the player-facing basics. This page is the detailed lookup for track rules,
possible entrances, reward records, and racing objectives.

The local files describe four car-racing activities, on-foot races, Monument
Race, and some legacy or test content. A stored definition does not guarantee
that a race is enabled on your server. For mission goals, follow your in-game
journal and the [Quest Guide](../Quest%20Guide.md).

## Browse the tracks and activities

- [Keelhaul Canyon Raceway](./tracks/keelhaul-canyon.md) — activity 39, instance 1303.
- [Vertigo Loop](./tracks/vertigo-loop.md) — activity 42, instance 1203.
- [Dragonmaw Chasm](./tracks/dragonmaw-chasm.md) — activity 54, instance 1403.
- [Space Blizzard](./tracks/space-blizzard.md) — activity 60, instance 1261.
- [Foot races and timed courses](./tracks/foot-races.md) — local generic foot-race templates and separately registered activity records.
- [Avant Gardens timed obstacle course](./tracks/ag-obstacle-course.md) — distinct from Monument Race.
- [Monument Race](./tracks/monument-race.md) — Avant Gardens on-foot timed course.
- [Race cars and modules](./tracks/race-cars-and-modules.md).
- [Legacy, seasonal, and test racing content](./tracks/legacy-and-test-racing.md).
- [Racing quests and achievements](./Racing%20Quests%20and%20Achievements.md) — links to existing numbered pages.

## Definition coverage

| Area | Local coverage |
| --- | --- |
| Full car tracks | 4 distinct activity IDs in Activities and track-controller server scripts (39, 42, 54, 60); activity 60 is seasonal/unmatched by ZoneTable. |
| Static race rewards | 80 ActivityRewards rows, with per-rating loot-matrix and currency indices retained. |
| Racing quest objectives | 84 mission/achievement pages with attached task-type-23 objectives; 84 typed rows. |
| Racing category | 66 existing quest/achievement pages carry the source Racing category; linked without duplicating them. |
| Reused quest pages | 97 distinct existing quest/achievement pages linked across typed objectives, Racing categories, and Monument-chain evidence. |
| Foot races | 7 ComponentsRegistry templates, plus map-LDF registrations for activity 53 and a cautious activity-49 Nexus Tower candidate; stored award rows are listed separately from leaderboard semantics. |
| AG obstacle course | Separate scripted on-foot activity; its mission hook and static object placements are documented on its own page. |
| Map evidence | 39 parsed local LUZ assets; 34 have one or more exact ZoneTable path matches. |
| Static race-related object names | 247 records matching race/track naming; not all are playable content. |

[Methodology and limitations](./Methodology.md) | [Revision-pinned community sources](./Community%20Sources.md) | [Machine-readable coverage](./Coverage.json)
