# Quest Database - Methodology and Limitations

[Quest database](./README.md)

Generated: **2026-11-17T09:49:07.652Z**. Reviewed local DarkflameServer source revision:
`8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4`. No gameplay/server code was changed.

## What this database covers

All **1427 Missions rows**: **682 quests** and
**745 achievements**, distinguished by isMission.
All **1800 attached MissionTasks rows** are included, preserving
target, targetGroup, targetValue, taskParam1, UID, and task type. Nothing is
filtered out merely because it looks old, internal, hidden, or unfinished.

[MissionText](../../db/MissionText.md) contains presentation/animation references,
not the complete localized offer/description/turn-in prose. A locale.xml file
was not supplied. Descriptions and checklists here are **original reconstructions
from local objective data**, not recovered dialogue or fully hand-verified
puzzle walkthroughs. Unsupported script-specific actions remain unknown.

## Mission lifecycle, order, and prerequisites

The normal quest flow is eligibility → acceptance → active objectives → ready
to complete → turn-in/reward selection → complete. Achievements are normally
discovered by eligible progress events and complete without a generic NPC
turn-in. Not every earlier action is retroactively credited. Acceptance catch-up
explicitly checks gather inventories, existing player flags, and racing
parameter-4 target mission completions.

Task rows are listed in source-loader order for readability. All must satisfy
their completion checks; row order alone does not impose a sequence.
Scripted phases can impose additional ordering not present in the table.

The [server prerequisite parser](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dMission/MissionPrerequisites.cpp)
is reproduced as inspected: a bare mission ID requires state COMPLETE, an
`ID:state` qualifier requires that exact state, `|` selects OR, and
`,`, `&`, and `(` start right-recursive AND branches. Spaces and closing
parentheses are skipped. It is **not a conventional grouping/precedence parser**.
Both the raw expression and this server evaluation are shown; client checks
may differ. State 2 is ACTIVE, 4 READY_TO_COMPLETE, and 8 COMPLETE; repeat states
10 and 12 are distinct. UIPrereqID is kept separate and not mistaken for a
Missions foreign key.

CanAccept treats cooldownTime as **minutes after previous completion** and
uses -1 for no cooldown. Random selectors only offer eligible pool candidates;
an empty randomPool is not offered by the inspected offer path. Potential
follow-ups are reverse prerequisite references, not promises of unlocks.
Stored mission/task gate_version is unused in the inspected generic table
loaders; scripts, map preconditions, and the client can still restrict content.

## Typed objective targets

Numbers are not interpreted as LOTs merely because an Objects row has the same ID.

| Type | Interpretation |
| --- | --- |
| 0 | Smash |
| 1 | Script event |
| 2 | Activity / Quick Build |
| 3 | Unique collectibles |
| 4 | Talk to NPC |
| 5 | Emote at target |
| 9 | Use item |
| 10 | Use skill |
| 11 | Gather items |
| 12 | Explore |
| 14 | Activity performance |
| 15 | Interact |
| 16 | Complete missions / achievements |
| 17 | Earn reputation |
| 21 | Collect power-ups |
| 22 | Tame pet |
| 23 | Racing |
| 24 | Player flag |
| 25 | Place model |
| 27 | Add behavior |
| 30 | Visit properties |
| 32 | Donation |


- Smash, collectible, NPC talk, emote targets, item use/gather, interaction,
  and pet-taming tasks use LOTs in their relevant target fields. The talk,
  emote, and use-item handlers check the primary target rather than all group
  values. Alternatives on ordinary combined counters are not instructions
  to perform the full quantity for every listed LOT.
- Collection tasks track unique collectible identity including zone information.
- Activity numbers are joined through SCRIPTED_ACTIVITY (39) or
  RebuildComponent.activityID; script-only activities may not resolve.
  PERFORMANCE tasks compare the specified metric/threshold instead of
  counting that many plays.
- Skill tasks use taskParam1 skill IDs and optional target LOTs. The inspected
  destruction path credits targeted skill kills; a no-target skill task has a
  separate cast/equip progress path.
- POWERUP carries skill IDs. Candidate pickup LOTs are joined via ObjectSkills
  and Objects.type=Powerup, not by equating a skill ID to a LOT.
