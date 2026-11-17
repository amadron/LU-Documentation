# Vertigo Loop

[Racing index](../README.md) | [Methodology](../Methodology.md) | [Race quests](../Racing%20Quests%20and%20Achievements.md)

## What and where

Activity 42 is the Nimbus Station racetrack instance. A local Nimbus map placement of LOT 10413 has LDF activityID 42 and transferZoneID 1203, so its entry coordinate is supported by the map configuration even though the reusable LOT registration has a different default activity ID.

**Which object is the Nimbus Station entrance:** the Race Activator at the Nimbus Station Race Place is the placed copy of LOT 10413. Its template name “GF - Race Activator” only reflects that the same template is reused from Gnarled Forest (where it keeps its default activity 39). The Nimbus copy overrides it in the map data with activityID 42, transferZoneID 1203 and the client script `L_NS_RACE_JOIN_CLIENT.lua` (the Gnarled Forest copy uses `L_GF_RACE_JOIN_CLIENT.lua`). LOT 8561 “Modular Car Race Activator” is **not** the entrance: a scan of all 661 local LVL files finds no placement or spawner of LOT 8561, and its own activity registration points to activity 5 (client name “Avant Gardens Survival”) with an Avant Gardens waves client script, so it is an unused or legacy template. Neither 10413 nor 8561 has an English client name in locale.xml; mission text calls the object the “Race Activator”.

