# Quest Guide

[Game Guide](./README.md) | [Item Guide](./Item%20Guide.md) | [Racing Guide](./Racing%20Guide.md) | [Pet Guide](./Pet%20Guide.md)

Missions give you goals to pursue as you explore LEGO Universe. Talk to
characters, take on an assignment, follow its objectives, then return to claim
the reward when the game asks you to. Achievements track accomplishments and
complete on their own as you play.

Use your in-game mission journal as the source of truth for what to do next.
The [Quest and Achievement Database](./quests/README.md) is a lookup tool for
details such as prerequisites, associated characters, possible rewards, and
locations. It includes test, hidden, and unused definitions too, so a listed
quest may not be available on your server.

For activity-specific advice, see the [Racing Guide](./Racing%20Guide.md)
or [Pet Guide](./Pet%20Guide.md). The detailed [Racing Database](./racing/README.md)
and [Pet Database](./pets/README.md) link activities back to their related quests.

## 1. Missions and achievements

The client database defines **1,427 entries**: **682 missions** and
**745 achievements**. Both use the same definition format; a single flag
decides which kind an entry is, and that changes how it behaves:

| | Missions | Achievements |
|---|---|---|
| How it starts | Offered by a character or object; you accept it. | Starts tracking automatically when you make matching progress. |
| How it ends | When all objectives are done it becomes *ready to complete*; you turn it in. | Completes and pays out the moment its last objective is done. |
| Repeatable | 221 can be repeated (217 of them on a daily timer). | Practically never (only 4 hidden entries are flagged repeatable). |

Achievements are grouped into the categories you see in the passport:
Location (377, e.g. Crux Prime, Ninjago Monastery, Gnarled Forest), General
(98), Battle (78), Racing (45), Play (42), Build (31), Events (18, the Winter
event in Frostburgh), and LUPs (2). Another 54 are hidden. On the mission side,
253 definitions are filed as "Hidden", including all 217 daily missions.

## 2. Starting a mission

1. Talk to an available mission-giving NPC and read the assignment.
2. Check any prerequisites shown in game. 624 missions require earlier
   missions first.
3. Accept the mission before beginning its objectives unless the game
   explicitly indicates otherwise.
4. Open your mission journal and check the exact targets and quantities.

If a mission is not offered, earlier missions, a repeat cooldown, or other
requirements may be involved. An NPC can offer one mission and accept another;
do not assume that the giver is always the turn-in NPC.

Progress generally counts only after you accept. In the DarkflameServer code
there are two exceptions when you accept: items you already carry count
toward "gather" objectives, and world flags you already earned count toward
flag-based objectives. Everything else starts from zero, so follow the
active journal entry.

A mission moves through these states (as named in the server code):
**available** → **active** → **ready to complete** (all objectives done,
turn-in pending) → **complete**. A repeatable mission you have finished
before uses "completed before" versions of the same states.

## 3. Completing objectives

The 1,427 definitions contain 1,800 objectives. The most common kinds, with
the client's own wording as examples:

| Objective kind (count) | What it means | Example from the client |
|---|---|---|
| Smash (459) | Smash a specific enemy or object. | "Smash 20 Stromling Admiral Invaders on Crux Prime." |
| Gather (268) | Have the item in your inventory. | "Gather 5 bananas for the monkey atop Brig Rock in Gnarled Forest." |
| Script (164) | A scripted action the world tracks. | "Grow 10 flowers." |
| Talk to NPC (140) | Speak to a specific character; missions only. | "Talk to Cole in the Monastery Dojo of Earth." |
| Activity (133) | Mostly Quick Builds. | "Quick Build 5 Catapults on the Ninjago Battlefield." |
| Meta (130) | Complete other missions or achievements. | "Complete 10 Missions or Achievements in Avant Gardens." |
| Use skill (91) | Equip or use an item's skill. | "Read the Rank 1 Engineer book." |
| Racing (84) | Race results and racing events. | "Place 3rd or better during a race at the Vertigo Loop racetrack." |
| Explore (79) | Reach a specific area. | "Discover the Ice Shrine in the caves below the Ninjago Monastery." |
| Player flag (60) | Reach a story or learning milestone. | "Learn to use Earth Spinjitzu Lanterns and burrow into the earth!" |
| Collection (56) | Pick up collectibles such as flags or Imagination Bricks. | "Collect 10 Heart Flags in Gnarled Forest." |
| Pet taming (38) | Tame a pet, sometimes a specific kind. | "Tame a Tortoise Pet." |
| Minigame score (31) | Reach a score or time in an activity. | "Score 50,000 points in one game in Cannon Cove Shooting Gallery." |
| Interact (23) | Use a specific NPC or object. | "Talk to Hu Where at the Avant Gardens Launch Area." |