- EXPLORE matches the exact targetGroup event key, PLAYER_FLAG uses flag IDs,
  and META uses mission/achievement completion IDs. Script event values are
  left as event values unless their specific handler semantics are verified.
- Racing taskParam1 changes the namespace: parameters 4/5 reference missions;
  17 references smashable LOTs; ordinary track tasks reference world IDs;
  parameter 6 is a modular-building event. Placement/time tasks compare
  lower-is-better thresholds; lap/race values are milliseconds. UID **984**
  (mission 668) needs both world-win bits (mask 3), despite stored targetValue 1.
  Placement credit can depend on the racing server's solo/player-count rules.
- Visit-property tasks track unique associate/property identity values in
  allowed zones. Generic place-model, add-behavior, and donation handlers
  increment supplied counts without using the stored target as a LOT filter.
- Gather parameter bit 1 prevents removal in YieldRewards; bit 4 prevents
  inventory-loss decrement in the inspected task path. Other bit meanings
  are not invented. Required gathered targets can otherwise be removed from
  item/quest inventories when rewards are granted.

## NPC and map evidence

Missions.offer_objectID and target_objectID are distinguished from
MissionNPCComponent offersMission/acceptsMission associations via registry
component **73**. Random-pool giver candidates are labeled as inherited from
their selector, not direct offers. Achievement NPC fields are not turned into
instructions to accept achievements.

LUZ files are joined by **exact normalized ZoneTable zoneName asset paths**,
not just embedded world IDs. Referenced LVL objects, LOT 176 spawntemplate
settings, and LUZ spawner waypoints supply candidate XYZ placements.
Client-only candidates are excluded. Feature gates, scene CheckPrecondition,
inactive-on-load spawners, and no_auto_spawn are retained as conditions.
Waypoints/scene records can overlap and are not population counts.

Exploration coordinates require a full join from LUZ scene ID to the LVL
trigger_id and the scene's .lutriggers updateMission command whose first
argument is exploretask and fifth argument exactly matches targetGroup.
The native XML parser read **30** such command definitions.
Scene layer 0 matches the inspected GetTrigger lookup; the map object can
reference another scene's trigger ID. Trigger enabled state, event, and
command target are retained. The published XYZ is a trigger-object position,
not the complete collision-volume geometry.

39 local LUZ assets were parsed; 34 matched
ZoneTable asset paths, and 536 distinct referenced LVL files parsed.
1122 client-only candidates were excluded.
1 non-finite-coordinate placement(s) were excluded and
reported in [Coverage.json](./Coverage.json); valid records in the same level
were retained. 0 level parse failures remain.

### Map assets without an authoritative ZoneTable path match

| Asset | Embedded ID (not assumed to be a zone mapping) |
| --- | --- |
| maps/01&#95;live&#95;maps/gnarled&#95;forest/survival/nd&#95;gf&#95;survival&#95;trench.luz | 58001 |
| maps/earthgauntlet/earthgauntlet.luz | 2100 |
| maps/earthgauntlet/nd&#95;nj&#95;earth.luz | 2100 |
| maps/seasonal&#95;live maps/december/ns&#95;winter&#95;racetrack/nd&#95;nimbus&#95;station&#95;winter-racetrack.luz | 1261 |
| maps/seasonal&#95;live maps/december/winter&#95;celebrity&#95;property/ns&#95;property&#95;large&#95;winter.luz | 1260 |


## Rewards

First and repeat item slots are separated. A stored item count of zero becomes
one in the inspected handler. Choice slots remain alternatives, not a random
loot table or a promise of all listed items. Negative repeat counts, if present
on a positive LOT, are surfaced as unsafe unsigned-conversion definitions.

Coins use the corresponding first/repeat field. U-Score and reputation run
before the repeat branch. At the configured level cap, U-Score can become
coins, so the exact payout depends on WorldConfig. Maximum Life/Imagination,
backpack space, vault item AND model capacity, and emote unlocks are
first-completion behavior. Positive max-model/widget/wallet fields are not
advertised as supported grants without a corresponding inspected handler.

