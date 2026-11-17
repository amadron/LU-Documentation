# Keelhaul Canyon Raceway

[Racing index](../README.md) | [Methodology](../Methodology.md) | [Race quests](../Racing%20Quests%20and%20Achievements.md)

## What and where

The current data ties this Gnarled Forest race instance to activity 39. The local object name and description identify LOT 10413 as the Gnarled Forest race activator.

- **World / activity instance:** Gnarled Forest (world 1300); instance 1303
- **Server activity:** 39; activity table location 1303
- **Local ZoneTable asset:** `01_Live_Maps/Gnarled_Forest/Racetrack/gf_racetrack.luz`
- **Map parse:** embedded world 1303; 1 scene(s); 185 spawner waypoint(s)
- **Scene names:** `Global Scene`
- **Historical track name:** Keelhaul Canyon Raceway (see revision-pinned [community source](../Community%20Sources.md#keelhaul-canyon))
- **Client name (locale.xml):** Keelhaul Canyon Racetrack (`Activities_39_ActivityName` and `ZoneTable_1303_DisplayDescription`)

### Entry point and coordinates

| Object LOT / name | Zone asset | Scene / level | XYZ (map units) | Evidence |
| --- | --- | --- | --- | --- |
| 10413 — GF - Race Activator | 1300 (ZoneTable 375, 1300) | Global Scene — nd_gnarled_forest.lvl | 76.23, 316.61, 503.79 | `client/res/maps/01_Live_Maps/Gnarled_Forest/nd_gnarled_forest.lvl`; LDF activityID 39; transferZoneID 1303; server script L_GF_RACE_INSTANCER.lua |

Coordinates are static LVL object origins in the authored map asset, not a live NPC/player position, path trigger, or guarantee that the activity is enabled. Where local component registration does not prove which object launches this track, it is not labeled as an entrance.

## How the race works

The local per-track server scripts configure this activity as a three-lap car race for individual racers: 2–6 teams/players, one player per team, a 60-second wait period, and a 3-second start delay. The configured vehicle is LOT 7703 (a static test-named “Racing Vehicle Min Balanced” vehicle template); this is not a player-car LOT recommendation. The race uses the `MainPath` route. Exact current deployment, player count, timing, client UI, or availability can differ.

Configured optional entry cost: [Green Imaginite (LOT 3039)](../../items/3039.md) × 1. This is the Activities row value; it is not a guaranteed deduction on every server/client flow.

1. Reach the track through its world activity/entry route, if available.
2. Bring/use a player-built race car and enter the race instance.
3. Complete the three laps, crossing track checkpoints and avoiding course hazards. The local track script sets race/activity state; track-specific item names and hazards are partly documented only by historical sources.
4. Finish to produce a placement/rating. The rating selects the stored activity-reward tier below; it does not itself specify the probability of an individual item.

### Track-specific route evidence

The LUZ scene is the single global track scene; the LVL model names expose track sections including canopy descent, ravine, caves, cliffs, beaches, docks, and ship battle.

The historical guide describes a winding route through the canyon and a waterfall branch that can shorten one section; treat the shortcut as community-reported driving advice, not a local server guarantee.

The waterfall shortcut and route hazards are historical community descriptions, not modeled as server route instructions.

## Race results and rewards

The local `ActivityRewards` table has 20 rows for activity 39, referencing 11 distinct loot matrices. The server chooses the highest `activityRating` not greater than the result rating. Each selected row provides a loot-matrix index and currency index. A matrix roll is not a “drop rate” for every item: each row triggers by its own percentage, the number of draws varies, rarity tables weight eligible loot rows, and MissionDrop/player/team/faction conditions may filter or transform results.

| Activity rating | Stored tier / place | Loot matrix | Currency index | Challenge rating |
| --- | --- | --- | --- | --- |
| 21 | GF Racetrack 1st Place - 2 players | 462 | 37 | 1 |
| 22 | GF Racetrack 2nd Place - 2 players | 463 | 38 | 1 |
| 31 | GF Racetrack 1st Place - 3 players | 459 | 34 | 1 |
| 32 | GF Racetrack 2nd Place - 3 players | 460 | 35 | 1 |
| 33 | GF Racetrack 3rd Place - 3 players | 461 | 36 | 1 |
| 41 | GF Racetrack 1st Place - 4 players | 285 | 25 | 1 |
| 42 | GF Racetrack 2nd Place - 4 players | 353 | 26 | 1 |
| 43 | GF Racetrack 3rd Place - 4 players | 354 | 27 | 1 |
| 44 | GF Racetrack 4th Place - 4 players | 355 | 28 | 1 |
| 51 | GF Racetrack 1st Place - 5 players | 285 | 25 | 1 |
| 52 | GF Racetrack 2nd Place - 5 players | 353 | 26 | 1 |
| 53 | GF Racetrack 3rd Place - 5 players | 354 | 27 | 1 |
| 54 | GF Racetrack 4th Place - 5 players | 355 | 28 | 1 |
| 55 | GF Racetrack 5th Place - 5 players | 356 | 29 | 1 |
| 61 | GF Racetrack 1st Place - 6 players | 285 | 25 | 1 |
| 62 | GF Racetrack 2nd Place - 6 players | 353 | 26 | 1 |
| 63 | GF Racetrack 3rd Place - 6 players | 354 | 27 | 1 |
| 64 | GF Racetrack 4th Place - 6 players | 355 | 28 | 1 |
| 65 | GF Racetrack 5th Place - 6 players | 356 | 29 | 1 |
| 66 | GF Racetrack 6th Place - 6 players | 357 | 30 | 1 |

### Possible item outcomes from those matrices

| Loot matrix | Distinct candidate LOTs | Candidate items and modeled chance |
| --- | --- | --- |
| 285 | 11 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item)<br>[Chase Cutter Engine Panel 2 (LOT 9336)](../../items/9336.md) — modeled 10% per matrix invocation<br>[Chase Cutter Engine Panel 2 (LOT 9339)](../../items/9339.md) — modeled 10% per matrix invocation<br>[Chase Cutter Rear Panel 3 (LOT 9362)](../../items/9362.md) — modeled 10% per matrix invocation<br>[Chase Cutter Rear Bumper 2 (LOT 9371)](../../items/9371.md) — modeled 10% per matrix invocation<br>[Bolt Ox Front Bumper 2 (LOT 9376)](../../items/9376.md) — modeled 10% per matrix invocation<br>[Bolt Ox Engine Panel 1 (LOT 9381)](../../items/9381.md) — modeled 10% per matrix invocation<br>[Bolt Ox Engine Panel 2 (LOT 9384)](../../items/9384.md) — modeled 10% per matrix invocation<br>[Paragon Warp Front Bumper 1 (LOT 9404)](../../items/9404.md) — modeled 10% per matrix invocation<br>[Paragon Warp Rear Panel 1 (LOT 9424)](../../items/9424.md) — modeled 10% per matrix invocation<br>[Paragon Warp Rear Panel 2 (LOT 9426)](../../items/9426.md) — modeled 10% per matrix invocation |
| 353 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 354 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 355 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 356 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 357 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 459 | 11 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item)<br>[Chase Cutter Engine Panel 2 (LOT 9336)](../../items/9336.md) — modeled 10% per matrix invocation<br>[Chase Cutter Engine Panel 2 (LOT 9339)](../../items/9339.md) — modeled 10% per matrix invocation<br>[Chase Cutter Rear Panel 3 (LOT 9362)](../../items/9362.md) — modeled 10% per matrix invocation<br>[Chase Cutter Rear Bumper 2 (LOT 9371)](../../items/9371.md) — modeled 10% per matrix invocation<br>[Bolt Ox Front Bumper 2 (LOT 9376)](../../items/9376.md) — modeled 10% per matrix invocation<br>[Bolt Ox Engine Panel 1 (LOT 9381)](../../items/9381.md) — modeled 10% per matrix invocation<br>[Bolt Ox Engine Panel 2 (LOT 9384)](../../items/9384.md) — modeled 10% per matrix invocation<br>[Paragon Warp Front Bumper 1 (LOT 9404)](../../items/9404.md) — modeled 10% per matrix invocation<br>[Paragon Warp Rear Panel 1 (LOT 9424)](../../items/9424.md) — modeled 10% per matrix invocation<br>[Paragon Warp Rear Panel 2 (LOT 9426)](../../items/9426.md) — modeled 10% per matrix invocation |
| 460 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 461 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 462 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 463 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |

