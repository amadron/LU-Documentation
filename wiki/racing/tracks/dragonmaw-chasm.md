# Dragonmaw Chasm

[Racing index](../README.md) | [Methodology](../Methodology.md) | [Race quests](../Racing%20Quests%20and%20Achievements.md)

## What and where

Activity 54 is the Forbidden Valley race instance. The local race activator LOT 11178 is registered to activity 54 and appears in Forbidden Valley.

- **World / activity instance:** Forbidden Valley (world 1400); instance 1403
- **Server activity:** 54; activity table location 1403
- **Local ZoneTable asset:** `FVracetrack/fv_racetrack.luz`
- **Map parse:** embedded world 1403; 17 scene(s); 150 spawner waypoint(s)
- **Scene names:** `Global Scene`, `StartArea`, `StartAreaBridge`, `StartAreaFall`, `Hatchery`, `DragonColumn`, `DragonBank`, `Dragon2Paradox`, `ParadoxRoad`, `Paradox`, `Paradox2Strom`, `StromStart`, `StromRoad`, `Bounce`, `Tree`, `TreeDrop`, `CaveStart`
- **Historical track name:** Dragonmaw Chasm Raceway (see revision-pinned [community source](../Community%20Sources.md#dragonmaw-chasm))
- **Client name (locale.xml):** Dragonmaw Chasm Racetrack (`Activities_54_ActivityName` and `ZoneTable_1403_DisplayDescription`)

### Entry point and coordinates

| Object LOT / name | Zone asset | Scene / level | XYZ (map units) | Evidence |
| --- | --- | --- | --- | --- |
| 11178 — FV - Race Activator | 1400 (ZoneTable 1400) | Global Scene — nd_forbidden_valley.lvl | 787.47, 240.56, 459.27 | `client/res/maps/01_Live_Maps/Forbidden_Valley/nd_forbidden_valley.lvl`; LDF activityID 54; transferZoneID 1403 |

Coordinates are static LVL object origins in the authored map asset, not a live NPC/player position, path trigger, or guarantee that the activity is enabled. Where local component registration does not prove which object launches this track, it is not labeled as an entrance.

## How the race works

The local per-track server scripts configure this activity as a three-lap car race for individual racers: 2–6 teams/players, one player per team, a 60-second wait period, and a 3-second start delay. The configured vehicle is LOT 7703 (a static test-named “Racing Vehicle Min Balanced” vehicle template); this is not a player-car LOT recommendation. The race uses the `MainPath` route. Exact current deployment, player count, timing, client UI, or availability can differ.

Configured optional entry cost: [Green Imaginite (LOT 3039)](../../items/3039.md) × 1. This is the Activities row value; it is not a guaranteed deduction on every server/client flow.

1. Reach the track through its world activity/entry route, if available.
2. Bring/use a player-built race car and enter the race instance.
3. Complete the three laps, crossing track checkpoints and avoiding course hazards. The local track script sets race/activity state; track-specific item names and hazards are partly documented only by historical sources.
4. Finish to produce a placement/rating. The rating selects the stored activity-reward tier below; it does not itself specify the probability of an individual item.

### Track-specific route evidence

The local LUZ splits the race into a global scene and named sections from StartArea through the hatchery, Paradox, Stromling, tree, and cave areas.

The public historical route account describes the course descending from the Forbidden Valley ridgeline through a dragon-egg area, refinery hazards and the Great Tree. Its hazards include gas jets and falling pillars; this is not proof of current dynamic activation.

Historical hazards and narrative route details below are community-reported; the local static map does not prove which dynamic hazards are enabled in a live server.

## Race results and rewards

The local `ActivityRewards` table has 20 rows for activity 54, referencing 11 distinct loot matrices. The server chooses the highest `activityRating` not greater than the result rating. Each selected row provides a loot-matrix index and currency index. A matrix roll is not a “drop rate” for every item: each row triggers by its own percentage, the number of draws varies, rarity tables weight eligible loot rows, and MissionDrop/player/team/faction conditions may filter or transform results.

| Activity rating | Stored tier / place | Loot matrix | Currency index | Challenge rating |
| --- | --- | --- | --- | --- |
| 21 | FV Racetrack 1st Place - 2 players | 651 | 78 | 1 |
| 22 | FV Racetrack 2nd Place - 2 players | 652 | 79 | 1 |
| 31 | FV Racetrack 1st Place - 3 players | 648 | 75 | 1 |
| 32 | FV Racetrack 2nd Place - 3 players | 649 | 76 | 1 |
| 33 | FV Racetrack 3rd Place - 3 players | 650 | 77 | 1 |
| 41 | FV Racetrack 1st Place - 4 players | 642 | 69 | 1 |
| 42 | FV Racetrack 2nd Place - 4 players | 643 | 70 | 1 |
| 43 | FV Racetrack 3rd Place - 4 players | 644 | 71 | 1 |
| 44 | FV Racetrack 4th Place - 4 players | 645 | 72 | 1 |
| 51 | FV Racetrack 1st Place - 5 players | 642 | 69 | 1 |
| 52 | FV Racetrack 2nd Place - 5 players | 643 | 70 | 1 |
| 53 | FV Racetrack 3rd Place - 5 players | 644 | 71 | 1 |
| 54 | FV Racetrack 4th Place - 5 players | 645 | 72 | 1 |
| 55 | FV Racetrack 5th Place - 5 players | 646 | 73 | 1 |
| 61 | FV Racetrack 1st Place - 6 players | 642 | 69 | 1 |
| 62 | FV Racetrack 2nd Place - 6 players | 643 | 70 | 1 |
| 63 | FV Racetrack 3rd Place - 6 players | 644 | 71 | 1 |
| 64 | FV Racetrack 4th Place - 6 players | 645 | 72 | 1 |
| 65 | FV Racetrack 5th Place - 6 players | 646 | 73 | 1 |
| 66 | FV Racetrack 6th Place - 6 players | 647 | 74 | 1 |

### Possible item outcomes from those matrices

| Loot matrix | Distinct candidate LOTs | Candidate items and modeled chance |
| --- | --- | --- |
| 642 | 11 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item)<br>[Chase Cutter Engine Panel 2 (LOT 9336)](../../items/9336.md) — modeled 10% per matrix invocation<br>[Chase Cutter Engine Panel 2 (LOT 9339)](../../items/9339.md) — modeled 10% per matrix invocation<br>[Chase Cutter Rear Panel 3 (LOT 9362)](../../items/9362.md) — modeled 10% per matrix invocation<br>[Chase Cutter Rear Bumper 2 (LOT 9371)](../../items/9371.md) — modeled 10% per matrix invocation<br>[Bolt Ox Front Bumper 2 (LOT 9376)](../../items/9376.md) — modeled 10% per matrix invocation<br>[Bolt Ox Engine Panel 1 (LOT 9381)](../../items/9381.md) — modeled 10% per matrix invocation<br>[Bolt Ox Engine Panel 2 (LOT 9384)](../../items/9384.md) — modeled 10% per matrix invocation<br>[Paragon Warp Front Bumper 1 (LOT 9404)](../../items/9404.md) — modeled 10% per matrix invocation<br>[Paragon Warp Rear Panel 1 (LOT 9424)](../../items/9424.md) — modeled 10% per matrix invocation<br>[Paragon Warp Rear Panel 2 (LOT 9426)](../../items/9426.md) — modeled 10% per matrix invocation |
| 643 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 644 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 645 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 646 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 647 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 648 | 11 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item)<br>[Chase Cutter Engine Panel 2 (LOT 9336)](../../items/9336.md) — modeled 10% per matrix invocation<br>[Chase Cutter Engine Panel 2 (LOT 9339)](../../items/9339.md) — modeled 10% per matrix invocation<br>[Chase Cutter Rear Panel 3 (LOT 9362)](../../items/9362.md) — modeled 10% per matrix invocation<br>[Chase Cutter Rear Bumper 2 (LOT 9371)](../../items/9371.md) — modeled 10% per matrix invocation<br>[Bolt Ox Front Bumper 2 (LOT 9376)](../../items/9376.md) — modeled 10% per matrix invocation<br>[Bolt Ox Engine Panel 1 (LOT 9381)](../../items/9381.md) — modeled 10% per matrix invocation<br>[Bolt Ox Engine Panel 2 (LOT 9384)](../../items/9384.md) — modeled 10% per matrix invocation<br>[Paragon Warp Front Bumper 1 (LOT 9404)](../../items/9404.md) — modeled 10% per matrix invocation<br>[Paragon Warp Rear Panel 1 (LOT 9424)](../../items/9424.md) — modeled 10% per matrix invocation<br>[Paragon Warp Rear Panel 2 (LOT 9426)](../../items/9426.md) — modeled 10% per matrix invocation |
| 649 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 650 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 651 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 652 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |

Per-item percentages above are **modeled chance of at least one LOT per matrix invocation**, before player/mission eligibility filters and proxy-token conversion, using the checked source's LootMatrix/RarityTable/LootTable selection rules. Repeated LootTable rows are retained in weighting. These are not unconditional per-race or per-player probabilities and do not account for team assignment, mission filters, or live-server overrides. Reward rows which share a matrix share its candidate pool; the rank/rating controls which matrix/currency pair is selected.

**Currency indexes are kept as indexes, not converted to a coin range here.** See the exact row in [ActivityRewards.csv](../../../db/ActivityRewards.csv) and related [CurrencyTable.csv](../../../db/CurrencyTable.csv).

## Related quests and achievements

| Existing quest/achievement page | Racing-linked objective(s) |
| --- | --- |
| [Quest 625](../../quests/625.md) — Speed Boost! | UID 941: Collect racing Imagination pickups until the counter reaches 9 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 648](../../quests/648.md) — Low Deductible 1 | UID 964: Finish 10 matching race(s) without being smashed: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 649](../../quests/649.md) — Low Deductible 2 | UID 965: Finish 25 matching race(s) without being smashed: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 650](../../quests/650.md) — Low Deductible 3 | UID 966: Finish 50 matching race(s) without being smashed: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 651](../../quests/651.md) — Street Sweeper 1 | UID 967: Smash racing smashables until the counter reaches 100 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 652](../../quests/652.md) — Street Sweeper 2 | UID 968: Smash racing smashables until the counter reaches 250 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 653](../../quests/653.md) — Street Sweeper 3 | UID 969: Smash racing smashables until the counter reaches 500 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 654](../../quests/654.md) — Drive-Thru Dreamer 1 | UID 970: Collect racing Imagination pickups until the counter reaches 100 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 655](../../quests/655.md) — Drive-Thru Dreamer 2 | UID 971: Collect racing Imagination pickups until the counter reaches 500 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 656](../../quests/656.md) — Drive-Thru Dreamer 3 | UID 972: Collect racing Imagination pickups until the counter reaches 1000 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 657](../../quests/657.md) — Racing Fanatic 1 | UID 973: Finish/participate in 25 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 658](../../quests/658.md) — Racing Fanatic 2 | UID 974: Finish/participate in 25 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 659](../../quests/659.md) — Racing Fanatic 3 | UID 975: Finish/participate in 50 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 661](../../quests/661.md) — Five-Time Champion | UID 977: Win 5 credited race(s) in allowed worlds: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 662](../../quests/662.md) — Ten-Time Champion | UID 978: Win 10 credited race(s) in allowed worlds: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 663](../../quests/663.md) — Twenty-Time Champion | UID 979: Win 20 credited race(s) in allowed worlds: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 667](../../quests/667.md) — Try, Try Again | UID 983: Finish last in 10 credited race(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1160](../../quests/1160.md) — Faster! Faster! | UID 1613: Finish the race in at most 245 seconds (245000 ms) on an allowed track: Dragonmaw Chasm Racetrack. |
| [Quest 1161](../../quests/1161.md) — Quick as a Lash | UID 1614: Finish a lap in at most 87 seconds (87000 ms) on an allowed track: Dragonmaw Chasm Racetrack. |
| [Quest 1162](../../quests/1162.md) — Dragonmaw Chasm Victory | UID 1615: Finish at position 1 or better on an allowed track: Dragonmaw Chasm Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1163](../../quests/1163.md) — Dragonmaw Top 3 | UID 1616: Finish at position 3 or better on an allowed track: Dragonmaw Chasm Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 1164](../../quests/1164.md) — Dragonmaw Chasm Super Champ | UID 1617: Win 10 credited race(s) in allowed worlds: Dragonmaw Chasm Racetrack. |
| [Quest 1165](../../quests/1165.md) — Nerves of Steel | UID 1618: Finish 1 matching race(s) without being smashed: Dragonmaw Chasm Racetrack. |
| [Quest 1408](../../quests/1408.md) — Drive Five | UID 1940: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1506](../../quests/1506.md) — Drive Five | UID 2078: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1543](../../quests/1543.md) — Drive Five | UID 2140: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1580](../../quests/1580.md) — Drive Five | UID 2202: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1626](../../quests/1626.md) — Dragonmaw Chasm Pro | UID 2278: Finish at position 1 or better on an allowed track: Dragonmaw Chasm Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1636](../../quests/1636.md) — Dragonmaw Chasm Pro | UID 2288: Finish at position 1 or better on an allowed track: Dragonmaw Chasm Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1646](../../quests/1646.md) — Dragonmaw Chasm Pro | UID 2298: Finish at position 1 or better on an allowed track: Dragonmaw Chasm Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1656](../../quests/1656.md) — Dragonmaw Chasm Pro | UID 2308: Finish at position 1 or better on an allowed track: Dragonmaw Chasm Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 1772](../../quests/1772.md) — Low Deductible | UID 2533: Finish 100 matching race(s) without being smashed: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1773](../../quests/1773.md) — Racing Fanatic | UID 2534: Finish/participate in 100 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1774](../../quests/1774.md) — Fifty-Time Champion | UID 2535: Win 50 credited race(s) in allowed worlds: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1775](../../quests/1775.md) — Street Sweeper | UID 2536: Smash racing smashables until the counter reaches 1000 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1776](../../quests/1776.md) — Drive-Thru Dreamer | UID 2537: Collect racing Imagination pickups until the counter reaches 1500 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |

Rewards for missions/achievements are documented on their existing quest pages; they are not substituted for the activity-result matrix above.

## Evidence and limits

- Local static tables: [Activities](../../../db/Activities.csv), [ActivityRewards](../../../db/ActivityRewards.csv), [ZoneTable](../../../db/ZoneTable.csv), [Objects](../../../db/Objects.csv), [ComponentsRegistry](../../../db/ComponentsRegistry.csv), [LootMatrix](../../../db/LootMatrix.csv), [LootTable](../../../db/LootTable.csv), and [RarityTable](../../../db/RarityTable.csv).
- Local server script: [FvRaceServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/ai/RACING/TRACK_FV/FvRaceServer.cpp); activity-result selection: [Loot.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/Loot.cpp).
- Historical route/name/hazards are attributed in [Community Sources](../Community%20Sources.md#dragonmaw-chasm); they are not treated as proof of this local revision's live state.
- No complete live server configuration, dialogue, client activation sequence, or authenticated deployment state is supplied.