MissionEmail type 1 sends mail (a positive attachment LOT has quantity 1);
type 2 is a chat announcement and does not send an attachment in that branch.
Links to the item database provide acquisition details for reward/gather LOTs.

## Public wiki research and uncertainty

Read-only MediaWiki requests researched **757 public pages**
transcluding Template:Mission or Template:Achievement. The parser separated
**982 infoboxes**, including achievement tiers on shared pages.
These templates contain **no explicit local mission-ID mapping**.

Titles are only associated when exactly one local definition satisfies a
multi-field signature: at least three matching evidence groups, including a
named NPC/reward/target or a region + objective-kind + threshold + U-Score
signature. Explicit known coin/score, NPC, and recognized reward conflicts
exclude matches. Numeric ID coincidence or one matching name is insufficient.
**409 definitions** have such candidate historical
associations. **93 infoboxes** matched multiple local
definitions and were not used to assign a title. Conflicting candidate names
are shown as references rather than silently selecting one title.

This is conservative corroboration, **not verification that the historical
quest title belongs to a particular localized ID**. Local numeric IDs,
objectives, and rewards remain separately traceable. Community factual method,
location, target, and reward references are kept separate from local evidence.
Article prose, NPC dialogue, and copyrighted walkthrough text were not copied.
No client assets or server source were uploaded.

Every researched page has a fixed revision link and retrieval timestamp in
[Community Sources](./Community%20Sources.md). Unmatched/ambiguous pages are not
used to fill unknowns; no match does not mean no public information exists.

## Orphan task rows / missing definitions

| Mission ID | UID | Type | Raw target / group |
| --- | --- | --- | --- |
| 959 | 1392 | 3 | 12050 /  |
| 989 | 1424 | 4 | 6014 /  |
| 990 | 1425 | 4 | 9680 /  |
| 1405 | 1937 | 23 |  / 8167,8165,7857,7860,7861,7862,8163 |


These 4 rows have no Missions parent in the supplied
snapshot; they are reported rather than made into invented quest definitions.
Missing prerequisite definition IDs:
none.

## Source implementation

- [Mission.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dMission/Mission.cpp):
  state transitions, acceptance catch-up, completion, item removal, rewards.
- [MissionTask.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dMission/MissionTask.cpp):
  exact target matching, counters, unique tracking, racing exceptions.
- [MissionComponent.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/MissionComponent.cpp):
  discovery and progress of achievements.
- [MissionOfferComponent.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/MissionOfferComponent.cpp):
  NPC associations, random pools, eligible offers.
- [TriggerComponent.cpp](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dComponents/TriggerComponent.cpp):
  exploration progress from trigger commands.
- [Mission prerequisites](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dMission/MissionPrerequisites.cpp),
  [task enum](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eMissionTaskType.h),
  [racing parameters](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eRacingTaskParam.h).
- [Exported static database](../../db/README.md).

## What is not claimed

This is not an exhaustive audit of every quest-specific C++/Lua script,
client cinematic, puzzle route, dialogue option, event setting, or live
character state. It does not guarantee reachability, deployment availability,
exact localized story text, or player eligibility. Static definitions and
historical community facts are not combined into invented instructions.
Where a script/event remains unknown, the page explicitly says so.

## Validation performed

- Verified all 1,427 definition pages: 682 quests and 745 achievements, with
  no missing or duplicate IDs.
- Compared all 1,800 attached objective rows and their raw target/parameter
  fields with the exported data; reported the four orphan rows separately.
- Checked 1,861 displayed item-reward slots, first/repeat quantities,
  266 choice-reward definitions, scalar rewards, and prerequisite expressions.
- Verified revision links and retrieval timestamps for all 757 public sources;
  ambiguous associations do not supply a localized ID claim.
- Passed 11 focused tests across the shared data/map helpers and quest helpers.
  End-to-end checks include Bob and quest 173, the mission 668 racing bitmask,
  a 70-second lap threshold, choice items, and exploration trigger 20:12.
- Checked 7,010 generated Markdown tables for consistent column counts and
  more than 466,000 local links across the player wiki: no malformed tables
  or broken targets. The largest quest-database Markdown page is 158,498 bytes.