Per-item percentages above are **modeled chance of at least one LOT per matrix invocation**, before player/mission eligibility filters and proxy-token conversion, using the checked source's LootMatrix/RarityTable/LootTable selection rules. Repeated LootTable rows are retained in weighting. These are not unconditional per-race or per-player probabilities and do not account for team assignment, mission filters, or live-server overrides. Reward rows which share a matrix share its candidate pool; the rank/rating controls which matrix/currency pair is selected.

**Currency indexes are kept as indexes, not converted to a coin range here.** See the exact row in [ActivityRewards.csv](../../../db/ActivityRewards.csv) and related [CurrencyTable.csv](../../../db/CurrencyTable.csv).

## Related quests and achievements

| Existing quest/achievement page | Racing-linked objective(s) |
| --- | --- |
| [Quest 625](../../quests/625.md) — Speed Boost! | UID 941: Collect racing Imagination pickups until the counter reaches 9 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 630](../../quests/630.md) — No Wreckin' | UID 946: Finish 1 matching race(s) without being smashed: Keelhaul Canyon Racetrack. |
| [Quest 631](../../quests/631.md) — Keelhaul Canyon Top 3 | UID 947: Finish at position 3 or better on an allowed track: Keelhaul Canyon Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 632](../../quests/632.md) — Swifty's Best Lap | UID 948: Finish a lap in at most 100 seconds (100000 ms) on an allowed track: Keelhaul Canyon Racetrack. |
| [Quest 635](../../quests/635.md) — Swifty's Best Time | UID 951: Finish the race in at most 300 seconds (300000 ms) on an allowed track: Keelhaul Canyon Racetrack. |
| [Quest 636](../../quests/636.md) — Keelhaul Canyon Victory | UID 952: Finish at position 1 or better on an allowed track: Keelhaul Canyon Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 640](../../quests/640.md) — Keelhaul Canyon Winners' Circle | UID 956: Finish at position 3 or better on an allowed track: Keelhaul Canyon Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 641](../../quests/641.md) — Keelhaul Canyon Champion | UID 957: Finish at position 1 or better on an allowed track: Keelhaul Canyon Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 644](../../quests/644.md) — Keelhaul Canyon Pacesetter | UID 960: Finish a lap in at most 90 seconds (90000 ms) on an allowed track: Keelhaul Canyon Racetrack. |
| [Achievement 645](../../quests/645.md) — Keelhaul Canyon Speed Demon | UID 961: Finish the race in at most 285 seconds (285000 ms) on an allowed track: Keelhaul Canyon Racetrack. |
| [Achievement 647](../../quests/647.md) — Keelhaul Canyon Safe Driver | UID 963: Finish 1 matching race(s) without being smashed: Keelhaul Canyon Racetrack. |
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
| [Achievement 666](../../quests/666.md) — Keelhaul Canyon Super Champ | UID 982: Win 10 credited race(s) in allowed worlds: Keelhaul Canyon Racetrack. |
| [Achievement 667](../../quests/667.md) — Try, Try Again | UID 983: Finish last in 10 credited race(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 668](../../quests/668.md) — Race Series 1 | UID 984: Win first place on both Nimbus Station (1203) and Gnarled Forest (1303). The server completes this task when both track bits are set (mask 3), despite stored targetValue 1. |
| [Quest 1408](../../quests/1408.md) — Drive Five | UID 1940: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1506](../../quests/1506.md) — Drive Five | UID 2078: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1543](../../quests/1543.md) — Drive Five | UID 2140: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1580](../../quests/1580.md) — Drive Five | UID 2202: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1624](../../quests/1624.md) — Keelhaul Canyon Pro | UID 2276: Finish at position 1 or better on an allowed track: Keelhaul Canyon Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1634](../../quests/1634.md) — Keelhaul Canyon Pro | UID 2286: Finish at position 1 or better on an allowed track: Keelhaul Canyon Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1644](../../quests/1644.md) — Keelhaul Canyon Pro | UID 2296: Finish at position 1 or better on an allowed track: Keelhaul Canyon Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1654](../../quests/1654.md) — Keelhaul Canyon Pro | UID 2306: Finish at position 1 or better on an allowed track: Keelhaul Canyon Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 1772](../../quests/1772.md) — Low Deductible | UID 2533: Finish 100 matching race(s) without being smashed: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1773](../../quests/1773.md) — Racing Fanatic | UID 2534: Finish/participate in 100 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1774](../../quests/1774.md) — Fifty-Time Champion | UID 2535: Win 50 credited race(s) in allowed worlds: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1775](../../quests/1775.md) — Street Sweeper | UID 2536: Smash racing smashables until the counter reaches 1000 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1776](../../quests/1776.md) — Drive-Thru Dreamer | UID 2537: Collect racing Imagination pickups until the counter reaches 1500 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |

Rewards for missions/achievements are documented on their existing quest pages; they are not substituted for the activity-result matrix above.

## Evidence and limits

- Local static tables: [Activities](../../../db/Activities.csv), [ActivityRewards](../../../db/ActivityRewards.csv), [ZoneTable](../../../db/ZoneTable.csv), [Objects](../../../db/Objects.csv), [ComponentsRegistry](../../../db/ComponentsRegistry.csv), [LootMatrix](../../../db/LootMatrix.csv), [LootTable](../../../db/LootTable.csv), and [RarityTable](../../../db/RarityTable.csv).
- Local server script: [GfRaceServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/ai/RACING/TRACK_GF/GfRaceServer.cpp); activity-result selection: [Loot.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/Loot.cpp).
- Historical route/name/hazards are attributed in [Community Sources](../Community%20Sources.md#keelhaul-canyon); they are not treated as proof of this local revision's live state.
- No complete live server configuration, dialogue, client activation sequence, or authenticated deployment state is supplied.