- **World / activity instance:** Nimbus Station (world 1200); instance 1203
- **Server activity:** 42; activity table location 1203
- **Local ZoneTable asset:** `01_Live_Maps/Nimbus_Station/Racetrack/nd_nimbus_station_racetrack.luz`
- **Map parse:** embedded world 1203; 1 scene(s); 130 spawner waypoint(s)
- **Scene names:** `Global Scene`
- **Historical track name:** Vertigo Loop Racetrack (see revision-pinned [community source](../Community%20Sources.md#vertigo-loop))
- **Client name (locale.xml):** Vertigo Loop Racetrack (`Activities_42_ActivityName` and `ZoneTable_1203_DisplayDescription`)

### Entry point and coordinates

| Object LOT / name | Zone asset | Scene / level | XYZ (map units) | Evidence |
| --- | --- | --- | --- | --- |
| 10413 — GF - Race Activator | 1200 (ZoneTable 1200) | Global Scene — nd_nimbus_station.lvl | 270.41, 289.19, 188.12 | `client/res/maps/01_Live_Maps/Nimbus_Station/nd_nimbus_station.lvl`; LDF activityID 42; transferZoneID 1203; server script L_GF_RACE_INSTANCER.lua |

Coordinates are static LVL object origins in the authored map asset, not a live NPC/player position, path trigger, or guarantee that the activity is enabled. Where local component registration does not prove which object launches this track, it is not labeled as an entrance.

## How the race works

The local per-track server scripts configure this activity as a three-lap car race for individual racers: 2–6 teams/players, one player per team, a 60-second wait period, and a 3-second start delay. The configured vehicle is LOT 7703 (a static test-named “Racing Vehicle Min Balanced” vehicle template); this is not a player-car LOT recommendation. The race uses the `MainPath` route. Exact current deployment, player count, timing, client UI, or availability can differ.

Configured optional entry cost: [Green Imaginite (LOT 3039)](../../items/3039.md) × 1. This is the Activities row value; it is not a guaranteed deduction on every server/client flow.

1. Reach the track through its world activity/entry route, if available.
2. Bring/use a player-built race car and enter the race instance.
3. Complete the three laps, crossing track checkpoints and avoiding course hazards. The local track script sets race/activity state; track-specific item names and hazards are partly documented only by historical sources.
4. Finish to produce a placement/rating. The rating selects the stored activity-reward tier below; it does not itself specify the probability of an individual item.

### Track-specific route evidence

The LVL has a single global scene and model names for the Nimbus start, drop-off, landing, planetside, space-loop and spaceship sections.

The public historical account describes a course that leaves Nimbus Station, traverses space and passes a ship under construction; it also identifies Maelstrom-infected cones as obstacles.

Do not interpret the legacy model origin coordinates as a track entrance; many component models share an origin pivot.

## Race results and rewards

The local `ActivityRewards` table has 20 rows for activity 42, referencing 11 distinct loot matrices. The server chooses the highest `activityRating` not greater than the result rating. Each selected row provides a loot-matrix index and currency index. A matrix roll is not a “drop rate” for every item: each row triggers by its own percentage, the number of draws varies, rarity tables weight eligible loot rows, and MissionDrop/player/team/faction conditions may filter or transform results.

| Activity rating | Stored tier / place | Loot matrix | Currency index | Challenge rating |
| --- | --- | --- | --- | --- |
| 21 | NS Racetrack 1st Place - 2 players | 640 | 67 | 1 |
| 22 | NS Racetrack 2nd Place - 2 players | 641 | 68 | 1 |
| 31 | NS Racetrack 1st Place - 3 players | 637 | 64 | 1 |
| 32 | NS Racetrack 2nd Place - 3 players | 638 | 65 | 1 |
| 33 | NS Racetrack 3rd Place - 3 players | 639 | 66 | 1 |
| 41 | NS Racetrack 1st Place - 4 players | 629 | 58 | 1 |
| 42 | NS Racetrack 2nd Place - 4 players | 630 | 59 | 1 |
| 43 | NS Racetrack 3rd Place - 4 players | 631 | 60 | 1 |
| 44 | NS Racetrack 4th Place - 4 players | 633 | 61 | 1 |
| 51 | NS Racetrack 1st Place - 5 players | 629 | 58 | 1 |
| 52 | NS Racetrack 2nd Place - 5 players | 630 | 59 | 1 |
| 53 | NS Racetrack 3rd Place - 5 players | 631 | 60 | 1 |
| 54 | NS Racetrack 4th Place - 5 players | 633 | 61 | 1 |
| 55 | NS Racetrack 5th Place - 5 players | 634 | 62 | 1 |
| 61 | NS Racetrack 1st Place - 6 players | 629 | 58 | 1 |
| 62 | NS Racetrack 2nd Place - 6 players | 630 | 59 | 1 |
| 63 | NS Racetrack 3rd Place - 6 players | 631 | 60 | 1 |
| 64 | NS Racetrack 4th Place - 6 players | 633 | 61 | 1 |
| 65 | NS Racetrack 5th Place - 6 players | 634 | 62 | 1 |
| 66 | NS Racetrack 6th Place - 6 players | 635 | 63 | 1 |

### Possible item outcomes from those matrices

| Loot matrix | Distinct candidate LOTs | Candidate items and modeled chance |
| --- | --- | --- |
| 629 | 11 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item)<br>![](../../../assets/icons/objects/9336.webp){ .lu-ti width="24" loading="lazy" } [Chase Cutter Engine Panel 2 (LOT 9336)](../../items/9336.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9339.webp){ .lu-ti width="24" loading="lazy" } [Chase Cutter Engine Panel 2 (LOT 9339)](../../items/9339.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9362.webp){ .lu-ti width="24" loading="lazy" } [Chase Cutter Rear Panel 3 (LOT 9362)](../../items/9362.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9371.webp){ .lu-ti width="24" loading="lazy" } [Chase Cutter Rear Bumper 2 (LOT 9371)](../../items/9371.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9376.webp){ .lu-ti width="24" loading="lazy" } [Bolt Ox Front Bumper 2 (LOT 9376)](../../items/9376.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9381.webp){ .lu-ti width="24" loading="lazy" } [Bolt Ox Engine Panel 1 (LOT 9381)](../../items/9381.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9384.webp){ .lu-ti width="24" loading="lazy" } [Bolt Ox Engine Panel 2 (LOT 9384)](../../items/9384.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9404.webp){ .lu-ti width="24" loading="lazy" } [Paragon Warp Front Bumper 1 (LOT 9404)](../../items/9404.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9424.webp){ .lu-ti width="24" loading="lazy" } [Paragon Warp Rear Panel 1 (LOT 9424)](../../items/9424.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9426.webp){ .lu-ti width="24" loading="lazy" } [Paragon Warp Rear Panel 2 (LOT 9426)](../../items/9426.md) — modeled 10% per matrix invocation |
| 630 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 631 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 633 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 634 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 635 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 637 | 11 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item)<br>![](../../../assets/icons/objects/9336.webp){ .lu-ti width="24" loading="lazy" } [Chase Cutter Engine Panel 2 (LOT 9336)](../../items/9336.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9339.webp){ .lu-ti width="24" loading="lazy" } [Chase Cutter Engine Panel 2 (LOT 9339)](../../items/9339.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9362.webp){ .lu-ti width="24" loading="lazy" } [Chase Cutter Rear Panel 3 (LOT 9362)](../../items/9362.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9371.webp){ .lu-ti width="24" loading="lazy" } [Chase Cutter Rear Bumper 2 (LOT 9371)](../../items/9371.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9376.webp){ .lu-ti width="24" loading="lazy" } [Bolt Ox Front Bumper 2 (LOT 9376)](../../items/9376.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9381.webp){ .lu-ti width="24" loading="lazy" } [Bolt Ox Engine Panel 1 (LOT 9381)](../../items/9381.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9384.webp){ .lu-ti width="24" loading="lazy" } [Bolt Ox Engine Panel 2 (LOT 9384)](../../items/9384.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9404.webp){ .lu-ti width="24" loading="lazy" } [Paragon Warp Front Bumper 1 (LOT 9404)](../../items/9404.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9424.webp){ .lu-ti width="24" loading="lazy" } [Paragon Warp Rear Panel 1 (LOT 9424)](../../items/9424.md) — modeled 10% per matrix invocation<br>![](../../../assets/icons/objects/9426.webp){ .lu-ti width="24" loading="lazy" } [Paragon Warp Rear Panel 2 (LOT 9426)](../../items/9426.md) — modeled 10% per matrix invocation |
| 638 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 639 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 640 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |
| 641 | 1 | Faction Token Proxy LOT 13763 — modeled 100.0000% (server replacement/discard is conditional; not a direct player item) |