Rarer kinds: visit properties (9), emote (7, e.g. "Perform a Dance Emote."),
collect power-ups (6), donate bricks (6, "Donate 50 bricks to the Nexus Jawbox
in Nimbus Station."), earn Reputation (5), use an item (3, "Eat 5 BBQ Blast
Hot Dogs."), place models (4), and add Behaviors to models (4).

Practical tips:

- Confirm the exact target. Similarly named enemies or scenery may not count;
  watch the counter after one successful action.
- Keep gathered items until you turn the mission in. In the DarkflameServer
  code, dropping or selling them lowers the counter again.
- "Talk", "interact", and "deliver" objectives need the specified NPC or
  object; standing nearby is not enough.
- Racing and minigame objectives ask for a specific result. Simply taking part
  does not count unless that is the objective.

Always follow the exact objective and conditions shown in your journal.

## 4. Turning in and choosing rewards

Completing the objective counters is not always the final step. If the
mission asks you to turn it in, return to the character or object shown in
your journal and finish the conversation. Achievements need no turn-in.

Rewards a mission or achievement can give:

| Reward | Notes |
|---|---|
| LEGO Score | 1,320 definitions give some, up to 710. In DarkflameServer, a character at the level cap gets coins instead (set by the server's world config). |
| Coins and items | Up to four item rewards per definition. |
| Reputation | Only 21 definitions give it, from 25 to 1,000. |
| Max Life | 7 definitions, e.g. the "Pirate Flag Hunter" achievement (+1). |
| Max Imagination | 36 definitions, e.g. the "Your Creative Spark" mission (+6) and the "A Creative Opportunity" achievements (+1 each). |
| Backpack space | 40 definitions add 1–4 inventory slots, e.g. "Nimbus Station Flag Hunter" (+4). |
| Vault space | 9 definitions add slots to the vault (bank). |
| Emotes | 26 definitions unlock an emote. |

**Choice rewards.** 207 missions offer two to four alternatives, such as
"Get Help!" (Basic Shortsword, Basic Spear, or Basic Hammer) or
"Back-up Bulwark!" (one of four Trial faction gear sets). You receive only the
one you pick, so inspect them before confirming.

Other things to know:

- Gathered mission items are usually taken when rewards are granted. In the
  DarkflameServer code this only removes them from the main Items and Quest
  inventories, and some gather objectives are flagged to let you keep them.
- Some completions send an in-game mail (40 definitions, 4 of them with an
  attached item). Others post an announcement in chat (232 definitions).
- Check your inventory, mail, and any completion message before reporting a
  missing reward or repeating the activity.

For item requirements and comparing rewards, see the
[Item Guide](./Item%20Guide.md).

## 5. Daily and repeatable missions

217 missions have a cooldown of 1,300 minutes (21 hours 40 minutes). These
are the daily missions. In the DarkflameServer code the timer starts when you
complete the mission. It is not a fixed daily reset, so a mission you finish
at 18:00 is available again at 15:40 the next day.

Most daily missions (199) sit in random pools. The character offers one
mission picked at random from those you can currently take, and keeps
offering the same one while it is active. Examples from the data:

- Bronson Jarls (Sentinel Faction Lieutenant) has a pool of 22 Crux Prime
  missions such as "Mutiny on Crux Prime".
- The four faction vendors in Nimbus Station have pools of 12–14, for example
  Xeno Blueblade (Sentinel Vendor).
- Toshiro Gojira and Hari Howzen, the Ninjago Monastery Guards, have pools
  of 6 each.

The other 18 dailies are fixed, for example "Avant Gardens Property Visitor"
("Visit 5 Block Yard or Avant Grove Properties today."), "Web of Destruction"
from Melodie Foxtrot, and "Protect the Monastery!" from Sensei Wu.

Repeat completions pay differently from the first one. The server always
gives LEGO Score and Reputation, but uses the separate "repeatable" coin and
item rewards on later completions. Stat rewards (Life, Imagination, backpack
and vault space) and emote unlocks are given only the first time. For
example, "Avant Gardens Property Visitor" gives 500 coins and a Surprise Pack
the first time, and 500 coins with no item on repeats.

## 6. When progress is blocked

| Symptom | Check first |
|---|---|
| NPC does not offer a quest | Earlier prerequisites, whether the quest is already active/completed, and any repeat cooldown. |
| Objective counter does not move | Active mission, correct target/action, required quantity, and any journal-specific conditions. |
| Gather counter went down | Whether you dropped, sold, or used the item before turning in. |
| All objectives appear finished | Whether a turn-in interaction or reward selection is still required. |
| Requested item appears missing | Relevant inventory categories and whether an earlier turn-in consumed it. Do not discard other quest items while investigating. |
| Repeat quest is unavailable | Whether it is actually repeatable and whether its 21 h 40 min cooldown has elapsed since your last completion. |
| Guide/catalog content cannot be found | Whether it is test, hidden, unavailable, or unimplemented content in this server version. |

If the problem persists, send staff:

```text
Character:
Quest title and mission ID, if known:
Zone and NPC:
Current objective and counter:
What I did:
What happened instead:
Screenshot and approximate time:
```

Avoid repeatedly claiming rewards or trying GM commands as a workaround.
Staff can investigate definitions and saved progress separately.

## Optional: looking up quest details

You do not need to read the raw tables to play. If you want to investigate a
specific entry:

- [Quest and achievement database](./quests/README.md) resolves the joins into
  readable detail pages, with [quest-character](./quests/NPC%20Index.md) and
  [zone](./quests/locations/README.md) indexes. Example pages:
  [Avant Gardens Property Visitor (1194)](./quests/1194.md),
  [Get Help! (311)](./quests/311.md),
  [Your Creative Spark (173)](./quests/173.md).
- The [table schema](../db/Schema.md) documents the
  [`Missions`](../db/Schema.md#table-missions) (IDs, prerequisites,
  repeatability, cooldowns, rewards),
  [`MissionTasks`](../db/Schema.md#table-missiontasks) (objectives),
  [`MissionNPCComponent`](../db/Schema.md#table-missionnpccomponent) (who offers
  and accepts what), and [`MissionEmail`](../db/Schema.md#table-missionemail)
  tables. Numeric fields are internal identifiers and can require
  interpretation.
- The [item database](./items/README.md) helps identify reward items.

The mission tables alone do not provide localized dialogue; that lives in
the client's locale strings. Some scripted puzzle steps are not recorded in
either. The database reconstructs supported objectives and checklists rather
than inventing missing narrative. Its [methodology](./quests/Methodology.md)
explains how technical fields, map evidence, and historical community matches
were interpreted.

## Source and limitations

Counts, categories, objectives, rewards, cooldowns, and random pools come
from the `Missions`, `MissionTasks`, `MissionNPCComponent`, and `MissionEmail`
tables of the local client database (CDServer.sqlite). Mission, objective,
character, and item names come from the English client strings (locale.xml).
Hidden and test definitions are included in the counts, so not every
counted entry is reachable in play.

Behavior described as "in the DarkflameServer code" was checked in the local
server source: mission states, achievement auto-completion, catch-up on
accept, cooldown timing, random pools, repeat rewards, item removal, and
level-cap coin conversion. See the
[mission implementation](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/dMission/Mission.cpp)
and [task-type enum](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/dEnums/eMissionTaskType.h).
The original live servers may have differed in details. Exact availability,
level cap, and client presentation can also differ between deployments.