Per-item percentages above are **modeled chance of at least one LOT per matrix invocation**, before player/mission eligibility filters and proxy-token conversion, using the checked source's LootMatrix/RarityTable/LootTable selection rules. Repeated LootTable rows are retained in weighting. These are not unconditional per-race or per-player probabilities and do not account for team assignment, mission filters, or live-server overrides. Reward rows which share a matrix share its candidate pool; the rank/rating controls which matrix/currency pair is selected.

**Currency indexes are kept as indexes, not converted to a coin range here.** See the exact row in [ActivityRewards.csv](../../../db/ActivityRewards.csv) and related [CurrencyTable.csv](../../../db/CurrencyTable.csv).

## Related quests and achievements

| Existing quest/achievement page | Racing-linked objective(s) |
| --- | --- |
| [Quest 624](../../quests/624.md) — Enter a Race | UID 940: Finish/participate in 1 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack. |
| [Quest 625](../../quests/625.md) — Speed Boost! | UID 941: Collect racing Imagination pickups until the counter reaches 9 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 626](../../quests/626.md) — Vertigo Loop Top 3 | UID 942: Finish at position 3 or better on an allowed track: Vertigo Loop Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 627](../../quests/627.md) — Max Velocity | UID 943: Finish a lap in at most 70 seconds (70000 ms) on an allowed track: Vertigo Loop Racetrack. |
| [Quest 628](../../quests/628.md) — Vertigo Loop Victory | UID 944: Finish at position 1 or better on an allowed track: Vertigo Loop Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 638](../../quests/638.md) — Vertigo Loop Winners' Circle | UID 954: Finish at position 3 or better on an allowed track: Vertigo Loop Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 639](../../quests/639.md) — Vertigo Loop Champion | UID 955: Finish at position 1 or better on an allowed track: Vertigo Loop Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 642](../../quests/642.md) — Vertigo Loop Pacesetter | UID 958: Finish a lap in at most 65 seconds (65000 ms) on an allowed track: Vertigo Loop Racetrack. |
| [Achievement 643](../../quests/643.md) — Vertigo Loop Speed Demon | UID 959: Finish the race in at most 190 seconds (190000 ms) on an allowed track: Vertigo Loop Racetrack. |
| [Achievement 646](../../quests/646.md) — Vertigo Loop Safe Driver | UID 962: Finish 1 matching race(s) without being smashed: Vertigo Loop Racetrack. |
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
| [Achievement 665](../../quests/665.md) — Vertigo Loop Super Champ | UID 981: Win 10 credited race(s) in allowed worlds: Vertigo Loop Racetrack. |
| [Achievement 667](../../quests/667.md) — Try, Try Again | UID 983: Finish last in 10 credited race(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 668](../../quests/668.md) — Race Series 1 | UID 984: Win first place on both Nimbus Station (1203) and Gnarled Forest (1303). The server completes this task when both track bits are set (mask 3), despite stored targetValue 1. |
| [Quest 1408](../../quests/1408.md) — Drive Five | UID 1940: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1506](../../quests/1506.md) — Drive Five | UID 2078: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1543](../../quests/1543.md) — Drive Five | UID 2140: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1580](../../quests/1580.md) — Drive Five | UID 2202: Finish/participate in 5 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Quest 1625](../../quests/1625.md) — Vertigo Loop Pro | UID 2277: Finish at position 1 or better on an allowed track: Vertigo Loop Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1635](../../quests/1635.md) — Vertigo Loop Pro | UID 2287: Finish at position 1 or better on an allowed track: Vertigo Loop Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1645](../../quests/1645.md) — Vertigo Loop Pro | UID 2297: Finish at position 1 or better on an allowed track: Vertigo Loop Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Quest 1655](../../quests/1655.md) — Vertigo Loop Pro | UID 2307: Finish at position 1 or better on an allowed track: Vertigo Loop Racetrack. Placement credit also depends on the racing server's solo/player-count rules. |
| [Achievement 1772](../../quests/1772.md) — Low Deductible | UID 2533: Finish 100 matching race(s) without being smashed: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1773](../../quests/1773.md) — Racing Fanatic | UID 2534: Finish/participate in 100 credited race completion(s) on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1774](../../quests/1774.md) — Fifty-Time Champion | UID 2535: Win 50 credited race(s) in allowed worlds: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1775](../../quests/1775.md) — Street Sweeper | UID 2536: Smash racing smashables until the counter reaches 1000 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |
| [Achievement 1776](../../quests/1776.md) — Drive-Thru Dreamer | UID 2537: Collect racing Imagination pickups until the counter reaches 1500 on allowed tracks: Vertigo Loop Racetrack / Keelhaul Canyon Racetrack / Dragonmaw Chasm Racetrack / Space Blizzard Racetrack (1261). |

Rewards for missions/achievements are documented on their existing quest pages; they are not substituted for the activity-result matrix above.

## Evidence and limits

- Local static tables: [Activities](../../../db/Activities.csv), [ActivityRewards](../../../db/ActivityRewards.csv), [ZoneTable](../../../db/ZoneTable.csv), [Objects](../../../db/Objects.csv), [ComponentsRegistry](../../../db/ComponentsRegistry.csv), [LootMatrix](../../../db/LootMatrix.csv), [LootTable](../../../db/LootTable.csv), and [RarityTable](../../../db/RarityTable.csv).
- Local server script: [NsRaceServer.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/ai/RACING/TRACK_NS/NsRaceServer.cpp); activity-result selection: [Loot.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dUtilities/Loot.cpp).
- Historical route/name/hazards are attributed in [Community Sources](../Community%20Sources.md#vertigo-loop); they are not treated as proof of this local revision's live state.
- No complete live server configuration, dialogue, client activation sequence, or authenticated deployment state is supplied.
